"""Tests for tcgc.scoring.provenance_f1."""

from __future__ import annotations

import pytest

from tcgc.scoring.provenance_f1 import score


def test_identity() -> None:
    gold = {
        "primitives": [{"id": "a", "provenance": "doc1"}, {"id": "b", "provenance": "doc2"}],
        "edges": [{"from": "a", "to": "b", "type": "ASSERTED", "provenance": "doc1"}],
    }
    result = score(gold, gold)
    assert result.value == pytest.approx(1.0)


def test_empty_both() -> None:
    result = score({"primitives": [], "edges": []}, {"primitives": [], "edges": []})
    assert result.value == pytest.approx(1.0)


def test_empty_pred() -> None:
    gold = {"primitives": [{"id": "a", "provenance": "doc1"}], "edges": []}
    result = score(gold, {"primitives": [], "edges": []})
    assert result.value == pytest.approx(0.0)
    assert any("no provenance" in n for n in result.notes)


def test_partial_precision_recall() -> None:
    gold = {
        "primitives": [
            {"id": "a", "provenance": "doc1"},
            {"id": "b", "provenance": "doc2"},
            {"id": "c", "provenance": "doc3"},
        ],
        "edges": [],
    }
    pred = {
        "primitives": [
            {"id": "a", "provenance": "doc1"},
            {"id": "b", "provenance": "doc2"},
            {"id": "d", "provenance": "doc99"},
        ],
        "edges": [],
    }
    result = score(gold, pred)
    assert result.components["precision"] == pytest.approx(2 / 3)
    assert result.components["recall"] == pytest.approx(2 / 3)
    assert result.value == pytest.approx(2 / 3)


def test_list_provenance() -> None:
    gold = {"primitives": [{"id": "x", "provenance": ["doc1", "doc2"]}], "edges": []}
    pred = {"primitives": [{"id": "x", "provenance": ["doc1", "doc2"]}], "edges": []}
    result = score(gold, pred)
    assert result.value == pytest.approx(1.0)
