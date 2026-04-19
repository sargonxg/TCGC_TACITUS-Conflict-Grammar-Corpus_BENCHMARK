"""The `graph_overlap` scorer — Jaccard over the typed subgraph."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from tcgc.ontology.edges import similarity


@dataclass
class ScoreResult:
    value: float
    components: dict[str, float] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def _node_key(n: dict[str, Any]) -> tuple[str, str]:
    return (n.get("type", ""), n.get("id", ""))


def _edge_key(e: dict[str, Any]) -> tuple[str, str]:
    return (e.get("from", ""), e.get("to", ""))


def _jaccard(a: set[Any], b: set[Any]) -> float:
    if not a and not b: return 1.0
    if not a or not b:  return 0.0
    return len(a & b) / len(a | b)


def _edge_match_score(gold_edges: list[dict[str, Any]], pred_edges: list[dict[str, Any]]) -> float:
    gold_by_pair: dict[tuple[str, str], list[str]] = {}
    pred_by_pair: dict[tuple[str, str], list[str]] = {}
    for e in gold_edges: gold_by_pair.setdefault(_edge_key(e), []).append(e.get("type", ""))
    for e in pred_edges: pred_by_pair.setdefault(_edge_key(e), []).append(e.get("type", ""))
    union = set(gold_by_pair) | set(pred_by_pair)
    if not union: return 1.0
    total = 0.0
    for pair in union:
        g, p = gold_by_pair.get(pair, []), pred_by_pair.get(pair, [])
        if not g or not p: continue
        total += max(similarity(a, b) for a in g for b in p)
    return total / len(union)


def score(gold: dict[str, Any], pred: dict[str, Any], *,
          node_weight: float = 0.4, edge_weight: float = 0.6) -> ScoreResult:
    if abs(node_weight + edge_weight - 1.0) > 1e-9:
        raise ValueError(f"weights must sum to 1.0 (got {node_weight + edge_weight})")
    gold_nodes = {_node_key(n) for n in gold.get("primitives", [])}
    pred_nodes = {_node_key(n) for n in pred.get("primitives", [])}
    node_j = _jaccard(gold_nodes, pred_nodes)
    edge_j = _edge_match_score(gold.get("edges", []), pred.get("edges", []))
    value = node_weight * node_j + edge_weight * edge_j
    notes: list[str] = []
    if not gold.get("edges"): notes.append("gold has no edges — score reduces to node overlap")
    if not pred.get("edges") and gold.get("edges"): notes.append("pred has no edges — edge_jaccard is 0")
    return ScoreResult(value=value, components={"node_jaccard": node_j, "edge_jaccard": edge_j}, notes=notes)
