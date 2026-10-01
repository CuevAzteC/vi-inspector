"""Viewer mode tests: parse-only describe, findings-free pages, CLI."""

import re

import pytest

from vi_inspector.cli import _collect_vi_paths, cmd_view
from vi_inspector.report import generate_viewer
from vi_inspector.review import describe_many, describe_vi, review_vi

VI = "fixtures/vessel/Launcher/Core.vi"
VIS = [
    "fixtures/vessel/Launcher/Core.vi",
    "fixtures/vessel/Launcher/Interface.vi",
    "fixtures/vessel/iC7-INU/Simulation.vi",
]


def _body(path):
    s = open(path).read()
    return re.sub(r"<script.*?</script>", "", s, flags=re.S)


def test_describe_runs_no_rules():
    reviewed = review_vi(VI)
    assert reviewed.findings, "fixture VI should have findings under review"
    described = describe_vi(VI)
    assert described.parse_ok
    assert described.findings == []
    assert described.metrics.get("nodes", 0) > 0
    assert described.metrics.get("wires", 0) > 0


def test_describe_parse_failure_is_soft():
    d = describe_vi("/nonexistent/Missing.vi")
    assert not d.parse_ok
    assert d.parse_error
    assert d.findings == []


def test_describe_many_resolves_calls():
    ds = describe_many(VIS)
    assert len(ds) == 3
    assert all(d.parse_ok for d in ds)
    # calls drive SubVI click-through navigation
    assert any(d.calls for d in ds)


def test_collect_vi_paths():
    paths = _collect_vi_paths(["fixtures/vessel/Launcher"])
    assert len(paths) > 1
    assert all(p.endswith(".vi") for p in paths)
    assert _collect_vi_paths([VI]) == [VI]


@pytest.fixture(scope="module")
def viewer_dir(tmp_path_factory):
    out = tmp_path_factory.mktemp("viewer")
    idx = generate_viewer(VIS, "Test Project", out)
    assert idx.name == "index.html"
    return out


def test_viewer_index_is_browser_not_dashboard(viewer_dir):
    b = _body(viewer_dir / "index.html")
    assert "VI Viewer" in b
    assert "Findings by rule" not in b
    assert "VI Code Review" not in b
    assert 'id="sev-filter"' not in b
    assert 'id="hide-clean"' not in b
    assert "25 VIs" not in b  # 3 VIs here
    assert "3 VIs" in b
    for vi in ("Core.vi", "Interface.vi", "Simulation.vi"):
        assert vi in b


def test_viewer_vi_pages_have_diagrams_no_findings(viewer_dir):
    import glob
    pages = sorted(glob.glob(str(viewer_dir / "vi_*.html")))
    assert len(pages) == 3
    for p in pages:
        b = _body(p)
        assert "Findings (" not in b
        assert "VI Review" not in b
        assert "VI Viewer" in b
        tabs = set(re.findall(r'data-tab="([^"]+)"', b))
        panes = set(re.findall(r'id="pane-([^"]+)"', b))
        assert tabs == panes and "bd" in tabs and "fp" in tabs
        assert "&larr; Project browser" in b
        assert 'id="hide-clean"' not in b
        assert "Hide VIs with no findings" not in b
        assert "theme-toggle" in b


def test_viewer_vi_page_has_wire_tips_and_cpane(viewer_dir):
    import glob
    pages = sorted(glob.glob(str(viewer_dir / "vi_*.html")))
    bodies = [_body(p) for p in pages]
    assert any("<title>Wire" in b for b in bodies)
    assert any('data-tab="cp"' in b for b in bodies)


def test_cmd_view_writes_site(tmp_path):
    class Args:
        paths = ["fixtures/vessel/Launcher"]
        out = str(tmp_path / "v")
        max_diagrams = 1
    assert cmd_view(Args()) == 0
    assert (tmp_path / "v" / "index.html").is_file()


def test_cmd_view_no_vis_found(tmp_path, capsys):
    class Args:
        paths = ["fixtures/vessel/Launcher"]
        out = str(tmp_path / "v")
        max_diagrams = 1
    import vi_inspector.cli as cli
    orig = cli._collect_vi_paths
    cli._collect_vi_paths = lambda paths: []
    try:
        assert cmd_view(Args()) == 2
    finally:
        cli._collect_vi_paths = orig


def test_cmd_view_multi_needs_out(capsys):
    class Args:
        paths = VIS
        out = None
        max_diagrams = None
    assert cmd_view(Args()) == 2
