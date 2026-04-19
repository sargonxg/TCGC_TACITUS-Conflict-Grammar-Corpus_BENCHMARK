"""The Agentic Conflict Ontology (ACO) — eight primitives."""

from __future__ import annotations

from enum import StrEnum


class Primitive(StrEnum):
    ACTOR = "actor"
    CLAIM = "claim"
    INTEREST = "interest"
    CONSTRAINT = "constraint"
    LEVERAGE = "leverage"
    COMMITMENT = "commitment"
    EVENT = "event"
    NARRATIVE = "narrative"


PRIMITIVES: tuple[str, ...] = tuple(p.value for p in Primitive)

DEFINITIONS: dict[str, str] = {
    "actor": "Any party capable of holding an interest or making a claim: individuals, organizations, states, coalitions.",
    "claim": "An asserted fact, evaluation, or normative statement attributed to an actor.",
    "interest": "An underlying goal or need that motivates claims and positions (Fisher/Ury distinction).",
    "constraint": "A rule, norm, or structural limit shaping feasible outcomes.",
    "leverage": "A resource, dependency, or capability that shifts bargaining power.",
    "commitment": "A promised future action, with a subject and typically a deadline.",
    "event": "A dated or orderable occurrence in the world.",
    "narrative": "A coherent framing across multiple claims, attributable to an actor.",
}
