"""Inspect policy-workflow recordings. Not a TCGC score or semantic quality judge.

Author: Giulio Catanzariti <giuliocatanzariti@gmail.com>
"""

import argparse
import hashlib
import json
from pathlib import Path

MAX_WORKFLOW_BYTES = 2_000_000


def inspect(path):
    raw = Path(path).read_bytes()
    if len(raw) > MAX_WORKFLOW_BYTES:
        raise ValueError("Workflow exceeds 2 MB")
    v = json.loads(raw)
    if v.get("format") != "tacitus-policy-workflow/1":
        raise ValueError("Unsupported workflow")
    ids = {s["id"] for s in v["capsule"]["statements"]}
    items = v["artifact"]["items"]
    used = {i for r in items for i in r["evidence_ids"]}
    unknown = sorted(used - ids)
    return {
        "file": Path(path).parent.name + "/" + Path(path).name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "arm": v["run"]["arm"],
        "model_calls": v["run"]["model_calls"],
        "usage_reported": v["run"].get("usage"),
        "items": len(items),
        "selected_evidence_records": len(ids),
        "cited_evidence_records": len(used & ids),
        "unknown_citation_ids": unknown,
        "draft_items_with_literal_qualification_flags": sum(
            bool(r.get("review_flags")) for r in items
        ),
        "semantic_entailment": "not_evaluated",
        "expert_review": "not_recorded",
        "tcgc_benchmark_score": "not_applicable",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("files", nargs="+")
    p.add_argument("--output")
    a = p.parse_args()
    r = {
        "format": "tacitus-policy-workflow-inspection/1",
        "scope": (
            "Recorded execution and reference integrity only. "
            "No TCGC corpus score or general model-quality comparison."
        ),
        "results": [inspect(x) for x in a.files],
    }
    text = json.dumps(r, indent=2)
    if a.output:
        Path(a.output).write_text(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
