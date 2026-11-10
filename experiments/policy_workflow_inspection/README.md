# Inspect a real policy drafting run

This standalone inspector reads `tacitus-policy-workflow/1` results from the [public policy pipeline](https://github.com/sargonxg/TACITUS-Knowledge-Pipeline-open/tree/main/reference-pipeline). It reports observed model usage, citation-ID coverage and literal qualification flags. It is separate from the TCGC corpus and scoring protocol.

```sh
python experiments/policy_workflow_inspection/report.py path/to/workflow-result.json
```

The [recorded inspection](recorded-inspection.json) covers two single-call Syria drafts and a two-step evidence-inspection agent, executed with Cloudflare on 10 November 2026. The report records result-file hashes and relative case names; use your own downloaded result paths to reproduce the counts. Full requests, provider responses and artifacts are retained in the pipeline example directory.

There is one frozen historical task, one model and one successful run per path. Both flat and structured drafts resolve their citations. Structured input uses more total tokens in this example. No entailment judge, blinded domain review, statistical comparison or current-situation assessment was performed. Do not present these counts as a TCGC score or a demonstrated saliency/efficiency improvement.

TCGC retains its existing CC BY-NC-SA 4.0 terms. The separate pipeline retains its own Apache-2.0 code and source rights notes.
