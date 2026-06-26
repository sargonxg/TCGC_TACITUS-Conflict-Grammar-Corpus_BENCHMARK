"""OpenAI client. Wraps the official SDK with the experiments contract."""

from __future__ import annotations

import hashlib
import os
import time

from experiments.llm_vs_typed.clients.base import ModelResponse


class OpenAIClient:
    name: str = "openai"

    def __init__(self, model: str) -> None:
        self.model = model
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Export it before running the experiment, or use "
                "the 'echo' client for a dry run."
            )

    def complete(self, system: str, user: str, *, temperature: float = 0.0) -> ModelResponse:
        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError(
                "Install the experiments extras: `pip install -e '.[experiments]'`."
            ) from exc

        client = OpenAI()
        prompt_hash = hashlib.sha256((system + user).encode()).hexdigest()[:16]
        start = time.monotonic()
        try:
            resp = client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            elapsed_ms = int((time.monotonic() - start) * 1000)
            text = resp.choices[0].message.content or ""
            return ModelResponse(
                text=text,
                model=self.model,
                temperature=temperature,
                elapsed_ms=elapsed_ms,
                prompt_hash=prompt_hash,
                response_hash=hashlib.sha256(text.encode()).hexdigest()[:16],
                api_call_made=True,
            )
        except Exception as exc:  # pragma: no cover - depends on remote API
            elapsed_ms = int((time.monotonic() - start) * 1000)
            return ModelResponse(
                text="",
                model=self.model,
                temperature=temperature,
                elapsed_ms=elapsed_ms,
                prompt_hash=prompt_hash,
                response_hash="",
                api_call_made=True,
                error=f"{type(exc).__name__}: {exc}",
            )
