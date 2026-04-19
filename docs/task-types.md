# Task Types

<!-- source: https://www.tacitus.me/research/tcgc -->

14 task types. Each maps to exactly one metric — mismatches are a validation error.

---

## 1. `actor-resolution` → `graph_overlap`

**Definition:** Identify and disambiguate all parties in the input who can hold interests or make claims. Resolve aliases and co-references to a canonical actor set.

**Input shape:** Messages, documents, or transcript. May include an `actors` hint list.

**Output shape:** Primitives of type `actor` with provenance bindings; edges where actors are in relationships.

**Failure modes:** Splitting one actor into two; merging two distinct actors; missing implicit actors (e.g., "the board" as a collective).

**Mini-example:** Input mentions "the Chair", "Director Park", and "she". A correct resolution collapses "she" → "Director Park".

---

## 2. `claim-extraction` → `graph_overlap`

**Definition:** Extract every asserted, denied, or acknowledged factual or evaluative statement, attributed to the speaker making it.

**Input shape:** Any input modality.

**Output shape:** Primitives of type `claim`; edges of type `ASSERTED`, `DENIED`, `ACKNOWLEDGED`, `ACKNOWLEDGED_AMBIGUOUSLY`.

**Failure modes:** Extracting background facts as claims; missing hedged claims; incorrect attribution.

---

## 3. `interest-extraction` → `llm_judge_anchored`

**Definition:** Extract the underlying goals and needs motivating each actor, distinct from their stated positions (Fisher/Ury distinction).

**Input shape:** Transcript or messages where positions are stated.

**Output shape:** Primitives of type `interest`; edges of type `HOLDS_INTEREST`.

**Failure modes:** Restating positions as interests; hallucinating interests not supported by text; missing latent interests.

---

## 4. `constraint-extraction` → `graph_overlap`

**Definition:** Identify structural rules, norms, or limits that bound feasible outcomes for one or more actors.

**Output shape:** Primitives of type `constraint`; edges of type `CONSTRAINED_BY`.

---

## 5. `leverage-mapping` → `graph_overlap`

**Definition:** Map resources, dependencies, or capabilities that shift bargaining power between actors.

**Output shape:** Primitives of type `leverage`; edges of type `LEVERAGES`.

---

## 6. `commitment-tracking` → `graph_overlap`

**Definition:** Identify promises of future action, who made them, whether they were acknowledged or contested, and their current status.

**Output shape:** Primitives of type `commitment` with `subject`, `deadline`, `status` fields; edges of type `COMMITS_TO`, `ASSERTED`, `ACKNOWLEDGED_AMBIGUOUSLY`, `DENIES_SCOPE`, `REVOKES`.

**Failure modes:** Confusing an aspiration with a commitment; missing a revocation; incorrect status.

---

## 7. `event-ordering` → `kendall_tau`

**Definition:** Reconstruct the chronological sequence of discrete events mentioned in the input, even when dates have been stripped.

**Output shape:** Primitives of type `event`; edges of type `PRECEDES`; a top-level `order` array.

**Failure modes:** Reversing causal chains; treating simultaneous events as sequential.

---

## 8. `narrative-drift` → `llm_judge_anchored`

**Definition:** Detect when an actor's framing of events shifts across time or documents, and characterize the direction and magnitude of the shift.

**Output shape:** Primitives of type `narrative`; edges of type `FRAMES`; temporal ordering of narrative versions.

---

## 9. `causal-chain` → `graph_overlap`

**Definition:** Reconstruct the causal pathway linking a trigger event to an outcome, identifying intermediate causes.

**Output shape:** Primitives of type `event`; edges of type `CAUSES`.

---

## 10. `contradiction-detection` → `contradiction_pair_f1`

**Definition:** Identify pairs of claims that contradict each other, and classify each pair as material (affects outcomes) or cosmetic (procedural/minor).

**Output shape:** `contradictions` array with `claim_a`, `claim_b`, `materiality`, `rationale`.

**Failure modes:** Flagging tension as contradiction; missing implicit contradictions; miscategorizing materiality.

---

## 11. `provenance-attribution` → `provenance_f1`

**Definition:** Extract every attributable claim and bind each to its exact source span in the input document.

**Output shape:** Primitives with `provenance` refs pointing to specific document ids or span identifiers.

**Failure modes:** Orphan provenance (ref not in input); merging claims from different sources.

---

## 12. `commitment-claim-mismatch` → `graph_overlap`

**Definition:** Identify cases where an actor's stated commitment contradicts their earlier or later claims.

**Output shape:** Commitment primitive + claim primitives + edges showing the mismatch.

---

## 13. `position-interest-separation` → `llm_judge_anchored`

**Definition:** For each actor, cleanly separate stated positions from inferred underlying interests.

**Output shape:** Both `claim` (position) and `interest` primitives for each actor; edges `ASSERTED` (positions) and `HOLDS_INTEREST` (interests).

---

## 14. `cross-document-synthesis` → `graph_overlap`

**Definition:** Synthesize a unified conflict graph from multiple documents that may contradict or complement each other.

**Output shape:** Full ACO subgraph integrating all documents; edges include `CONTRADICTS`, `SUPPORTS`, `CITES`.
