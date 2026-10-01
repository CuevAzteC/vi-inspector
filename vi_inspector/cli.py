"""CLI for vi-inspector."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vi_inspector.vi import inspect_vi  # noqa: E402
from vi_inspector.project import parse_project_file, summarize_project  # noqa: E402
from vi_inspector.review import review_many, SEVERITY_ORDER, ReviewContext  # noqa: E402
from vi_inspector.report import generate_report  # noqa: E402


def _relpath(p: str) -> str:
    return os.path.relpath(p)


def _fingerprint(rule_id: str, relpath: str, title: str) -> str:
    return f"{rule_id}::{relpath}::{title}"


def _load_baseline(path: str) -> set[str]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    findings = data.get("findings", data)  # allow a bare list too
    return set(findings)


def _save_baseline(path: str, reviews) -> None:
    fps = []
    for r in reviews:
        rel = _relpath(r.vi_path)
        for fnd in r.findings:
            fps.append(_fingerprint(fnd.rule_id, rel, fnd.title))
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "findings": sorted(fps)}, f, indent=2)


def _write_sarif(path: str, reviews, new_fps: set[str] | None) -> None:
    """Minimal SARIF 2.1.0 for GitHub code scanning / generic SARIF consumers."""
    rules = {}
    results = []
    for r in reviews:
        rel = _relpath(r.vi_path)
        for fnd in r.findings:
            rules.setdefault(fnd.rule_id, {
                "id": fnd.rule_id,
                "name": fnd.rule_id,
                "shortDescription": {"text": fnd.title.split(" (×")[0]},
                "defaultConfiguration": {"level": {
                    "high": "error", "medium": "warning",
                    "low": "note", "info": "note"}[fnd.severity]},
            })
            fp = _fingerprint(fnd.rule_id, rel, fnd.title)
            if new_fps is not None and fp not in new_fps:
                continue  # baseline: only new findings surface in scans
            results.append({
                "ruleId": fnd.rule_id,
                "message": {"text": f"{fnd.title}. {fnd.detail}"},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": rel.replace(os.sep, "/")},
                        "region": {"startLine": 1},
                    }
                }],
            })
    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {
                "name": "vi-inspector",
                "informationUri": "https://github.com/vi-inspector/vi-inspector",
                "rules": list(rules.values()),
            }},
            "results": results,
        }],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sarif, f, indent=2)


def _emit_github_annotations(new_findings) -> None:
    """File-level workflow commands; auto-enabled when GITHUB_ACTIONS=true."""
    level = {"high": "error", "medium": "warning",
             "low": "notice", "info": "notice"}
    for rel, fnd in new_findings:
        print(f"::{level[fnd.severity]} file={rel}"
              f"::{fnd.rule_id}: {fnd.title}")


def cmd_review(args) -> int:
    import glob as _glob
    vi_paths: list[str] = []
    for p in args.paths:
        if os.path.isdir(p):
            vi_paths.extend(sorted(_glob.glob(os.path.join(p, "**", "*.vi"),
                                              recursive=True)))
        else:
            vi_paths.append(p)
    ctx = ReviewContext(vi_paths)
    reviews = review_many(vi_paths, ctx)

    parse_failures = [r for r in reviews if not r.parse_ok]
    if parse_failures and not args.ignore_parse_errors:
        for r in parse_failures:
            print(f"PARSE ERROR {r.vi_path}: {r.parse_error}", file=sys.stderr)
        return 2

    if args.update_baseline:
        _save_baseline(args.update_baseline, reviews)
        n = sum(len(r.findings) for r in reviews)
        print(f"Baseline written to {args.update_baseline} "
              f"({n} findings across {len(reviews)} VIs).")
        return 0

    baseline = _load_baseline(args.baseline) if args.baseline else None

    # (relpath, finding, is_new)
    rows: list[tuple[str, object, bool]] = []
    for r in reviews:
        rel = _relpath(r.vi_path)
        for fnd in r.findings:
            fp = _fingerprint(fnd.rule_id, rel, fnd.title)
            rows.append((rel, fnd, baseline is None or fp not in baseline))
    # fingerprint -> is_new lookup for the JSON/SARIF emitters below
    new_by_fp = {_fingerprint(fnd.rule_id, rel, fnd.title): is_new
                 for rel, fnd, is_new in rows}

    fail_sevs = {s for s, o in SEVERITY_ORDER.items()
                 if o <= SEVERITY_ORDER[args.fail_on]} if args.fail_on != "never" else set()
    failing = [(rel, fnd) for rel, fnd, is_new in rows
               if is_new and fnd.severity in fail_sevs]
    new_findings = [(rel, fnd) for rel, fnd, is_new in rows if is_new]

    if args.json:
        out = []
        for r in reviews:
            rel = _relpath(r.vi_path)
            out.append({
                "vi": r.vi_name, "path": r.vi_path, "parse_ok": r.parse_ok,
                "metrics": r.metrics,
                "findings": [
                    {"rule": f.rule_id, "severity": f.severity,
                     "title": f.title, "detail": f.detail,
                     "node": f.node_name,
                     "new": new_by_fp[_fingerprint(f.rule_id, rel, f.title)]}
                    for f in r.findings
                ],
            })
        print(json.dumps(out, indent=2))
    else:
        totals: dict[str, int] = {}
        new_totals: dict[str, int] = {}
        for _, fnd, is_new in rows:
            totals[fnd.severity] = totals.get(fnd.severity, 0) + 1
            if is_new:
                new_totals[fnd.severity] = new_totals.get(fnd.severity, 0) + 1
        summary = ", ".join(f"{v} {k}" for k, v in sorted(totals.items()))
        print(f"Reviewed {len(reviews)} VIs: {summary}")
        if baseline is not None:
            new_summary = ", ".join(f"{v} {k}"
                                    for k, v in sorted(new_totals.items()))
            print(f"New since baseline: {new_summary or 'none'}")
        for rel, fnd in failing:
            print(f"  FAIL [{fnd.severity}/{fnd.rule_id}] {rel}: {fnd.title}")

    if args.sarif:
        new_fps = {fp for fp, is_new in new_by_fp.items() if is_new}
        _write_sarif(args.sarif, reviews, new_fps)
        print(f"SARIF report: {args.sarif}")

    if os.environ.get("GITHUB_ACTIONS") == "true":
        _emit_github_annotations(new_findings)

    if args.html:
        idx = generate_report(reviews, "LabVIEW Code Review", args.html,
                              ground_truth_dir=args.ground_truth)
        print(f"\nHTML report: {idx}")
    return 1 if failing else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Inspect LabVIEW files without LabVIEW installed.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_vi = sub.add_parser("vi", help="Inspect a .vi/.ctl binary")
    p_vi.add_argument("path")

    p_proj = sub.add_parser("project",
                            help="Inspect a .lvproj/.lvlib/.lvclass file")
    p_proj.add_argument("path")
    p_proj.add_argument("--full", action="store_true",
                        help="Emit the full nested tree, not just the summary")
    p_proj.add_argument("--dispatch", action="store_true",
                        help="For .lvclass: report dynamic-dispatch status of "
                             "member VIs (from NI.ClassItem.IsStaticMethod)")

    p_rev = sub.add_parser("review", help="Run automated code review on VIs")
    p_rev.add_argument("paths", nargs="+",
                       help=".vi files or directories (recursive)")
    p_rev.add_argument("--html", metavar="OUT_DIR",
                       help="Write HTML report to OUT_DIR")
    p_rev.add_argument("--json", action="store_true",
                       help="Emit findings as JSON instead of text summary")
    p_rev.add_argument("--ground-truth", metavar="DIR",
                       help="Folder of LabVIEW-exported PNGs (from "
                            "export_vi_images.py); embeds the genuine "
                            "front-panel/block-diagram images in the report")
    p_rev.add_argument("--fail-on", default="high",
                       choices=["high", "medium", "low", "info", "never"],
                       help="Exit 1 if any NEW finding at or above this "
                            "severity (default: high)")
    p_rev.add_argument("--baseline", metavar="FILE",
                       help="JSON baseline from --update-baseline; only "
                            "findings not in the baseline count as new")
    p_rev.add_argument("--update-baseline", metavar="FILE",
                       help="Write current findings as a new baseline file "
                            "and exit 0")
    p_rev.add_argument("--sarif", metavar="FILE",
                       help="Write SARIF 2.1.0 report (for GitHub code "
                            "scanning); honors the baseline")
    p_rev.add_argument("--ignore-parse-errors", action="store_true",
                       help="Exit 0/1 on findings even if some VIs failed "
                            "to parse (default: exit 2)")

    args = ap.parse_args(argv)
    if args.cmd == "review":
        return cmd_review(args)
    if args.cmd == "vi":
        report = inspect_vi(args.path)
    else:
        info = parse_project_file(args.path,
                                  resolve_dispatch=args.dispatch)
        report = info if args.full else summarize_project(info)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    sys.exit(main())
