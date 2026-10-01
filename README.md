# vi-inspector

Read LabVIEW project files **without LabVIEW installed**. Prototype for a
LabVIEW documentation / code-review tool.

## What it does

* `vi` — parse a `.vi` / `.ctl` binary (RSRC container) and report:
  LabVIEW version that saved it, block inventory, password/locked-diagram
  status, execution flags (reentrant, run-on-open, dynamic dispatch…),
  connector pane, SubVI/library dependencies, icon presence.
* `project` — parse `.lvproj` / `.lvlib` / `.lvclass` XML: project tree,
  class inheritance (parent class), member VIs with access scope, and —
  with `--dispatch` — dynamic-dispatch status per member VI
  (from `NI.ClassItem.IsStaticMethod` in the class XML).

## How it works

Binary parsing is handled by the MIT-licensed
[pylabview](https://github.com/mefistotelis/pylabview) package (pip).
`.lvproj` / `.lvlib` / `.lvclass` files are plain XML and parsed directly.

Multi-version strategy: the RSRC *container* layout is stable across LabVIEW
versions; per-block contents vary. The parser walks the container generically,
decodes the blocks it understands, records the exact saving LabVIEW version,
and skips unknown blocks instead of failing. 32-bit vs 64-bit LabVIEW saves
byte-identical files — bitness does not affect parsing.

## Usage

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m vi_inspector.cli vi path/to/file.vi
.venv/bin/python -m vi_inspector.cli project path/to/project.lvproj
```

## Fixtures

`fixtures/` holds sample files from
[tomsoftware/VI-Explorer-VI](https://github.com/tomsoftware/VI-Explorer-VI)
(MIT, © 2016 Thomas Zeugner), used to validate the parser.
