"""Zero-shot OpenAI baseline for TCGC."""

import os

if os.environ.get("TCGC_RUN_BASELINES") != "1":  # pragma: no cover
    raise RuntimeError("Set TCGC_RUN_BASELINES=1 to enable this baseline.")

import json
from typing import Any

_SYSTEM_PROMPT = """You are a conflict analysis expert. Given source material and a question,
extract a structured answer as a JSON object matching the gold schema shape.
Return ONLY valid JSON. No explanation."""


def predict(item_id: str, inputs: dict[str, Any]) -> dict[str, Any]:
    """Return a prediction matching the gold shape for the item's task_type."""
    from openai import OpenAI  # type: ignore[import-not-found]

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    user_msg = f"Question: {inputs['question']}\n\nInput:\n{json.dumps(inputs, indent=2)}"
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )
    text = response.choices[0].message.content or "{}"
    try:
        pred = json.loads(text)
    except json.JSONDecodeError:
        pred = {}
    pred["id"] = item_id
    return pred
