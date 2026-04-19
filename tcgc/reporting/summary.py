"""Markdown summary rendering for score results."""

from __future__ import annotations

from typing import Any


def render_markdown(scores: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.append("## Per-task-type results\n")
    lines.append("| task_type | n | mean |")
    lines.append("|-----------|---|------|")
    per_item = scores.get("per_item", [])
    task_counts: dict[str, int] = {}
    for row in per_item:
        task_counts[row["task_type"]] = task_counts.get(row["task_type"], 0) + 1
    for tt, mean_val in sorted(scores.get("per_task_type", {}).items()):
        n = task_counts.get(tt, 0)
        lines.append(f"| {tt} | {n} | {mean_val:.3f} |")

    lines.append("")
    lines.append("## Per-domain results\n")
    lines.append("| domain | n | mean |")
    lines.append("|--------|---|------|")
    domain_counts: dict[str, int] = {}
    for row in per_item:
        domain_counts[row["domain"]] = domain_counts.get(row["domain"], 0) + 1
    for domain, mean_val in sorted(scores.get("per_domain", {}).items()):
        n = domain_counts.get(domain, 0)
        lines.append(f"| {domain} | {n} | {mean_val:.3f} |")

    lines.append("")
    overall = scores.get("overall", 0.0)
    n_total = len(per_item)
    lines.append(f"overall: {overall:.3f} (n={n_total})")

    return "\n".join(lines)
