"""Author: Giulio Catanzariti <giuliocatanzariti@gmail.com>."""

import json
from pathlib import Path

import pytest

from experiments.policy_workflow_inspection.report import inspect


def test_workflow_reference_counts_are_not_semantic_scores(tmp_path: Path) -> None:
    path = tmp_path / "result.json"
    path.write_text(
        json.dumps(
            {
                "format": "tacitus-policy-workflow/1",
                "capsule": {"statements": [{"id": "selected"}]},
                "artifact": {
                    "items": [
                        {"evidence_ids": ["selected", "unknown"], "review_flags": ["condition"]}
                    ]
                },
                "run": {"arm": "flat", "model_calls": 1, "usage": {"total_tokens": 100}},
            }
        )
    )
    r = inspect(path)
    assert r["unknown_citation_ids"] == ["unknown"]
    assert r["semantic_entailment"] == "not_evaluated"
    assert r["tcgc_benchmark_score"] == "not_applicable"
    assert len(r["sha256"]) == 64


def test_inspector_refuses_other_contracts(tmp_path: Path) -> None:
    path = tmp_path / "result.json"
    path.write_text('{"format":"other"}')
    with pytest.raises(ValueError, match="Unsupported workflow"):
        inspect(path)
