"""lm-evaluation-harness adapter for TCGC."""
from __future__ import annotations
try:
    from lm_eval.api.task import ConfigurableTask  # type: ignore[import-not-found]
except ImportError:
    raise ImportError("Install tcgc[adapters] and lm-eval to use this adapter.") from None

import json
from typing import Any
from tcgc.adapters._common import load_split
from tcgc.scoring import REGISTRY


class TCGCTask(ConfigurableTask):
    """Base lm-eval task for TCGC. Subclassed per task_type."""

    VERSION = 0
    DATASET_NAME: str = "v0.1-sample"
    TASK_TYPE: str = ""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._items = [i for i in load_split(self.DATASET_NAME) if i["task_type"] == self.TASK_TYPE]

    def has_training_docs(self) -> bool:
        return False

    def has_validation_docs(self) -> bool:
        return False

    def has_test_docs(self) -> bool:
        return True

    def test_docs(self) -> list[dict[str, Any]]:
        return self._items

    def doc_to_text(self, doc: dict[str, Any]) -> str:
        return (
            f"Task: {doc['task_type']}\n"
            f"Domain: {doc['domain']}\n"
            f"Question: {doc['inputs']['question']}\n"
            f"Input: {json.dumps(doc['inputs'])}"
        )

    def doc_to_target(self, doc: dict[str, Any]) -> str:
        return json.dumps(doc["gold"])

    def process_results(self, doc: dict[str, Any], results: list[str]) -> dict[str, Any]:
        pred_text = results[0] if results else "{}"
        try:
            pred = json.loads(pred_text)
        except json.JSONDecodeError:
            pred = {}
        scorer = REGISTRY.get(doc["rubric"]["scoring"])
        if scorer is None:
            return {"score": 0.0}
        result = scorer(doc["gold"], pred)
        return {"score": float(result.value)}

    def aggregation(self) -> dict[str, Any]:
        return {"score": lambda xs: sum(xs) / len(xs) if xs else 0.0}

    def higher_is_better(self) -> dict[str, bool]:
        return {"score": True}


def _make_task_class(task_type: str) -> type:
    return type(
        f"TCGC_{task_type.replace('-', '_')}",
        (TCGCTask,),
        {"TASK_TYPE": task_type},
    )


TASK_REGISTRY: dict[str, type] = {
    f"tcgc_{tt.replace('-', '_')}": _make_task_class(tt)
    for tt in [
        "actor-resolution", "claim-extraction", "interest-extraction",
        "constraint-extraction", "leverage-mapping", "commitment-tracking",
        "event-ordering", "narrative-drift", "causal-chain",
        "contradiction-detection", "provenance-attribution",
        "commitment-claim-mismatch", "position-interest-separation",
        "cross-document-synthesis",
    ]
}
