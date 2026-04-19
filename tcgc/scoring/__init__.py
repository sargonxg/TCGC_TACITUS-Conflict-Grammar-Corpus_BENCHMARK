"""Scorer registry."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from tcgc.scoring.contradiction_pair_f1 import score as contradiction_pair_f1_score
from tcgc.scoring.graph_overlap import ScoreResult
from tcgc.scoring.graph_overlap import score as graph_overlap_score
from tcgc.scoring.kendall_tau import score as kendall_tau_score
from tcgc.scoring.llm_judge_anchored import score as llm_judge_anchored_score
from tcgc.scoring.provenance_f1 import score as provenance_f1_score

Scorer = Callable[[dict[str, Any], dict[str, Any]], ScoreResult]

REGISTRY: dict[str, Scorer] = {
    "graph_overlap": graph_overlap_score,
    "provenance_f1": provenance_f1_score,
    "kendall_tau": kendall_tau_score,
    "contradiction_pair_f1": contradiction_pair_f1_score,
    "llm_judge_anchored": llm_judge_anchored_score,
}


def get(name: str) -> Scorer:
    if name not in REGISTRY:
        raise KeyError(f"Unknown scorer {name!r}. Known: {', '.join(sorted(REGISTRY))}")
    return REGISTRY[name]


__all__ = ["REGISTRY", "ScoreResult", "Scorer", "get"]
