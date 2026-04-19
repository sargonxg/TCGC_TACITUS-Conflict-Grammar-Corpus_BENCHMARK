"""Tests for tcgc.io."""

from __future__ import annotations

from pathlib import Path

import pytest

from tcgc.io import dump_json, load_item, load_items, read_predictions, write_predictions


def test_load_item(sample_items_dir: Path) -> None:
    item = load_item(sample_items_dir / "tcgc-0001.json")
    assert item["id"] == "tcgc-0001"


def test_load_items_dir(sample_items_dir: Path) -> None:
    items = list(load_items(sample_items_dir))
    assert len(items) == 5
    ids = [item["id"] for _, item in items]
    assert "tcgc-0001" in ids


def test_load_items_single_file(sample_items_dir: Path) -> None:
    items = list(load_items(sample_items_dir / "tcgc-0001.json"))
    assert len(items) == 1


def test_load_items_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        list(load_items(tmp_path / "nonexistent"))


def test_write_read_predictions_roundtrip(tmp_path: Path) -> None:
    preds = [{"id": "tcgc-0001", "value": 1.0}, {"id": "tcgc-0002", "value": 0.5}]
    out = tmp_path / "preds.jsonl"
    write_predictions(preds, out)
    result = list(read_predictions(out))
    assert len(result) == 2
    assert result[0]["id"] == "tcgc-0001"
    assert result[1]["value"] == 0.5


def test_dump_json(tmp_path: Path) -> None:
    obj = {"b": 2, "a": 1}
    out = tmp_path / "out.json"
    dump_json(obj, out)
    import json

    loaded = json.loads(out.read_text())
    assert loaded == obj
