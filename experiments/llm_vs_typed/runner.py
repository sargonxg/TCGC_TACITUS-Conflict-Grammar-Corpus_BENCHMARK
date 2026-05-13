"""Single-item runner. Given a TCGC item, a client, and a mode, produce a record."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from experiments.llm_vs_typed.clients import ModelClient, ModelResponse

PROMPTS_DIR = Path(__file__).parent / "prompts"


def _render_prompt(template_path: Path, *, question: str, documents: str) -> tuple[str, str]:
    """Render a prompt file into (system, user) strings."""
    body = template_path.read_text(encoding="utf-8")
    # Split on the SYSTEM:/USER: markers.
    if "SYSTEM:" not in body or "USER" not in body:
        raise ValueError(f"Prompt {template_path} must contain SYSTEM: and USER: sections.")
    system_raw, _, user_raw = body.partition("USER")
    system = system_raw.replace("SYSTEM:", "", 1).strip()
    # Drop the parenthetical schema/template line and keep the body.
    user_body = user_raw.split("\n", 1)[1] if "\n" in user_raw else ""
    user = (
        user_body.replace("{question}", question)
        .replace("{documents}", documents)
        .strip()
    )
    return system, user


def _serialise_documents(inputs: dict[str, Any]) -> str:
    """Render the item inputs into a single string for the prompt."""
    parts: list[str] = []
    for d in inputs.get("documents", []):
        title = d.get("title", d.get("id", "doc"))
        kind = d.get("kind", "")
        date = d.get("date", "")
        parts.append(
            f"[{d['id']}] {title}"
            + (f" — {kind}" if kind else "")
            + (f" — {date}" if date else "")
            + "\n"
            + d.get("text", "")
        )
    for m in inputs.get("messages", []):
        parts.append(
            f"[{m.get('id', '')}] {m.get('from', '')} ({m.get('time', '')}): {m.get('text', '')}"
        )
    for t in inputs.get("transcript", []):
        parts.append(
            f"[turn:{t.get('turn')}] {t.get('speaker', '')}: {t.get('text', '')}"
        )
    return "\n\n---\n\n".join(parts)


@dataclass
class RunRecord:
    item_id: str
    task_type: str
    domain: str
    mode: str                 # "vanilla" | "typed"
    client_name: str
    model: str
    temperature: float
    elapsed_ms: int
    api_call_made: bool
    prompt_hash: str
    response_hash: str
    response_text: str
    error: str | None
    timestamp: str            # ISO-8601


def run_one(item: dict[str, Any], client: ModelClient, mode: str, *, temperature: float = 0.0) -> RunRecord:
    """Run a single item through a client in either 'vanilla' or 'typed' mode."""
    if mode not in {"vanilla", "typed"}:
        raise ValueError(f"mode must be 'vanilla' or 'typed', got {mode!r}.")
    template = PROMPTS_DIR / f"{mode}.txt"
    question = item.get("inputs", {}).get("question", "")
    documents = _serialise_documents(item.get("inputs", {}))
    system, user = _render_prompt(template, question=question, documents=documents)
    resp: ModelResponse = client.complete(system, user, temperature=temperature)
    return RunRecord(
        item_id=item["id"],
        task_type=item["task_type"],
        domain=item["domain"],
        mode=mode,
        client_name=client.name,
        model=client.model,
        temperature=resp.temperature,
        elapsed_ms=resp.elapsed_ms,
        api_call_made=resp.api_call_made,
        prompt_hash=resp.prompt_hash,
        response_hash=resp.response_hash,
        response_text=resp.text,
        error=resp.error,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def write_record(record: RunRecord, out_dir: Path) -> Path:
    """Write a record as JSON; return the path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{record.item_id}__{record.mode}.json"
    out_path.write_text(
        json.dumps(asdict(record), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return out_path
