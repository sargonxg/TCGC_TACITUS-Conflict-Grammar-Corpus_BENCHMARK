# Datasheet for TCGC v0.1-sample

*Following Gebru et al. (2021) "Datasheets for Datasets"*

---

## Motivation

**Why was this dataset created?**
To measure what generic language models and RAG systems fail at in conflict-analysis settings: commitment tracking, causal ordering, interest/position separation, provenance attribution, and narrative drift. Existing benchmarks evaluate information retrieval or general reasoning; none target the structured, typed subgraph outputs required for conflict intelligence work.

**Who created it and on whose behalf?**
Giulio Catanzariti (TACITUS). No external funding.

---

## Composition

**What does the dataset contain?**
5 public sample items across 5 task types, 5 domains, and 3 input modalities (messages, documents, transcript). Each item has: source text, a structured question, a gold answer as a typed subgraph (primitives + edges), and a rubric specifying the scoring metric.

**How many instances?**
5 public (v0.1-sample). Full corpus: ~480+ items (under DUA).

**Does it contain personal data?**
No. All items are synthetic or fully anonymized. Actor labels are generic (Sam, Alex, State A, Vendor/Buyer).

**Inter-annotator agreement:**
Reported per item via `source.inter_annotator_kappa`. Sample range: κ = 0.64–0.91.

---

## Collection Process

**How was it collected?**
Expert authoring from the Conflict Grammar framework. Items were designed to test specific failure modes, not scraped from existing corpora.

**Over what timeframe?**
March 2026 (v0.1-sample).

---

## Preprocessing / Labeling

**Three-pass annotation protocol:**
1. Primitive tagging (actor, claim, interest, etc.)
2. Edge labeling (ACO edge types, provenance binding)
3. Ground-truth QA (second annotator reviews full item)

IAA targets: κ ≥ 0.70 for graph-scored tasks, subjective review for LLM-judged tasks.

---

## Uses

**Intended uses:**
Benchmark evaluation of conflict-analysis AI systems.

**Out-of-scope uses:**
Training generative models (see DUA), surveillance, profiling, or any harm-enabling application.

---

## Distribution

- v0.1-sample: GitHub, CC-BY-NC-SA 4.0
- Full corpus: via Data Use Agreement (email hello@tacitus.me)

---

## Maintenance

**Who maintains it?**
Giulio Catanzariti (giuliocatanzariti@gmail.com).

**How is it versioned?**
Semantic Versioning. Issues via GitHub. Dataset paper forthcoming Q4 2026.
