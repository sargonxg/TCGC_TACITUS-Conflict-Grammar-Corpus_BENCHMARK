# `experiments/llm_vs_typed/` — reproducible benchmark harness

This is the concrete, runnable harness for producing real **vanilla-vs-typed** comparisons against TCGC items. It is provider-agnostic (Anthropic, OpenAI, plus an `echo` no-op client for CI), deterministic (T=0 by default, prompt + response hashes recorded), and structured so that **every run is reproducible from a single command**.

The harness is what closes the gap between the qualitative comparisons in `RESULTS.md` and a real first leaderboard row. The output of a single command (`tcgc-experiment ...`) is a directory of records plus a `REPORT.md` you can drop into a PR or share with a reviewer.

---

## What it does

For every item you point it at, the harness runs the **same model** twice:

1. **Vanilla mode** — the model is given the passage(s) and the analyst question with a normal chat prompt. It returns prose.
2. **Typed mode** — the model is given the passage(s), the analyst question, **and the ACO schema** with hard rules (every primitive cites a span; `CAUSES` requires `mechanism`+`conditions`; `CONTRADICTS` requires `materiality`+`rationale`; etc.). It returns JSON Lines of typed graph operations.

Each call captures: model id, temperature, elapsed ms, prompt SHA-256 (first 16 hex chars), response SHA-256, timestamp, and whether an API call was actually made (the echo client says `false`, real clients say `true`). All of that lands in a per-item JSON record.

After the run, `--report` produces a side-by-side `REPORT.md` with:

- Run provenance for both modes.
- The full vanilla prose response.
- The parsed typed JSON Lines + counts (CREATE nodes, CREATE edges, with-provenance, CAUSES-with-mechanism, CONTRADICTS-with-materiality, interests-with-derivation).
- The gold reference counts.
- A "diff signal" table — **shape diagnostics, not benchmark scores**.

To produce the real benchmark scores (`graph_overlap`, `provenance_f1`, `kendall_tau`, etc.), you take the typed-mode output, parse it into a `predictions.jsonl` in TCGC's prediction format, and run `tcgc score`. That conversion step is intentionally a separate piece of work — it is where the "system" of the submission lives, and we publish each submission's converter alongside its system card.

---

## Layout

```
experiments/llm_vs_typed/
├── README.md                # this file
├── __init__.py
├── prompts/
│   ├── vanilla.txt          # the vanilla chat prompt template
│   └── typed.txt            # the typed-extraction prompt with ACO contract
├── clients/
│   ├── __init__.py          # build_client("anthropic:<model>") factory
│   ├── base.py              # ModelClient Protocol + ModelResponse dataclass
│   ├── echo_client.py       # deterministic no-op for CI / dry runs
│   ├── anthropic_client.py  # Anthropic SDK wrapper
│   └── openai_client.py     # OpenAI SDK wrapper
├── runner.py                # run_one(item, client, mode) -> RunRecord
├── compare.py               # parse + count typed ops, render side-by-side md
└── orchestrate.py           # CLI: tcgc-experiment
```

---

## Quickstart

### 1. Dry run — verify the harness end-to-end with no API spend

```bash
pip install -e '.[dev]'

python -m experiments.llm_vs_typed.orchestrate \
    --client echo \
    --items items/v0.2-public-domain/ \
    --out-dir runs/echo-smoke
```

This produces `runs/echo-smoke/tcgc-NNNN__{vanilla,typed}.json` for every item, with `api_call_made=false`. Use it in CI and before any paid run to make sure your wiring is right.

### 2. Real run — Anthropic, single item

```bash
pip install -e '.[experiments]'   # adds the SDK extras
export ANTHROPIC_API_KEY=sk-ant-...

python -m experiments.llm_vs_typed.orchestrate \
    --client anthropic:claude-opus-4-7 \
    --items items/v0.2-public-domain/tcgc-0010.json \
    --out-dir runs/anthropic-claude-opus-4-7-melian
```

### 3. Full sweep — every item under `items/`

```bash
python -m experiments.llm_vs_typed.orchestrate \
    --client anthropic:claude-opus-4-7 \
    --items items/ \
    --out-dir runs/anthropic-claude-opus-4-7-$(date -u +%Y%m%dT%H%M%SZ)
```

Expect roughly **2 API calls per item** (vanilla + typed). At current pricing, the full corpus (11 items as of this writing) costs in the low single-digit USD per model.

### 4. Produce the side-by-side `REPORT.md`

```bash
python -m experiments.llm_vs_typed.orchestrate \
    --report runs/anthropic-claude-opus-4-7-melian
```

This writes `runs/<run-id>/REPORT.md`. Open in a markdown viewer or commit alongside a submission.

---

## What the records look like

Per item, per mode, a record is a JSON file like this:

```jsonc
{
  "item_id": "tcgc-0010",
  "task_type": "leverage-mapping",
  "domain": "diplomatic",
  "mode": "typed",
  "client_name": "anthropic",
  "model": "claude-opus-4-7",
  "temperature": 0.0,
  "elapsed_ms": 5832,
  "api_call_made": true,
  "prompt_hash": "0c2a9b1f4e8d7e6a",
  "response_hash": "f4b8e1d9a3c5b7e2",
  "response_text": "{ \"op\":\"CREATE\", \"node\": ... } ...",
  "error": null,
  "timestamp": "2026-05-13T18:22:14+00:00"
}
```

Every field is there so that a reviewer six months later can reproduce the run or verify that it has not been silently re-run with a different prompt.

---

## Honesty about what this harness is and is not

**What this harness IS**

- A way to produce the **same model on the same passage in two different surface contracts**, deterministically, with full provenance.
- A way to count **shape signals** — did the typed output cite spans, did `CAUSES` carry a `mechanism`, did `CONTRADICTS` carry a `materiality` — without claiming a score.
- A way to make the qualitative comparisons in `RESULTS.md` actually reproducible by anyone with an API key.

**What this harness IS NOT**

- A benchmark scorer. The scorer lives in `tcgc/scoring/`. To produce real graph_overlap / provenance_f1 / kendall_tau numbers, you take the typed-mode output, convert it to a TCGC prediction (the conversion is small but submission-specific), and run `tcgc score`.
- An evaluation of "PRAXIS" or any product. It is a comparison of two prompt surfaces against the same base model. PRAXIS the product wraps a typed pipeline like this one with retrieval, validation, the seven-graph engine, and a UI; the harness here only measures the prompt-surface delta.
- A claim that the typed surface is "better." It is a claim that the typed surface is **structurally different** in measurable ways, and that for downstream institutional use (audit, retrospective review, dashboards, mediator handoff) the difference matters.

---

## Cost discipline

The harness is small but the API bill is real. Best practices:

- **Always smoke with `--client echo` first.** It produces records with `api_call_made=false` so you can shake out path bugs without spending tokens.
- **Run one item before sweeping all of them.** `--items items/v0.2-public-domain/tcgc-0010.json` is one item; `--items items/` is the whole corpus.
- **Temperature 0 is the default.** Increase only when you are characterising variance, and then run at least 3 times per item.
- **Hash prompts.** Two runs with the same `prompt_hash` should be byte-identical; if they are not, your wiring is non-deterministic and the comparison is invalid.

---

## Wiring a new provider

Implement the `ModelClient` Protocol in `clients/base.py` and register it in `clients/__init__.py::build_client`. The contract is one method:

```python
def complete(self, system: str, user: str, *, temperature: float = 0.0) -> ModelResponse: ...
```

The factory accepts a spec like `myprovider:<model-id>`. Open a PR; we will review it.

---

## Path to the first measured leaderboard row

1. Wire a provider (you, with an API key).
2. Run `tcgc-experiment --client <provider>:<model> --items items/ --out-dir runs/<run-id>`.
3. Convert the typed-mode outputs into a TCGC `predictions.jsonl`. The mapping is straightforward for items whose `task_type` lives natively in the typed graph (e.g. `leverage-mapping`, `commitment-tracking`, `contradiction-detection`). For `event-ordering`, populate `order` from the `PRECEDES` chain. For `provenance-attribution`, lift the `(primitive_id, provenance)` pairs directly.
4. Run `tcgc score predictions.jsonl items/ --out scores.json`; `tcgc report scores.json`; `tcgc card scores.json --out SYSTEM_CARD.md`.
5. Open a PR under `submissions/<system>/<date>/` with `predictions.jsonl`, `SYSTEM_CARD.md`, and the `runs/<run-id>/REPORT.md` from the experiment.

The leaderboard CI re-runs the canonical scorer and posts the per-task-type table back as a PR comment. Your numbers become the first measured row.

---

*Maintainer: Giulio Catanzariti · `giuliocatanzariti@gmail.com` · TACITUS · NYC*
