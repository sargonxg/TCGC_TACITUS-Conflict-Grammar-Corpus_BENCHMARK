"""Tests for tcgc.scoring.contradiction_pair_f1."""

from __future__ import annotations

import pytest

from tcgc.scoring.contradiction_pair_f1 import score


def _make(pairs: list[tuple[str, str, str]]) -> dict:  # type: ignore[type-arg]
    return {"contradictions": [{"claim_a": a, "claim_b": b, "materiality": m} for a, b, m in pairs]}


def test_identity() -> None:
    gold = _make([("c1", "c2", "material"), ("c3", "c4", "cosmetic")])
    assert score(gold, gold).value == pytest.approx(1.0)


def test_empty_both() -> None:
    assert score(_make([]), _make([])).value == pytest.approx(1.0)


def test_empty_pred() -> None:
    gold = _make([("c1", "c2", "material")])
    result = score(gold, _make([]))
    assert result.value == pytest.approx(0.0)
    assert any("no contradictions" in n for n in result.notes)


def test_unordered_pair_equivalence() -> None:
    gold = _make([("c1", "c2", "material")])
    pred = _make([("c2", "c1", "material")])
    assert score(gold, pred).value == pytest.approx(1.0)


def test_material_beats_cosmetic() -> None:
    gold = _make([("a", "b", "material"), ("c", "d", "cosmetic")])
    pred_material_only = _make([("a", "b", "material")])
    pred_cosmetic_only = _make([("c", "d", "cosmetic")])
    assert score(gold, pred_material_only).value > score(gold, pred_cosmetic_only).value


def test_f1_unweighted_in_components() -> None:
    gold = _make([("c1", "c2", "material")])
    result = score(gold, gold)
    assert "f1_unweighted" in result.components
