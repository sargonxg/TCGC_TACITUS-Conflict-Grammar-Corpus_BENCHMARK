"""Tests for tcgc.ontology."""
from __future__ import annotations
import pytest
from tcgc.ontology import EDGE_TYPES, PRIMITIVES, Edge, Primitive, similarity, validate_type


def test_primitive_enum_members() -> None:
    expected = {"actor", "claim", "interest", "constraint", "leverage", "commitment", "event", "narrative"}
    assert set(PRIMITIVES) == expected


def test_edge_enum_has_18_members() -> None:
    assert len(EDGE_TYPES) == 18


def test_edge_enum_members_include_asserted() -> None:
    assert "ASSERTED" in EDGE_TYPES


def test_similarity_identity() -> None:
    assert similarity("ASSERTED", "ASSERTED") == pytest.approx(1.0)


def test_similarity_unknown_returns_zero() -> None:
    assert similarity("FOO", "BAR") == pytest.approx(0.0)


def test_similarity_near_miss() -> None:
    val = similarity("ASSERTED", "ACKNOWLEDGED")
    assert val == pytest.approx(0.5)


def test_validate_type_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown edge type"):
        validate_type("INVENTED")


def test_validate_type_known_no_raise() -> None:
    validate_type("ASSERTED")
    validate_type("CONTRADICTS")


def test_similarity_symmetric() -> None:
    assert similarity("ASSERTED", "ACKNOWLEDGED") == similarity("ACKNOWLEDGED", "ASSERTED")
