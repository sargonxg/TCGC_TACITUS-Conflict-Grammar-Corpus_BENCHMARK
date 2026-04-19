"""HELM adapter for TCGC."""
from __future__ import annotations
try:
    from helm.benchmark.scenarios.scenario import Scenario, Instance, Reference, CORRECT_TAG, Input, Output
except ImportError:
    raise ImportError("Install tcgc[adapters] and HELM to use this adapter.") from None

import json
from typing import Any
from tcgc.adapters._common import load_split


class TCGCScenario(Scenario):
    """HELM Scenario that emits one Instance per TCGC item."""

    name = "tcgc"
    description = "TACITUS Conflict Grammar Corpus benchmark."
    tags: list[str] = ["conflict", "reasoning"]

    def __init__(self, split: str = "v0.1-sample") -> None:
        super().__init__()
        self.split = split

    def get_instances(self, output_path: str) -> list[Instance]:
        instances: list[Instance] = []
        for item in load_split(self.split):
            input_text = (
                f"Task: {item['task_type']}\n"
                f"Domain: {item['domain']}\n"
                f"Question: {item['inputs']['question']}\n"
                f"Input: {json.dumps(item['inputs'])}"
            )
            gold_text = json.dumps(item["gold"])
            instances.append(Instance(
                input=Input(text=input_text),
                references=[Reference(output=Output(text=gold_text), tags=[CORRECT_TAG])],
                split=self.split,
            ))
        return instances
