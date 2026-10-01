"""Parse LabVIEW project/library/class XML files.

.lvproj, .lvlib and .lvclass are plain UTF-8 XML (with BOM). This module builds:
  * the project tree (targets, folders, VIs, libraries, dependencies)
  * class hierarchies: for each .lvclass, its parent class (inheritance) and
    member VIs, distinguishing dynamic-dispatch VIs.

No LabVIEW installation required.
"""

import os
import xml.etree.ElementTree as ET

# Dynamic dispatch VIs carry this property on the owning class or the VI item.
DISPATCH_HINT_PROPS = {"NI.LVClass.IsDispatch", "NI.Lib.IsDispatch"}


def _strip_bom(path):
    with open(path, "rb") as fh:
        data = fh.read()
    return data.decode("utf-8-sig")


def _item_to_dict(item):
    d = {"name": item.get("Name"), "type": item.get("Type"),
         "url": item.get("URL"), "properties": {}, "children": []}
    for prop in item.findall("Property"):
        d["properties"][prop.get("Name")] = (prop.get("Type"), prop.text)
    for child in item.findall("Item"):
        d["children"].append(_item_to_dict(child))
    return d


def parse_project_file(path, resolve_dispatch=False):
    """Parse .lvproj / .lvlib / .lvclass into a nested dict.

    With resolve_dispatch=True, each member VI of an .lvclass gets its
    dynamic-dispatch status from the class XML (NI.ClassItem.IsStaticMethod).
    """
    path = os.path.abspath(path)
    root = ET.fromstring(_strip_bom(path))
    kind = {  # root tag -> file kind
        "Project": "lvproj", "Library": "lvlib", "LVClass": "lvclass",
    }.get(root.tag, root.tag)
    info = {"file": path, "kind": kind,
            "labview_version": root.get("LVVersion"),
            "properties": {}, "items": []}
    for prop in root.findall("Property"):
        info["properties"][prop.get("Name")] = (prop.get("Type"), prop.text)
    for item in root.findall("Item"):
        info["items"].append(_item_to_dict(item))
    if kind == "lvclass":
        info["class"] = _class_summary(root, path, resolve_dispatch)
    return info


def _find_parent_class(root):
    """Parent class: <Inheritance> in older files, Item Type='Parent' in newer."""
    inherit = root.find("Inheritance")
    if inherit is not None:
        parent = inherit.find("ParentClass")
        if parent is not None:
            return {"name": parent.get("Name"), "url": parent.get("URL")}
    for item in root.iter("Item"):
        if item.get("Type") == "Parent":
            return {"name": item.get("Name"), "url": item.get("URL")}
    return None


def _class_summary(root, path, resolve_dispatch=False):
    """Inheritance + members for one .lvclass file.

    Member VIs sit under top-level folders ('public'/'private' in older
    files; 'Accessors'/'Overrides'/... in newer ones). The folder name is
    recorded as scope, and LabVIEW's own 'Overrides' folder convention marks
    override VIs. Dynamic-dispatch status comes from the class XML itself:
    each member VI carries NI.ClassItem.IsStaticMethod (false = dynamic
    dispatch). The VI binary's own dispatch flag is unreliable on LV 2021
    files, so the class record is authoritative.
    """
    summary = {"name": os.path.splitext(os.path.basename(path))[0],
               "parent_class": _find_parent_class(root), "member_vis": []}

    def _walk(items, scope):
        for item in items:
            itype, name = item.get("Type"), item.get("Name")
            if itype in ("VI", "LVClass"):
                entry = {"name": name, "type": itype,
                         "url": item.get("URL"), "scope": scope,
                         "override": scope == "Overrides"}
                if resolve_dispatch and itype == "VI":
                    entry["dynamic_dispatch"] = None
                    for prop in item.findall("Property"):
                        if prop.get("Name") == "NI.ClassItem.IsStaticMethod":
                            entry["dynamic_dispatch"] = (
                                (prop.text or "").strip().lower() == "false")
                            break
                summary["member_vis"].append(entry)
            _walk(item.findall("Item"),
                  scope if itype != "Folder" else name)

    _walk(root.findall("Item"), None)
    return summary


def walk_items(items, kinds=("VI", "LVClass", "Library")):
    """Yield every item of the given kinds, recursively."""
    for item in items:
        if item["type"] in kinds:
            yield item
        yield from walk_items(item["children"], kinds)


def summarize_project(info):
    """Flat, documentation-friendly summary of a parsed project file."""
    items = list(walk_items(info["items"]))
    by_type = {}
    for it in items:
        by_type.setdefault(it["type"], []).append(it["name"])
    return {
        "file": info["file"], "kind": info["kind"],
        "labview_version": info["labview_version"],
        "counts": {k: len(v) for k, v in by_type.items()},
        "vis": sorted(by_type.get("VI", [])),
        "libraries": sorted(by_type.get("Library", [])),
        "classes": sorted(by_type.get("LVClass", [])),
        "class_detail": info.get("class"),
    }
