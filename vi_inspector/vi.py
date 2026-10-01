"""Inspect LabVIEW .vi/.ctl binaries without LabVIEW installed.

Uses the MIT-licensed ``pylabview`` package (mefistotelis/pylabview) to walk the
RSRC container: block table, version info (LVSR/vers), password metadata (BDPW),
connector pane (CONP), dependencies, and execution flags.

Design notes for multi-version support:
  * The RSRC *container* layout is stable across LabVIEW versions; per-block
    *contents* vary. We parse the container generically, decode the blocks we
    understand, and skip anything unknown instead of failing.
  * Every report records the exact LabVIEW version that saved the file so
    version-specific quirks can be branched on later.
  * 32-bit vs 64-bit LabVIEW save byte-identical files; bitness is not recorded
    in the format and does not affect parsing.
"""

import io
import os
import re
import xml.etree.ElementTree as ET
from types import SimpleNamespace

EMPTY_MD5 = "d41d8cd98f00b204e9800998ecf8427e"  # md5 of empty string


def _patch_pylabview():
    """Work around a pylabview bug hit by some LV 2021 files.

    LVblock.integrateData() only runs commentSpecialTypes(), a purely
    cosmetic annotation pass over type descriptors. On some files it calls
    getNumRepeats() on a TD object that lacks the method
    (e.g. TDObjectNumberPtr), which aborts the whole VI parse. Skipping the
    pass loses nothing but comments.
    """
    try:
        from pylabview import LVblock
    except ImportError:
        return
    # integrateData() on type-descriptor blocks only runs commentSpecialTypes(),
    # a purely cosmetic annotation pass. Guard that pass directly.
    cls = LVblock.TypeDescListBase
    orig = cls.commentSpecialTypes

    def safe_commentSpecialTypes(self, section_num):
        try:
            orig(self, section_num)
        except AttributeError:
            pass

    cls.commentSpecialTypes = safe_commentSpecialTypes


_patch_pylabview()


def _make_options():
    return SimpleNamespace(
        rsrc="", xml="", filebase="", verbose=0, print_map=None,
        keep_names=False, raw_connectors=False,
        typedesc_list_limit=4095, array_data_limit=(2 ** 28) - 1,
        store_as_data_above=4095, textcp="mac_roman",
    )


def _sanitize_xml(raw: str) -> str:
    """Strip character references that are illegal in XML 1.0.

    pylabview decodes binary strings as mac_roman, which can emit e.g.
    &#x00; inside attribute values. Expat rejects those outright.
    """

    def _fix(m):
        body = m.group(1)
        try:
            v = int(body[1:], 16) if body[:1].lower() == "x" else int(body)
        except ValueError:
            return m.group(0)
        if v in (0x9, 0xA, 0xD) or 0x20 <= v <= 0xD7FF \
                or 0xE000 <= v <= 0xFFFD or 0x10000 <= v <= 0x10FFFF:
            return m.group(0)
        return ""

    return re.sub(r"&#(x[0-9a-fA-F]+|[0-9]+);", _fix, raw)


def _load_vi(path):
    from pylabview.LVrsrcontainer import VI
    po = _make_options()
    # NOTE: the handle must stay open for the VI's lifetime — pylabview reads
    # some block contents lazily during exportXMLTree(). Callers must close it.
    fh = open(path, "rb")
    return VI(po, rsrc_fh=fh, text_encoding="mac_roman"), fh


def _block_inventory(vi):
    inv = []
    for ident, block in vi.blocks.items():
        name = ident.decode("utf-8", errors="replace") \
            if isinstance(ident, (bytes, bytearray)) else str(ident)
        size = getattr(block, "data_len", None)
        if size is None:
            for attr in ("size", "blockSize", "length"):
                size = getattr(block, attr, None)
                if size is not None:
                    break
        inv.append({"id": name, "size": size})
    return inv


def _lvsr_section(root):
    for sec in root.iter("Section"):
        parent = None  # ET has no parent pointers; match by context below
        return sec
    return None


def _find_lvsr_section(root):
    lvsr = root.find("LVSR")
    if lvsr is not None:
        return lvsr.find("Section")
    return None


def _execution_summary(section):
    """Pull the handful of execution flags that matter for documentation."""
    if section is None:
        return {}
    wanted = ("IsReentrant", "RunOnOpen", "ShowFPOnLoad", "ShowFPOnCall",
              "HasNoBD", "DynamicDispatch", "IsSubroutine", "InlinableDiagram",
              "SourceOnly", "Priority")
    out = {"name": section.get("Name"), "protected": None}
    for tag in ("Version", "Execution", "Library", "Instrument"):
        el = section.find(tag)
        if el is None:
            continue
        for k, v in el.attrib.items():
            if tag == "Version" or k in wanted or k in ("Protected", "PasswordHash"):
                out[f"{tag}.{k}"] = v
    lib = section.find("Library")
    if lib is not None:
        out["password_protected"] = (
            lib.get("Protected") == "1"
            and (lib.get("PasswordHash") or "").lower() != EMPTY_MD5
        )
    return out


def _dependencies(root):
    """SubVI / library references found in the extracted metadata."""
    deps = []
    seen = set()
    for item in root.iter("Item"):
        text = item.get("Text") or ""
        if any(ext in text for ext in (".vi", ".lvlib", ".lvclass", ".ctl", ".llb")):
            # Binary path records look like "<junk>!<real path>"; the real
            # reference follows the last '!'. Control chars are separators.
            text = text.split("!")[-1]
            cleaned = re.sub(r"[\x00-\x1f\x7f]", " ", text).strip()
            cleaned = re.sub(r"\s+", " ", cleaned)
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                deps.append(cleaned)
    for el in root.iter("LinkSavePathRef"):
        text = (el.text or "").strip()
        if text and text not in seen:
            seen.add(text)
            deps.append(text)
    return deps


def _connector_pane(root):
    conp = root.find("CONP")
    if conp is None:
        return {"present": False}
    sec = conp.find("Section")
    td = sec.find("TypeDesc") if sec is not None else None
    return {
        "present": True,
        "type_id": td.get("TypeID") if td is not None else None,
    }


def inspect_vi(path):
    """Return a JSON-serialisable report for one .vi/.ctl file."""
    path = os.path.abspath(path)
    report = {"file": path, "size_bytes": os.path.getsize(path),
              "warnings": [], "supported": True}
    try:
        vi, _fh = _load_vi(path)
    except Exception as exc:  # noqa: BLE001 - version quirks must not crash
        report["supported"] = False
        report["error"] = f"{type(exc).__name__}: {exc}"
        return report

    try:
        ver = vi.getFileVersion() or {}
    except Exception:  # noqa: BLE001
        ver = {}
    report["labview_version"] = {
        "major": ver.get("major"), "minor": ver.get("minor"),
        "bugfix": ver.get("bugfix"), "stage": ver.get("stage_text"),
        "build": ver.get("build"),
        "display": f"{ver.get('major')}.{ver.get('minor')}"
        if ver.get("major") is not None else None,
    }

    report["blocks"] = _block_inventory(vi)
    block_ids = {b["id"] for b in report["blocks"]}

    # Password / locked-diagram detection (BDPW block + LVSR Library flags)
    report["password_protected"] = None
    try:
        bdpw = vi.get_one_of("BDPW")
        if bdpw is not None:
            md5 = getattr(bdpw, "password_md5", b"").hex() \
                if hasattr(getattr(bdpw, "password_md5", b""), "hex") else ""
            report["password_protected"] = md5.lower() != EMPTY_MD5
    except Exception:  # noqa: BLE001
        pass

    try:
        root = vi.exportXMLTree()
        xml_text = ET.tostring(root, encoding="unicode")
        xml_root = ET.fromstring(_sanitize_xml(xml_text))
    except Exception as exc:  # noqa: BLE001
        report["warnings"].append(f"xml_export_failed: {exc}")
        xml_root = None

    if xml_root is not None:
        section = _find_lvsr_section(xml_root)
        report["vi"] = _execution_summary(section)
        if report["password_protected"] is None:
            report["password_protected"] = report["vi"].pop(
                "password_protected", None)
        else:
            report["vi"].pop("password_protected", None)
        report["connector_pane"] = _connector_pane(xml_root)
        report["dependencies"] = _dependencies(xml_root)
        report["has_icon"] = "ICON" in block_ids
        report["has_block_diagram"] = not (
            report["vi"].get("Execution.HasNoBD") == "1")
    else:
        report["has_icon"] = "ICON" in block_ids

    if not report["warnings"]:
        del report["warnings"]
    _fh.close()
    return report
