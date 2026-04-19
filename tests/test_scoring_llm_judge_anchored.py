"""Tests for tcgc.scoring.llm_judge_anchored."""
from __future__ import annotations
import os
import pytest
from tcgc.scoring.llm_judge_anchored import score


def test_skipped_without_api_flag() -> None:
    env = os.environ.copy()
    env.pop("TCGC_RUN_API", None)
    os.environ.pop("TCGC_RUN_API", None)
    result = score({}, {})
    assert result.value == pytest.approx(0.0)
    assert any("skipped" in n for n in result.notes)


@pytest.mark.requires_api
def test_real_api_call() -> None:
    os.environ["TCGC_RUN_API"] = "1"
    try:
        result = score({"primitives": []}, {"primitives": []})
        assert 0.0 <= result.value <= 1.0
    finally:
        del os.environ["TCGC_RUN_API"]
