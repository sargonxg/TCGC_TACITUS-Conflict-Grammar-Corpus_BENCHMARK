"""Scoring driver — dispatches by rubric.scoring and aggregates."""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
from tcgc.io import load_items, read_predictions
from tcgc.scoring import get as get_scorer


def score_predictions(predictions_path: Path, items_dir: Path) -> dict[str, Any]:
    preds_by_id = {p["id"]: p for p in read_predictions(predictions_path)}
    per_item: list[dict[str, Any]] = []
    for _, item in load_items(items_dir):
        if item["id"] not in preds_by_id:
            per_item.append({"id": item["id"], "task_type": item["task_type"],
                             "domain": item["domain"], "metric": item["rubric"]["scoring"],
                             "value": 0.0, "notes": ["no prediction submitted"]})
            continue
        scorer = get_scorer(item["rubric"]["scoring"])
        r = scorer(item["gold"], preds_by_id[item["id"]])
        per_item.append({
            "id": item["id"], "task_type": item["task_type"], "domain": item["domain"],
            "metric": item["rubric"]["scoring"], "value": float(r.value),
            "components": r.components, "notes": r.notes,
        })
    tb: dict[str, list[float]] = defaultdict(list)
    db: dict[str, list[float]] = defaultdict(list)
    for row in per_item:
        tb[row["task_type"]].append(row["value"])
        db[row["domain"]].append(row["value"])
    return {
        "per_item": per_item,
        "per_task_type": {k: float(mean(v)) for k, v in tb.items()},
        "per_domain":    {k: float(mean(v)) for k, v in db.items()},
        "overall":       float(mean([r["value"] for r in per_item])) if per_item else 0.0,
    }
