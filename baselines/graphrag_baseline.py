"""GraphRAG baseline for TCGC — LLM-driven graph construction then query."""
import os
if os.environ.get("TCGC_RUN_BASELINES") != "1":  # pragma: no cover
    raise RuntimeError("Set TCGC_RUN_BASELINES=1 to enable this baseline.")

import json
from typing import Any

_GRAPH_PROMPT = """Extract entities and relationships from the text as a JSON graph with
'primitives' (list of {id, type, label, provenance}) and
'edges' (list of {from, to, type, provenance}).
Return ONLY valid JSON."""

_QUERY_PROMPT = """Given this conflict graph and a question, answer the question by
selecting and returning the relevant subgraph as JSON.
Return ONLY valid JSON matching the gold schema shape."""


def predict(item_id: str, inputs: dict[str, Any]) -> dict[str, Any]:
    """Build a graph from input, then query it for the answer."""
    from openai import OpenAI  # type: ignore[import-not-found]
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    source_text = json.dumps(inputs, indent=2)
    graph_resp = client.chat.completions.create(
        model="gpt-4o", temperature=0,
        messages=[
            {"role": "system", "content": _GRAPH_PROMPT},
            {"role": "user", "content": source_text},
        ],
    )
    graph_text = graph_resp.choices[0].message.content or "{}"
    try:
        graph = json.loads(graph_text)
    except json.JSONDecodeError:
        graph = {}

    query_resp = client.chat.completions.create(
        model="gpt-4o", temperature=0,
        messages=[
            {"role": "system", "content": _QUERY_PROMPT},
            {"role": "user", "content": f"Graph:\n{json.dumps(graph)}\n\nQuestion: {inputs.get('question','')}"},
        ],
    )
    answer_text = query_resp.choices[0].message.content or "{}"
    try:
        pred = json.loads(answer_text)
    except json.JSONDecodeError:
        pred = {}
    pred["id"] = item_id
    return pred
