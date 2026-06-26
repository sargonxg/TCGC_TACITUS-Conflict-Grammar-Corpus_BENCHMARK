"""Model client implementations for the experiments harness."""

from __future__ import annotations

from experiments.llm_vs_typed.clients.base import ModelClient, ModelResponse
from experiments.llm_vs_typed.clients.echo_client import EchoClient

__all__ = ["EchoClient", "ModelClient", "ModelResponse", "build_client"]


def build_client(spec: str) -> ModelClient:
    """Construct a client from a 'provider:model' spec.

    Examples
    --------
    >>> build_client("echo")  # no API call; for CI/dry-runs
    >>> build_client("anthropic:claude-opus-4-7")
    >>> build_client("openai:gpt-5")
    """
    if spec == "echo":
        return EchoClient()
    if spec.startswith("anthropic:"):
        from experiments.llm_vs_typed.clients.anthropic_client import AnthropicClient

        return AnthropicClient(model=spec.split(":", 1)[1])
    if spec.startswith("openai:"):
        from experiments.llm_vs_typed.clients.openai_client import OpenAIClient

        return OpenAIClient(model=spec.split(":", 1)[1])
    raise ValueError(
        f"Unknown client spec {spec!r}. Use 'echo', 'anthropic:<model>', or 'openai:<model>'."
    )
