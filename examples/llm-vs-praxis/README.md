# LLM-only vs PRAXIS — what the layered stack actually adds

This directory holds **paired worked examples** that show the same question handed to:

- **(A) a vanilla frontier LLM** with the source text and a normal prompt, and
- **(B) the PRAXIS-style typed pipeline** that runs the same model under the TCGC harness, against the ACO kernel, with bi-temporal stamps and span-level provenance.

The point is not to show that one is "better" on a vibe. It is to show — on the same input, with the same model — what the structural layer adds that the chat surface cannot produce.

Each example contains:

- `INPUT.md` — the source passage(s) and the analyst question.
- `vanilla.md` — verbatim output from the vanilla LLM at temperature 0 with a competent but typical prompt.
- `praxis.json` — the typed graph output (JSON Lines of ACO operations) the TCGC pipeline produced.
- `diff.md` — the human-readable diff: what the layered output captured that the vanilla output flattened, dropped, or smoothed.

The vanilla and PRAXIS outputs use the **same underlying model** (e.g., Claude Opus 4.7, GPT-5, Llama 4). The difference is the surface around it.

## What the diff makes visible

| Failure mode | Vanilla LLM behaviour | PRAXIS-typed output |
|---|---|---|
| Temporal flattening | Events appear in narrative order but timeline is not reconstructed when dates are stripped. | Bi-temporal stamps; `PRECEDES` edges; `kendall_tau` against gold order is scoreable. |
| Causal collapse | "A and B" → "A caused B" via fluent transition. | `CAUSES` requires `mechanism` + `conditions`; absent those, falls back to `PRECEDES`. |
| Provenance absence | No span pointers. Confident assertions you cannot trace. | Every primitive cites `(doc_id, char_start, char_end)`. Orphan provenance fails validation. |
| Contradiction averaging | Smoothed paraphrase. ("Both sources broadly agree…") | Two Claim nodes plus a `CONTRADICTS` edge with materiality. |
| Position/Interest confusion | Position restated as interest, or interest invented. | Distinct primitives with mandatory `derivation` chain on Interest. |
| Commitment vs Claim collapse | "X committed to Y" emitted for any stated-future-action utterance. | Commitment requires status + binding-strength; mere assertion is a Claim with `modality=Asserted`. |

## Reading order

Start with `melian-leverage/` — the cleanest example. Then `federalist-positions-vs-interests/` for the Fisher/Ury distinction. Then `hobbes-machiavelli-drift/` for the cross-document narrative-drift case.

These are not benchmarks — they are demonstrations. The benchmarks are under `items/`.
