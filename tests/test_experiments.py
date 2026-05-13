"""Smoke tests for the experiments/llm_vs_typed/ harness using the echo client."""
from __future__ import annotations

import json
from pathlib import Path

from experiments.llm_vs_typed.clients import build_client
from experiments.llm_vs_typed.compare import _count_ops, _try_parse_jsonl, load_pair, render_markdown
from experiments.llm_vs_typed.orchestrate import main as orchestrate_main
from experiments.llm_vs_typed.runner import run_one, write_record


def _load_sample_item() -> dict:
    p = Path(__file__).parent.parent / "items" / "v0.1-sample" / "tcgc-0001.json"
    return json.loads(p.read_text(encoding="utf-8"))


def test_build_echo_client() -> None:
    client = build_client("echo")
    assert client.name == "echo"
    assert client.model == "echo"


def test_run_one_with_echo_vanilla(tmp_path: Path) -> None:
    item = _load_sample_item()
    client = build_client("echo")
    record = run_one(item, client, "vanilla")
    assert record.item_id == "tcgc-0001"
    assert record.mode == "vanilla"
    assert record.api_call_made is False
    assert record.prompt_hash  # non-empty
    assert record.response_hash  # non-empty
    out = write_record(record, tmp_path)
    assert out.exists()
    assert json.loads(out.read_text(encoding="utf-8"))["item_id"] == "tcgc-0001"


def test_run_one_with_echo_typed() -> None:
    item = _load_sample_item()
    client = build_client("echo")
    record = run_one(item, client, "typed")
    assert record.mode == "typed"
    assert record.response_text  # echo client returns deterministic text


def test_jsonl_parser_counts() -> None:
    text = """
    {"op":"CREATE","node":{"id":"a","type":"actor","provenance":"doc1"}}
    {"op":"CREATE","node":{"id":"i","type":"interest","derivation":["c1"],"provenance":"doc1"}}
    {"op":"CREATE","edge":{"from":"a","to":"b","type":"CAUSES","attributes":{"mechanism":"M","conditions":"C"},"provenance":"doc1"}}
    {"op":"CREATE","edge":{"from":"a","to":"c","type":"CONTRADICTS","attributes":{"materiality":"material"},"provenance":"doc1"}}
    not json
    """.strip()
    ops, errors = _try_parse_jsonl(text)
    assert errors == 1
    counts = _count_ops(ops)
    assert counts["total"] == 4
    assert counts["create_node"] == 2
    assert counts["create_edge"] == 2
    assert counts["with_provenance"] == 4
    assert counts["causes_with_mechanism"] == 1
    assert counts["contradicts_with_materiality"] == 1
    assert counts["interests_with_derivation"] == 1


def test_orchestrate_dry_run(tmp_path: Path, capsys) -> None:
    out_dir = tmp_path / "echo-run"
    items_glob = Path(__file__).parent.parent / "items" / "v0.1-sample" / "tcgc-0001.json"
    exit_code = orchestrate_main([
        "--client", "echo",
        "--items", str(items_glob),
        "--out-dir", str(out_dir),
    ])
    assert exit_code == 0
    assert (out_dir / "tcgc-0001__vanilla.json").exists()
    assert (out_dir / "tcgc-0001__typed.json").exists()


def test_orchestrate_report(tmp_path: Path) -> None:
    # First run a small dry-run.
    out_dir = tmp_path / "echo-run"
    items_glob = Path(__file__).parent.parent / "items" / "v0.1-sample" / "tcgc-0001.json"
    orchestrate_main([
        "--client", "echo",
        "--items", str(items_glob),
        "--out-dir", str(out_dir),
    ])
    # Then produce a report.
    exit_code = orchestrate_main(["--report", str(out_dir)])
    assert exit_code == 0
    report = out_dir / "REPORT.md"
    assert report.exists()
    body = report.read_text(encoding="utf-8")
    assert "tcgc-0001" in body
    assert "Vanilla output" in body
    assert "Typed output" in body


def test_load_pair_roundtrip(tmp_path: Path) -> None:
    item = _load_sample_item()
    client = build_client("echo")
    write_record(run_one(item, client, "vanilla"), tmp_path)
    write_record(run_one(item, client, "typed"), tmp_path)
    vanilla, typed = load_pair("tcgc-0001", tmp_path)
    assert vanilla.mode == "vanilla"
    assert typed.mode == "typed"
    # Render markdown doesn't blow up on echo content.
    md = render_markdown("tcgc-0001", vanilla, typed, item)
    assert "tcgc-0001" in md
    assert "Vanilla output" in md
