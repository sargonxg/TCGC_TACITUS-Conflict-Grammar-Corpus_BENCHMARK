"""Tests for tcgc.adapters.lm_eval — skipped if lm_eval not installed."""

from __future__ import annotations

import pytest

lm_eval = pytest.importorskip("lm_eval", reason="lm_eval not installed; skipping adapter test")


def test_lm_eval_task_registry_has_14_tasks() -> None:
    from tcgc.adapters.lm_eval import TASK_REGISTRY

    assert len(TASK_REGISTRY) == 14


def test_lm_eval_commitment_tracking_enumerates_1_item() -> None:
    from tcgc.adapters.lm_eval import TCGCTask

    class CommitmentTask(TCGCTask):
        TASK_TYPE = "commitment-tracking"

    task = CommitmentTask()
    docs = task.test_docs()
    assert len(docs) >= 1
    assert all(d["task_type"] == "commitment-tracking" for d in docs)
