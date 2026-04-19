# TCGC — TACITUS Conflict Grammar Corpus

*An open benchmark for conflict reasoning, grounded in the Agentic Conflict Ontology.*

**Version** `v0.1-sample` (public) · **Full** in development · **Homepage** <https://www.tacitus.me/research/tcgc>

The TCGC measures what generic language models fail at in the conflict-analysis setting — time, causality, provenance, commitment tracking, interest/position separation, narrative drift. Items are short, structured, and scored on a typed subgraph, not on free text. Every extracted primitive must cite the source span it came from.

This repository ships: the JSON Schema (`schema/tcgc-v0.1.json`), five public sample items (`items/v0.1-sample/`), a reference harness (`tcgc/`), a CLI (`tcgc`), and adapters for HELM and `lm-evaluation-harness`. The full corpus (~480+ items) is under the Data Use Agreement.

## Quickstart

    git clone https://github.com/tacitus-me/tcgc && cd tcgc
    pip install -e '.[dev]'
    tcgc validate items/v0.1-sample/
    tcgc schema --version v0.1 | jq .
    tcgc score predictions.jsonl items/v0.1-sample/ --out scores.json
    tcgc report scores.json

## Task types and metrics

14 task types, 7 domains, 5 metrics. Per-task numbers are reported separately; no single headline score. See `docs/task-types.md`, `docs/domains.md`, `docs/metrics.md`.

## Submit

Fork, add `predictions.jsonl` and `SYSTEM_CARD.md` under `submissions/<name>/<date>/`, open a PR. The leaderboard workflow re-runs your predictions against the canonical scorer and posts the table back on the PR. Alternatively: email the per-metric CSV plus system card to <hello@tacitus.me>.

## Cite

See `CITATION.cff`. Full BibTeX in the dataset paper (Q4 2026, forthcoming).

## License

- Sample items and harness: CC-BY-NC-SA 4.0 (`LICENSE`).
- Full corpus: `DATA_USE_AGREEMENT.md`.

---

*Maintainer: Giulio Catanzariti · <giuliocatanzariti@gmail.com> · Building in public · NYC*
*TACITUS — making conflict legible. Member of Google Cloud for Startups · Neo4j · Databricks.*
