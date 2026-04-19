"""Tests for tcgc.validate."""

from __future__ import annotations

from pathlib import Path

import jsonschema

from tcgc.validate import Report, _validate_item, load_schema, validate_path


def _validator() -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(load_schema())


def test_schema_is_valid_draft202012() -> None:
    schema = load_schema()
    jsonschema.Draft202012Validator.check_schema(schema)


def test_all_sample_items_valid(sample_items_dir: Path) -> None:
    report = validate_path(sample_items_dir)
    assert report.ok, "\n".join(report.as_lines())
    assert not report.has_warnings, "\n".join(report.as_lines())


def test_report_ok_property() -> None:
    from tcgc.validate import Issue

    r = Report()
    r.by_path["x"] = []
    assert r.ok
    r.by_path["y"] = [Issue("p", "error", "c", "m")]
    assert not r.ok


def test_report_as_dict() -> None:
    from tcgc.validate import Issue

    r = Report()
    r.by_path["x"] = [Issue("p", "warning", "dangling-node", "msg")]
    d = r.as_dict()
    assert d["ok"] is True
    assert len(d["by_path"]["x"]) == 1


def test_id_shape_error() -> None:
    v = _validator()
    item = {
        "id": "bad-id",
        "task_type": "commitment-tracking",
        "domain": "workplace",
        "inputs": {"messages": [{"from": "A", "text": "hi", "id": "m1"}], "question": "q"},
        "gold": {"primitives": [], "edges": []},
        "rubric": {"scoring": "graph_overlap"},
    }
    issues = _validate_item(item, v)
    # Schema catches the pattern violation; id-shape fires on items that pass schema
    assert any(i.level == "error" for i in issues)


def test_task_metric_mismatch_error() -> None:
    v = _validator()
    item = {
        "id": "tcgc-0099",
        "task_type": "event-ordering",
        "domain": "workplace",
        "inputs": {"messages": [{"from": "A", "text": "hi", "id": "m1"}], "question": "q"},
        "gold": {"primitives": [], "edges": [], "order": []},
        "rubric": {"scoring": "graph_overlap"},
    }
    issues = _validate_item(item, v)
    codes = {i.code for i in issues}
    assert "task-metric-mismatch" in codes


def test_orphan_provenance_error() -> None:
    v = _validator()
    item = {
        "id": "tcgc-0099",
        "task_type": "commitment-tracking",
        "domain": "workplace",
        "inputs": {"messages": [{"from": "A", "text": "hi", "id": "m1"}], "question": "q"},
        "gold": {
            "primitives": [{"id": "n1", "type": "actor", "provenance": "nonexistent"}],
            "edges": [],
        },
        "rubric": {"scoring": "graph_overlap"},
    }
    issues = _validate_item(item, v)
    codes = {i.code for i in issues}
    assert "orphan-provenance" in codes


def test_edge_endpoint_error() -> None:
    v = _validator()
    item = {
        "id": "tcgc-0099",
        "task_type": "commitment-tracking",
        "domain": "workplace",
        "inputs": {"messages": [{"from": "A", "text": "hi", "id": "m1"}], "question": "q"},
        "gold": {
            "primitives": [{"id": "n1", "type": "actor", "provenance": "m1"}],
            "edges": [{"from": "n1", "to": "missing", "type": "ASSERTED", "provenance": "m1"}],
        },
        "rubric": {"scoring": "graph_overlap"},
    }
    issues = _validate_item(item, v)
    codes = {i.code for i in issues}
    assert "edge-endpoint" in codes


def test_dangling_node_warning() -> None:
    v = _validator()
    item = {
        "id": "tcgc-0099",
        "task_type": "commitment-tracking",
        "domain": "workplace",
        "inputs": {"messages": [{"from": "A", "text": "hi", "id": "m1"}], "question": "q"},
        "gold": {
            "primitives": [
                {"id": "a1", "type": "actor", "provenance": "m1"},
                {"id": "c1", "type": "claim", "provenance": "m1"},
            ],
            "edges": [],
        },
        "rubric": {"scoring": "graph_overlap"},
    }
    issues = _validate_item(item, v)
    codes = {i.code for i in issues}
    assert "dangling-node" in codes


def test_validate_path_single_file(sample_items_dir: Path) -> None:
    p = sample_items_dir / "tcgc-0001.json"
    report = validate_path(p)
    assert report.ok
