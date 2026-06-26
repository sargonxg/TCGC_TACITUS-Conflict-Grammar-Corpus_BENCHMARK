"""Base protocol for model clients."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ModelResponse:
    """A model response with provenance for honest reporting."""

    text: str
    model: str
    temperature: float
    elapsed_ms: int
    prompt_hash: str
    response_hash: str
    api_call_made: bool
    error: str | None = None


class ModelClient(Protocol):
    """Provider-agnostic model client. Implementations live in `clients/`."""

    name: str
    model: str

    def complete(self, system: str, user: str, *, temperature: float = 0.0) -> ModelResponse:
        """Return a `ModelResponse` for the given system+user prompts."""
        ...
