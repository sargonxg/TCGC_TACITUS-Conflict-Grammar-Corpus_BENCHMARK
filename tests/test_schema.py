"""Tests for schema validity and sample item conformance."""
from __future__ import annotations
from pathlib import Path
import pytest
import jsonschema
from tcgc.validate import load_schema
from tcgc.io import load_item


def test_schema_well_formed() -> None:
    schema = load_schema()
    jsonschema.Draft202012Validator.check_schema(schema)


def test_all_sample_items_conform_to_schema(sample_items_dir: Path) -> None:
    schema = load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    for p in sorted(sample_items_dir.rglob("tcgc-*.json")):
        item = load_item(p)
        errors = list(validator.iter_errors(item))
        assert not errors, f"{p.name}: {[e.message for e in errors]}"


@pytest.mark.parametrize("filename", [
    "tcgc-0001.json",
    "tcgc-0002.json",
    "tcgc-0003.json",
    "tcgc-0004.json",
    "tcgc-0005.json",
])
def test_each_item_individually(sample_items_dir: Path, filename: str) -> None:
    schema = load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    item = load_item(sample_items_dir / filename)
    errors = list(validator.iter_errors(item))
    assert not errors, f"{filename}: {[e.message for e in errors]}"
