# Diff — what the typed layer captured

Same model. Same passage. Different surface. Below is what the layered output contains that the vanilla prose did not — or, where the vanilla output gestured at something, what it failed to lock down structurally.

## 1. Leverage typed, not gestured

- **Vanilla**: "Athens has coercive power, Melos has only moral/normative appeal."
- **PRAXIS**: Two Leverage primitives, mechanism-typed (`Coercive`, `Normative`), each bound to its holder via a `LEVERAGES` edge. Mechanism is queryable. Cross-corpus comparisons become possible.

## 2. Procedural constraint as a first-class object

- **Vanilla**: Mentions that Athens "sets the terms" — the constraint is described as part of the situation.
- **PRAXIS**: `Constraint(kind=Procedural, binding_strength=Hard)` with both Athens and Melos bound to it via `CONSTRAINED_BY`. Queryable, citable, and — critically — visible as the thing the Melian counter-claim is targeting.

## 3. Position vs Interest, distinct primitives

- **Vanilla**: "Athens wants empire-stability; Melos wants survival." Treated as background colour.
- **PRAXIS**: Two `Interest` nodes, each with a `derivation` chain that names the source claims and leverage edges that ground them. Inference is auditable.

## 4. The contradiction edge

- **Vanilla**: Notices the Melian rhetorical move ("use Athens' constraint against them") and describes it in a sentence.
- **PRAXIS**: A `CONTRADICTS` edge from the Melian claim back to the Athenian constraint, with materiality `material` and a rationale string. The dispute is held structurally, not summarised.

## 5. Provenance everywhere

- **Vanilla**: No span pointers. Every assertion is uncited.
- **PRAXIS**: 17 typed operations, every single one carrying `provenance: "melian-opening:spans:N"`. The validator rejects orphans.

## What this matters for, in production

- **For a mediation analyst**: the typed output lets them filter for "all leverage edges in this case" or "every contradiction edge of material weight." The vanilla output requires re-reading.
- **For a reviewer**: every claim a partner institution might dispute is anchored to the character offset the partner can verify.
- **For a downstream model**: the next system in the pipeline reads typed graph state instead of free prose. Garbage-in degrades.

## What this does *not* claim

This diff does not claim PRAXIS is "smarter" than the vanilla LLM. The model is the same. What changed is the surface around the model: hard validation, typed contract, mandatory provenance. The layered output is what the analyst's typed reasoning looks like when the tooling stops dropping it on the floor between turns.
