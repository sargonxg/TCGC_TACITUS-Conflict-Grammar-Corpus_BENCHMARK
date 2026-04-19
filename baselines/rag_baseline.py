"""RAG baseline for TCGC — embed, retrieve, extract."""

import os

if os.environ.get("TCGC_RUN_BASELINES") != "1":  # pragma: no cover
    raise RuntimeError("Set TCGC_RUN_BASELINES=1 to enable this baseline.")

import json
from typing import Any


def _get_chunks(inputs: dict[str, Any]) -> list[str]:
    chunks = []
    for m in inputs.get("messages", []):
        chunks.append(m.get("text", ""))
    for d in inputs.get("documents", []):
        chunks.append(d.get("text", ""))
    for t in inputs.get("transcript", []):
        chunks.append(t.get("text", ""))
    return [c for c in chunks if c]


def predict(item_id: str, inputs: dict[str, Any]) -> dict[str, Any]:
    """Embed chunks, retrieve top-k, extract with OpenAI."""
    import numpy as np
    from openai import OpenAI  # type: ignore[import-not-found]
    from sentence_transformers import SentenceTransformer  # type: ignore[import-not-found]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = _get_chunks(inputs)
    if not chunks:
        return {"id": item_id, "primitives": [], "edges": []}

    query = inputs.get("question", "")
    chunk_embs = model.encode(chunks)
    query_emb = model.encode([query])
    scores = (chunk_embs @ query_emb.T).squeeze()
    top_k = int(np.argsort(scores)[-3:][::-1].tolist()[0])
    context = "\n\n".join(chunks[: top_k + 1])

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "Extract a conflict analysis graph as JSON."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
        ],
    )
    text = response.choices[0].message.content or "{}"
    try:
        pred = json.loads(text)
    except json.JSONDecodeError:
        pred = {}
    pred["id"] = item_id
    return pred
