"""The `provenance_f1` scorer — F1 over (primitive_id, provenance_ref) pairs."""

from __future__ import annotations

from typing import Any

from tcgc.scoring.graph_overlap import ScoreResult


def _norm(p: Any) -> list[str]:
    if p is None:
        return []
    if isinstance(p, str):
        return [p]
    if isinstance(p, list):
        return [str(x) for x in p]
    return []


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    gold_pairs: set[tuple[str, str]] = set()
    pred_pairs: set[tuple[str, str]] = set()
    for n in gold.get("primitives", []):
        for ref in _norm(n.get("provenance")):
            gold_pairs.add((n.get("id", ""), ref))
    for e in gold.get("edges", []):
        k = f"edge:{e.get('from')}->{e.get('to')}:{e.get('type')}"
        for ref in _norm(e.get("provenance")):
            gold_pairs.add((k, ref))
    for n in pred.get("primitives", []):
        for ref in _norm(n.get("provenance")):
            pred_pairs.add((n.get("id", ""), ref))
    for e in pred.get("edges", []):
        k = f"edge:{e.get('from')}->{e.get('to')}:{e.get('type')}"
        for ref in _norm(e.get("provenance")):
            pred_pairs.add((k, ref))
    if not gold_pairs and not pred_pairs:
        return ScoreResult(value=1.0, components={"precision": 1.0, "recall": 1.0})
    if not pred_pairs:
        return ScoreResult(
            value=0.0,
            components={"precision": 0.0, "recall": 0.0},
            notes=["pred has no provenance-bearing primitives"],
        )
    if not gold_pairs:
        return ScoreResult(value=0.0, components={"precision": 0.0, "recall": 0.0})
    tp = len(gold_pairs & pred_pairs)
    prec: float = tp / len(pred_pairs)
    rec: float = tp / len(gold_pairs)
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return ScoreResult(value=f1, components={"precision": prec, "recall": rec, "tp": float(tp)})
