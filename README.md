# vi-inspector

Automated code review for LabVIEW — in CI, **without LabVIEW installed**.

Point it at your VIs; it flags error-handling defects, broken error chains,
race-condition risks, and oversized diagrams. Designed for pull-request
gating: stable exit codes, baselines ("fail only on new findings"), SARIF
output for GitHub code scanning, and a marketplace-ready GitHub Action.

## Quickstart

```bash
pip install vi-inspector
vi-inspector review path/to/project --fail-on high
```

Exit codes: `0` = clean, `1` = new findings at/above `--fail-on`,
`2` = operational error (e.g. a VI failed to parse).

## CI usage

```yaml
- uses: vi-inspector/vi-inspector@v1
  with:
    path: 'src/'
    fail-on: high
    baseline: .vi-inspector-baseline.json
    sarif: true   # needs security-events: write
```

Adopting on an existing codebase? Bless the current state, then gate on
regressions:

```bash
vi-inspector review src/ --update-baseline .vi-inspector-baseline.json
# commit the baseline; CI now fails only on NEW findings
```

Other useful flags: `--json`, `--sarif FILE`, `--html OUT_DIR`,
`--ignore-parse-errors`. Under `GITHUB_ACTIONS`, file-level
`::error`/`::warning` annotations are emitted automatically.

## Rule catalog

| Rule | Severity | What it flags |
|------|----------|---------------|
| ERR-1 | high / medium | Unwired error terminals on SubVI calls. Unwired **error out** → high (errors silently dropped). Unwired **error in** with error-out wired → medium (node runs even when upstream errored). Error-handler VIs are exempt (chain terminators by design). |
| ERR-1b | medium | Broken error chain on primitives: error-in wired but error-out unwired. Node names include method/property names (e.g. `Invoke Node 'FP.Close'`). |
| ERR-2 | high | Connector pane exposes error in/out but no error cluster is wired anywhere on the diagram. |
| RACE-1 | medium | Local variables (one summarized finding per VI — they break dataflow and risk races). |
| CPLX-1 | info | Diagrams over 50 nodes — consider splitting into subVIs. |

**Precision:** every rule was audited against genuine LabVIEW-rendered block
diagrams (15 findings sampled, verified by hand). ERR-1 true-positive rate
75%, RACE-1 and CPLX-1 100%. A former WIRE-1 rule ("unwired SubVI inputs")
was **removed** after the audit found 0% actionable hits — method-call nodes
expose phantom terminals in the parsed model and the rest were
optional-with-defaults noise. A precise version needs cross-VI connector-pane
analysis and is tracked as a planned rule.

## Compatibility

Verified against 106 real `.vi` files — see [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md):

| Saved in | Files | Status |
|----------|-------|--------|
| LabVIEW 21.0 | 103 | ✓ full review |
| LabVIEW 14.0 | 2 | ✓ full review |
| LabVIEW 8.6 | 1 | ✗ known limitation (diagram extraction fails) |

Untested versions are untested — no claim is made about them.

## How it works

- `pylabview` (MIT) reads the RSRC binary container: version, blocks, connector pane, dependencies.
- `lvkit` 0.8.6 (Apache-2.0) parses block diagrams semantically (nodes, terminals, wires) and renders diagrams.
- `vi_inspector/review.py` runs the rules; `report.py` builds the HTML dashboard.

## Development

```bash
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"  # or: pip install -r requirements.txt
.venv/bin/python -m pytest tests/ -q
```

## License

MIT — see [LICENSE](LICENSE). "LabVIEW" is a trademark of National
Instruments / Emerson; this project is not affiliated with or endorsed by
NI or Emerson.
