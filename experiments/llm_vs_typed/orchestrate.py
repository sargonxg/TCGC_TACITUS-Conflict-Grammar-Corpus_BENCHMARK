"""CLI orchestrator: run vanilla + typed against TCGC items and emit a report.

Usage examples
--------------

    # Dry run (no API calls). Verifies the wiring works.
    python -m experiments.llm_vs_typed.orchestrate \\
        --client echo \\
        --items items/v0.2-public-domain/ \\
        --out-dir runs/echo-$(date -u +%Y%m%dT%H%M%SZ)

    # Real Anthropic run, single item.
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m experiments.llm_vs_typed.orchestrate \\
        --client anthropic:claude-opus-4-7 \\
        --items items/v0.2-public-domain/tcgc-0010.json \\
        --out-dir runs/anthropic-claude-opus-4-7-$(date -u +%Y%m%dT%H%M%SZ)

    # Real OpenAI run, every item.
    export OPENAI_API_KEY=sk-...
    python -m experiments.llm_vs_typed.orchestrate \\
        --client openai:gpt-5 \\
        --items items/ \\
        --out-dir runs/openai-gpt-5-$(date -u +%Y%m%dT%H%M%SZ)

    # Produce a side-by-side markdown report from an existing run dir.
    python -m experiments.llm_vs_typed.orchestrate \\
        --report runs/anthropic-claude-opus-4-7-20260513T180000Z

Conventions
-----------

- Output dir layout: `runs/<run-id>/{tcgc-NNNN__vanilla.json, tcgc-NNNN__typed.json}` plus
  a `REPORT.md` after `--report` is run.
- Every record carries: model id, temperature, elapsed ms, prompt hash, response hash,
  timestamp, and whether an API call was actually made.
- `--client echo` makes no API calls and produces deterministic placeholders. Use it in
  CI and for smoke-testing your runner before you spend tokens.
- The orchestrator NEVER edits files outside `--out-dir`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from experiments.llm_vs_typed.clients import build_client
from experiments.llm_vs_typed.compare import load_pair, render_markdown
from experiments.llm_vs_typed.runner import run_one, write_record


def _iter_items(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(p for p in path.rglob("tcgc-*.json"))


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tcgc-experiment", description="Run vanilla + typed against TCGC items."
    )
    parser.add_argument(
        "--client",
        default="echo",
        help="Client spec: 'echo' | 'anthropic:<model>' | 'openai:<model>'.",
    )
    parser.add_argument("--items", type=Path, default=Path("items"), help="Item file or directory.")
    parser.add_argument(
        "--out-dir", type=Path, help="Where to write per-item records and the REPORT.md."
    )
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--report", type=Path, help="Skip the run; produce REPORT.md from an existing run dir."
    )
    args = parser.parse_args(argv)

    if args.report:
        run_dir: Path = args.report
        items = sorted({p.stem.split("__")[0] for p in run_dir.glob("tcgc-*__*.json")})
        if not items:
            print(f"No run records found in {run_dir}", file=sys.stderr)
            return 2
        # Gold items live under items/; for the report we need the gold JSON.
        report_md = [
            "# Experiment report — `" + run_dir.name + "`",
            "",
            "Side-by-side vanilla vs typed comparison across the items in this run.",
            "All counts in this report are SHAPE DIAGNOSTICS, not benchmark scores.",
            "",
        ]
        for item_id in items:
            try:
                vanilla, typed = load_pair(item_id, run_dir)
            except FileNotFoundError as exc:
                report_md.append(f"## `{item_id}` — incomplete run\n\n> {exc}\n")
                continue
            gold_candidates = list(Path("items").rglob(f"{item_id}.json"))
            if not gold_candidates:
                report_md.append(f"## `{item_id}` — gold not found under items/\n")
                continue
            gold = _load(gold_candidates[0])
            report_md.append(render_markdown(item_id, vanilla, typed, gold))
            report_md.append("\n---\n")
        out = run_dir / "REPORT.md"
        out.write_text("\n".join(report_md), encoding="utf-8")
        print(f"Wrote {out}")
        return 0

    if not args.out_dir:
        parser.error("--out-dir is required unless --report is passed.")

    client = build_client(args.client)
    api_warning_shown = False
    if args.client == "echo":
        print(
            "[info] Using echo client. No API calls will be made. "
            "Use --client anthropic:<model> or openai:<model> for measured runs."
        )
        api_warning_shown = True

    paths = _iter_items(args.items)
    if not paths:
        print(f"No items found at {args.items}", file=sys.stderr)
        return 2

    total = len(paths) * 2  # vanilla + typed per item
    done = 0
    for item_path in paths:
        item = _load(item_path)
        for mode in ("vanilla", "typed"):
            done += 1
            print(
                f"[{done:>3}/{total}] {item['id']} :: {mode} ({client.name}:{client.model}) …",
                end=" ",
                flush=True,
            )
            record = run_one(item, client, mode, temperature=args.temperature)
            write_record(record, args.out_dir)
            tag = "ERR" if record.error else "OK"
            print(f"{tag} ({record.elapsed_ms} ms)")

    # Echo client gets a tip; real runs get an end-of-run note.
    if not api_warning_shown:
        print("[info] Records written. Run with `--report` to produce REPORT.md.")
    print(f"Done. Records in {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
