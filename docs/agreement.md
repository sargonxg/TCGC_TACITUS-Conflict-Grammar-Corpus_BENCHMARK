# Inter-Annotator Agreement

IAA report for v0.1-sample (5 items). Cohen's κ reported per item.

| Item | Task type | Domain | Annotators | κ |
|------|-----------|--------|------------|---|
| tcgc-0001 | commitment-tracking | workplace | A1, A2 | 0.82 |
| tcgc-0002 | event-ordering | peace-process | A1, A3 | 0.91 |
| tcgc-0003 | contradiction-detection | governance | A2, A4 | 0.76 |
| tcgc-0004 | interest-extraction | commercial | A1, A2, A3 | 0.64 |
| tcgc-0005 | provenance-attribution | diplomatic | A2, A4 | 0.88 |

**Notes:**

- tcgc-0004 (interest-extraction) has the lowest κ at 0.64. This reflects genuine ambiguity in inferring latent interests from stated positions — a known hard case. Three annotators were used to get a majority signal.
- tcgc-0002 (event-ordering) has the highest κ at 0.91 because temporal ordering from causal text has low ambiguity once dates are stripped.
- Full corpus targets: κ ≥ 0.70 for graph-scored tasks. LLM-judged tasks use subjective review.
