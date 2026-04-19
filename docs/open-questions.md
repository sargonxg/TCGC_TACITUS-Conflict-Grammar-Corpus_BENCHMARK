# Open Questions

<!-- source: https://www.tacitus.me/research/tcgc -->

Six open questions the TCGC was designed to surface. These are active areas of investigation.

---

## 1. Does position/interest separation generalize across cultures?

The Fisher/Ury distinction between positions and interests is well-established in Western negotiation theory. It is unclear whether this distinction maps cleanly onto conflict structures from non-Western cultural contexts.

**Current thinking:** We are collecting items from peace-process and diplomatic domains with non-Western actors to test this. The interest-extraction task type is the primary probe.

---

## 2. How much does provenance granularity matter for downstream reasoning?

TCGC requires every primitive to cite a source span. But spans can range from a message-level id to a character-level offset. Does finer-grained provenance improve downstream conflict reasoning, or is document-level attribution sufficient?

**Current thinking:** v0.1 uses message/document ids. v0.2 will add character-span items to test this directly via the `provenance_f1` IoU scoring path.

---

## 3. Can LLMs reliably separate commitment from aspiration?

The `commitment-tracking` task requires distinguishing a genuine commitment ("I'll own it") from an aspiration ("we should try to"). This is a key failure mode in conflict analysis.

**Current thinking:** Preliminary runs suggest GPT-4-class models confuse these ~30% of the time. The `COMMITS_TO` vs `ASSERTED` partial-credit similarity (0.5) is designed to surface this.

---

## 4. Is narrative drift detectable without temporal metadata?

tcgc-0002 strips dates explicitly. It is unknown whether LLMs can reconstruct temporal order from causal language alone, or whether they rely on date markers.

**Current thinking:** The kendall_tau metric on date-stripped items is the cleanest probe. Early results suggest significant degradation when dates are removed.

---

## 5. What is the right materiality threshold for contradictions?

The `contradiction-detection` task classifies pairs as material or cosmetic. The current threshold (1.0 vs 0.25 weight) is a judgment call. A miscalibrated threshold distorts leaderboard rankings.

**Current thinking:** We will run a calibration study on the full corpus to fit the weight empirically from annotator materiality judgments.

---

## 6. How do graph-overlap scores correlate with downstream task performance?

TCGC scores a typed subgraph — but does a higher graph_overlap score actually predict better performance on downstream conflict-analysis tasks (e.g., mediation support, risk assessment)?

**Current thinking:** This requires a downstream task paired study. The TACITUS Dialectica reference system will provide the first data point.
