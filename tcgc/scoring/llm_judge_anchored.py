"""The `llm_judge_anchored` scorer — isotonic-calibrated LLM judge.

Gated behind TCGC_RUN_API=1. Cite Zheng et al. (2023) "Judging LLM-as-a-Judge".
Known failure modes: position bias, verbosity bias, self-preference bias.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from tcgc.scoring.graph_overlap import ScoreResult

_ANCHOR_PATH = Path(__file__).parent / "anchors" / "v0.1.jsonl"

_DEFAULT_JUDGE_PROMPT = """You are an expert annotator evaluating conflict-analysis outputs.
You will be shown an INPUT (source material plus a question), a GOLD reference
answer structured as a typed subgraph, and a PREDICTED answer in the same shape.
Score the PREDICTED answer on a scale from 0.0 to 1.0.
Return ONLY a single floating-point number.
"""


def _load_anchors() -> list[dict[str, Any]]:  # pragma: no cover
    if not _ANCHOR_PATH.exists(): return []
    import orjson
    return [orjson.loads(line) for line in _ANCHOR_PATH.read_bytes().splitlines() if line.strip()]


def _call_judge(input_obj: dict[str, Any], gold: dict[str, Any], pred: dict[str, Any],
                *, model: str | None = None) -> float:  # pragma: no cover
    raise NotImplementedError(
        "llm_judge_anchored requires a model backend. Implement _call_judge in this module."
    )


def _isotonic(raw: float, anchors: list[dict[str, Any]]) -> float:
    if len(anchors) < 2: return raw
    try:
        from sklearn.isotonic import IsotonicRegression  # type: ignore[import-not-found]
    except ImportError:  # pragma: no cover
        return raw
    xs = [a["raw"] for a in anchors]
    ys = [a["human_score"] for a in anchors]
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    iso.fit(xs, ys)
    return float(iso.predict([raw])[0])


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    if os.environ.get("TCGC_RUN_API") != "1":
        return ScoreResult(value=0.0, components={"raw": 0.0, "calibrated": 0.0},
                           notes=["llm_judge_anchored skipped: set TCGC_RUN_API=1 to enable"])
    input_obj = pred.get("_inputs", {})
    raw = _call_judge(input_obj, gold, pred)  # pragma: no cover
    raw = max(0.0, min(1.0, float(raw)))
    calibrated = _isotonic(raw, _load_anchors())
    return ScoreResult(value=calibrated, components={"raw": raw, "calibrated": calibrated})
