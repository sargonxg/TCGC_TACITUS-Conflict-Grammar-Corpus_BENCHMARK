<div align="center">

# TCGC

### TACITUS Conflict Grammar Corpus

**An alpha benchmark and corpus for evaluating structured, source-grounded analysis of conflict and policy text.**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](pyproject.toml)
[![Status](https://img.shields.io/badge/status-alpha-yellow)](RESULTS.md)
[![CI](https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK/actions/workflows/ci.yml)
[![Docs](https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK/actions/workflows/docs.yml)
[![Current license](https://img.shields.io/badge/current%20license-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE)

</div>

---

## 30-second read

- **What it is:** a schema, corpus, scoring toolkit, CLI, adapters, and experiment harness for evaluating typed graph output rather than free-form prose alone.
- **What it evaluates:** actors, claims, interests, constraints, leverage, commitments, events, narratives, contradictions, chronology, and source-span provenance.
- **What exists today:** synthetic and public-domain sample items, validation and scoring code, baseline interfaces, worked examples, and a repeatable experiment scaffold.
- **What does not exist yet:** a published, independently reproducible leaderboard of measured model runs. Illustrative examples are not benchmark results.

TCGC asks a narrow empirical question: **when a system analyzes a complex conflict or policy text, how much of the supported structure does it recover, and can each material object be traced back to evidence?**

## Why typed evaluation?

A fluent answer can omit chronology, merge actors, soften contradictions, or detach a claim from its source while remaining persuasive. TCGC therefore evaluates a structured output surface in which systems must identify objects and relationships explicitly.

The benchmark does not assume that a typed pipeline will outperform a general-purpose model. That is the proposition to be tested. Model scale, prompting, retrieval, schemas, graph layers, and human review should be compared under recorded conditions rather than inferred from worked examples.

## Repository contents

| Asset | Path | Purpose |
| --- | --- | --- |
| Canonical schema | [`schema/tcgc-v0.1.json`](schema/tcgc-v0.1.json) | Item and prediction contract |
| Synthetic samples | [`items/v0.1-sample/`](items/v0.1-sample/) | Small fixtures covering core task types |
| Public-domain samples | [`items/v0.2-public-domain/`](items/v0.2-public-domain/) | Items grounded in stable, redistributable texts |
| Corpus manifests | [`corpora/public-domain/`](corpora/public-domain/) | Source URLs and anchor information |
| Python package | [`tcgc/`](tcgc/) | Validation, scoring, reporting, ontology, and CLI |
| Baseline interfaces | [`baselines/`](baselines/) | Provider and retrieval baselines behind a common surface |
| Adapters | [`tcgc/adapters/`](tcgc/adapters/) | Evaluation-framework integration |
| Experiment harness | [`experiments/llm_vs_typed/`](experiments/llm_vs_typed/) | Same-item, same-model comparison workflow |
| Worked examples | [`examples/llm-vs-praxis/`](examples/llm-vs-praxis/) | Illustrative output shapes, not measured results |
| Evidence statement | [`RESULTS.md`](RESULTS.md) | Current result boundary and publication requirements |

## Quick start

```bash
git clone https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK.git tcgc
cd tcgc
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e '.[dev]'

# Validate corpus items.
tcgc validate items/

# Inspect the canonical schema.
tcgc schema --version v0.1 | jq .

# Run a system that implements the documented prediction interface.
tcgc run --system mypkg.runner:predict items/v0.1-sample/ --out predictions.jsonl

# Score and report.
tcgc score predictions.jsonl items/v0.1-sample/ --out scores.json
tcgc report scores.json
```

No paid API is required for validation, scoring, or the echo/dry-run paths. API-backed experiments remain opt-in.

## Evaluation surface

TCGC organizes tasks around five broad capabilities:

1. **Entity and role structure:** actor resolution, claim extraction, interest/position separation, constraints, and leverage.
2. **Time and commitment:** event ordering, commitments, status changes, and commitment–claim mismatch.
3. **Disagreement and narrative:** contradiction pairs, narrative drift, and competing frames.
4. **Provenance:** exact or near-exact source attribution for claim-bearing objects.
5. **Cross-document structure:** synthesis across partially overlapping or inconsistent sources.

Metrics are reported by task rather than collapsed into a single headline number. Current implementations include typed graph overlap, provenance F1, contradiction-pair F1, Kendall rank correlation for chronology, and an anchored judge surface for tasks that cannot be reduced to exact matching.

Any judge-based metric should be reported separately, with judge model, prompt, anchors, and variance visible. It should not be treated as ground truth.

## Experiment protocol

The experiment harness is designed to run the same underlying model on the same item under two different interfaces, for example:

- a general analysis prompt; and
- a typed output contract with explicit provenance requirements.

A publishable run should retain at least:

- corpus and scorer commit SHAs;
- model and provider identifiers;
- prompts and schema versions;
- raw predictions;
- elapsed time and API settings;
- per-task and per-domain results;
- failure examples; and
- human-review protocol where applicable.

```bash
# No external API call.
make experiment-dry ITEMS=items/v0.2-public-domain/

# Generate a report from a completed run directory.
make experiment-report RUN=runs/<run-id>
```

Provider-specific instructions live in [`experiments/llm_vs_typed/README.md`](experiments/llm_vs_typed/README.md).

## Current evidence boundary

The repository currently demonstrates that a typed evaluation surface can represent distinctions that free prose may leave implicit. It does **not** yet establish the size of any performance gap between frontier models, retrieval systems, graph-augmented systems, or PRAXIS-style pipelines.

Worked examples in `examples/` and `RESULTS.md` are pedagogical. They should not be cited as measured model performance. The first credible leaderboard release requires complete prediction files, scorer version, reproducible commands, and clear separation between synthetic, public-domain, and any later expert-annotated data.

## Corpus design principles

- Every scored object should be supported by a source span or explicitly marked as an inference.
- Gold annotations should permit disagreement and adjudication rather than conceal interpretive choices.
- Public-domain items provide stable redistribution and verification, but they do not substitute for modern domain data.
- Test contamination and pretraining exposure must be discussed rather than assumed away.
- Sensitive real-world cases require data governance, consent, redaction, and domain review.
- Results should be disaggregated by task and domain.

## Limitations

The current corpus is small and does not represent the full diversity of diplomatic, legal, workplace, commercial, family, or peace-process material. Some tasks are inherently interpretive. Source spans can support more than one reasonable graph. Judge-based metrics introduce model dependence. Public-domain texts may be familiar to evaluated models. Synthetic examples may be cleaner than real records. These limitations should remain visible in any reported result.

TCGC should not be used to make decisions about individuals or to claim clinical, legal, mediation, intelligence, or policy validity without appropriate independent evaluation.

## Relationship to TACITUS

- [DIALECTICA](https://github.com/sargonxg/A3_DIALECTICAbyTACITUS_v3) builds reviewable context capsules.
- [AGON](https://github.com/sargonxg/AGON) explores evidence-linked conflict perception.
- [KAIROS](https://github.com/sargonxg/KAIROS-temporal-vision-TACITUS) explores temporal structure.
- **TCGC** provides a public evaluation surface for claims made by those systems and by external baselines.

## Licensing note

The repository is currently distributed under CC BY-NC-SA 4.0; see [LICENSE](LICENSE). Because the repository contains both software and data, a future release should state separately which license governs code, corpus items, annotations, documentation, and third-party source material. No licensing change has been made in this documentation pass.

## Contributing

Issues and pull requests should include the affected task type, schema version, evidence spans, and a reproducible validation or scoring command. Corpus additions should document source rights and annotation procedure.
