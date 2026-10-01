# Developer workflow

How a LabVIEW developer adopts vi-inspector, from first run to daily CI.
No LabVIEW license needed anywhere in this flow.

## 1. Try it locally (5 minutes)

```bash
pip install vi-inspector
vi-inspector review path/to/project --html report/
```

Open `report/index.html`: a Project-Explorer-style sidebar lists every VI
in its folder hierarchy with severity dots — pick a VI to see its findings
next to the rendered block diagram. This is the "is this tool telling the
truth about my code?" step — spot-check a few findings against diagrams
you know.

The report speaks LabVIEW:

- **Block diagram / Front panel tabs** — `Ctrl+E` toggles, just like LabVIEW.
- **Click a SubVI node** in the diagram to jump to its report page;
  **double-click it** to open the `.vi` in LabVIEW (works when the report
  is viewed from disk).
- **Open in LabVIEW** / **Copy path** buttons on every VI page.
- **Calls / Called by** hierarchy per VI, so you can walk the call chain.
- Sidebar **search** and **hide-clean** toggle for big projects.

## 2. Triage: fix what's real, bless the rest

Run the review and sort findings into two piles:

- **Real bugs** (unwired error terminals are the classic) — fix them in
  LabVIEW.
- **Accepted / legacy** — everything you won't fix right now.

Bless the accepted pile as your baseline:

```bash
vi-inspector review path/to/project --update-baseline .vi-inspector-baseline.json
```

Commit `.vi-inspector-baseline.json` next to your code. From now on the
tool only reports **new** findings — legacy code never blocks you.

## 3. Gate pull requests (one workflow file)

`.github/workflows/labview-review.yml`:

```yaml
name: LabVIEW review
on: [push, pull_request]
permissions:
  contents: read
  security-events: write   # only needed for sarif: true
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: CuevAzteC/vi-inspector@v1
        with:
          path: 'src/'
          fail-on: high
          baseline: .vi-inspector-baseline.json
          sarif: true
```

What happens on every PR:

1. The action installs vi-inspector and reviews the changed code —
   no LabVIEW, no license, ~a minute.
2. New findings appear as **inline annotations** on the PR diff
   (`::error` for high, `::warning` for medium).
3. SARIF results land in the **Security → Code scanning** tab.
4. The check fails only if there are **new** findings at/above
   `fail-on`. Old findings in the baseline never block a merge.

## 4. The daily loop

- Open a PR → review runs automatically → annotations point at the
  exact VI and node.
- Fix the finding in LabVIEW, push again — annotation clears.
- If a finding is a false positive or accepted risk, don't argue with
  the tool in the PR: update the baseline
  (`--update-baseline`), commit it, and move on. The baseline is the
  team's shared record of accepted findings.
- Tighten `fail-on` from `high` → `medium` once the high-severity
  backlog is cleared.

## 5. Reading the output

- **Text summary** (default): per-VI counts, exit code tells CI pass/fail.
- **HTML report** (`--html`): Project-Explorer-style dashboard with folder
  tree, block-diagram / front-panel / connector-pane tabs (`Ctrl+E`),
  clickable SubVI nodes (click = report page, double-click = open in
  LabVIEW), click-a-finding to flash its node on the diagram, hover any
  wire for its data type, a ◐ Theme toggle for dark mode, and per-VI
  Calls / Called-by hierarchy — good for reviews and audits.
- **JSON** (`--json`): machine-readable, `new: true/false` per finding —
  feed it to your own tooling.
- **SARIF** (`--sarif`): GitHub code scanning / any SARIF viewer.

Exit codes: `0` = clean (or only baseline findings), `1` = new findings
at/above `--fail-on`, `2` = a VI failed to parse (use
`--ignore-parse-errors` to treat those as non-blocking).

## Notes for LabVIEW teams

- The tool reads `.vi`/`.ctl` binaries directly — it never needs your
  LabVIEW install, license server, or a Windows runner.
- Binary VIs diff poorly in git; the HTML report is the readable
  review surface for LabVIEW code.
- Start with `fail-on: high` and a baseline. Teams that start at
  `fail-on: info` with no baseline drown in legacy findings and turn
  the check off — the baseline is what makes this adoptable.
