"""CLI for vi-inspector."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vi_inspector.vi import inspect_vi  # noqa: E402
from vi_inspector.project import parse_project_file, summarize_project  # noqa: E402
from vi_inspector.review import review_many  # noqa: E402
from vi_inspector.report import generate_report  # noqa: E402


def cmd_review(args) -> int:
    import glob as _glob
    vi_paths: list[str] = []
    for p in args.paths:
        if os.path.isdir(p):
            vi_paths.extend(sorted(_glob.glob(os.path.join(p, "**", "*.vi"),
                                              recursive=True)))
        else:
            vi_paths.append(p)
    reviews = review_many(vi_paths)
    if args.json:
        out = []
        for r in reviews:
            out.append({
                "vi": r.vi_name, "path": r.vi_path, "parse_ok": r.parse_ok,
                "metrics": r.metrics,
                "findings": [
                    {"rule": f.rule_id, "severity": f.severity,
                     "title": f.title, "detail": f.detail,
                     "node": f.node_name}
                    for f in r.findings
                ],
            })
        print(json.dumps(out, indent=2))
    else:
        totals: dict[str, int] = {}
        for r in reviews:
            for f in r.findings:
                totals[f.severity] = totals.get(f.severity, 0) + 1
        print(f"Reviewed {len(reviews)} VIs: " +
              ", ".join(f"{v} {k}" for k, v in sorted(totals.items())))
        for r in reviews:
            highs = r.by_severity("high")
            if highs:
                print(f"\n{r.vi_name}:")
                for f in highs:
                    print(f"  [{f.rule_id}] {f.title}")
    if args.html:
        idx = generate_report(reviews, "LabVIEW Code Review", args.html,
                              ground_truth_dir=args.ground_truth)
        print(f"\nHTML report: {idx}")
    return 0


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
    main()
