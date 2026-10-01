#!/usr/bin/env python3
"""
Bulk-export front-panel and block-diagram PNGs for every .vi under a folder.

This is the companion to vi-inspector's `review` command: it uses the real
LabVIEW (via ActiveX/VI Server) to render ground-truth images so review
findings can be reconciled against the actual source.

Mechanism: for each VI it calls VI.PrintVIToHTML (format=Standard, PNG,
24-bit) into a per-VI temp folder, then picks the front-panel and
block-diagram PNGs out of the generated HTML. This works through LabVIEW's
ActiveX type library, which (unlike the G VI Server) does not expose the
VI.FP / VI.BD properties at all -- verified against the live type info.

Requirements (run on the Windows machine that has LabVIEW):
  - LabVIEW installed with the ActiveX server enabled:
      Tools > Options > VI Server > ActiveX : "Enable ActiveX Server" checked
    (LabVIEW 2021 32-bit works; Python may be 64-bit, COM is out-of-process.)
  - Python packages:  pip install pywin32 numpy pillow

Usage:
    python export_vi_images.py "C:\\path\\to\\Vessel Simulator" -o vi_images

Output:
    vi_images/<relative-path>/<VI name>.fp.png
    vi_images/<relative-path>/<VI name>.bd.png
    vi_images/manifest.csv   (vi path, fp ok, bd ok, notes)

Then zip the output folder and upload it for visual reconciliation.
"""

import argparse
import csv
import gc
import os
import shutil
import sys
import tempfile
import traceback

# win32com is imported lazily inside main() -- this script only *runs* on
# Windows, but the pixmap-conversion helpers stay importable/testable anywhere.

try:
    import numpy as np
except ImportError:
    sys.exit("numpy is required: pip install numpy")

try:
    from PIL import Image
except ImportError:
    sys.exit("pillow is required: pip install pillow")


# ---------------------------------------------------------------------------
# COM helpers (LabVIEW's type library needs some coaxing via pywin32)
# ---------------------------------------------------------------------------

def _flagged_call(obj, name, *args):
    """Call a COM method, applying the _FlagAsMethod workaround if needed."""
    try:
        method = getattr(obj, name)
        return method(*args)
    except TypeError:
        # LabVIEW's type library does not flag some methods as callable.
        obj._FlagAsMethod(name)
        return getattr(obj, name)(*args)


def _lv_invoke(obj, name, *args):
    """Invoke a LabVIEW COM method by dispid, bypassing type-info quirks.

    LabVIEW's ActiveX type library mis-declares some methods as properties
    (verified live: VI.GetPanelImage; VI.PrintVIToHTML failed with
    "Required parameter missing" because a bare getattr dispatched it as
    a no-argument property get). Going straight to
    IDispatch.GetIDsOfNames + Invoke with an explicit DISPATCH_METHOD flag
    is unambiguous. IDispatch results are re-wrapped as dynamic objects.
    """
    import pythoncom
    from win32com.client import dynamic

    raw = getattr(obj, "_oleobj_", obj)  # unwrap CDispatch -> PyIDispatch
    dispid = raw.GetIDsOfNames(0, name)
    result = raw.Invoke(dispid, 0, pythoncom.DISPATCH_METHOD, 1, *args)
    if isinstance(result, type(raw)):
        return dynamic.Dispatch(result)
    return result


def _first_attr(obj, *names):
    """Return the first attribute that exists and is not None."""
    for name in names:
        try:
            value = getattr(obj, name)
        except Exception:
            continue
        if value is not None:
            return value
    raise AttributeError(f"none of {names} found on COM object")


def _first_method_result(obj, candidates, *args):
    """Try method names in order; return (name_used, result)."""
    errors = []
    for name in candidates:
        try:
            return name, _flagged_call(obj, name, *args)
        except Exception as exc:  # noqa: BLE001 - we want the diagnostics
            errors.append(f"{name}: {type(exc).__name__}: {exc}")
    raise RuntimeError("no working method. Tried:\n  " + "\n  ".join(errors))


# ---------------------------------------------------------------------------
# Image conversion
# ---------------------------------------------------------------------------

def pixmap_to_png(image_data, out_path):
    """Convert LabVIEW 'Get Image' flattened-pixmap output to a PNG file.

    At 24-bit depth LabVIEW returns a 2D array of packed RGB values and
    ignores the color table. LabVIEW packs colors as 0x00BBGGRR
    (red = 0x000000FF), so R is the low byte.
    """
    rows = [list(r) for r in image_data]
    if not rows or not rows[0]:
        raise ValueError("empty image data returned")
    arr = np.array(rows, dtype=np.int64)
    h, w = arr.shape
    v = (arr & 0xFFFFFF).astype(np.uint32)
    r = (v & 0xFF).astype(np.uint8)
    g = ((v >> 8) & 0xFF).astype(np.uint8)
    b = ((v >> 16) & 0xFF).astype(np.uint8)
    rgb = np.dstack([r, g, b])
    Image.fromarray(rgb, mode="RGB").save(out_path)
    return w, h


def _safe_get(obj, *names, default="?"):
    """Return the first attribute that exists, else default."""
    for name in names:
        try:
            value = getattr(obj, name)
        except Exception:
            continue
        if value is not None:
            return value
    return default


def _probe_candidates(obj, label, names):
    """Report per-name what a COM object exposes (exists / None / missing)."""
    print(f"--- {label}: probing {len(names)} candidate names ---")
    for name in names:
        try:
            value = getattr(obj, name)
        except Exception as exc:
            print(f"  {name:18s} MISSING ({type(exc).__name__})")
            continue
        if value is None:
            print(f"  {name:18s} exists -> None")
        else:
            print(f"  {name:18s} exists -> {type(value).__name__}")


def probe(vi_path):
    """Dump the real COM member names via true dynamic dispatch (no makepy).

    The makepy typed wrapper on this machine is a partial/broken view of
    LabVIEW's type library (properties only, no methods), so the probe
    re-wraps the live server with win32com.client.dynamic.Dispatch and
    enumerates the live type info instead.
    """
    _purge_labview_makepy_cache()
    app, how = _dynamic_connect()
    print(f"connected: {how}")
    print(f"app object type: {type(app)}")

    members = sorted(n for n in dir(app) if not n.startswith("_"))
    print(f"--- Application members ({len(members)}) ---")
    for n in members:
        print("  ", n)

    _raw_names(app, "Application", ["GetVIReference", "Quit", "OpenProject"])

    path = os.path.abspath(vi_path)
    print(f"opening: {path}")
    vi = None
    for args in [(path, "", False, 0), (path,)]:
        try:
            vi = app.GetVIReference(*args)
            print(f"GetVIReference with {len(args)} arg(s): OK -> {type(vi)}")
            break
        except Exception as exc:  # noqa: BLE001
            print(f"GetVIReference with {len(args)} arg(s): "
                  f"{type(exc).__name__}: {exc}")
    if vi is None:
        print("could not open VI reference; probe stops here")
        return

    members = sorted(n for n in dir(vi) if not n.startswith("_"))
    print(f"--- VI members ({len(members)}) ---")
    for n in members:
        print("  ", n)

    _raw_names(vi, "VI", ["FP", "FrontPanel", "BD", "BlockDiagram",
                          "GetImage", "Print"])

    _probe_candidates(vi, "VI panel/diagram accessors",
                      ["FP", "FrontPanel", "BD", "BlockDiagram",
                       "Panel", "Diagram", "GetPanelImage", "ExportImage",
                       "Print", "GetImage", "GetImageScaled"])

    for name in ["FP", "FrontPanel", "BD", "BlockDiagram", "Panel", "Diagram"]:
        try:
            sub = getattr(vi, name)
        except Exception as exc:  # noqa: BLE001
            print(f"{name}: getattr raised {type(exc).__name__}: {exc}")
            continue
        if sub is None:
            print(f"{name}: exists -> None")
            continue
        print(f"--- {name}: object type {type(sub)} ---")
        members = sorted(n for n in dir(sub) if not n.startswith("_"))
        print(f"--- {name} members ({len(members)}) ---")
        for n in members:
            print("  ", n)

    # End-to-end: PrintVIToHTML should render panel + diagram PNGs.
    # Invoked by dispid with an explicit DISPATCH_METHOD flag -- LabVIEW's
    # type library mis-declares some methods as properties, and a normal
    # getattr would dispatch them as no-arg property gets.
    print("--- resolving PrintVIToHTML via raw GetIDsOfNames(0, name) ---")
    try:
        dispid = vi._oleobj_.GetIDsOfNames(0, "PrintVIToHTML")
        print(f"PrintVIToHTML dispid={dispid}")
    except Exception as exc:  # noqa: BLE001
        print(f"GetIDsOfNames FAILED: {type(exc).__name__}: {exc}")

    print("--- attempting PrintVIToHTML "
          "(append=False, format=1/Standard, imageFormat=0/PNG, depth=24) ---")
    tmp = tempfile.mkdtemp(prefix="lvprint_")
    html_path = os.path.join(tmp, "vi_doc.html")
    img_dir = os.path.join(tmp, "images")
    os.makedirs(img_dir, exist_ok=True)
    try:
        _lv_invoke(vi, "PrintVIToHTML", html_path, False, 1, 0, 24, img_dir)
        print("PrintVIToHTML returned OK")
    except Exception as exc:  # noqa: BLE001
        print(f"PrintVIToHTML FAILED: {type(exc).__name__}: {exc}")
    print(f"--- files under {tmp} ---")
    for root, _d, files in os.walk(tmp):
        for f in sorted(files):
            p = os.path.join(root, f)
            print(f"  {os.path.relpath(p, tmp)}  ({os.path.getsize(p)} bytes)")
    if os.path.isfile(html_path):
        print("--- vi_doc.html content ---")
        with open(html_path, encoding="utf-8", errors="ignore") as fh:
            print(fh.read())
        print("--- end html ---")
        roles = _map_print_images(html_path)
        print(f"mapped roles: {roles}")
        for role, p in roles.items():
            try:
                with Image.open(p) as im:
                    print(f"  {role}: {im.size[0]}x{im.size[1]} {im.mode} "
                          f"({os.path.getsize(p)} bytes)")
            except Exception as exc:  # noqa: BLE001
                print(f"  {role}: unreadable ({type(exc).__name__})")
    else:
        print("no HTML file was generated")

    print("probe complete. Send this whole output back.")


def _dynamic_connect():
    """Connect to LabVIEW via true dynamic dispatch.

    Bypasses the makepy typed-wrapper cache: on this machine makepy
    generated a partial LabVIEW wrapper (properties only, no methods),
    which then poisons every plain Dispatch/GetActiveObject call.
    win32com.client.dynamic.Dispatch always talks to the live server.
    """
    import win32com.client
    from win32com.client import dynamic

    try:
        running = win32com.client.GetActiveObject("LabVIEW.Application")
    except Exception as exc:  # noqa: BLE001
        print(f"  (no running LabVIEW to attach to: {exc})")
    else:
        try:
            return dynamic.Dispatch(running), "attached to running LabVIEW"
        except Exception as exc:  # noqa: BLE001
            print(f"  (could not re-wrap running instance dynamically: {exc})")
    return dynamic.Dispatch("LabVIEW.Application"), "launched LabVIEW via COM"


def _purge_labview_makepy_cache():
    """Delete the broken cached LabVIEW wrapper, if makepy made one."""
    try:
        import os
        import shutil
        import win32com.client.gencache as gencache
        gen_path = gencache.GetGeneratePath()
        removed = []
        if os.path.isdir(gen_path):
            for entry in os.listdir(gen_path):
                sub = os.path.join(gen_path, entry)
                if not os.path.isdir(sub):
                    continue
                hit = False
                for root, _d, files in os.walk(sub):
                    for f in files:
                        if not f.endswith(".py"):
                            continue
                        try:
                            with open(os.path.join(root, f), encoding="utf-8",
                                      errors="ignore") as fh:
                                if "labview" in fh.read(65536).lower():
                                    hit = True
                                    break
                        except OSError:
                            continue
                    if hit:
                        break
                if hit:
                    shutil.rmtree(sub, ignore_errors=True)
                    removed.append(entry)
            # Drop the cache index too; it is rebuilt on demand.
            dicts = os.path.join(gen_path, "dicts.dat")
            if removed and os.path.exists(dicts):
                try:
                    os.remove(dicts)
                except OSError:
                    pass
        if removed:
            print(f"  removed stale makepy LabVIEW wrapper(s): {removed}")
    except Exception as exc:  # noqa: BLE001 - cache cleanup must never be fatal
        print(f"  (could not purge makepy cache: {exc})")


def _raw_names(obj, label, names):
    """Check name resolution directly against the raw IDispatch.

    Distinguishes "name missing from type info" from "name truly absent":
    dynamic dispatch can still call a method the type info does not list.
    """
    raw = getattr(obj, "_oleobj_", None)
    if raw is None:
        print(f"{label}: no raw IDispatch available")
        return
    print(f"--- {label}: raw GetIDsOfNames ---")
    for n in names:
        try:
            dispid = raw.GetIDsOfNames(0, n)
            print(f"  {n:18s} resolves, dispid={dispid}")
        except Exception as exc:  # noqa: BLE001
            print(f"  {n:18s} NOT resolved ({type(exc).__name__})")


def connect_app():
    """Connect to LabVIEW via ActiveX (dynamic dispatch).

    Tries an already-running LabVIEW instance first (most reliable),
    then falls back to launching one via COM.
    """
    _purge_labview_makepy_cache()
    return _dynamic_connect()


def _map_print_images(html_path):
    """Map PrintVIToHTML output images to 'fp' / 'bd' roles.

    LabVIEW names its generated image files unpredictably, so parse the
    HTML first: each <img> is attributed to the nearest preceding section
    whose text mentions 'front panel' or 'block diagram'. As a fallback
    for roles the HTML parse misses, use LabVIEW's filename convention
    <htmlbase><suffix>.png (observed on LV2021: 'c' connector pane,
    'p' front panel, 'd' block diagram). Returns a dict like
    {'fp': path, 'bd': path} for the roles that could be identified.
    """
    import re

    with open(html_path, encoding="utf-8", errors="ignore") as fh:
        html = fh.read()
    base = os.path.dirname(os.path.abspath(html_path))

    tokens = []  # ("text", str) | ("img", src), in document order
    pos = 0
    for m in re.finditer(r"<img\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"'][^>]*>",
                         html, re.I):
        chunk = re.sub(r"<[^>]+>", " ", html[pos:m.start()])
        tokens.append(("text", " ".join(chunk.split())))
        tokens.append(("img", m.group(1)))
        pos = m.end()
    chunk = re.sub(r"<[^>]+>", " ", html[pos:])
    tokens.append(("text", " ".join(chunk.split())))

    roles = {}
    section = ""
    for kind, val in tokens:
        if kind == "text":
            low = val.lower()
            if "block diagram" in low:
                section = "bd"
            elif "front panel" in low:
                section = "fp"
        else:
            p = (val if os.path.isabs(val)
                 else os.path.normpath(os.path.join(base, val)))
            if section in ("fp", "bd") and section not in roles \
                    and os.path.isfile(p):
                roles[section] = p

    # Fallback: filename suffix convention for roles the HTML parse missed.
    if not ("fp" in roles and "bd" in roles):
        html_base = os.path.splitext(os.path.basename(html_path))[0]
        img_dir = os.path.join(base, "images")
        suffix_roles = {"p": "fp", "d": "bd"}
        if os.path.isdir(img_dir):
            for f in sorted(os.listdir(img_dir)):
                if not f.lower().endswith(".png"):
                    continue
                stem = f[:-len(".png")]
                if not stem.startswith(html_base):
                    continue
                role = suffix_roles.get(stem[len(html_base):])
                if role and role not in roles:
                    roles[role] = os.path.join(img_dir, f)
    return roles


def export_via_print(vi, work_dir):
    """Export a VI's front-panel / block-diagram PNGs via PrintVIToHTML.

    Renders the VI documentation (format=Standard: description, icon and
    connector pane, front panel, block diagram) as PNG files into work_dir,
    then identifies the panel/diagram images from the generated HTML.
    Returns {'fp': png_path, 'bd': png_path} for the roles found.
    Raises on COM failure.
    """
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir, ignore_errors=True)
    img_dir = os.path.join(work_dir, "images")
    os.makedirs(img_dir, exist_ok=True)
    html_path = os.path.join(work_dir, "vi_doc.html")

    # format=1 Standard, imageFormat=0 PNG, imageDepth=24 true color.
    _lv_invoke(vi, "PrintVIToHTML", html_path, False, 1, 0, 24, img_dir)

    return _map_print_images(html_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("src", help="folder to scan recursively for .vi files")
    ap.add_argument("-o", "--out", default="vi_images",
                    help="output folder (default: vi_images)")
    ap.add_argument("--fp-only", action="store_true",
                    help="export front panels only")
    ap.add_argument("--bd-only", action="store_true",
                    help="export block diagrams only")
    ap.add_argument("--probe", metavar="VI_PATH",
                    help="diagnostic: dump COM member names for one VI and exit")
    args = ap.parse_args()

    if args.probe:
        probe(args.probe)
        return

    src = os.path.abspath(args.src)
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    vi_files = []
    for root, _dirs, files in os.walk(src):
        for f in files:
            if f.lower().endswith(".vi"):
                vi_files.append(os.path.join(root, f))
    vi_files.sort()
    if not vi_files:
        sys.exit(f"no .vi files found under {src}")
    print(f"found {len(vi_files)} .vi files under {src}")

    print("connecting to LabVIEW via ActiveX ...")
    try:
        import win32com.client  # noqa: F401
    except ImportError:
        sys.exit("pywin32 is required on the LabVIEW machine: pip install pywin32")
    try:
        app, how = connect_app()
    except Exception as exc:  # noqa: BLE001
        sys.exit(
            "Could not connect to LabVIEW via ActiveX.\n"
            "Checklist:\n"
            "  - Open LabVIEW 2021 first and keep it running, then re-run this script\n"
            "  - If you just enabled ActiveX, restart LabVIEW\n"
            "  - Tools > Options > VI Server > ActiveX: server is enabled\n"
            f"  - details:\n{exc}"
        )
    print(f"connected ({how}): {_safe_get(app, 'Name', 'ApplicationName', 'OSName', default='LabVIEW')}")

    manifest_path = os.path.join(out, "manifest.csv")
    manifest = open(manifest_path, "w", newline="", encoding="utf-8")
    writer = csv.writer(manifest)
    writer.writerow(["vi_path", "fp_png", "bd_png", "status", "notes"])

    do_fp = not args.bd_only
    do_bd = not args.fp_only

    for i, vi_path in enumerate(vi_files, 1):
        rel = os.path.relpath(vi_path, src)
        stem = os.path.splitext(rel)[0]
        fp_png = os.path.join(out, stem + ".fp.png")
        bd_png = os.path.join(out, stem + ".bd.png")
        work = os.path.join(out, "_print_work", stem + ".work")
        fp_done = bd_done = False

        notes, status = [], "ok"
        try:
            vi = _lv_invoke(app, "GetVIReference",
                            os.path.abspath(vi_path), "", False, 0)
        except Exception as exc:  # noqa: BLE001
            status = "open_failed"
            notes.append(f"GetVIReference: {type(exc).__name__}: {exc}")
            writer.writerow([rel, "", "", status, " | ".join(notes)])
            print(f"[{i}/{len(vi_files)}] OPEN-FAILED {rel}")
            continue

        try:
            roles = export_via_print(vi, work)
            if do_fp:
                if "fp" in roles:
                    os.makedirs(os.path.dirname(fp_png) or ".", exist_ok=True)
                    shutil.copy2(roles["fp"], fp_png)
                    fp_done = True
                    notes.append("front panel ok")
                else:
                    status = "partial"
                    notes.append("front panel image not identified")
            if do_bd:
                if "bd" in roles:
                    os.makedirs(os.path.dirname(bd_png) or ".", exist_ok=True)
                    shutil.copy2(roles["bd"], bd_png)
                    bd_done = True
                    notes.append("block diagram ok")
                else:
                    status = "partial"
                    notes.append("block diagram image not identified")
            if status == "ok":
                shutil.rmtree(work, ignore_errors=True)
            else:
                notes.append("raw print output kept at "
                             f"{os.path.relpath(work, out)}")
        except Exception as exc:  # noqa: BLE001
            status = "error"
            notes.append(f"PrintVIToHTML: {type(exc).__name__}: {exc}")
        finally:
            # Release the reference so LabVIEW can unload the VI.
            try:
                del vi
            except Exception:  # noqa: BLE001
                pass
            gc.collect()

        writer.writerow([rel,
                         os.path.relpath(fp_png, out) if fp_done else "",
                         os.path.relpath(bd_png, out) if bd_done else "",
                         status, " | ".join(notes)])
        print(f"[{i}/{len(vi_files)}] {status.upper()} {rel}")

    manifest.close()
    print(f"\ndone. manifest: {manifest_path}")
    print("Zip the output folder and upload it for reconciliation.")


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 - show full trace for diagnostics
        traceback.print_exc()
        sys.exit(1)
