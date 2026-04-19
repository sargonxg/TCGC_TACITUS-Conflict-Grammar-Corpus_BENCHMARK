"""Typed edges of the ACO. Closed set for v0.1."""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class Edge(StrEnum):
    ASSERTED = "ASSERTED"
    DENIED = "DENIED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ACKNOWLEDGED_AMBIGUOUSLY = "ACKNOWLEDGED_AMBIGUOUSLY"
    DENIES_SCOPE = "DENIES_SCOPE"
    COMMITS_TO = "COMMITS_TO"
    REVOKES = "REVOKES"
    BLOCKS = "BLOCKS"
    ENABLES = "ENABLES"
    CAUSES = "CAUSES"
    PRECEDES = "PRECEDES"
    CONTRADICTS = "CONTRADICTS"
    SUPPORTS = "SUPPORTS"
    CITES = "CITES"
    HOLDS_INTEREST = "HOLDS_INTEREST"
    FRAMES = "FRAMES"
    LEVERAGES = "LEVERAGES"
    CONSTRAINED_BY = "CONSTRAINED_BY"


EDGE_TYPES: Final[tuple[str, ...]] = tuple(e.value for e in Edge)


def _identity() -> dict[tuple[str, str], float]:
    return {(e, e): 1.0 for e in EDGE_TYPES}


# Every nonzero off-diagonal carries a rationale; see CLAUDE.md §3.3.
TYPE_SIMILARITY: dict[tuple[str, str], float] = _identity() | {
    (Edge.ASSERTED, Edge.ACKNOWLEDGED): 0.5,
    (Edge.ACKNOWLEDGED, Edge.ASSERTED): 0.5,
    (Edge.ACKNOWLEDGED, Edge.ACKNOWLEDGED_AMBIGUOUSLY): 0.75,
    (Edge.ACKNOWLEDGED_AMBIGUOUSLY, Edge.ACKNOWLEDGED): 0.75,
    (Edge.DENIED, Edge.DENIES_SCOPE): 0.5,
    (Edge.DENIES_SCOPE, Edge.DENIED): 0.5,
    (Edge.BLOCKS, Edge.CONSTRAINED_BY): 0.4,
    (Edge.CONSTRAINED_BY, Edge.BLOCKS): 0.4,
    (Edge.ENABLES, Edge.CAUSES): 0.5,
    (Edge.CAUSES, Edge.ENABLES): 0.5,
    (Edge.COMMITS_TO, Edge.ASSERTED): 0.5,
    (Edge.ASSERTED, Edge.COMMITS_TO): 0.5,
}


def similarity(a: str, b: str) -> float:
    if a == b:
        return 1.0
    return TYPE_SIMILARITY.get((a, b), 0.0)


def validate_type(t: str) -> None:
    if t not in EDGE_TYPES:
        raise ValueError(f"Unknown edge type {t!r}. Valid: {', '.join(EDGE_TYPES)}")
