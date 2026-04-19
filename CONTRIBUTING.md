# Contributing to TCGC

## Tier 01 — Run v0.1 sample

Run any system over the five public sample items and submit your results:

1. Install the harness: `pip install -e '.[dev]'`
2. Run your system over `items/v0.1-sample/` and produce a `predictions.jsonl` (one JSON object per line, each with an `id` field matching the item).
3. Score: `tcgc score predictions.jsonl items/v0.1-sample/ --out scores.json`
4. Generate a system card: `tcgc card scores.json --out SYSTEM_CARD.md` and fill in the placeholders.
5. Submit via PR: fork this repo, add your files under `submissions/<your-system-name>/<date>/`, and open a pull request. The leaderboard CI will re-score and post results back on the PR.
6. Alternatively, email `predictions.jsonl` and `SYSTEM_CARD.md` to `hello@tacitus.me`.

## Tier 02 — Read the protocol

Before proposing changes to task definitions, metrics, or the ontology, read:
- `docs/methodology.md` — three-pass annotation protocol
- `docs/task-types.md` — all 14 task type definitions

Open an issue to discuss. The ontology is locked for v0.1; changes go into the v0.2 roadmap.

## Tier 03 — Request full-corpus access

The full corpus (~480+ items) is under a Data Use Agreement. See `DATA_USE_AGREEMENT.md` and email `hello@tacitus.me` with your institution and intended use.

## Tier 04 — Propose a new task type

Use the `.github/ISSUE_TEMPLATE/task_type_proposal.yml` template. Include:
- Motivation (one paragraph)
- A worked example item in TCGC JSON format
- The proposed metric and rationale
- Domain(s) covered

## Developer setup

```bash
git clone https://github.com/tacitus-me/tcgc
cd tcgc
pip install -e '.[dev]'
pre-commit install
pytest -q --cov=tcgc --cov-fail-under=90
tcgc validate items/v0.1-sample/
```

Commits must follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`).
