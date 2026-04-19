# TCGC — TACITUS Conflict Grammar Corpus

The TCGC is an open benchmark for evaluating AI systems on conflict-analysis tasks. It measures what generic RAG systems fail at: commitment tracking, causal ordering, interest/position separation, provenance attribution, and narrative drift.

Items are short, structured, and scored against a typed subgraph — not free text. Every extracted primitive must cite its source span.

## What's in this repo

| Resource | Path | Description |
|----------|------|-------------|
| JSON Schema | `schema/tcgc-v0.1.json` | Canonical item shape |
| Sample items | `items/v0.1-sample/` | 5 public items |
| Harness | `tcgc/` | Python package |
| CLI | `tcgc validate`, `tcgc score` | Validation and scoring |
| Adapters | `tcgc/adapters/` | HELM and lm-eval |

## Pages

- [Quickstart](quickstart.md) — run your first evaluation in 5 minutes
- [Task types](task-types.md) — all 14 task definitions
- [Domains](domains.md) — 7 conflict domains
- [Metrics](metrics.md) — 5 scoring functions
- [Methodology](methodology.md) — annotation protocol
- [Submission guide](submission-guide.md) — submit to the leaderboard
- [Leaderboard](leaderboard.md) — current standings
- [Roadmap](roadmap.md) — what's coming

**Homepage:** <https://www.tacitus.me/research/tcgc>
