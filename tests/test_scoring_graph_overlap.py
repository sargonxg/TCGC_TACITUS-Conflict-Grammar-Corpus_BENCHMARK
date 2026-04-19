"""Tests for tcgc.scoring.graph_overlap."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tcgc.scoring.graph_overlap import score


def _make_gold(primitives: list[dict], edges: list[dict]) -> dict:  # type: ignore[type-arg]
    return {"primitives": primitives, "edges": edges}


_SIMPLE_GOLD = _make_gold(
    [{"id": "a", "type": "actor"}, {"id": "c", "type": "claim"}],
    [{"from": "a", "to": "c", "type": "ASSERTED", "provenance": "s1"}],
)


def test_identity_score() -> None:
    result = score(_SIMPLE_GOLD, _SIMPLE_GOLD)
    assert result.value == pytest.approx(1.0)


def test_empty_pred_score() -> None:
    result = score(_SIMPLE_GOLD, {"primitives": [], "edges": []})
    assert result.value == pytest.approx(0.0)


def test_partial_node_overlap() -> None:
    pred = _make_gold([{"id": "a", "type": "actor"}], [])
    result = score(_SIMPLE_GOLD, pred)
    assert 0.0 < result.value < 1.0


def test_near_miss_edge_partial_credit() -> None:
    gold = _make_gold(
        [{"id": "a", "type": "actor"}, {"id": "c", "type": "claim"}],
        [{"from": "a", "to": "c", "type": "ASSERTED", "provenance": "s1"}],
    )
    pred = _make_gold(
        [{"id": "a", "type": "actor"}, {"id": "c", "type": "claim"}],
        [{"from": "a", "to": "c", "type": "ACKNOWLEDGED", "provenance": "s1"}],
    )
    result_exact = score(gold, gold)
    result_near = score(gold, pred)
    assert result_near.value < result_exact.value
    assert result_near.value > 0.0


def test_invalid_weights_raise() -> None:
    with pytest.raises(ValueError, match="weights must sum to 1.0"):
        score(_SIMPLE_GOLD, _SIMPLE_GOLD, node_weight=0.3, edge_weight=0.3)


def test_empty_gold_and_pred() -> None:
    result = score({"primitives": [], "edges": []}, {"primitives": [], "edges": []})
    assert result.value == pytest.approx(1.0)


def test_score_result_components() -> None:
    result = score(_SIMPLE_GOLD, _SIMPLE_GOLD)
    assert "node_jaccard" in result.components
    assert "edge_jaccard" in result.components


def test_no_gold_edges_note() -> None:
    gold = _make_gold([{"id": "a", "type": "actor"}], [])
    result = score(gold, gold)
    assert any("no edges" in n for n in result.notes)


def test_no_pred_edges_note() -> None:
    pred = _make_gold([{"id": "a", "type": "actor"}], [])
    result = score(_SIMPLE_GOLD, pred)
    assert any("no edges" in n for n in result.notes)


@settings(max_examples=30)
@given(
    st.lists(
        st.fixed_dictionaries({"id": st.text(min_size=1, max_size=3), "type": st.just("actor")}),
        min_size=0,
        max_size=5,
    )
)
def test_subgraph_deletion_monotone(primitives: list[dict]) -> None:  # type: ignore[type-arg]
    gold = _make_gold(primitives, [])
    full_score = score(gold, gold).value
    for p in primitives:
        reduced = _make_gold([x for x in primitives if x["id"] != p["id"]], [])
        reduced_score = score(gold, reduced).value
        assert reduced_score <= full_score + 1e-9
