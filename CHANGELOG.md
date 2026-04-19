# Changelog

All notable changes to the TCGC harness and sample are documented here.
The format is based on Keep a Changelog; the project adheres to Semantic Versioning.

## [0.1.0] — 2026-04-18

### Added
- Initial public release of the v0.1-sample (5 items).
- Canonical JSON Schema (`schema/tcgc-v0.1.json`).
- ACO ontology module (8 primitives, 18 edge types, partial-credit similarity).
- Five reference scorers (`graph_overlap`, `provenance_f1`, `kendall_tau`, `contradiction_pair_f1`, `llm_judge_anchored`).
- `tcgc` CLI: `validate`, `schema`, `run`, `score`, `report`, `card`, `manifest`.
- HELM and lm-evaluation-harness adapters.
- mkdocs-material documentation scaffold.
- 20-entry calibration anchor set for the LLM judge.
- GitHub Actions workflows for CI, release, and leaderboard intake.
