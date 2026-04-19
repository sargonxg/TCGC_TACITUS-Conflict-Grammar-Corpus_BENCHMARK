"""Tests for tcgc.scoring.kendall_tau."""
from __future__ import annotations
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from tcgc.scoring.kendall_tau import score


def test_identity_returns_1() -> None:
    gold = {"order": ["e1", "e2", "e3"]}
    result = score(gold, gold)
    assert result.value == pytest.approx(1.0)


def test_fully_reversed_below_half() -> None:
    gold = {"order": ["e1", "e2", "e3", "e4"]}
    pred = {"order": ["e4", "e3", "e2", "e1"]}
    result = score(gold, pred)
    assert result.value <= 0.5


def test_empty_gold() -> None:
    result = score({"order": []}, {"order": []})
    assert result.value == pytest.approx(1.0)


def test_empty_pred() -> None:
    gold = {"order": ["e1", "e2"]}
    result = score(gold, {"order": []})
    assert result.value == pytest.approx(0.0)


def test_missing_events_penalized() -> None:
    gold = {"order": ["e1", "e2", "e3"]}
    pred = {"order": ["e1"]}
    result = score(gold, pred)
    assert result.value < 1.0
    assert result.components["missing"] > 0


@settings(max_examples=20)
@given(st.lists(st.text(min_size=1, max_size=2), min_size=2, max_size=6, unique=True))
def test_reversed_le_half(events: list[str]) -> None:
    gold = {"order": events}
    pred = {"order": list(reversed(events))}
    result = score(gold, pred)
    assert result.value <= 0.5 + 1e-9
