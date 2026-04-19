# Methodology

## Annotation Protocol

TCGC uses a three-pass annotation protocol.

### Pass 1 — Primitive tagging

The lead annotator reads the source material and tags every relevant entity as one of the 8 ACO primitives: actor, claim, interest, constraint, leverage, commitment, event, narrative. Each primitive receives a `provenance` reference pointing at the source span (message id, document id, or `turn:N`).

### Pass 2 — Edge labeling

The same annotator labels directed edges between primitives using the 18 ACO edge types. Every edge must carry a `provenance` reference. Unlabeled edges fail validation.

### Pass 3 — Ground-truth QA

A second annotator reviews the complete item: checks primitive types, edge directions, provenance bindings, and the `rubric.scoring` assignment. Disagreements are resolved by discussion; persistent disagreements are flagged with a lower `inter_annotator_kappa` value.

---

## IAA Targets

| Task type group | Target κ |
|-----------------|----------|
| Graph-scored (graph_overlap, provenance_f1, contradiction_pair_f1, kendall_tau) | ≥ 0.70 |
| LLM-judged (interest-extraction, narrative-drift, position-interest-separation) | Subjective review by two annotators; no hard κ floor |

IAA values are reported per item in `source.inter_annotator_kappa`.

---

## Bulk Import

To import items into the TACITUS platform for annotation:

1. Draft source text and question in the TCGC JSON template
2. Run `tcgc validate <item>.json` — must exit 0
3. Submit via the platform API or PR to `items/`
4. Assign to two annotators via the platform assignment tool

The `scripts/build_manifest.py` script regenerates `items/manifest.json` after any batch import.
