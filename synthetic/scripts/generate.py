"""Generate synthetic TCGC items using Claude via Anthropic API.

Usage:
    python synthetic/scripts/generate.py \\
        --task-type commitment-tracking \\
        --domain workplace \\
        --count 5 \\
        --out synthetic/generated/

Requires: ANTHROPIC_API_KEY env var and pip install anthropic jinja2
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))


def load_template(task_type: str) -> str:
    slug = task_type.replace("-", "_")
    tpl_path = REPO_ROOT / "synthetic" / "templates" / f"{slug}.j2"
    if not tpl_path.exists():
        return _default_template(task_type)
    return tpl_path.read_text()


def _default_template(task_type: str) -> str:
    return f"""Generate a synthetic TCGC benchmark item for task_type="{task_type}",
domain="{{{{ domain }}}}", actors={{{{ actor_count }}}}, modality={{{{ modality }}}}.
Return ONLY a valid TCGC JSON item. Every primitive must have provenance.
id format: "tcgc-SYNTH-{{{{ '%04d'|format(index) }}}}"
"""


def render(template: str, **kwargs: object) -> str:
    try:
        from jinja2 import Template  # type: ignore[import-not-found]
        return Template(template).render(**kwargs)
    except ImportError:
        return template.replace("{{ domain }}", str(kwargs.get("domain", ""))) \
                       .replace("{{ actor_count }}", str(kwargs.get("actor_count", 2))) \
                       .replace("{{ modality }}", str(kwargs.get("modality", "messages"))) \
                       .replace("{{ index }}", str(kwargs.get("index", 0))) \
                       .replace("{{ date }}", str(kwargs.get("date", date.today())))


def generate_item(prompt: str, model: str = "claude-opus-4-7") -> dict:  # type: ignore[type-arg]
    import anthropic  # type: ignore[import-not-found]
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=1,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text if msg.content else "{}"
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end]) if start >= 0 else {}


def validate_item(item: dict) -> bool:  # type: ignore[type-arg]
    from tcgc.validate import validate_path
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump(item, f)
        tmp = Path(f.name)
    try:
        report = validate_path(tmp)
        return report.ok
    finally:
        tmp.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-type", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--actor-count", type=int, default=2)
    parser.add_argument("--modality", default="messages")
    parser.add_argument("--out", type=Path, default=Path("synthetic/generated"))
    parser.add_argument("--model", default="claude-opus-4-7")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    template = load_template(args.task_type)
    generated = 0
    attempts = 0

    while generated < args.count and attempts < args.count * 3:
        attempts += 1
        prompt = render(template, task_type=args.task_type, domain=args.domain,
                        actor_count=args.actor_count, modality=args.modality,
                        index=generated + 1, date=date.today())
        try:
            item = generate_item(prompt, model=args.model)
            if not item:
                print(f"  attempt {attempts}: empty response, retrying...")
                continue
            item_id = item.get("id", f"tcgc-SYNTH-{generated+1:04d}")
            out_path = args.out / f"{item_id}.json"
            out_path.write_text(json.dumps(item, indent=2, ensure_ascii=False))
            valid = validate_item(item)
            status = "VALID" if valid else "INVALID (needs review)"
            print(f"  {item_id}: {status} → {out_path}")
            generated += 1
        except Exception as e:
            print(f"  attempt {attempts}: error — {e}")

    print(f"\nGenerated {generated}/{args.count} items in {args.out}")
    print("Run: tcgc validate synthetic/generated/ to check all items")


if __name__ == "__main__":
    main()
