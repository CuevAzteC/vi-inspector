"""Report feature tests: wire tooltips, connector-pane tab, finding locate,
dark mode. Slow (renders real fixture VIs) -- kept to a few VIs."""

import re

import pytest

from vi_inspector.report import (
    _extract_cpane,
    _inject_wire_tips,
    _locate_ids,
    _node_name_index,
    _render_views,
)

VI = "fixtures/vessel/Launcher/Core.vi"


@pytest.fixture(scope="module")
def views():
    bd, fp, info = _render_views(VI)
    assert bd, "BD render failed"
    return bd, fp, info


def test_wire_tips_recorded_and_injected(views):
    bd, _fp, info = views
    tips = info["wire_tips"]
    assert len(tips) >= 1, "no wire nets recorded during render"
    labels = set(tips.values())
    assert any(l.startswith("Wire") for l in labels)
    out = _inject_wire_tips(bd, tips)
    injected = re.findall(r"<title>(Wire[^<]*)</title>", out)
    assert injected, "no wire <title> injected"
    # every recorded branch d got its tooltip (casing + color strokes)
    assert len(injected) >= len(tips)


def test_wire_tip_label_mentions_type(views):
    _bd, _fp, info = views
    labels = " | ".join(info["wire_tips"].values())
    # Core.vi wires: error cluster, class refnum, boolean
    assert "Error" in labels
    assert "launcher.lvclass" in labels


def test_inject_wire_tips_noop():
    assert _inject_wire_tips(None, {"d": "x"}) is None
    assert _inject_wire_tips("<svg/>", {}) == "<svg/>"


def test_cpane_extracted(views):
    bd, _fp, _info = views
    cp = _extract_cpane(bd)
    assert cp, "no connector-pane aside extracted"
    assert "<svg" in cp
    assert "lv-pane-cell" in cp, "pane grid cells missing"
    assert _extract_cpane(None) is None


def test_node_index_and_locate(views):
    bd, _fp, _info = views
    idx = _node_name_index(bd)
    assert idx.get("interface.vi"), f"index keys: {sorted(idx)}"
    # exact + qualified-suffix matching
    assert _locate_ids("Interface.vi", idx) == idx["interface.vi"]
    assert _locate_ids("Core.vi", idx) == idx["launcher.lvclass:core.vi"]
    # unknown name -> no ids, never raises
    assert _locate_ids("No Such Node.vi", idx) == []
    assert _locate_ids(None, idx) == []


def test_locate_ambiguous_qualified_name():
    # "Property Node 'X'" only locates when exactly one property node exists
    idx = {"property node": ["7", "9"]}
    assert _locate_ids("Property Node 'AllObjs[]'", idx) == []
    assert _locate_ids("Property Node 'AllObjs[]'", {"property node": ["7"]}) == ["7"]


def test_auto_theme_css_embedded(views):
    bd, fp, _info = views
    for svg in (bd, fp):
        assert 'prefers-color-scheme' in svg, "auto theme CSS missing"
        assert 'data-theme="dark"' in svg


def test_js_syntax():
    import subprocess
    import tempfile
    src = open("vi_inspector/report.py").read()
    m = re.search(r'\nJS = """\n(.*?)\n"""\n', src, re.S)
    assert m, "JS block not found"
    with tempfile.NamedTemporaryFile("w", suffix=".js",
                                     delete=False) as fh:
        fh.write(m.group(1))
        path = fh.name
    p = subprocess.run(["node", "--check", path], capture_output=True)
    assert p.returncode == 0, p.stderr.decode()[:500]
