"""Compare vanilla vs typed records for the same item; emit a markdown diff."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from experiments.llm_vs_typed.runner import RunRecord

JSONL_LINE = re.compile(r"^\s*\{.*\}\s*$")


def _try_parse_jsonl(text: str) -> tuple[list[dict[str, Any]], int]:
    """Parse JSON Lines defensively. Return (ops, parse_errors)."""
    ops: list[dict[str, Any]] = []
    errors = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        if not JSONL_LINE.match(line):
            errors += 1
            continue
        try:
            ops.append(json.loads(line))
        except json.JSONDecodeError:
            errors += 1
    return ops, errors


def _count_ops(ops: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {
        "total": len(ops),
        "create_node": 0,
        "create_edge": 0,
        "update_status": 0,
        "invalidate": 0,
        "with_provenance": 0,
        "causes_with_mechanism": 0,
        "contradicts_with_materiality": 0,
        "interests_with_derivation": 0,
    }
    for op in ops:
        if "node" in op:
            counts["create_node"] += 1
            node = op["node"]
            if node.get("provenance"):
                counts["with_provenance"] += 1
            if node.get("type") == "interest" and node.get("derivation"):
                counts["interests_with_derivation"] += 1
        if "edge" in op:
            counts["create_edge"] += 1
            edge = op["edge"]
            if edge.get("provenance"):
                counts["with_provenance"] += 1
            attrs = edge.get("attributes", {})
            if edge.get("type") == "CAUSES" and attrs.get("mechanism"):
                counts["causes_with_mechanism"] += 1
            if edge.get("type") == "CONTRADICTS" and attrs.get("materiality"):
                counts["contradicts_with_materiality"] += 1
        if op.get("op") == "UPDATE":
            counts["update_status"] += 1
        if op.get("op") == "INVALIDATE":
            counts["invalidate"] += 1
    return counts


def load_pair(item_id: str, runs_dir: Path) -> tuple[RunRecord, RunRecord]:
    vanilla_path = runs_dir / f"{item_id}__vanilla.json"
    typed_path = runs_dir / f"{item_id}__typed.json"
    if not vanilla_path.exists() or not typed_path.exists():
        raise FileNotFoundError(
            f"Missing run file(s) for {item_id} in {runs_dir} — run the orchestrator first."
        )
    vanilla = RunRecord(**json.loads(vanilla_path.read_text(encoding="utf-8")))
    typed = RunRecord(**json.loads(typed_path.read_text(encoding="utf-8")))
    return vanilla, typed


def render_markdown(item_id: str, vanilla: RunRecord, typed: RunRecord, gold: dict[str, Any]) -> str:
    """Produce a side-by-side markdown comparison for one item."""
    typed_ops, parse_errors = _try_parse_jsonl(typed.response_text)
    counts = _count_ops(typed_ops)

    gold_primitives = gold.get("gold", {}).get("primitives", [])
    gold_edges = gold.get("gold", {}).get("edges", [])

    lines: list[str] = []
    lines.append(f"# `{item_id}` · {gold.get('task_type', '?')} · {gold.get('domain', '?')}")
    lines.append("")
    lines.append("## Run provenance")
    lines.append("")
    lines.append(f"- Vanilla: model `{vanilla.model}` · temp {vanilla.temperature} · "
                 f"{vanilla.elapsed_ms} ms · api_call={vanilla.api_call_made} · "
                 f"prompt={vanilla.prompt_hash} · response={vanilla.response_hash} · "
                 f"`{vanilla.timestamp}`")
    lines.append(f"- Typed:   model `{typed.model}` · temp {typed.temperature} · "
                 f"{typed.elapsed_ms} ms · api_call={typed.api_call_made} · "
                 f"prompt={typed.prompt_hash} · response={typed.response_hash} · "
                 f"`{typed.timestamp}`")
    if vanilla.error or typed.error:
        lines.append("")
        lines.append("> ⚠️ One or both runs reported an error. See raw JSON in `runs/`.")
    lines.append("")

    lines.append("## Vanilla output (prose)")
    lines.append("")
    lines.append("```")
    lines.append(vanilla.response_text.strip() or "(empty)")
    lines.append("```")
    lines.append("")

    lines.append("## Typed output (parsed JSON Lines)")
    lines.append("")
    lines.append(f"- Parsed ops: **{counts['total']}** (parse errors: {parse_errors})")
    lines.append(f"  - CREATE node: {counts['create_node']} · CREATE edge: {counts['create_edge']}")
    lines.append(f"  - UPDATE status: {counts['update_status']} · INVALIDATE: {counts['invalidate']}")
    lines.append(f"  - With provenance: {counts['with_provenance']}")
    lines.append(f"  - CAUSES with `mechanism` populated: {counts['causes_with_mechanism']}")
    lines.append(f"  - CONTRADICTS with `materiality` populated: {counts['contradicts_with_materiality']}")
    lines.append(f"  - Interests with `derivation` populated: {counts['interests_with_derivation']}")
    lines.append("")
    lines.append("```jsonl")
    lines.append(typed.response_text.strip() or "(empty)")
    lines.append("```")
    lines.append("")

    lines.append("## Gold (for reference)")
    lines.append("")
    lines.append(f"- Gold primitives: **{len(gold_primitives)}**")
    lines.append(f"- Gold edges: **{len(gold_edges)}**")
    target = gold.get("rubric", {})
    if target:
        lines.append("- Rubric targets:")
        for k, v in target.items():
            lines.append(f"  - `{k}`: {v}")
    lines.append("")

    lines.append("## Diff signal (counts only — not the harness score)")
    lines.append("")
    lines.append("| Axis | Gold | Typed run | Vanilla run |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Primitives | {len(gold_primitives)} | {counts['create_node']} | "
                 f"0 (no typed output by construction) |")
    lines.append(f"| Edges | {len(gold_edges)} | {counts['create_edge']} | 0 |")
    lines.append(f"| Provenance pointers | required on each | {counts['with_provenance']} | 0 |")
    lines.append(f"| CAUSES with mechanism | required when present | {counts['causes_with_mechanism']} | 0 |")
    lines.append("")
    lines.append(
        "> The counts above are **shape diagnostics**, not benchmark scores. To produce a real "
        "graph_overlap / provenance_f1 / kendall_tau number, parse the typed-run output into a "
        "TCGC prediction and run `tcgc score predictions.jsonl items/...`."
    )
    lines.append("")
    return "\n".join(lines)
