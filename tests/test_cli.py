"""Tests for tcgc.cli via typer.testing.CliRunner."""
from __future__ import annotations
import json
from pathlib import Path
import pytest
from typer.testing import CliRunner
from tcgc.cli import app

runner = CliRunner()


def test_validate_sample_items_exits_0(sample_items_dir: Path) -> None:
    result = runner.invoke(app, ["validate", str(sample_items_dir)])
    assert result.exit_code == 0, result.output


def test_validate_single_item_exits_0(sample_items_dir: Path) -> None:
    result = runner.invoke(app, ["validate", str(sample_items_dir / "tcgc-0001.json")])
    assert result.exit_code == 0, result.output


def test_validate_json_format(sample_items_dir: Path) -> None:
    result = runner.invoke(app, ["validate", str(sample_items_dir), "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["ok"] is True


def test_schema_command() -> None:
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "TACITUS Conflict Grammar Corpus item" in data["title"]


def test_schema_missing_version() -> None:
    result = runner.invoke(app, ["schema", "--version", "v99.0"])
    assert result.exit_code == 1


def test_score_command(sample_items_dir: Path, tmp_path: Path) -> None:
    preds_path = tmp_path / "pred.jsonl"
    out_path = tmp_path / "scores.json"
    preds = []
    for p in sorted(sample_items_dir.rglob("tcgc-*.json")):
        item = json.loads(p.read_text())
        pred = {"id": item["id"]}
        pred.update(item["gold"])
        preds.append(json.dumps(pred))
    preds_path.write_text("\n".join(preds))
    result = runner.invoke(app, ["score", str(preds_path), str(sample_items_dir), "--out", str(out_path)])
    assert result.exit_code == 0, result.output
    scores = json.loads(out_path.read_text())
    assert "per_item" in scores
    assert "overall" in scores


def test_report_command(sample_items_dir: Path, tmp_path: Path) -> None:
    scores_data = {
        "per_item": [{"task_type": "commitment-tracking", "domain": "workplace", "value": 1.0}],
        "per_task_type": {"commitment-tracking": 1.0},
        "per_domain": {"workplace": 1.0},
        "overall": 1.0,
    }
    scores_path = tmp_path / "scores.json"
    scores_path.write_text(json.dumps(scores_data))
    result = runner.invoke(app, ["report", str(scores_path)])
    assert result.exit_code == 0
    assert "overall" in result.output


def test_card_command(tmp_path: Path) -> None:
    scores_data = {
        "per_item": [{"task_type": "commitment-tracking", "domain": "workplace", "value": 1.0}],
        "per_task_type": {"commitment-tracking": 1.0},
        "per_domain": {"workplace": 1.0},
        "overall": 1.0,
    }
    scores_path = tmp_path / "scores.json"
    scores_path.write_text(json.dumps(scores_data))
    out_path = tmp_path / "card.md"
    result = runner.invoke(app, ["card", str(scores_path), "--out", str(out_path)])
    assert result.exit_code == 0
    card_text = out_path.read_text()
    assert "SYSTEM_CARD" in card_text
    assert "overall" in card_text


def test_score_no_prediction(sample_items_dir: Path, tmp_path: Path) -> None:
    preds_path = tmp_path / "empty.jsonl"
    preds_path.write_text("")
    out_path = tmp_path / "scores.json"
    result = runner.invoke(app, ["score", str(preds_path), str(sample_items_dir), "--out", str(out_path)])
    assert result.exit_code == 0
    scores = json.loads(out_path.read_text())
    assert scores["overall"] == pytest.approx(0.0)
