"""HTML report generation for VI code reviews.

Project-Explorer-style dashboard: a folder-tree sidebar on every page,
per-VI pages with findings, block-diagram / front-panel tabs (Ctrl+E
toggles, like LabVIEW), double-click-to-open in LabVIEW, and Calls /
Called-by navigation.

Dependency-free output: inline CSS/JS, diagrams as inline SVG via lvkit.
"""
from __future__ import annotations

import csv
import html
import os
import re
import shutil
from pathlib import Path, PurePath

from .review import SEVERITY_ORDER, VIReview, build_call_graph

SEV_COLORS = {
    "high": "#c0392b",
    "medium": "#d68910",
    "low": "#2e86c1",
    "info": "#7f8c8d",
}

CSS = """
:root{
--bg:#f7f8fa;--card:#ffffff;--ink:#1a1a1a;--muted:#666;--faint:#8b95a1;
--line:#e3e6ea;--line-soft:#eef0f2;--soft:#fafbfc;--chip:#eef0f2;--chip-ink:#555;
--tab-bg:#f4f6f8;--tab-ink:#555;--tab-bd:#d5dae0;--tab-active:#232a33;
--btn-bg:#ffffff;--btn-bd:#d5dae0;--btn-ink:#2e86c1;--btn-hover:#f0f4f8;
--link:#2e86c1;--flash:#f59e0b;
}
html[data-theme="dark"]{
--bg:#0c1322;--card:#121c31;--ink:#e6ebf4;--muted:#9aa6bd;--faint:#7c8aa3;
--line:#24334f;--line-soft:#1b2942;--soft:#0f1830;--chip:#1c2946;--chip-ink:#b9c4d8;
--tab-bg:#1c2946;--tab-ink:#c4cede;--tab-bd:#2c3d5e;--tab-active:#3b5a7d;
--btn-bg:#16223a;--btn-bd:#2c3d5e;--btn-ink:#7fb6e8;--btn-hover:#1c2a47;
--link:#7fb6e8;--flash:#fbbf24;
}
body{font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
margin:0;color:var(--ink);background:var(--bg)}
.layout{display:flex;min-height:100vh}
.sidebar{width:300px;flex:0 0 300px;background:#232a33;color:#cfd6dd;
display:flex;flex-direction:column;position:sticky;top:0;height:100vh;
overflow:hidden}
.side-head{padding:14px 16px 10px;border-bottom:1px solid #39424d}
.side-head h2{font-size:14px;margin:0 0 2px;color:#fff;white-space:nowrap;
overflow:hidden;text-overflow:ellipsis}
.side-head .count{font-size:12px;color:#8b95a1}
.side-tools{padding:10px 12px;border-bottom:1px solid #39424d}
#tree-search{width:100%;box-sizing:border-box;padding:7px 10px;border-radius:6px;
border:1px solid #39424d;background:#2e3742;color:#e6ebf0;font-size:13px}
#tree-search::placeholder{color:#8b95a1}
.side-opt{display:flex;align-items:center;gap:7px;margin-top:8px;font-size:12.5px;
color:#aeb7c2;cursor:pointer;user-select:none}
.side-opt input{accent-color:#2e86c1}
.tree{flex:1;overflow-y:auto;padding:8px 6px 20px;font-size:13.5px}
.tree-folder .frow{display:flex;align-items:center;gap:6px;padding:4px 6px;
border-radius:5px;cursor:pointer;color:#cfd6dd;white-space:nowrap}
.tree-folder .frow:hover{background:#2e3742}
.tree-folder .frow .arrow{font-size:10px;color:#8b95a1;width:12px;flex:0 0 12px;
transition:transform .12s}
.tree-folder.closed > .frow .arrow{transform:rotate(-90deg)}
.tree-folder .fchildren{margin-left:14px;border-left:1px solid #39424d;
padding-left:4px}
.tree-folder.closed > .fchildren{display:none}
.ficon{flex:0 0 auto}
.fname{overflow:hidden;text-overflow:ellipsis}
.fcount{margin-left:auto;font-size:11px;background:#39424d;border-radius:8px;
padding:1px 7px;color:#aeb7c2;flex:0 0 auto}
.tree-vi{display:flex;align-items:center;gap:7px;padding:4px 6px 4px 22px;
border-radius:5px;color:#cfd6dd;text-decoration:none;white-space:nowrap}
.tree-vi:hover{background:#2e3742;text-decoration:none;color:#fff}
.tree-vi.active{background:#2e4a63;color:#fff}
.tree-vi .vname{overflow:hidden;text-overflow:ellipsis}
.tree-vi .vcnt{margin-left:auto;font-size:11px;color:#8b95a1;flex:0 0 auto}
.dot{width:9px;height:9px;border-radius:50%;flex:0 0 9px}
.dot.clean{background:#5a6572}
.proj-link{display:block;margin:0 12px 10px;padding:8px 10px;background:#2e4a63;
border-radius:6px;color:#fff;font-size:13px;text-align:center;text-decoration:none}
.proj-link:hover{background:#38607f;text-decoration:none;color:#fff}
.main{flex:1;min-width:0;padding:24px 28px;max-width:1200px}
.vi-head{display:flex;justify-content:space-between;align-items:flex-start;
gap:16px;margin-bottom:4px}
.vi-head h1{font-size:24px;margin:0 0 4px;word-break:break-word}
.actions{display:flex;gap:8px;flex:0 0 auto;padding-top:4px}
.btn{display:inline-block;padding:8px 14px;border-radius:7px;font-size:13.5px;
font-weight:600;border:1px solid var(--btn-bd);background:var(--btn-bg);color:var(--btn-ink);
cursor:pointer;text-decoration:none;white-space:nowrap}
.btn:hover{background:var(--btn-hover);text-decoration:none}
.btn.primary{background:#2e86c1;border-color:#2e86c1;color:#fff}
.btn.primary:hover{background:#2574a8}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:18px 22px;margin-bottom:18px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
h2{font-size:19px;margin:0 0 10px}
.sub{color:var(--muted);font-size:13.5px;margin-bottom:14px;word-break:break-all}
.badges{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.badge{border-radius:8px;padding:10px 16px;color:#fff;font-weight:600;font-size:15px}
.badge small{display:block;font-weight:400;font-size:12px;opacity:.9}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;padding:8px 10px;border-bottom:2px solid var(--line);color:var(--muted);
font-size:12px;text-transform:uppercase;letter-spacing:.04em}
td{padding:8px 10px;border-bottom:1px solid var(--line-soft);vertical-align:top}
tbody tr:hover td{background:var(--soft)}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
.finding{border-left:4px solid #ccc;padding:10px 14px;margin:10px 0;
background:var(--soft);border-radius:0 8px 8px 0}
.finding h3{margin:0 0 4px;font-size:15px}
.finding p{margin:4px 0 0;font-size:13.5px;color:var(--ink)}
.rule{display:inline-block;font-size:11px;font-weight:700;background:var(--chip);
border-radius:4px;padding:2px 7px;margin-right:8px;color:var(--chip-ink)}
.sev{display:inline-block;font-size:11px;font-weight:700;color:#fff;
border-radius:4px;padding:2px 7px;margin-right:6px;text-transform:uppercase}
.tabs{display:flex;align-items:center;gap:6px;margin-bottom:12px;flex-wrap:wrap}
.tab{padding:8px 16px;border:1px solid var(--tab-bd);background:var(--tab-bg);border-radius:7px;
font-size:13.5px;font-weight:600;color:var(--tab-ink);cursor:pointer}
.tab.active{background:var(--tab-active);border-color:var(--tab-active);color:#fff}
.tab:hover:not(.active){filter:brightness(.94)}
.tab-hint{margin-left:auto;font-size:12px;color:var(--faint)}
.tabpane{border:1px solid var(--line);border-radius:8px;background:var(--card);
padding:12px;overflow:auto;cursor:default}
.tabpane.dbl{cursor:pointer}
.tabpane svg{max-width:100%;height:auto}
.tabpane img{max-width:100%;height:auto;display:block}
.hidden{display:none}
.gt{border:1px solid var(--line);border-radius:8px;background:var(--card);
padding:12px;overflow:auto;margin:6px 0 8px}
.gt img{max-width:100%;height:auto;display:block}
.metrics{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin:8px 0}
.metrics b{color:var(--ink)}
.nav{font-size:13px;margin-bottom:14px;color:var(--muted)}
.call-list{list-style:none;margin:6px 0;padding:0;font-size:14px}
.call-list li{padding:5px 0;border-bottom:1px solid var(--line-soft)}
.call-list li:last-child{border-bottom:none}
.call-list .dot{display:inline-block;margin-right:8px;vertical-align:1px}
.call-cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.call-cols h3{font-size:14px;margin:0 0 4px;color:var(--muted)}
.footer{color:var(--faint);font-size:12px;margin-top:24px;text-align:center}
.filter-row{display:flex;align-items:center;gap:10px;margin-bottom:12px;
font-size:13.5px;color:var(--muted)}
.filter-row select{padding:6px 10px;border-radius:6px;border:1px solid var(--tab-bd);
font-size:13.5px;background:var(--card);color:var(--ink)}
body.hide-clean .tree-vi[data-clean="1"]{display:none !important}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
background:#232a33;color:#fff;padding:10px 18px;border-radius:8px;font-size:13.5px;
opacity:0;transition:opacity .25s;pointer-events:none;z-index:99}
.toast.show{opacity:1}

.finding.locatable{cursor:pointer}
.finding.locatable:hover{filter:brightness(.97)}
@keyframes viFlash{0%,100%{filter:none}50%{filter:drop-shadow(0 0 12px var(--flash))}}
.vi-flash{animation:viFlash .8s ease-in-out 3}
.cpane-wrap{display:flex;flex-direction:column;align-items:center;gap:10px;
padding:8px 4px}
.cpane-wrap>svg{width:min(620px,100%);height:auto}
.cpane-wrap svg text{font-family:-apple-system,'Segoe UI',Roboto,sans-serif}
.cpane-cap{font-size:12.5px;color:var(--muted);margin:0;text-align:center}
@media (max-width:900px){
.sidebar{width:230px;flex-basis:230px}
.call-cols{grid-template-columns:1fr}
.vi-head{flex-direction:column}
}
"""

JS = """
function toast(msg){
  var t=document.getElementById('toast');
  if(!t){t=document.createElement('div');t.id='toast';t.className='toast';
    document.body.appendChild(t);}
  t.textContent=msg;t.classList.add('show');
  setTimeout(function(){t.classList.remove('show');},1800);
}
function openLabVIEW(){
  var u=document.body.getAttribute('data-lvuri');
  if(u){window.location.href=u;}
  else{toast('No local file path recorded for this VI');}
}
function copyPath(){
  var p=document.body.getAttribute('data-lvpath')||'';
  function done(){toast('Path copied to clipboard');}
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(p).then(done,function(){toast('Copy failed');});
  }else{toast('Clipboard unavailable');}
}
/* --- tabs (Ctrl+E / Cmd+E toggles, like LabVIEW) --- */
function showTab(name){
  document.querySelectorAll('.tab').forEach(function(t){
    t.classList.toggle('active',t.getAttribute('data-tab')===name);});
  document.querySelectorAll('.tabpane').forEach(function(p){
    p.classList.toggle('hidden',p.id!=='pane-'+name);});
}
function cycleTab(){
  var tabs=Array.prototype.map.call(document.querySelectorAll('.tab'),
    function(t){return t.getAttribute('data-tab');});
  if(!tabs.length)return;
  var cur=tabs.indexOf(document.querySelector('.tab.active').getAttribute('data-tab'));
  showTab(tabs[(cur+1)%tabs.length]);
}
document.querySelectorAll('.tab').forEach(function(t){
  t.addEventListener('click',function(){showTab(t.getAttribute('data-tab'));});
});
document.addEventListener('keydown',function(e){
  if((e.ctrlKey||e.metaKey)&&e.key&&e.key.toLowerCase()==='e'){
    if(document.querySelector('.tab')){e.preventDefault();cycleTab();}
  }
});
/* --- project tree --- */
document.querySelectorAll('.tree-folder > .frow').forEach(function(row){
  row.addEventListener('click',function(){
    row.parentElement.classList.toggle('closed');});
});
var searchBox=document.getElementById('tree-search');
if(searchBox){
  searchBox.addEventListener('input',function(){
    var s=searchBox.value.toLowerCase();
    document.querySelectorAll('.tree-vi').forEach(function(v){
      v.style.display=v.getAttribute('data-name').indexOf(s)>=0?'':'none';});
    Array.prototype.slice.call(
      document.querySelectorAll('.tree-folder')).reverse().forEach(function(f){
      var any=Array.prototype.slice.call(
        f.querySelectorAll('.tree-vi')).some(function(v){
          return v.style.display!=='none';});
      f.style.display=any?'':'none';});
  });
}
var hideClean=document.getElementById('hide-clean');
if(hideClean){
  hideClean.addEventListener('change',function(){
    document.body.classList.toggle('hide-clean',hideClean.checked);});
}
/* --- index table severity filter --- */
var sevFilter=document.getElementById('sev-filter');
if(sevFilter){
  sevFilter.addEventListener('change',function(){
    var v=sevFilter.value;
    document.querySelectorAll('#vi-table tbody tr').forEach(function(tr){
      var sev=tr.getAttribute('data-sev');
      var show=v==='all'||sev===v||(v==='findings'&&sev!=='clean');
      tr.style.display=show?'':'none';});
  });
}
/* --- theme: light / dark. The diagram SVGs render with theme_mode="auto"
   and re-theme themselves off <html data-theme>; this only flips the page
   chrome to match. Choice persists in localStorage. --- */
function setTheme(mode){
  var root=document.documentElement;
  if(mode==='dark'||mode==='light'){root.setAttribute('data-theme',mode);}
  else{root.removeAttribute('data-theme');}
  try{localStorage.setItem('vi-theme',mode||'auto');}catch(e){}
}
(function(){
  var saved='auto';
  try{saved=localStorage.getItem('vi-theme')||'auto';}catch(e){}
  if(saved==='dark'||saved==='light'){setTheme(saved);}
  var btn=document.getElementById('theme-toggle');
  if(btn){btn.addEventListener('click',function(){
    var cur=document.documentElement.getAttribute('data-theme');
    setTheme(cur==='dark'?'light':'dark');
  });}
})();
/* --- click a finding to flash its node on the block diagram --- */
document.querySelectorAll('.finding[data-locate]').forEach(function(card){
  card.addEventListener('click',function(){
    if(document.querySelector('.tab')){showTab('bd');}
    var pane=document.getElementById('pane-bd');
    if(!pane){return;}
    var first=null;
    card.getAttribute('data-locate').split(/\s+/).forEach(function(id){
      if(!id){return;}
      var g=pane.querySelector('g[data-node="'+id+'"]');
      if(!g){return;}
      g.classList.remove('vi-flash');
      void g.getBoundingClientRect();
      g.classList.add('vi-flash');
      setTimeout(function(){g.classList.remove('vi-flash');},2600);
      if(!first){first=g;}
    });
    if(first&&first.scrollIntoView){
      first.scrollIntoView({block:'center',behavior:'smooth'});}
  });
});
"""


def _sev_badge(sev: str) -> str:
    return f'<span class="sev" style="background:{SEV_COLORS[sev]}">{sev}</span>'


def _worst_sev(review: VIReview) -> str | None:
    for sev in SEVERITY_ORDER:
        if review.by_severity(sev):
            return sev
    return None


def _file_uri(path: str) -> str | None:
    """file:// URI for 'Open in LabVIEW'. None when it cannot be built."""
    try:
        return Path(path).resolve().as_uri()
    except Exception:  # noqa: BLE001 -- weird paths: hide the button instead
        return None


def _render_views(vi_path: str) -> tuple[str | None, str | None, dict]:
    """Render block diagram and front panel SVGs from a single graph load.

    Returns (bd_svg, fp_svg, info); either SVG may be None on failure.
    ``info`` carries ``wire_tips`` ({svg path d: tooltip text}) recorded
    while the renderer drew its wire nets, for hover tooltips. A bad
    render must never kill the report.

    Diagrams render with ``theme_mode="auto"`` so they follow the page's
    ``<html data-theme>`` (toggled by the report's theme button) with no
    re-render.
    """
    try:
        from lvkit.graph.core import InMemoryVIGraph
        from lvkit.load_mode import LoadMode
        from lvkit.render import render_vi
        from lvkit.render import composite as _composite
        from lvkit.render.front_panel import render_vi_front_panel
    except Exception:  # noqa: BLE001 -- lvkit too old: no diagrams
        return None, None, {"wire_tips": {}}
    for mode in (LoadMode.MINIMAL, LoadMode.NONE):
        graph = None
        try:
            graph = InMemoryVIGraph()
            key = graph.load_vi(Path(vi_path), mode=mode, layout=True)
            name = key or graph.resolve_vi_name(Path(vi_path).name)
            _WIRE_CTX["graph"] = graph
            _WIRE_CTX["records"] = []
            global _WIRE_ORIG_DRAW
            _WIRE_ORIG_DRAW = _composite._draw_wire_nets
            _composite._draw_wire_nets = _recording_draw_wire_nets
            try:
                bd = render_vi(graph, name, theme_mode="auto")
                try:
                    fp = render_vi_front_panel(graph, name, theme_mode="auto")
                except Exception:  # noqa: BLE001 -- FP optional
                    fp = None
            finally:
                _composite._draw_wire_nets = _WIRE_ORIG_DRAW
                _WIRE_ORIG_DRAW = None
            info = {"wire_tips": dict(_WIRE_CTX["records"])}
            return bd, fp, info
        except Exception:  # noqa: BLE001 -- degrade to NONE, then give up
            continue
        finally:
            _WIRE_CTX["graph"] = None
            _WIRE_CTX["records"] = []
    return None, None, {"wire_tips": {}}


# ---------------------------------------------------------------------------
# Wire hover tooltips (data type per wire)
# ---------------------------------------------------------------------------
#
# The lvkit renderer draws wires as bare <path> elements with no metadata,
# so we record each wire net WHILE it is drawn: _recording_draw_wire_nets
# wraps lvkit.render.composite._draw_wire_nets during render_vi and logs
# every branch's exact SVG path data plus a data-type label resolved from
# the graph. _inject_wire_tips then staples a <title> into each matching
# path. The path-data format must byte-match SVGBackend.path.

_WIRE_CTX: dict = {"graph": None, "records": []}
_WIRE_ORIG_DRAW = None  # original composite._draw_wire_nets while recording


def _wire_type_label(graph, net) -> str | None:
    """Human data-type label for a rendered wire net, via the graph."""
    wire = getattr(net, "source", None)
    if wire is None or graph is None:
        return None
    try:
        term = graph.get_terminal(wire.source.terminal_id)
        label = term.type_label()
    except Exception:  # noqa: BLE001 -- tooltip is optional
        return None
    if not label:
        return None
    name = (getattr(term, "name", None) or "").strip()
    if name:
        return f"Wire '{name}': {label}"
    return f"Wire: {label}"


def _branch_d(branch) -> str:
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in branch)


def _recording_draw_wire_nets(nets, backend, theme):
    """Wrap lvkit's wire-net painter; record (path d, type label)."""
    for net in nets:
        label = _wire_type_label(_WIRE_CTX["graph"], net)
        if not label:
            continue
        for branch in net.branches:
            try:
                _WIRE_CTX["records"].append((_branch_d(branch), label))
            except Exception:  # noqa: BLE001 -- one bad branch: skip it
                continue
    return _WIRE_ORIG_DRAW(nets, backend, theme)


def _inject_wire_tips(bd_svg: str | None, wire_tips: dict) -> str | None:
    """Staple a <title> (data type) into each recorded wire <path>.

    Both the casing and the color stroke of a wire share the same path
    data, so both get the tooltip. Patterned class wires draw links
    instead of the branch path and simply get no tooltip.
    """
    if not bd_svg or not wire_tips:
        return bd_svg
    ordered = sorted(wire_tips, key=len, reverse=True)
    pat = re.compile(
        r'<path d="(' + "|".join(re.escape(d) for d in ordered) + r')"'
        r"([^>]*?)/>")

    def _one(m: re.Match) -> str:
        label = wire_tips[m.group(1)]
        return (f'<path d="{m.group(1)}"{m.group(2)}>'
                f"<title>{html.escape(label)}</title></path>")

    return pat.sub(_one, bd_svg)


def _inject_subvi_links(bd_svg: str | None, vi_path: str,
                        page_for: dict[str, str]) -> str | None:
    """Make SubVI nodes in the diagram clickable.

    The lvkit renderer tags every SubVI node group with
    ``data-lv-vi-rel`` -- the callee's .vi path relative to the rendered
    VI's directory. We resolve it and add:

    - ``data-callee-page``: this report's page for the callee (in-report
      navigation, single click)
    - ``data-callee-open``: file:// URI of the callee (double-click opens
      the .vi in LabVIEW, exactly like LabVIEW's own double-click)

    Callees that exist on disk but were not reviewed still get
    double-click-to-open (e.g. vi.lib VIs). JS in the page supplies the
    behavior; the SVG stays a static document otherwise.
    """
    if not bd_svg:
        return bd_svg
    vi_dir = Path(vi_path).parent
    pattern = re.compile(r'<g([^>]*?)data-lv-vi-rel="([^"]+)"([^>]*)>')

    def _one(m: re.Match) -> str:
        attrs, rel = m.group(1), m.group(2)
        if "lv-node" not in attrs:
            return m.group(0)
        if not rel.lower().endswith((".vi", ".vim", ".ctl")):
            return m.group(0)
        try:
            callee = (vi_dir / rel).resolve()
        except Exception:  # noqa: BLE001 -- odd path: leave the node alone
            return m.group(0)
        page = page_for.get(os.path.normcase(str(callee)))
        uri = _file_uri(str(callee)) if callee.exists() else None
        if not page and not uri:
            return m.group(0)
        extra = ""
        if page:
            extra += f' data-callee-page="{html.escape(page, quote=True)}"'
        if uri:
            extra += (f' data-callee-open="{html.escape(uri, quote=True)}"')
        return f"<g{attrs}data-lv-vi-rel=\"{html.escape(rel, quote=True)}\"" \
               f"{m.group(3)}{extra}>"

    return pattern.sub(_one, bd_svg)


def _extract_cpane(bd_svg: str | None) -> str | None:
    """Pull the VI's icon + connector-pane face out of the SVG defs.

    The renderer embeds it as ``<g class="lv-vi-aside">`` (icon raster,
    VI name, connector-pane grid whose cells already carry <title>
    tooltips with terminal name/type/direction). We lift the inner
    <svg> -- balanced-scan because the pane grid nests another <svg> --
    for a dedicated "Connector pane" tab.
    """
    if not bd_svg:
        return None
    start = bd_svg.find('<g class="lv-vi-aside"')
    if start < 0:
        return None
    svg_start = bd_svg.find("<svg", start)
    if svg_start < 0:
        return None
    # Balanced scan over nested <svg>...</svg> to find the matching close.
    depth = 0
    pos = svg_start
    end = -1
    while pos < len(bd_svg):
        lt = bd_svg.find("<", pos)
        if lt < 0:
            break
        if bd_svg.startswith("<svg", lt):
            gt = bd_svg.find(">", lt)
            if gt < 0:
                break
            if bd_svg[gt - 1] != "/":
                depth += 1
            pos = gt + 1
        elif bd_svg.startswith("</svg>", lt):
            depth -= 1
            pos = lt + len("</svg>")
            if depth == 0:
                end = pos
                break
        else:
            pos = lt + 1
    if end < 0:
        return None
    return bd_svg[svg_start:end]


def _node_name_index(bd_svg: str | None) -> dict:
    """Map lowercase node display names -> [data-node dom ids].

    Built from the rendered diagram's own <g class="lv-node" ...><title>
    groups, so finding -> diagram correlation needs no id-space mapping.
    """
    index: dict[str, list[str]] = {}
    if not bd_svg:
        return index
    for m in re.finditer(r"<g([^>]*?)>\s*<title>(.*?)</title>", bd_svg, re.S):
        attrs, title = m.group(1), m.group(2)
        if "lv-node" not in attrs:
            continue
        dm = re.search(r'data-node="([^"]+)"', attrs)
        if not dm:
            continue
        # Title format: "<qualified node name>\nInputs:\n ..."; the name is
        # the first line.
        first_line = title.strip().split("\n")[0].strip()
        name = " ".join(first_line.split()).lower()
        if name:
            index.setdefault(name, []).append(dm.group(1))
    return index


def _match_name(nm: str, index: dict) -> list:
    out: list[str] = []
    for cand, ids in index.items():
        if cand == nm or cand.endswith(":" + nm) or cand.endswith("/" + nm):
            out.extend(ids)
    return list(dict.fromkeys(out))


def _locate_ids(node_name: str | None, index: dict) -> list:
    """dom ids of diagram nodes a finding's node name refers to.

    A quoted qualifier (``Property Node 'AllObjs[]'``) names WHICH node of
    a generic kind -- but the diagram title only carries the generic kind,
    so we locate it only when exactly one node of that kind exists.
    Otherwise a flash across several nodes would mislead.
    """
    nm = (node_name or "").strip().lower()
    if not nm or not index:
        return []
    ids = _match_name(nm, index)
    if ids:
        return ids
    qualified = re.match(r"^(.*?) '[^']*'$", nm)
    if qualified:
        ids = _match_name(qualified.group(1), index)
        return ids if len(ids) == 1 else []
    return []


def _finding_html(f, locate_ids: list | None = None) -> str:
    ids = locate_ids or []
    if ids:
        extra = (f' data-locate="{" ".join(html.escape(i, quote=True) for i in ids)}"'
                 ' title="Click to locate this node on the block diagram"')
        cls = "finding locatable"
    else:
        extra, cls = "", "finding"
    return (
        f'<div class="{cls}" style="border-color:{SEV_COLORS[f.severity]}"{extra}>'
        f"{_sev_badge(f.severity)}"
        f'<span class="rule">{html.escape(f.rule_id)}</span>'
        f"<h3 style=\"display:inline\">{html.escape(f.title)}</h3>"
        f"<p>{html.escape(f.detail)}</p></div>"
    )


# ---------------------------------------------------------------------------
# Project tree sidebar
# ---------------------------------------------------------------------------

def _common_root(reviews: list[VIReview]) -> Path | None:
    try:
        common = Path(os.path.commonpath([r.vi_path for r in reviews]))
    except ValueError:  # e.g. paths on different drives
        return None
    return common if common.is_dir() else common.parent


def _build_tree(reviews: list[VIReview], page_names: dict[str, str],
                common_root: Path | None) -> dict:
    """Nested {dirs: {name: node}, vis: [entries]} folder tree."""
    root: dict = {"dirs": {}, "vis": []}
    for r in reviews:
        if common_root is not None:
            try:
                rel = Path(r.vi_path).relative_to(common_root)
            except ValueError:
                rel = Path(Path(r.vi_path).name)
        else:
            rel = Path(Path(r.vi_path).name)
        node = root
        for part in rel.parent.parts:
            if part in (".", ""):
                continue
            node = node["dirs"].setdefault(part, {"dirs": {}, "vis": []})
        node["vis"].append({
            "name": r.vi_name,
            "page": page_names[r.vi_path],
            "sev": _worst_sev(r),
            "n": len(r.findings),
        })
    return root


def _subtree_stats(node: dict) -> tuple[int, str | None]:
    """(total findings, worst severity) for a folder subtree."""
    total = sum(v["n"] for v in node["vis"])
    worst = next((v["sev"] for v in node["vis"] if v["sev"]), None)
    for sub in node["dirs"].values():
        st, sw = _subtree_stats(sub)
        total += st
        if sw and (worst is None or
                   SEVERITY_ORDER[sw] < SEVERITY_ORDER[worst]):
            worst = sw
    return total, worst


def _tree_html(node: dict, active_page: str | None = None,
               depth: int = 0) -> str:
    parts = []
    for dname in sorted(node["dirs"], key=str.lower):
        sub = node["dirs"][dname]
        total, worst = _subtree_stats(sub)
        n_vis = sum(1 for _ in _iter_vis(sub))
        dot = (f'<span class="dot" style="background:{SEV_COLORS[worst]}"></span>'
               if worst else '<span class="dot clean"></span>')
        kids = _tree_html(sub, active_page, depth + 1)
        parts.append(
            f'<div class="tree-folder{" closed" if depth > 0 else ""}">'
            f'<div class="frow" title="{html.escape(dname)}">'
            f'<span class="arrow">&#9662;</span>'
            f'<span class="ficon">&#128193;</span>{dot}'
            f'<span class="fname">{html.escape(dname)}</span>'
            f'<span class="fcount">{n_vis}</span></div>'
            f'<div class="fchildren">{kids}</div></div>')
    for v in sorted(node["vis"], key=lambda v: v["name"].lower()):
        dot = (f'<span class="dot" style="background:{SEV_COLORS[v["sev"]]}"></span>'
               if v["sev"] else '<span class="dot clean"></span>')
        cnt = f'<span class="vcnt">{v["n"]}</span>' if v["n"] else ""
        active = ' active' if v["page"] == active_page else ""
        parts.append(
            f'<a class="tree-vi{active}" href="{html.escape(v["page"], quote=True)}"'
            f' data-name="{html.escape(v["name"].lower(), quote=True)}"'
            f' data-clean="{"1" if not v["n"] else "0"}"'
            f' title="{html.escape(v["name"])}">{dot}'
            f'<span class="vname">{html.escape(v["name"])}</span>{cnt}</a>')
    return "".join(parts)


def _iter_vis(node: dict):
    yield from node["vis"]
    for sub in node["dirs"].values():
        yield from _iter_vis(sub)


def _sidebar_html(project_name: str, tree: dict,
                  active_page: str | None = None,
                  lvproj_uri: str | None = None) -> str:
    n_vis = sum(1 for _ in _iter_vis(tree))
    n_findings = sum(v["n"] for v in _iter_vis(tree))
    proj = ""
    if lvproj_uri:
        proj = (
            f'<a class="proj-link" href="{html.escape(lvproj_uri, quote=True)}"'
            ' title="Open the .lvproj in LabVIEW (works when viewing this'
            ' report from disk)">&#9656; Open project in LabVIEW</a>')
    return (
        '<aside class="sidebar">'
        f'<div class="side-head"><h2>{html.escape(project_name)}</h2>'
        f'<div class="count">{n_vis} VIs &middot; {n_findings} findings</div></div>'
        f"{proj}"
        '<div class="side-tools">'
        '<input id="tree-search" type="text" placeholder="Filter VIs&hellip;"'
        ' autocomplete="off">'
        '<label class="side-opt"><input type="checkbox" id="hide-clean">'
        " Hide VIs with no findings</label></div>"
        f'<div class="tree">{_tree_html(tree, active_page)}</div>'
        "</aside>")


# ---------------------------------------------------------------------------
# Ground truth (genuine LabVIEW exports)
# ---------------------------------------------------------------------------

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


def _gt_inner_html(gt: dict) -> str:
    """Inner HTML for the 'LabVIEW export' tab."""
    parts = [
        '<p class="sub">Genuine front panel and block diagram rendered by '
        "LabVIEW via PrintVIToHTML. Use these to validate the findings "
        "above and the parser render.</p>",
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
    return "".join(parts)


# ---------------------------------------------------------------------------
# Per-VI page
# ---------------------------------------------------------------------------

def _calls_html(review: VIReview, graph: dict, page_names: dict[str, str],
                sev_by_path: dict[str, str | None]) -> str:
    entry = graph.get(review.vi_path, {})
    calls = entry.get("calls", [])
    called_by = entry.get("called_by", [])
    external = entry.get("external", 0)

    def _li(p: str) -> str:
        sev = sev_by_path.get(p)
        dot = (f'<span class="dot" style="background:{SEV_COLORS[sev]}"></span>'
               if sev else '<span class="dot clean"></span>')
        return (f"<li>{dot}"
                f'<a href="{html.escape(page_names[p], quote=True)}">'
                f"{html.escape(Path(p).name)}</a></li>")

    calls_list = "".join(_li(p) for p in calls) or \
        "<li><em>No SubVI calls into reviewed VIs.</em></li>"
    if external:
        calls_list += (f"<li><em>+ {external} call(s) to VIs outside this "
                       "review (vi.lib, unreviewed files).</em></li>")
    by_list = "".join(_li(p) for p in called_by) or \
        "<li><em>Not called by any reviewed VI (top-level or unused).</em></li>"
    return (
        '<div class="call-cols"><div><h3>Calls</h3>'
        f'<ul class="call-list">{calls_list}</ul></div>'
        "<div><h3>Called by</h3>"
        f'<ul class="call-list">{by_list}</ul></div></div>')


def _diagram_pane(svg: str | None, pane_id: str, label: str,
                  lv_hint: bool = True) -> str:
    if svg:
        dbl = (' class="tabpane dbl" ondblclick="openLabVIEW()"'
               f' title="Double-click to open this VI in LabVIEW"'
               if lv_hint else ' class="tabpane"')
        return f'<div id="{pane_id}"{dbl}>{svg}</div>'
    return (f'<div id="{pane_id}" class="tabpane">'
            f"<p><em>{html.escape(label)} unavailable.</em></p></div>")


NODE_CLICK_JS = """
/* SubVI nodes: click -> callee page, double-click -> open .vi in LabVIEW */
document.querySelectorAll('.lv-node[data-callee-page],.lv-node[data-callee-open]')
.forEach(function(n){
  n.style.cursor='pointer';
  var t=n.querySelector('title');
  if(t){t.textContent=t.textContent+
    '\\n\\nClick: open in this report. Double-click: open in LabVIEW.';}
  if(n.hasAttribute('data-callee-page')){
    n.addEventListener('click',function(){
      window.location.href=n.getAttribute('data-callee-page');});
  }
  n.addEventListener('dblclick',function(e){
    e.stopPropagation();
    var u=n.getAttribute('data-callee-open');
    if(u){window.location.href=u;}
    else if(n.hasAttribute('data-callee-page')){
      window.location.href=n.getAttribute('data-callee-page');}
  });
});
"""


def _vi_page(review: VIReview, sidebar: str, page_names: dict[str, str],
             sev_by_path: dict[str, str | None], graph: dict,
             bd_svg: str | None, fp_svg: str | None,
             cpane_svg: str | None, node_index: dict,
             ground_truth: dict | None) -> str:
    counts = {s: len(review.by_severity(s)) for s in SEVERITY_ORDER}
    badges = "".join(
        f'<span class="badge" style="background:{SEV_COLORS[s]}">{counts[s]}'
        f"<small>{s}</small></span>"
        for s in SEVERITY_ORDER if counts[s]
    ) or '<span class="sub">No findings &mdash; clean review</span>'

    lv_uri = _file_uri(review.vi_path)
    open_btn = ""
    if lv_uri:
        open_btn = (
            f'<a class="btn primary" href="{html.escape(lv_uri, quote=True)}"'
            ' title="Open this VI in LabVIEW (works when viewing the report'
            ' from disk)">Open in LabVIEW</a>')
    theme_btn = (
        '<button class="btn" id="theme-toggle" '
        'title="Toggle light/dark diagrams and page">◐ Theme</button>')

    if not review.parse_ok:
        findings_card = (
            '<div class="card"><h2>Parse failed</h2>'
            f"<p>{html.escape(review.parse_error or '')}</p></div>")
        diagrams_card = ""
    else:
        findings = "".join(
            _finding_html(f, _locate_ids(f.node_name, node_index))
            for f in review.findings) or "<p>No findings. Clean review.</p>"
        findings_card = (
            f'<div class="card"><h2>Findings ({len(review.findings)})</h2>'
            f"{findings}</div>")

        tabs = [
            '<button class="tab active" data-tab="bd">Block diagram</button>',
            '<button class="tab" data-tab="fp">Front panel</button>',
        ]
        panes = [
            _diagram_pane(bd_svg, "pane-bd", "Block diagram render"),
            _diagram_pane(fp_svg, "pane-fp", "Front panel render"),
        ]
        if cpane_svg:
            tabs.append(
                '<button class="tab" data-tab="cp">Connector pane</button>')
            panes.append(
                f'<div id="pane-cp" class="tabpane hidden">'
                f'<div class="cpane-wrap">{cpane_svg}'
                '<p class="cpane-cap">VI icon and connector pane as defined '
                "in the VI &mdash; hover a terminal for its details.</p>"
                "</div></div>")
        if ground_truth:
            tabs.append(
                '<button class="tab" data-tab="gt">LabVIEW export</button>')
            panes.append(
                f'<div id="pane-gt" class="tabpane hidden">'
                f"{_gt_inner_html(ground_truth)}</div>")
        diagrams_card = (
            '<div class="card"><h2>Diagram</h2>'
            '<div class="tabs">' + "".join(tabs) +
            '<span class="tab-hint">Ctrl+E toggles &middot; hover a wire for '
            "its data type &middot; double-click a SubVI to open it &middot; "
            "double-click empty space opens this VI</span></div>"
            + "".join(panes) + "</div>")

    metrics = "".join(
        f"<span><b>{v}</b> {html.escape(k.replace('_', ' '))}</span>"
        for k, v in review.metrics.items()
    )
    body = (
        f'<div class="vi-head"><div><h1>{html.escape(review.vi_name)}</h1>'
        f'<div class="sub">{html.escape(review.vi_path)}</div>'
        f'<div class="badges">{badges}</div></div>'
        f'<div class="actions">{open_btn}'
        '<button class="btn" onclick="copyPath()" '
        'title="Copy the VI file path to the clipboard">Copy path</button>'
        f"{theme_btn}"
        "</div></div>"
        f"{findings_card}"
        f"{diagrams_card}"
        '<div class="card"><h2>Hierarchy</h2>'
        f"{_calls_html(review, graph, page_names, sev_by_path)}</div>"
        '<div class="card"><h2>Metrics</h2>'
        f'<div class="metrics">{metrics}</div></div>'
    )
    body_attrs = ""
    if lv_uri:
        body_attrs = (
            f' data-lvuri="{html.escape(lv_uri, quote=True)}"'
            f' data-lvpath="{html.escape(str(Path(review.vi_path).resolve()), quote=True)}"')
    return (
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(review.vi_name)} - VI Review</title>"
        f"<style>{CSS}</style></head>"
        f"<body{body_attrs}>"
        '<div class="layout">'
        f"{sidebar}"
        '<main class="main">'
        f'<div class="nav"><a href="index.html">&larr; Project report</a></div>'
        f"{body}"
        '<div class="footer">Generated by vi-inspector (lvkit engine, '
        "Apache-2.0)</div>"
        "</main></div>"
        f"<script>{JS}</script><script>{NODE_CLICK_JS}</script>"
        "</body></html>")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def _index_page(project_name: str, reviews: list[VIReview], sidebar: str,
                page_names: dict[str, str],
                totals: dict[str, int]) -> str:
    from collections import Counter
    ok = [r for r in reviews if r.parse_ok]

    def sort_key(r: VIReview):
        return (-len(r.by_severity("high")), -len(r.by_severity("medium")),
                r.vi_name)

    rows = []
    for r in sorted(ok, key=sort_key):
        m = r.metrics
        worst = _worst_sev(r) or "clean"
        cells = "".join(
            f"<td>{len(r.by_severity(s))}</td>" for s in ("high", "medium", "low")
        )
        rows.append(
            f'<tr data-sev="{worst}">'
            f'<td><a href="{html.escape(page_names[r.vi_path], quote=True)}">'
            f"{html.escape(r.vi_name)}</a></td>"
            f"<td>{m.get('nodes', '?')}</td><td>{m.get('wires', '?')}</td>"
            f"<td>{m.get('structures', '?')}</td>"
            f"<td>{m.get('subvi_calls', '?')}</td>{cells}</tr>"
        )
    failed = [r for r in reviews if not r.parse_ok]
    for r in failed:
        rows.append(
            f'<tr data-sev="clean"><td>{html.escape(r.vi_name)}</td>'
            f'<td colspan="7"><em>Parse failed: '
            f"{html.escape(r.parse_error or '')}</em></td></tr>"
        )

    rule_counts = Counter(f.rule_id for r in ok for f in r.findings)
    rule_rows = "".join(
        f"<tr><td>{html.escape(rid)}</td><td>{c}</td></tr>"
        for rid, c in rule_counts.most_common()
    )
    badges = "".join(
        f'<span class="badge" style="background:{SEV_COLORS[s]}">{totals[s]}'
        f"<small>{s}</small></span>"
        for s in SEVERITY_ORDER
    )
    return (
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(project_name)} - VI Code Review</title>"
        f"<style>{CSS}</style></head><body>"
        '<div class="layout">'
        f"{sidebar}"
        '<main class="main">'
        f"<h1>{html.escape(project_name)}</h1>"
        f'<div class="sub">Automated LabVIEW code review &mdash; '
        f"{len(ok)}/{len(reviews)} VIs parsed, no LabVIEW required</div>"
        f'<div class="badges">{badges}'
        '<button class="btn" id="theme-toggle" style="margin-left:auto"'
        ' title="Toggle light/dark page theme">◐ Theme</button></div>'
        '<div class="card"><h2>Findings by rule</h2>'
        "<table><tr><th>Rule</th><th>Count</th></tr>"
        f"{rule_rows}</table></div>"
        '<div class="card"><h2>VIs</h2>'
        '<div class="filter-row"><label for="sev-filter">Show:</label>'
        '<select id="sev-filter">'
        '<option value="all">All VIs</option>'
        '<option value="high">High severity</option>'
        '<option value="medium">Medium severity</option>'
        '<option value="findings">Any findings</option>'
        '<option value="clean">Clean only</option>'
        "</select></div>"
        '<table id="vi-table"><tr><th>VI</th><th>Nodes</th><th>Wires</th>'
        "<th>Structures</th><th>SubVI calls</th>"
        "<th>High</th><th>Med</th><th>Low</th></tr>"
        f"{''.join(rows)}</table></div>"
        '<div class="footer">Generated by vi-inspector (lvkit engine, '
        "Apache-2.0). Rules: ERR-1 unwired error terminals on SubVI calls, "
        "ERR-1b broken error chains, ERR-2 missing error handling, WIRE-1 "
        "unwired required SubVI inputs, RACE-1 local variables, CPLX-1 large "
        "diagrams.</div>"
        "</main></div>"
        f"<script>{JS}</script>"
        "</body></html>")


def generate_report(reviews: list[VIReview], project_name: str,
                    out_dir: str | Path,
                    max_diagrams: int | None = None,
                    ground_truth_dir: str | Path | None = None) -> Path:
    """Write the Project-Explorer-style report. Returns the index.html path.

    max_diagrams caps how many per-VI pages embed rendered diagrams
    (rendering is the slow step); all VIs still get findings pages.

    ground_truth_dir points at an export_vi_images.py output folder; its
    manifest.csv maps VIs to genuine LabVIEW-rendered PNGs, shown on a
    "LabVIEW export" tab per VI.
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

    page_names = {r.vi_path: f"vi_{i:03d}.html" for i, r in enumerate(reviews)}
    graph = build_call_graph(reviews)
    sev_by_path = {r.vi_path: _worst_sev(r) for r in reviews}
    common = _common_root(reviews)
    tree = _build_tree(reviews, page_names, common)
    # normcase absolute-path -> page, for SubVI click-link injection
    page_for = {os.path.normcase(str(Path(p).resolve())): pg
                for p, pg in page_names.items()}

    lvproj_uri = None
    if common is not None:
        lvprojs = sorted(common.glob("*.lvproj"))
        if lvprojs:
            lvproj_uri = _file_uri(str(lvprojs[0]))

    sidebar_index = _sidebar_html(project_name, tree,
                                  lvproj_uri=lvproj_uri)

    for i, r in enumerate(reviews):
        with_views = max_diagrams is None or i < max_diagrams
        bd_svg, fp_svg, cpane_svg, node_index = None, None, None, {}
        if with_views and r.parse_ok:
            bd_svg, fp_svg, info = _render_views(r.vi_path)
            bd_svg = _inject_subvi_links(bd_svg, r.vi_path, page_for)
            bd_svg = _inject_wire_tips(bd_svg, info.get("wire_tips", {}))
            cpane_svg = _extract_cpane(bd_svg)
            node_index = _node_name_index(bd_svg)
        sidebar = _sidebar_html(project_name, tree,
                                active_page=page_names[r.vi_path],
                                lvproj_uri=lvproj_uri)
        html_text = _vi_page(r, sidebar, page_names, sev_by_path, graph,
                             bd_svg, fp_svg, cpane_svg, node_index,
                             _gt_for(r))
        (out / page_names[r.vi_path]).write_text(html_text, encoding="utf-8")

    index_html = _index_page(project_name, reviews, sidebar_index,
                             page_names, totals)
    index_path = out / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    return index_path
