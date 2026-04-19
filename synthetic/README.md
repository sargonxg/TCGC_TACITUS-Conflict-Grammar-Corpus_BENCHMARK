# Synthetic Item Generation

This directory contains tooling for generating synthetic TCGC items using LLMs guided by the Agentic Conflict Ontology.

## Why synthetic data?

- Scales corpus without expensive human annotation for every item
- Enables controlled variation (domain, task type, actor count, modality)
- Human review + IAA still required before items enter `items/`

## Pipeline

```
templates/  →  scripts/generate.py  →  generated/  →  human review  →  items/
```

1. **Templates** (`templates/`) — Jinja2 prompt templates per task type
2. **Generate** — LLM generates candidate items from templates
3. **Review** — human annotator validates primitives, edges, provenance
4. **Promote** — approved items moved to `items/` and validated with `tcgc validate`

## Quickstart

```bash
export ANTHROPIC_API_KEY=sk-...
python synthetic/scripts/generate.py \
  --task-type commitment-tracking \
  --domain workplace \
  --count 5 \
  --out synthetic/generated/
```

Then review each generated item and run:
```bash
tcgc validate synthetic/generated/
```

## Quality controls

- All generated items pass `tcgc validate` before human review
- Human annotators score IAA on a random 20% sample
- Items with κ < 0.70 are revised or discarded
- No synthetic item enters `items/` without at least one human review pass

## Template format

Templates are Jinja2 with variables: `{{ task_type }}`, `{{ domain }}`, `{{ actor_count }}`, `{{ modality }}`.
