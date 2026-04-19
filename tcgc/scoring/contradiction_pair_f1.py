"""The `contradiction_pair_f1` scorer — materiality-weighted F1."""

from __future__ import annotations

from typing import Any

from tcgc.scoring.graph_overlap import ScoreResult

_WEIGHT = {"material": 1.0, "cosmetic": 0.25}


def _pair(a: str, b: str) -> frozenset[str]:
    return frozenset({a, b})


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    gm: dict[frozenset[str], str] = {
        _pair(g["claim_a"], g["claim_b"]): g.get("materiality", "material")
        for g in gold.get("contradictions", [])
    }
    pp: set[frozenset[str]] = {
        _pair(p["claim_a"], p["claim_b"]) for p in pred.get("contradictions", [])
    }
    if not gm and not pp:
        return ScoreResult(value=1.0, components={"f1_weighted": 1.0, "f1_unweighted": 1.0})
    if not gm:
        return ScoreResult(
            value=0.0,
            components={"f1_weighted": 0.0, "f1_unweighted": 0.0, "precision": 0.0, "recall": 0.0},
        )
    if not pp:
        return ScoreResult(
            value=0.0,
            components={"f1_weighted": 0.0, "f1_unweighted": 0.0, "precision": 0.0, "recall": 0.0},
            notes=["pred has no contradictions"],
        )
    tp_w = sum(_WEIGHT[gm[p]] for p in pp if p in gm)
    fp_w = sum(1.0 for p in pp if p not in gm)
    fn_w = sum(_WEIGHT[gm[p]] for p in gm if p not in pp)
    prec_w = tp_w / (tp_w + fp_w) if (tp_w + fp_w) else 0.0
    rec_w = tp_w / (tp_w + fn_w) if (tp_w + fn_w) else 0.0
    f1_w = 2 * prec_w * rec_w / (prec_w + rec_w) if (prec_w + rec_w) else 0.0
    tp = len(pp & set(gm.keys()))
    prec_u = tp / len(pp) if pp else 0.0
    rec_u = tp / len(gm) if gm else 0.0
    f1_u = 2 * prec_u * rec_u / (prec_u + rec_u) if (prec_u + rec_u) else 0.0
    return ScoreResult(
        value=f1_w,
        components={
            "f1_weighted": f1_w,
            "f1_unweighted": f1_u,
            "precision": prec_w,
            "recall": rec_w,
        },
    )
