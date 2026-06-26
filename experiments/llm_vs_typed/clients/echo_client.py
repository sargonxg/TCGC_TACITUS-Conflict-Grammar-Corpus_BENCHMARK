"""Echo client — deterministic, no API call. Used for CI smoke tests."""

from __future__ import annotations

import hashlib

from experiments.llm_vs_typed.clients.base import ModelResponse


class EchoClient:
    name: str = "echo"
    model: str = "echo"

    def complete(self, system: str, user: str, *, temperature: float = 0.0) -> ModelResponse:
        text = (
            "ECHO CLIENT (no API call). This is a deterministic stub used for dry runs.\n"
            "To produce a real measurement, configure ANTHROPIC_API_KEY or OPENAI_API_KEY and "
            "pass --client anthropic:<model> or --client openai:<model> to the orchestrator.\n\n"
            f"--- SYSTEM (truncated) ---\n{system[:200]}...\n\n"
            f"--- USER (truncated) ---\n{user[:200]}...\n"
        )
        return ModelResponse(
            text=text,
            model="echo",
            temperature=temperature,
            elapsed_ms=0,
            prompt_hash=hashlib.sha256((system + user).encode()).hexdigest()[:16],
            response_hash=hashlib.sha256(text.encode()).hexdigest()[:16],
            api_call_made=False,
        )
