# Metrics

5 scoring functions. Each is bound to specific task types — mismatches are a validation error.

---

## `graph_overlap`

**Formula:** Weighted mean of node Jaccard and edge Jaccard.

```
score = 0.4 × node_jaccard + 0.6 × edge_jaccard
```

Node Jaccard: `|gold_nodes ∩ pred_nodes| / |gold_nodes ∪ pred_nodes|`

Edge Jaccard: soft Jaccard using partial-credit type similarity (see `tcgc/ontology/edges.py`). Near-miss edge types (e.g., `ASSERTED` vs `ACKNOWLEDGED`) receive partial credit (0.5) rather than 0.

**Worked example:** Gold has 2 nodes and 1 edge. Pred has both nodes (node_j = 1.0) but the edge type is `ACKNOWLEDGED` instead of `ASSERTED` (similarity = 0.5). Score = 0.4 × 1.0 + 0.6 × 0.5 = **0.70**.

**Edge cases:** Empty gold + empty pred → 1.0. Empty pred with non-empty gold → 0.0. Node weights must sum to 1.0.

**When it can mislead:** Rewards node-heavy predictions that miss edge semantics. Watch `components["edge_jaccard"]` separately.

---

## `provenance_f1`

**Formula:** F1 over `(primitive_id, provenance_ref)` pairs.

```
precision = |pred_pairs ∩ gold_pairs| / |pred_pairs|
recall    = |pred_pairs ∩ gold_pairs| / |gold_pairs|
F1        = 2 × P × R / (P + R)
```

**Worked example:** Gold has 3 (id, ref) pairs. Pred has 3 pairs: 2 matching, 1 wrong. P = 2/3, R = 2/3, F1 = **0.667**.

**Edge cases:** Span refs are matched as prefixes (`doc1:spans:1` resolves if `doc1` is in inputs). Future items may use character-span IoU.

**When it can mislead:** Does not penalize citing a real span for the wrong primitive.

---

## `kendall_tau`

**Formula:** Kendall's τ-b, normalized to [0, 1].

```
score = (τ + 1) / 2
```

Missing gold events in pred receive worst-case rank. NaN → 0.0 with a diagnostic note.

**Worked example:** Gold order [e1, e2, e3, e4]. Pred reverses to [e4, e3, e2, e1]. τ = -1.0, score = **0.0**.

**Edge cases:** Single-element order → always 1.0. All events missing → 0.0.

**When it can mislead:** Robust to small local swaps; a single large transposition can dominate.

---

## `contradiction_pair_f1`

**Formula:** Materiality-weighted F1 over unordered `{claim_a, claim_b}` pairs.

```
material pair weight = 1.0
cosmetic pair weight = 0.25
```

Pair order is ignored: `{c1, c2}` equals `{c2, c1}`.

**Worked example:** Gold has 1 material + 1 cosmetic pair. Pred finds only the material pair. Weighted recall = 1.0 / (1.0 + 0.25) = 0.80. Precision = 1.0. F1 = **0.889**.

**Edge cases:** Empty gold + empty pred → 1.0. `components["f1_unweighted"]` always reported alongside weighted F1.

**When it can mislead:** A system that finds only material pairs scores higher than one that finds all pairs including cosmetic ones with FPs.

---

## `llm_judge_anchored`

**Formula:** LLM judge score calibrated via isotonic regression on 20 anchor triples.

Gated behind `TCGC_RUN_API=1`. Returns 0.0 with a "skipped" note otherwise.

**Known failure modes (Zheng et al. 2023):** Position bias, verbosity bias, self-preference bias.

**Calibration:** Raw LLM score is passed through isotonic regression fitted on `tcgc/scoring/anchors/v0.1.jsonl` (20 `{raw, human_score}` pairs). This monotonically maps raw scores toward human-annotated values.

**When it can mislead:** Calibration is only as good as the anchor set. Small anchor sets (n=20) have high variance. Do not treat calibrated scores as ground truth; report alongside human spot-checks.
