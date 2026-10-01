"""Automated code-review rules for LabVIEW VIs.

Built on lvkit's parsed block-diagram model (Apache-2.0). Each rule inspects
the diagram semantically -- nodes, terminals, wires, structures -- and emits
findings with a severity, the same way a human reviewer would flag them.
"""
from __future__ import annotations

import glob as _glob
import os as _os
from dataclasses import dataclass, field
from pathlib import Path

from lvkit.parser.vi import parse_vi
from lvkit.parser.models import ParsedVI, ParsedWiringRule

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}

# Wiring-rule values (LabVIEW connector-pane TypeDesc Flags bits 8-9).
_WIRING_REQUIRED = ParsedWiringRule.REQUIRED.value  # 1


class ReviewContext:
    """Cross-VI state shared by rules that need callee information.

    Built once per review run over all reviewed VI paths. Resolves SubVI
    call nodes to callee files (same-directory match wins on ambiguous
    names) and caches each callee's connector-pane wiring rules and
    terminal labels. Anything unresolvable -- vi.lib VIs, missing files,
    unparseable callees -- yields None, and rules skip silently: we never
    flag on missing data.
    """

    def __init__(self, vi_paths: list[str | Path]):
        self._index: dict[str, list[str]] = {}
        for p in vi_paths:
            self._index.setdefault(Path(p).name.lower(), []).append(str(p))
        # Also index malleable VIs (.vim) sitting next to the reviewed files;
        # they are callable SubVIs but never reviewed themselves.
        seen_dirs = {str(Path(p).parent) for p in vi_paths}
        for d in seen_dirs:
            for vim in _glob.glob(_os.path.join(d, "**", "*.vim"),
                                  recursive=True):
                self._index.setdefault(Path(vim).name.lower(), []).append(vim)
        self._callee_cache: dict[str, tuple | None] = {}

    def _resolve_callee(self, caller_path: str, node_name: str) -> str | None:
        # Library-qualified names look like "lib.lvlib:VI.vi".
        base = node_name.split(":")[-1].strip().lower()
        cands = self._index.get(base)
        if not cands:
            return None
        cdir = str(Path(caller_path).parent)
        cands = sorted(cands, key=lambda c: (str(Path(c).parent) != cdir, c))
        return cands[0]

    def resolve_callee(self, caller_path: str, node_name: str) -> str | None:
        """Public wrapper: callee file path for a SubVI call node, or None."""
        return self._resolve_callee(caller_path, node_name)

    def callee_interface(
        self, caller_path: str, node_name: str
    ) -> tuple[str, dict[int, int], dict[int, str]] | None:
        """(callee path, {slot: wiring rule}, {slot: label}) or None."""
        callee = self._resolve_callee(caller_path, node_name)
        if callee is None:
            return None
        if callee not in self._callee_cache:
            self._callee_cache[callee] = self._load_interface(callee)
        info = self._callee_cache[callee]
        return (callee, info[0], info[1]) if info else None

    @staticmethod
    def _load_interface(callee: str) -> tuple[dict, dict] | None:
        try:
            from lvkit.extractor import extract_vi_xml
            from lvkit.parser.front_panel import (
                parse_connector_pane,
                parse_connector_pane_types,
                parse_connector_pane_labels,
            )
            _, fp_xml, main_xml = extract_vi_xml(callee)
            if not fp_xml or not main_xml:
                return None
            conpane = parse_connector_pane(fp_xml)
            if conpane is None:
                return None
            rules = parse_connector_pane_types(main_xml, conpane)
            labels = parse_connector_pane_labels(main_xml)
            return (rules, labels)
        except Exception:  # noqa: BLE001 -- unresolvable callee: skip
            return None


@dataclass
class ReviewFinding:
    rule_id: str
    severity: str  # high | medium | low | info
    title: str
    detail: str
    node_name: str | None = None
    node_type: str | None = None


@dataclass
class VIReview:
    vi_path: str
    vi_name: str
    findings: list[ReviewFinding] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    parse_ok: bool = True
    parse_error: str | None = None
    # Resolved callee file paths for plain SubVI calls (iUse) in this VI.
    # Drives the report's Calls / Called-by navigation.
    calls: list[str] = field(default_factory=list)

    def by_severity(self, sev: str) -> list[ReviewFinding]:
        return [f for f in self.findings if f.severity == sev]


def _is_error_cluster(parsed_type) -> bool:
    """Standard LabVIEW error cluster: {status: Boolean, code: I32, source: String}."""
    if parsed_type is None or getattr(parsed_type, "kind", None) != "cluster":
        return False
    fields = getattr(parsed_type, "fields", None) or []
    names = {(f.name or "").lower() for f in fields}
    return names == {"status", "code", "source"}


def _wired_terminals(bd) -> set[str]:
    wired: set[str] = set()
    for w in bd.wires:
        wired.add(w.from_term)
        wired.add(w.to_term)
    return wired


SUBVI_NODE_TYPES = {"iUse", "polyIUse", "dynIUse", "callParentDynIUse"}

# VIs that terminate error chains by design: an unwired error terminal on
# these is normal, not a defect (audit: Simple Error Handler.vi flagged high).
_ERROR_HANDLER_HINT = "error handler"


def _node_display_name(parent, ptype: str | None, node_name: str | None) -> str:
    """Human-locatable node name: prefer method/property names for invoke and
    property nodes, which otherwise render as bare 'Invoke Node'/'Property Node'."""
    name = (node_name or "").strip()
    if parent is not None:
        if ptype == "invokeNode":
            method = (getattr(parent, "method_name", "") or "").strip()
            if method:
                return f"Invoke Node '{method}'"
        elif ptype == "propNode":
            props = getattr(parent, "properties", None) or []
            if props:
                first = props[0] if isinstance(props[0], dict) else {}
                pname = str(
                    first.get("name") or first.get("property")
                    or first.get("prop_name") or ""
                ).strip()
                if pname:
                    return f"Property Node '{pname}'"
    return name or (ptype or "node")


def _rule_unwired_error_terminals(pvi: ParsedVI, review: VIReview) -> None:
    """ERR-1: unwired error terminals on SubVI calls.

    Severity is calibrated by failure mode (precision audit, 2026-10-01):
    - unwired error OUT -> high: errors raised by this call are silently
      dropped and invisible to callers.
    - unwired error IN with error out wired -> medium: the node runs even
      when upstream code errored, breaking the chain, but its own errors
      still propagate downstream.
    Error-handler VIs (Simple/General Error Handler) terminate chains by
    design and are exempt.

    ERR-1b: a primitive with error-in wired but error-out unwired breaks the
    error chain mid-diagram (medium). Primitives with both error terminals
    unwired are deliberately skipped: that is normal LabVIEW practice and
    flagging it would drown the report.
    """
    bd = pvi.block_diagram
    wired = _wired_terminals(bd)
    # group error terminals by parent node
    by_parent: dict[str, list] = {}
    for uid, t in bd.terminal_info.items():
        if not _is_error_cluster(getattr(t, "parsed_type", None)):
            continue
        by_parent.setdefault(t.parent_uid, []).append((uid, t))

    for parent_uid, terms in by_parent.items():
        parent = bd.get_node(parent_uid)
        ptype = getattr(parent, "node_type", None)
        raw_name = getattr(parent, "name", None) or getattr(parent, "label", None)
        node_name = _node_display_name(parent, ptype, raw_name)
        if ptype in SUBVI_NODE_TYPES:
            if _ERROR_HANDLER_HINT in (raw_name or "").lower():
                continue  # chain terminator by design
            in_unwired = any(uid not in wired and not t.is_output for uid, t in terms)
            out_unwired = any(uid not in wired and t.is_output for uid, t in terms)
            if out_unwired:
                review.findings.append(ReviewFinding(
                    rule_id="ERR-1",
                    severity="high",
                    title=f"Unwired error out on SubVI '{node_name}'",
                    detail=(
                        f"The error out terminal of '{node_name}' is not wired. "
                        "Errors from this call are silently dropped and invisible to callers."
                    ),
                    node_name=node_name,
                    node_type=ptype,
                ))
            elif in_unwired:
                review.findings.append(ReviewFinding(
                    rule_id="ERR-1",
                    severity="medium",
                    title=f"Unwired error in on SubVI '{node_name}'",
                    detail=(
                        f"The error in terminal of '{node_name}' is not wired, so it "
                        "executes even when upstream code has errored. Its own errors "
                        "still propagate downstream."
                    ),
                    node_name=node_name,
                    node_type=ptype,
                ))
        else:
            in_wired = any(uid in wired and not t.is_output for uid, t in terms)
            out_unwired = any(uid not in wired and t.is_output for uid, t in terms)
            if in_wired and out_unwired:
                review.findings.append(ReviewFinding(
                    rule_id="ERR-1b",
                    severity="medium",
                    title=f"Broken error chain on '{node_name}'",
                    detail=(
                        "Error in is wired but error out is not. Downstream nodes "
                        "never see errors raised here."
                    ),
                    node_name=node_name,
                    node_type=ptype,
                ))


def _rule_unwired_required_inputs(
    pvi: ParsedVI, review: VIReview, ctx: ReviewContext | None
) -> None:
    """WIRE-1: unwired REQUIRED inputs on SubVI calls (high).

    Precision rebuild of the WIRE-1 rule removed after the 2026-10-01 audit
    (0/6 samples actionable: phantom terminals on method-call nodes plus
    optional-with-default noise). Instead of flagging every unwired input,
    this resolves the callee VI and reads its connector-pane wiring rules
    (TypeDesc Flags bits 8-9). Only REQUIRED inputs are flagged: an unwired
    required input means the VI cannot run, a genuine defect rather than
    style noise. Recommended/optional inputs have defaults and are never
    flagged; unresolvable callees (vi.lib, missing files) are skipped.
    Only plain SubVI calls (iUse) are considered -- method-call nodes
    (dynIUse) expose phantom terminals in the parsed model that do not
    exist in LabVIEW, and polymorphic calls (polyIUse) cannot be resolved
    to a single callee interface.
    """
    if ctx is None:
        return
    bd = pvi.block_diagram
    wired = _wired_terminals(bd)
    for node in bd.nodes:
        if getattr(node, "node_type", None) != "iUse":
            continue
        raw_name = getattr(node, "name", None) or getattr(node, "label", None)
        if not raw_name:
            continue
        iface = ctx.callee_interface(review.vi_path, raw_name)
        if iface is None:
            continue
        _callee, rules, labels = iface
        node_name = _node_display_name(node, "iUse", raw_name)
        for uid, t in bd.terminal_info.items():
            if t.parent_uid != node.uid or t.is_output:
                continue
            if uid in wired:
                continue
            # paramIdx == connector-pane slot index (verified: SubVI node
            # terminals are exposed per pattern position).
            if rules.get(t.index) != _WIRING_REQUIRED:
                continue
            term_label = labels.get(t.index) or f"terminal {t.index}"
            review.findings.append(ReviewFinding(
                rule_id="WIRE-1",
                severity="high",
                title=(f"Unwired required input '{term_label}' "
                       f"on SubVI '{node_name}'"),
                detail=(
                    f"Input '{term_label}' of '{node_name}' is marked "
                    f"Required on its connector pane but is not wired. "
                    f"This VI cannot run as drawn."
                ),
                node_name=node_name,
                node_type="iUse",
            ))


def _collect_calls(pvi: ParsedVI, review: VIReview,
                   ctx: ReviewContext | None) -> None:
    """Record resolved callee paths for plain SubVI calls (iUse).

    Powers the report's Calls / Called-by navigation. Unresolvable callees
    (vi.lib, missing files) are skipped, matching WIRE-1's fail-silent rule.
    """
    if ctx is None:
        return
    bd = pvi.block_diagram
    seen: set[str] = set()
    for node in bd.nodes:
        if getattr(node, "node_type", None) != "iUse":
            continue
        raw_name = getattr(node, "name", None) or getattr(node, "label", None)
        if not raw_name:
            continue
        callee = ctx.resolve_callee(review.vi_path, raw_name)
        if callee and callee not in seen:
            seen.add(callee)
            review.calls.append(callee)


def _rule_missing_error_handling(pvi: ParsedVI, review: VIReview) -> None:
    """ERR-2: VI exposes error in/out but wires no error cluster on the diagram."""
    pane_terms = [t for t in pvi.block_diagram.fp_terminals]
    has_error_io = any(
        _is_error_cluster(getattr(t, "parsed_type", None)) for t in pane_terms
    )
    if not has_error_io:
        return
    wired_error = any(
        _is_error_cluster(getattr(pvi.block_diagram.terminal_info.get(uid), "parsed_type", None))
        for w in pvi.block_diagram.wires
        for uid in (w.from_term, w.to_term)
    )
    if not wired_error:
        review.findings.append(ReviewFinding(
            rule_id="ERR-2",
            severity="high",
            title="Error terminals exposed but never wired",
            detail=(
                "The connector pane has error in/out, but no error cluster is "
                "wired anywhere on the block diagram. Callers cannot rely on "
                "this VI's error reporting."
            ),
        ))


def _rule_local_variables(pvi: ParsedVI, review: VIReview) -> None:
    """RACE-1: local variables are a race-condition risk; flag each use."""
    bd = pvi.block_diagram
    grefs = [n for n in bd.nodes if n.node_type in ("gRef", "gRefDCO")]
    if grefs:
        review.findings.append(ReviewFinding(
            rule_id="RACE-1",
            severity="medium",
            title=f"{len(grefs)} local variable(s) used",
            detail=(
                "Local variables break dataflow and can introduce race "
                "conditions between parallel code paths. Prefer wires, shift "
                "registers, or functional globals."
            ),
        ))


# NOTE (2026-10-01): WIRE-1 ("unwired SubVI inputs") was removed after a
# precision audit found 0% actionable hits (6 sampled, verified against
# genuine LabVIEW renders). Method-call nodes expose phantom unnamed
# terminals in the parsed model, and the remaining hits are optional inputs
# with sensible defaults. A precise version needs cross-VI analysis: resolve
# the callee's connector pane and flag unwired REQUIRED inputs only. Tracked
# as a planned rule, not an active one.
#
#
def _collect_metrics(pvi: ParsedVI, review: VIReview) -> None:
    bd = pvi.block_diagram
    n_structures = (
        len(bd.loops) + len(bd.case_structures) + len(bd.flat_sequences)
        + len(bd.event_structures) + len(bd.decompose_structures)
        + len(bd.disable_structures)
    )
    review.metrics = {
        "nodes": len(bd.nodes),
        "wires": len(bd.wires),
        "constants": len(bd.constants),
        "structures": n_structures,
        "loops": len(bd.loops),
        "case_structures": len(bd.case_structures),
        "event_structures": len(bd.event_structures),
        "sequences": len(bd.flat_sequences),
        "subvi_calls": sum(1 for n in bd.nodes if n.node_type in ("iUse", "polyIUse", "dynIUse", "callParentDynIUse")),
        "fp_terminals": len(bd.fp_terminals),
    }
    if review.metrics["nodes"] > 50:
        review.findings.append(ReviewFinding(
            rule_id="CPLX-1", severity="info", title="Large block diagram",
            detail=f"{review.metrics['nodes']} nodes on one diagram. Consider splitting into subVIs.",
        ))


def _dedupe_findings(findings: list[ReviewFinding]) -> list[ReviewFinding]:
    """Merge identical (rule, title) findings within one VI, e.g. four call
    sites of the same utility VI become one finding with a ×4 count."""
    buckets: dict[tuple[str, str], list] = {}
    order: list[tuple[str, str]] = []
    for f in findings:
        key = (f.rule_id, f.title)
        if key in buckets:
            buckets[key][1] += 1
        else:
            buckets[key] = [f, 1]
            order.append(key)
    out = []
    for key in order:
        f, n = buckets[key]
        if n > 1:
            f.title = f"{f.title} (×{n})"
        out.append(f)
    return out


def review_vi(vi_path: str | Path,
             ctx: ReviewContext | None = None) -> VIReview:
    """Run all review rules against a single VI file.

    Pass a ReviewContext (built over the whole reviewed set) to enable
    cross-VI rules such as WIRE-1; without one those rules are skipped.
    """
    vi_path = str(vi_path)
    review = VIReview(vi_path=vi_path, vi_name=Path(vi_path).name)
    try:
        pvi = parse_vi(vi_path)
    except Exception as e:  # noqa: BLE001 -- one bad VI must not kill the run
        review.parse_ok = False
        review.parse_error = f"{type(e).__name__}: {e}"
        return review
    _rule_unwired_error_terminals(pvi, review)
    _rule_unwired_required_inputs(pvi, review, ctx)
    _rule_missing_error_handling(pvi, review)
    _rule_local_variables(pvi, review)
    _collect_metrics(pvi, review)
    _collect_calls(pvi, review, ctx)
    review.findings = _dedupe_findings(review.findings)
    review.findings.sort(key=lambda f: SEVERITY_ORDER[f.severity])
    return review


def build_call_graph(reviews: list[VIReview]) -> dict[str, dict[str, list[str]]]:
    """Calls / called-by map restricted to the reviewed set.

    Returns {vi_path: {"calls": [...], "called_by": [...]}} with both lists
    sorted by VI name. Callees outside the reviewed set (vi.lib, .vim,
    unreviewed files) are counted but not linked.
    """
    reviewed = {r.vi_path for r in reviews}
    graph: dict[str, dict[str, list[str]]] = {
        r.vi_path: {"calls": [], "called_by": [], "external": 0} for r in reviews
    }
    for r in reviews:
        for callee in r.calls:
            if callee in reviewed:
                graph[r.vi_path]["calls"].append(callee)
                graph[callee]["called_by"].append(r.vi_path)
            else:
                graph[r.vi_path]["external"] += 1
    for entry in graph.values():
        entry["calls"] = sorted(set(entry["calls"]),
                                key=lambda p: Path(p).name.lower())
        entry["called_by"] = sorted(set(entry["called_by"]),
                                    key=lambda p: Path(p).name.lower())
    return graph


def review_many(vi_paths: list[str | Path],
                ctx: ReviewContext | None = None) -> list[VIReview]:
    if ctx is None:
        ctx = ReviewContext(vi_paths)
    return [review_vi(p, ctx) for p in vi_paths]
