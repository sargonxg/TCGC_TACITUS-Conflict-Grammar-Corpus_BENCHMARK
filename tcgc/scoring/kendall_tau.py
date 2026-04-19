"""The `kendall_tau` scorer — τ-b normalized to [0, 1]."""

from __future__ import annotations

from typing import Any

from scipy.stats import kendalltau

from tcgc.scoring.graph_overlap import ScoreResult


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    gold_order = list(gold.get("order", []))
    pred_order = list(pred.get("order", []))
    if not gold_order:
        return ScoreResult(value=1.0, components={"tau": 1.0}, notes=["gold has no order"])
    if not pred_order:
        return ScoreResult(value=0.0, components={"tau": -1.0}, notes=["pred has no order"])
    gold_rank = {eid: i for i, eid in enumerate(gold_order)}
    pred_rank = {eid: i for i, eid in enumerate(pred_order)}
    missing = [eid for eid in gold_order if eid not in pred_rank]
    x = [gold_rank[eid] for eid in gold_order]
    y = [pred_rank.get(eid, len(pred_order)) for eid in gold_order]
    tau, _ = kendalltau(x, y, variant="b")
    if tau is None or tau != tau:  # noqa: PLR0124  # NaN check
        return ScoreResult(value=0.0, components={"tau": 0.0}, notes=["kendalltau returned NaN"])
    norm = (float(tau) + 1.0) / 2.0
    notes = [f"{len(missing)} gold events missing from prediction"] if missing else []
    return ScoreResult(
        value=norm,
        components={"tau": float(tau), "normalized": norm, "missing": float(len(missing))},
        notes=notes,
    )
