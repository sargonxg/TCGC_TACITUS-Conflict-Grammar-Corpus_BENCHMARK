<div align="center">

# TCGC

### The TACITUS Conflict Grammar Corpus

**An open benchmark for *structural* conflict reasoning — grounded in the Agentic Conflict Ontology, scored on the typed subgraph the system actually produces.**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](pyproject.toml)
[![mypy strict](https://img.shields.io/badge/mypy-strict-success.svg)](pyproject.toml)
[![tests](https://img.shields.io/badge/coverage-92%25-brightgreen.svg)](tests/)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![Homepage](https://img.shields.io/badge/Homepage-tacitus.me%2Fresearch%2Ftcgc-00D1B2.svg)](https://www.tacitus.me/research/tcgc)

</div>

---

## What this is

A **benchmark** for whether an AI system can read complex policy, mediation, and conflict texts the way a careful analyst reads them — *as typed structure*, not as paraphrase.

We do not score free prose. We score the **typed subgraph** the system produces against gold: actors, claims, interests, constraints, leverage, commitments, events, narratives, and the typed edges between them. Every primitive must cite the source span it was extracted from. Every commitment is bi-temporal. Every contradiction is a first-class edge — not a smoothed paragraph.

**The thesis.** Generic language models — even at frontier scale — fail on five measurable axes when handed a real conflict, mediation, or policy file: *time, causality, span-level provenance, contradiction handling, long-horizon context.* A larger model patches none of these; they are architectural. TCGC measures the gap directly, on the same models, with and without the typed layer.

---

## What you get from this repo

| Asset | Path | Purpose |
|---|---|---|
| **JSON Schema** (Draft 2020-12) | [`schema/tcgc-v0.1.json`](schema/tcgc-v0.1.json) | Canonical item shape |
| **Sample items (synthetic)** | [`items/v0.1-sample/`](items/v0.1-sample/) | 5 short items spanning 5 task types |
| **Sample items (public-domain corpora)** | [`items/v0.2-public-domain/`](items/v0.2-public-domain/) | 6 items grounded in Thucydides, Federalist Papers, Machiavelli, Caesar, Hobbes |
| **Public-domain corpus manifests** | [`corpora/public-domain/`](corpora/public-domain/) | Project Gutenberg URLs + anchor spans for the v0.2 items |
| **Reference harness** | [`tcgc/`](tcgc/) | Typed Python package: validation, scoring, CLI |
| **CLI** | `tcgc` | `validate`, `score`, `run`, `report`, `card`, `schema` |
| **Adapters** | [`tcgc/adapters/`](tcgc/adapters/) | HELM + `lm-evaluation-harness` |
| **Baselines** | [`baselines/`](baselines/) | Zero-shot OpenAI, Anthropic, vanilla RAG, GraphRAG — same interface |
| **LLM-vs-PRAXIS worked examples** | [`examples/llm-vs-praxis/`](examples/llm-vs-praxis/) | Same passage, same model, two surfaces — see what the typed layer adds |
| **Leaderboard** | [`leaderboard/v0.1-sample.json`](leaderboard/v0.1-sample.json) | Public scorecard, per task type and per domain |

---

## Quickstart (60 seconds)

```bash
git clone https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK tcgc
cd tcgc
pip install -e '.[dev]'

# 1) Confirm every item validates against the schema (structural + semantic).
tcgc validate items/

# 2) Look at the canonical schema in your terminal.
tcgc schema --version v0.1 | jq .

# 3) Run a model and produce a predictions file (replace with your runner).
tcgc run --system mypkg.runner:predict items/v0.1-sample/ --out predictions.jsonl

# 4) Score predictions against gold.
tcgc score predictions.jsonl items/v0.1-sample/ --out scores.json
tcgc report scores.json
```

That's it. No GPUs required. No paid API calls unless your runner needs them. The `llm-judge` metric is gated behind `TCGC_RUN_API=1`.

---

## Early results — illustrative only, not measured yet

[**RESULTS.md**](RESULTS.md) holds three side-by-side comparisons (Melian Dialogue, regulatory commitment mismatch, sanctions causal chain) showing the *target shape* of vanilla-chat output vs the typed-surface output the benchmark would score against. **No model has been run against the harness yet.** The file is intentionally explicit about that: the vanilla paragraphs were hand-written to approximate what a competent chat model would plausibly say; the typed outputs were constructed from the gold subgraphs; and any numbers you read are illustrative, not measured.

The benchmark is built to be falsifiable, not asserted. Formal measured results — with the scorer commit SHA, per-task numbers, per-domain numbers, and the prediction JSONL of every system — are what `v0.2` (Q3 2026) is for. The "How we will produce real measured results" section at the end of `RESULTS.md` lists exactly what has to happen first.

Until then the honest statement is the narrow one in §1 of the white paper and the methodology docs: *the typed surface preserves what the prose surface flattens — time, causality, span provenance, contradiction, position vs interest, commitment vs claim. The magnitude of the gap in any given frontier model is an empirical question, not yet answered.*

If you have API keys and want to produce the first real numbers, see the "Reproducing this honestly" section of `RESULTS.md`. The path is short and the result will be the first leaderboard row.

---

## What it tests, exactly

**14 task types** (v0.1) and **3 dynamic-ontology task types** (v0.2 design freeze Q3 2026):

| # | Task | Metric | What it stresses |
|---|---|---|---|
| 1 | `actor-resolution` | `graph_overlap` | Cross-document alias clusters, role attribution |
| 2 | `claim-extraction` | `graph_overlap` | Speech-act typing under noise |
| 3 | `interest-extraction` | `llm_judge_anchored` | Inferred interests with derivation chains |
| 4 | `constraint-extraction` | `graph_overlap` | Statutory / regulatory / procedural classification |
| 5 | `leverage-mapping` | `graph_overlap` | Mechanism typing (Coercive / Normative / Information / …) |
| 6 | `commitment-tracking` | `graph_overlap` | Status transitions with bi-temporal stamps |
| 7 | `event-ordering` | `kendall_tau` | Chronology reconstruction *with dates stripped* |
| 8 | `narrative-drift` | `llm_judge_anchored` | Reframing across time and framer |
| 9 | `causal-chain` | `graph_overlap` | Multi-hop A→B via mechanism M under condition C |
| 10 | `contradiction-detection` | `contradiction_pair_f1` | Material vs cosmetic disagreement |
| 11 | `provenance-attribution` | `provenance_f1` | Span-exact source binding |
| 12 | `commitment-claim-mismatch` | `graph_overlap` | "Said X, signed Y, did Z" |
| 13 | `position-interest-separation` | `llm_judge_anchored` | Fisher/Ury distinction at the type level |
| 14 | `cross-document-synthesis` | `graph_overlap` | Coherent subgraph from contradictory sources |
| v0.2 — 15 | `schema-extension-induction` | structural | Inducing a per-domain subclass from cases |
| v0.2 — 16 | `kernel-invariant-validation` | structural | Holding parent-primitive invariants under extension |
| v0.2 — 17 | `cross-domain-primitive-transfer` | structural | Same kernel, different domain, transferable primitives |

**7 domains**: workplace, commercial, governance, peace-process, policy, family, diplomatic.

**5 metrics** (per-task, never collapsed into a headline score):

- `graph_overlap` — Jaccard over the typed subgraph with partial-credit on near-miss edge types.
- `provenance_f1` — F1 over `(primitive_id, source_span)` pairs.
- `kendall_tau` — rank correlation against gold chronological order, dates stripped on ~50% of items.
- `contradiction_pair_f1` — material/cosmetic-weighted F1 over `(claim_a, claim_b)` pairs.
- `llm_judge_anchored` — LLM-judge calibrated against a 20-entry human-anchor set.

---

## The novel surface: LLM-only vs PRAXIS-layered, side by side

This is where most readers should start. [`examples/llm-vs-praxis/`](examples/llm-vs-praxis/) holds paired worked examples that run the **same model on the same passage** through:

- **(A) a vanilla chat prompt** — fluent prose response.
- **(B) the PRAXIS-style typed pipeline** — typed graph operations under hard validation.

The first example uses Thucydides' **Melian Dialogue**: a 5th-century BCE negotiation that contains almost every primitive the kernel was designed to capture. Read [`examples/llm-vs-praxis/melian-leverage/diff.md`](examples/llm-vs-praxis/melian-leverage/diff.md) to see, line by line, what the typed layer surfaces that the chat layer flattens.

The pattern repeats with **Federalist No. 10** (position vs interest), **The Prince Chapter VII** (event ordering with implicit causal chain), **Hobbes vs Machiavelli** (cross-document narrative drift on the same primitive), and **Caesar's Gallic War** (multi-tribe actor resolution).

> *These texts are not soft humanities scaffolding.* The Melian Dialogue has more typed structure per paragraph than most modern policy memos. We use them because every modern model has read them — so the benchmark is **not** a memorisation test. It is a *structural-reasoning* test: can the system produce the typed subgraph the source actually supports?

---

## Why the public-domain corpora

| Property | Why it matters |
|---|---|
| **Immutable canonical URLs** | Project Gutenberg URLs do not rotate. Citations stay live. |
| **Free to redistribute** | No DUA blocks reproducibility. |
| **Saturated in pre-training** | The text is in every frontier model. So the benchmark is *not* a recall test. It is a structural-reading test. |
| **Dense in typed primitives** | One Melian paragraph encodes 8+ primitives + 3 contradictions. |
| **Stable across decades of citation conventions** | A reviewer at any institution can verify a span by reading the named chapter. |

**Corpora included so far**:

- [Federalist Papers](corpora/public-domain/federalist-papers.json) — commitments, counter-positions, constitutional negotiation
- [Melian Dialogue (Thucydides V.84–116)](corpora/public-domain/melian-dialogue.json) — leverage asymmetry, ultimatum, commitment breach
- [Leviathan (Hobbes)](corpora/public-domain/leviathan.json) — covenant as commitment-primitive
- [The Prince (Machiavelli)](corpora/public-domain/the-prince.json) — virtù, fortuna, deliberate commitment-breach
- [The Art of War (Sun Tzu)](corpora/public-domain/the-art-of-war.json) — leverage typology, narrative as mechanism
- [Caesar's Gallic War](corpora/public-domain/caesar-gallic-wars.json) — actor disambiguation across tribes

Planned: Aristotle's *Athenian Constitution*, Machiavelli's *Discourses on Livy*, Tacitus' *Annals* (the namesake), Plutarch's *Lives*.

---

## Scoring philosophy

**Per-task reporting only.** No single headline score is published. A system that hits 0.9 on `actor-resolution` and 0.4 on `commitment-claim-mismatch` is not a 0.65 system — those two numbers tell a reviewer two different things about where the system breaks.

**Partial-credit aware on edge types.** The kernel has 18 edge types. Some are near-synonyms (`ASSERTED` vs `ACKNOWLEDGED`) and the scorer gives partial credit on those misses. The similarity matrix is in [`tcgc/ontology/edges.py`](tcgc/ontology/edges.py).

**Materiality-weighted contradictions.** Not every disagreement matters equally. A material contradiction (strategic decision made vs not made) weighs 4× a cosmetic one (agenda timing). Both are surfaced.

**Anchored LLM judge.** For interpretive tasks the judge is calibrated against a 20-entry human-anchor set with isotonic regression. Bias modes (position / verbosity / self-preference) are disclosed in the docstring. Gated behind `TCGC_RUN_API=1`.

---

## How to submit

```bash
# 1. Run the harness against your system.
tcgc run --system yourpkg.runner:predict items/v0.1-sample/ --out predictions.jsonl

# 2. Score locally.
tcgc score predictions.jsonl items/v0.1-sample/ --out scores.json

# 3. Generate the system card.
tcgc card scores.json --out SYSTEM_CARD.md

# 4. Open a PR adding submissions/<your-system>/<date>/{predictions.jsonl, SYSTEM_CARD.md}
```

The leaderboard workflow re-runs your predictions against the canonical scorer in CI and posts the per-task-type table back as a PR comment. The scorer commit SHA is part of every leaderboard row.

Alternative: email per-metric CSV + system card to **hello@tacitus.me**.

See [`docs/submission-guide.md`](docs/submission-guide.md).

---

## Roadmap

- **Q2 2026** — v0.2 specification freeze: 3 dynamic-ontology task types added, target corpus 480+ items (mix of synthetic + public-domain).
- **Q3 2026** — first published baseline scores: vanilla GPT-class, Claude-class, Llama-class, RAG, GraphRAG, OG-RAG, plus the TACITUS layered stack reference, all under the same harness.
- **Q4 2026** — TCGC dataset paper.
- **Q1 2027** — OAG methodology paper (target ACL).
- **Q2 2027** — v0.3: multilingual extension (ES / FR / AR / ZH) + adversarial split.

See [`docs/roadmap.md`](docs/roadmap.md).

---

## Project documents

- [`docs/quickstart.md`](docs/quickstart.md) — beyond the 60-second start.
- [`docs/task-types.md`](docs/task-types.md) — one section per task, with worked mini-example.
- [`docs/metrics.md`](docs/metrics.md) — formulas, edge cases, when each metric misleads.
- [`docs/methodology.md`](docs/methodology.md) — three-pass annotation protocol, IAA targets.
- [`docs/domains.md`](docs/domains.md) — scope statements for the 7 domains.
- [`docs/open-questions.md`](docs/open-questions.md) — what remains unsettled.
- [`DATASHEET.md`](DATASHEET.md) — Gebru et al. (2021) datasheet for the corpus.
- [`DATA_USE_AGREEMENT.md`](DATA_USE_AGREEMENT.md) — terms for full-corpus access.

---

## License

- **Harness + schema + sample items**: [CC BY-NC-SA 4.0](LICENSE).
- **Full corpus**: under DUA. See [`DATA_USE_AGREEMENT.md`](DATA_USE_AGREEMENT.md).
- **Public-domain texts referenced**: Public Domain (Project Gutenberg). We do not redistribute the source bytes; manifests in [`corpora/`](corpora/) carry the canonical URLs.

---

## Citation

```bibtex
@misc{tacitus2026tcgc,
  title  = {TCGC: The TACITUS Conflict Grammar Corpus},
  author = {Catanzariti, Giulio},
  year   = {2026},
  url    = {https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK},
  note   = {Open benchmark for structural conflict reasoning, grounded in the Agentic Conflict Ontology.}
}
```

See [`CITATION.cff`](CITATION.cff).

---

## Maintainer

Giulio Catanzariti · `giuliocatanzariti@gmail.com` · TACITUS · NYC.

Building in public. The harness, the schema, the sample items, and the kernel ontology are CC/MIT-licensed. Issue templates are wired for bug reports, task-type proposals, and submission intake. We read everything.

> **TACITUS — making conflict legible.**
> Member: Google Cloud for Startups · Neo4j · Databricks.
> Homepage: <https://www.tacitus.me/research/tcgc>
