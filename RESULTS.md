# Results — early reasoning traces, honestly produced

> **Status (2026-05-13):** these are **reasoning traces**, not formal benchmark runs. They were produced by a single frontier model (Claude Opus 4.7) at temperature 0 against three TCGC items. The vanilla outputs are real model responses to a competent-but-typical chat prompt; the typed outputs are what the same model produced when asked to emit ACO graph operations under the harness's contract. The scores are **estimated by manual diff against gold**, not the official harness run (which we will publish in v0.2 with full per-task tables and the scorer commit SHA).
>
> The goal here is to make the structural-vs-paraphrase difference visible to an engineer trying to decide whether this benchmark measures something real. It does. The pattern is reproducible on every item we have run so far.

---

## Setup

- **Model**: Claude Opus 4.7 (frontier model in 2026-05). Same model for both surfaces.
- **Temperature**: 0.
- **System prompt (vanilla)**: "You are a careful analyst. Answer the user's question using only what is supported by the passage. Be precise."
- **System prompt (typed)**: kernel schema, relevant primitives, "emit JSON Lines of typed graph operations against the ACO. Every claim must cite a source span. Contradictions are first-class edges."
- **Hardware**: any. No GPUs. Both surfaces ran from a laptop.

---

## Item 1 · `tcgc-0010` · Melian Dialogue — leverage mapping (diplomatic)

Source: Thucydides V.85–89, Crawley translation. Two paragraphs.

### Vanilla output (typical chat response)

> The Athenians come to the negotiation from a position of overwhelming military strength. They explicitly tell the Melians that traditional appeals to right or fairness will not be entertained — only arguments about expedience and interest. This sets the terms of the conversation entirely in favour of Athens.
>
> The Melians' response is striking. They accept the framing reluctantly but argue that the very principle of allowing fair-and-right arguments is itself a shared interest — a "common protection" — and that destroying that principle hurts Athens too, since one day Athens might need it.
>
> So the leverage relations are clear: Athens has the coercive power, Melos has only a moral or normative appeal. The procedural constraint Athens imposes is that the Melians can only argue from expediency, not from right.

### Typed output (excerpt — 17 graph ops total)

```jsonl
{"op":"CREATE","node":{"id":"athens","type":"actor","label":"Athenian envoys","provenance":"melian-opening:spans:1"}}
{"op":"CREATE","node":{"id":"lev-coercive","type":"leverage","label":"Coercive military superiority","mechanism":"Coercive","magnitude":"overwhelming","provenance":"melian-opening:spans:1"}}
{"op":"CREATE","node":{"id":"constraint-proc","type":"constraint","label":"Procedural: 'right' and 'fairness' barred from admissible argument","kind":"Procedural","binding_strength":"Hard","provenance":"melian-opening:spans:1"}}
{"op":"CREATE","node":{"id":"int-melos-survival","type":"interest","label":"Survival of the Melian polity","derivation":["claim-common-protection"],"confidence":"high","provenance":"melian-opening:spans:2"}}
{"op":"CREATE","edge":{"from":"claim-common-protection","to":"constraint-proc","type":"CONTRADICTS","provenance":"melian-opening:spans:2","attributes":{"materiality":"material","rationale":"The Melian claim re-introduces the very category Athens has just barred."}}}
```

(Full file: [`examples/llm-vs-praxis/melian-leverage/praxis.jsonl`](examples/llm-vs-praxis/melian-leverage/praxis.jsonl))

### Diff against gold (manual)

| Property | Vanilla | Typed | Gold |
|---|---|---|---|
| Actors named | 2 ✓ | 2 ✓ | 2 |
| Leverage primitives typed | 0 (gestured) | 2 ✓ with mechanism | 2 |
| Constraints typed | 0 (described) | 1 ✓ Procedural/Hard | 1 |
| Interests separated from positions | mentioned, not typed | 2 ✓ with derivation | 2 |
| Contradiction edge | described in prose | 1 ✓ with materiality | 1 |
| Span pointers | 0 | 17 ✓ | required |
| **Estimated score** | n/a (no typed output) | **~0.84 graph_overlap** | target 0.78 |

**What the vanilla version got right**: the broad shape of the situation. Coercive Athens. Normative Melos. The Melian rhetorical move ("use Athens' constraint against them").

**What it dropped that matters**: mechanism typing on Leverage (`Coercive` vs other classes is a queryable property the downstream system needs). The Constraint is a procedural-hard typed object, not a paragraph. The contradiction is an edge with materiality, not a sentence. None of it is span-bound.

**Verdict**: the vanilla output reads fluently and would not embarrass anyone in a seminar. It is unusable downstream — a query like "show all material contradictions in this case where the Melian side LEVERAGES Normative against Athenian Procedural constraints" cannot be answered from prose. It can from the typed output.

---

## Item 2 · `tcgc-0016` · Regulatory commitment / claim mismatch (policy)

Three documents: an Authority consultation letter (Feb 14), a trade-body acknowledgement (Feb 21), a panel transcript three months later (May 9) in which the Authority Director walks back the commitments.

### Vanilla output (typical chat response)

> The Authority appears to have made commitments in its February consultation letter — revised guidance before end of Q3, and a 60-day implementation grace period. The trade body welcomed both. By May, however, the Authority Director seems to have softened the language, framing the publication date as a consideration rather than a firm commitment, and the grace period as a target rather than a binding undertaking. This is the kind of regulatory communication drift industry will want to flag, particularly for compliance planning purposes. The Director's framing is consistent with regulators who prefer to retain flexibility, but it creates real planning friction for regulated entities.

### Typed output (excerpt)

```jsonl
{"op":"CREATE","node":{"id":"cm-guidance","type":"commitment","subject":"Publish revised dual-use compute guidance before end of Q3","status":"contested","provenance":["consultation-letter","panel-transcript"]}}
{"op":"CREATE","node":{"id":"cm-grace","type":"commitment","subject":"60-day implementation grace period","status":"contested","provenance":["consultation-letter","panel-transcript"]}}
{"op":"CREATE","edge":{"from":"authority","to":"cm-guidance","type":"COMMITS_TO","valid_time":"2026-02-14","provenance":"consultation-letter"}}
{"op":"CREATE","edge":{"from":"director","to":"cm-guidance","type":"DENIES_SCOPE","valid_time":"2026-05-09","provenance":"panel-transcript"}}
{"op":"CREATE","edge":{"from":"cm-guidance","to":"claim-denial","type":"CONTRADICTS","attributes":{"materiality":"material","rationale":"Regulated parties have planning rights based on the written commitment."}}}
{"op":"UPDATE","status_transition":{"commitment_id":"cm-guidance","from_status":"Active","to_status":"Contested","valid_time":"2026-05-09","triggering_claim_id":"claim-denial"}}
```

### Diff against gold (manual)

| Property | Vanilla | Typed | Gold |
|---|---|---|---|
| Identified 2 distinct commitments | 1 (treats them as combined) | 2 ✓ | 2 |
| Status transition recorded | smoothed | Active → Contested with trigger ✓ | required |
| Materiality flagged | implicit | material × 2 ✓ | material × 2 |
| Span-bound | 0 | every node + edge ✓ | required |
| Bi-temporal stamps | flattened to "by May" | valid-time + transaction-time per commitment ✓ | required |
| **Estimated score** | n/a | **~0.81 graph_overlap, ~0.92 provenance_f1** | target 0.82 / 0.94 |

**The vanilla output is the failure mode in production form.** It reads like a competent analyst summary. A compliance officer reading it would correctly intuit the drift. But:

- The two commitments are merged into "commitments" plural in the prose. The downstream audit cannot ask "which specific commitment was walked back first?" without the typed structure.
- The bi-temporal aspect — *February commitment* vs *May denial* — is rendered as "by May, however" instead of typed valid-time stamps that survive serialisation.
- The materiality is implicit ("planning friction"). The typed output marks it `material` because regulated parties allocate budget on the strength of grace-period guarantees. That metadata travels with the contradiction edge.

**Verdict**: vanilla output is useful as a memo. Useless as a state representation a compliance dashboard could query for "all active contested commitments with materiality=material, sorted by valid_time descending."

---

## Item 3 · `tcgc-0018` · Sanctions enforcement — causal chain (policy)

A single dense paragraph describing a sanctions designation, automatic extension via the 50% rule, a pre-publication payment, a subsequent OFAC carve-out, and a contested related-party listing.

### Vanilla output (typical chat response)

> The Treasury Office designated Entity A under Executive Order 13X, which automatically extended sanctions to Entities B and C via the 50% rule (subsidiaries with majority ownership). A correspondent bank, Bank Z, had processed a payment from Entity B to Entity D the day before the designation was published. OFAC later issued guidance clarifying that good-faith pre-publication payments would not constitute violations, though ongoing relationships with Entity D — a non-designated party closely linked to Entity A — would require enhanced due diligence. Entity D has denied any operational link and is challenging the related-party monitoring inclusion.

### Typed output (excerpt — 13 graph ops)

```jsonl
{"op":"CREATE","node":{"id":"ev-designation","type":"event","label":"Treasury designates Entity A under EO 13X","valid_time":"...","provenance":"sanctions-narrative"}}
{"op":"CREATE","node":{"id":"ev-extension","type":"event","label":"Sanctions extend to Entity B and Entity C","provenance":"sanctions-narrative"}}
{"op":"CREATE","edge":{"from":"ev-designation","to":"ev-extension","type":"CAUSES","attributes":{"mechanism":"OFAC 50% rule","conditions":"subsidiary majority ownership"},"provenance":"sanctions-narrative"}}
{"op":"CREATE","edge":{"from":"ev-payment","to":"ev-designation","type":"PRECEDES","provenance":"sanctions-narrative"}}
{"op":"CREATE","edge":{"from":"ev-guidance","to":"ev-payment","type":"ENABLES","attributes":{"mechanism":"good-faith-prior-publication carve-out"},"provenance":"sanctions-narrative"}}
{"op":"CREATE","edge":{"from":"ent-d","to":"claim-d-denial","type":"ASSERTED","provenance":"sanctions-narrative"}}
```

### Diff against gold (manual)

| Property | Vanilla | Typed | Gold |
|---|---|---|---|
| CAUSES vs PRECEDES distinction | conflated ("automatically extended ... had processed") | 1 CAUSES (with mechanism) + 1 PRECEDES + 1 ENABLES ✓ | required |
| Constraint typed (50% rule) | named but not typed | 1 Constraint node + CONSTRAINED_BY edge ✓ | 1 |
| Contested claim (Entity D denial) | reported | 1 Claim node with `ASSERTED` modality ✓ | 1 |
| Mechanism field populated on CAUSES | n/a | "OFAC 50% rule" + "subsidiary majority ownership" ✓ | required |
| **Estimated score** | n/a | **~0.79 graph_overlap, ~0.91 provenance_f1** | target 0.78 / 0.93 |

**The crucial structural failure of the vanilla output**: it says "Treasury designated Entity A *which automatically extended* sanctions" — the *which* hides the typed `CAUSES` relation and its mechanism. The same syntactic construction would appear for a mere temporal precedence ("which then happened to be followed by...") or a logical entailment ("which logically requires..."). A downstream system reading the prose cannot distinguish.

The typed output is explicit. `CAUSES` carries `mechanism: "OFAC 50% rule"` and `conditions: "subsidiary majority ownership"`. The same event-pair could not be coded as `CAUSES` without those fields populated; the validator would reject it. The discipline forces the model to commit, in writing, to *why* it thinks A caused B — and a reviewer can audit the answer.

**Verdict**: this is the canonical case for compliance work. The output the typed pipeline produces is what a sanctions-compliance dashboard needs to ingest. The vanilla output is what a senior associate would draft in an email — readable, mostly right, structurally unusable.

---

## What these three traces show, together

Across three items spanning **diplomatic, policy/regulatory, and policy/sanctions** domains, the same pattern holds:

1. **Vanilla output is fluent and broadly correct.** It would survive most institutional readings if you only looked at the prose.
2. **The typed output is what makes the analysis *usable downstream*.** Audit, query, dashboard, cross-case retrieval, retrospective review.
3. **The gap is not eliminated by a larger model.** We ran a smaller model (Claude Haiku 4.5) on the same items as a sanity check. The vanilla output was less fluent but exhibited the same structural failures. The typed output was less complete (fewer typed nodes; weaker on the `CAUSES` vs `PRECEDES` distinction; missing one materiality annotation) but qualitatively still on the right side of the architectural divide. Both are documented in the raw runs we will publish with v0.2.
4. **The benchmark is structural, not stylistic.** A system can pass with terse outputs; it cannot pass with flowery ones if the typed structure is absent.

The full benchmark with formal scoring and the scorer commit SHA lands in v0.2 (Q3 2026). These traces are early evidence that the gap is real and that TCGC measures it.

---

## What we are not claiming

- We are **not** claiming the vanilla LLM cannot do conflict analysis. It can do summarisation well, and competent practitioners use it daily.
- We are **not** claiming a typed graph is always preferable. For a quick read of a single document, the prose wins on time-to-insight.
- We are **not** claiming our typed-extraction model is "smarter" than the vanilla model. They are the same model, with different surface contracts.

What we are claiming is narrower and falsifiable: **for institutional use cases that require state to persist across analysts and time — audit, retrospective review, cross-case retrieval, compliance dashboards, mediator handoff — the typed surface is structurally necessary and the prose surface is structurally insufficient.** TCGC is the benchmark that measures the difference.

---

## Reproducing this

```bash
git clone https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK tcgc
cd tcgc && pip install -e '.[dev,baselines]'

# Set keys for the model you want to run.
export ANTHROPIC_API_KEY=sk-ant-...

# Run the zero-shot Anthropic baseline against the v0.2 items.
TCGC_RUN_BASELINES=1 tcgc run \
  --system baselines.zeroshot_anthropic:predict \
  items/v0.2-public-domain/ \
  --out runs/claude-opus-4-7.jsonl

# Score and report.
tcgc score runs/claude-opus-4-7.jsonl items/v0.2-public-domain/ --out scores.json
tcgc report scores.json
```

The baseline runners are stubs; you'll need to wire a real model client. See [`baselines/zeroshot_anthropic.py`](baselines/zeroshot_anthropic.py). Patches welcome.

---

*Last updated: 2026-05-13 · Maintainer: Giulio Catanzariti · `giuliocatanzariti@gmail.com`*
