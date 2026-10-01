"""HTML report generation for VI code reviews.

Dashboard + per-VI pages with findings and embedded block-diagram renders.
Dependency-free output: inline CSS, diagrams as inline SVG via lvkit.
"""
from __future__ import annotations

import csv
import html
import shutil
from pathlib import Path, PurePath

from lvkit.render import render_vi_file

from .review import SEVERITY_ORDER, VIReview

SEV_COLORS = {
    "high": "#c0392b",
    "medium": "#d68910",
    "low": "#2e86c1",
    "info": "#7f8c8d",
}

CSS = """
body{font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
margin:0;color:#1a1a1a;background:#f7f8fa}
.wrap{max-width:1100px;margin:0 auto;padding:24px}
.card{background:#fff;border:1px solid #e3e6ea;border-radius:10px;
padding:18px 22px;margin-bottom:18px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
h1{font-size:26px;margin:0 0 6px}h2{font-size:19px;margin:0 0 10px}
.sub{color:#666;font-size:14px;margin-bottom:16px}
.badges{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.badge{border-radius:8px;padding:10px 16px;color:#fff;font-weight:600;font-size:15px}
.badge small{display:block;font-weight:400;font-size:12px;opacity:.9}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;padding:8px 10px;border-bottom:2px solid #e3e6ea;color:#555;
font-size:12px;text-transform:uppercase;letter-spacing:.04em}
td{padding:8px 10px;border-bottom:1px solid #eef0f2;vertical-align:top}
tr:hover td{background:#fafbfc}
a{color:#2e86c1;text-decoration:none}a:hover{text-decoration:underline}
.finding{border-left:4px solid #ccc;padding:10px 14px;margin:10px 0;
background:#fafbfc;border-radius:0 8px 8px 0}
.finding h3{margin:0 0 4px;font-size:15px}
.finding p{margin:4px 0 0;font-size:13.5px;color:#444}
.rule{display:inline-block;font-size:11px;font-weight:700;background:#eef0f2;
border-radius:4px;padding:2px 7px;margin-right:8px;color:#555}
.sev{display:inline-block;font-size:11px;font-weight:700;color:#fff;
border-radius:4px;padding:2px 7px;margin-right:6px;text-transform:uppercase}
.diagram{border:1px solid #e3e6ea;border-radius:8px;background:#fff;
padding:12px;overflow:auto;margin-top:12px}
.diagram svg{max-width:100%;height:auto}
.gt{border:1px solid #e3e6ea;border-radius:8px;background:#fff;
padding:12px;overflow:auto;margin:6px 0 8px}
.gt img{max-width:100%;height:auto;display:block}
.metrics{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:#555;margin:8px 0}
.metrics b{color:#1a1a1a}
.nav{font-size:13px;margin-bottom:14px;color:#666}
.footer{color:#999;font-size:12px;margin-top:24px;text-align:center}
"""


def _sev_badge(sev: str) -> str:
    return f'<span class="sev" style="background:{SEV_COLORS[sev]}">{sev}</span>'


def _finding_html(f) -> str:
    return (
        f'<div class="finding" style="border-color:{SEV_COLORS[f.severity]}">'
        f"{_sev_badge(f.severity)}"
        f'<span class="rule">{html.escape(f.rule_id)}</span>'
        f"<h3 style=\"display:inline\">{html.escape(f.title)}</h3>"
        f"<p>{html.escape(f.detail)}</p></div>"
    )


def _render_diagram(vi_path: str) -> str:
    try:
        svg = render_vi_file(Path(vi_path))
    except Exception as e:  # noqa: BLE001 -- a bad render must not kill the report
        return f"<p><em>Diagram render unavailable: {html.escape(str(e))}</em></p>"
    if not svg:
        return "<p><em>No block diagram.</em></p>"
    return f'<div class="diagram">{svg}</div>'


def _ground_truth_html(gt: dict) -> str:
    """Card with genuine LabVIEW-exported panel/diagram images.

    gt maps 'fp'/'bd' to hrefs relative to the per-VI page.
    """
    parts = [
        '<div class="card"><h2>Ground truth &mdash; exported from LabVIEW</h2>',
        '<p class="sub">Genuine front panel and block diagram rendered by '
        "LabVIEW via PrintVIToHTML. Use these to validate the findings "
        "above and the parser render below.</p>",
    ]
    if gt.get("fp"):
        parts.append(
            '<h3 style="font-size:15px;margin:12px 0 6px">Front panel</h3>'
            f'<div class="gt"><img src="{html.escape(gt["fp"])}" '
            'alt="Front panel (LabVIEW export)"></div>'
        )
    if gt.get("bd"):
        parts.append(
            '<h3 style="font-size:15px;margin:12px 0 6px">Block diagram</h3>'
            f'<div class="gt"><img src="{html.escape(gt["bd"])}" '
            'alt="Block diagram (LabVIEW export)"></div>'
        )
    parts.append("</div>")
    return "".join(parts)


def _load_ground_truth(gt_dir: str | Path) -> dict:
    """Read an export_vi_images.py manifest.

    Returns {posix_rel_path: {'fp': Path|None, 'bd': Path|None}} with
    absolute source paths. Missing manifest -> {}.
    """
    gt_dir = Path(gt_dir)
    manifest = gt_dir / "manifest.csv"
    result: dict = {}
    if not manifest.is_file():
        return result
    with manifest.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = row["vi_path"].replace("\\", "/")
            entry = result.setdefault(key, {"fp": None, "bd": None})
            if row.get("fp_png"):
                entry["fp"] = gt_dir / row["fp_png"].replace("\\", "/")
            if row.get("bd_png"):
                entry["bd"] = gt_dir / row["bd_png"].replace("\\", "/")
    return result


def _match_ground_truth(review: VIReview, gt_map: dict) -> dict | None:
    """Find the manifest entry whose relative path is a tail of the VI path."""
    rp = PurePath(review.vi_path).as_posix()
    for key, entry in gt_map.items():
        if rp == key or rp.endswith("/" + key):
            return entry
    return None


def _vi_page(review: VIReview, back_link: str = "index.html",
             with_diagram: bool = True,
             ground_truth: dict | None = None) -> str:
    counts = {s: len(review.by_severity(s)) for s in SEVERITY_ORDER}
    metrics = review.metrics
    m_html = "".join(
        f"<span><b>{v}</b> {k.replace('_', ' ')}</span>"
        for k, v in metrics.items()
    )
    if not review.parse_ok:
        body = f'<div class="card"><h2>Parse failed</h2><p>{html.escape(review.parse_error or "")}</p></div>'
    else:
        findings = "".join(_finding_html(f) for f in review.findings) or \
            "<p>No findings. Clean review.</p>"
        diagram = _render_diagram(review.vi_path) if with_diagram else \
            "<p><em>Diagram omitted in this build.</em></p>"
        gt_html = _ground_truth_html(ground_truth) if ground_truth else ""
        body = (
            f'<div class="card"><h2>Metrics</h2><div class="metrics">{m_html}</div></div>'
            f'<div class="card"><h2>Findings ({len(review.findings)})</h2>{findings}</div>'
            f"{gt_html}"
            f'<div class="card"><h2>Block diagram (parser render)</h2>{diagram}</div>'
        )
    badges = "".join(
        f'<span class="badge" style="background:{SEV_COLORS[s]}">{counts[s]}<small>{s}</small></span>'
        for s in SEVERITY_ORDER if counts[s]
    )
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>{html.escape(review.vi_name)} - VI Review</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="nav"><a href="{back_link}">&larr; Back to project report</a></div>
<h1>{html.escape(review.vi_name)}</h1>
<div class="sub">{html.escape(review.vi_path)}</div>
<div class="badges">{badges or '<span class="sub">No findings</span>'}</div>
{body}
<div class="footer">Generated by vi-inspector MVP (lvkit engine, Apache-2.0)</div>
</div></body></html>"""


def generate_report(reviews: list[VIReview], project_name: str, out_dir: str | Path,
                    max_diagrams: int | None = None,
                    ground_truth_dir: str | Path | None = None) -> Path:
    """Write dashboard + per-VI pages. Returns the index.html path.

    max_diagrams caps how many per-VI pages embed a rendered diagram
    (rendering is the slow step); all VIs still get findings pages.

    ground_truth_dir points at an export_vi_images.py output folder; its
    manifest.csv maps VIs to genuine LabVIEW-rendered PNGs, which are
    copied into the report and embedded on each VI page.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ok = [r for r in reviews if r.parse_ok]
    totals = {s: sum(len(r.by_severity(s)) for r in ok) for s in SEVERITY_ORDER}

    gt_map = _load_ground_truth(ground_truth_dir) if ground_truth_dir else {}
    gt_root = Path(ground_truth_dir) if ground_truth_dir else None

    def _gt_for(review: VIReview) -> dict | None:
        entry = _match_ground_truth(review, gt_map)
        if not entry or gt_root is None:
            return None
        gt: dict = {}
        for role in ("fp", "bd"):
            src = entry.get(role)
            if src and Path(src).is_file():
                rel = Path(src).relative_to(gt_root).as_posix()
                dst = out / "ground_truth" / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                gt[role] = f"ground_truth/{rel}"
        return gt or None

    # Per-VI pages (render diagrams only for the first max_diagrams VIs;
    # rendering is the slow step, findings are always complete)
    page_names: dict[str, str] = {}
    for i, r in enumerate(reviews):
        fname = f"vi_{i:03d}.html"
        page_names[r.vi_path] = fname
        with_diagram = max_diagrams is None or i < max_diagrams
        html_text = _vi_page(r, with_diagram=with_diagram,
                             ground_truth=_gt_for(r))
        (out / fname).write_text(html_text, encoding="utf-8")

    # Dashboard rows sorted by high-severity count desc
    def sort_key(r: VIReview):
        return (-len(r.by_severity("high")), -len(r.by_severity("medium")), r.vi_name)
    rows = []
    for r in sorted(ok, key=sort_key):
        m = r.metrics
        cells = "".join(
            f"<td>{len(r.by_severity(s))}</td>" for s in ("high", "medium", "low")
        )
        rows.append(
            f'<tr><td><a href="{page_names[r.vi_path]}">{html.escape(r.vi_name)}</a></td>'
            f"<td>{m.get('nodes', '?')}</td><td>{m.get('wires', '?')}</td>"
            f"<td>{m.get('structures', '?')}</td><td>{m.get('subvi_calls', '?')}</td>"
            f"{cells}</tr>"
        )
    # Rule summary
    from collections import Counter
    rule_counts = Counter(f.rule_id for r in ok for f in r.findings)
    rule_rows = "".join(
        f"<tr><td>{html.escape(rid)}</td><td>{c}</td></tr>"
        for rid, c in rule_counts.most_common()
    )
    badges = "".join(
        f'<span class="badge" style="background:{SEV_COLORS[s]}">{totals[s]}<small>{s}</small></span>'
        for s in SEVERITY_ORDER
    )
    index = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>{html.escape(project_name)} - VI Code Review</title><style>{CSS}</style></head>
<body><div class="wrap">
<h1>{html.escape(project_name)}</h1>
<div class="sub">Automated LabVIEW code review &mdash; {len(ok)}/{len(reviews)} VIs parsed, no LabVIEW required</div>
<div class="badges">{badges}</div>
<div class="card"><h2>Findings by rule</h2>
<table><tr><th>Rule</th><th>Count</th></tr>{rule_rows}</table></div>
<div class="card"><h2>VIs</h2>
<table><tr><th>VI</th><th>Nodes</th><th>Wires</th><th>Structures</th>
<th>SubVI calls</th><th>High</th><th>Med</th><th>Low</th></tr>
{"".join(rows)}</table></div>
<div class="footer">Generated by vi-inspector MVP (lvkit engine, Apache-2.0).
Rules: ERR-1 unwired error terminals on SubVI calls, ERR-1b broken error chains,
ERR-2 missing error handling, RACE-1 local variables, CPLX-1 large diagrams.</div>
</div></body></html>"""
    index_path = out / "index.html"
    index_path.write_text(index, encoding="utf-8")
    return index_path
