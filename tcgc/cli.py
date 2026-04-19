"""The `tcgc` command-line interface (Typer)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

app = typer.Typer(
    name="tcgc",
    help="TACITUS Conflict Grammar Corpus CLI.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.command()
def validate(
    path: Annotated[Path, typer.Argument(help="Item file or directory")],
    fmt: Annotated[str, typer.Option("--format", help="'pretty' or 'json'")] = "pretty",
) -> None:
    """Validate one or more TCGC items."""
    from tcgc.validate import validate_path

    report = validate_path(path)
    if fmt == "json":
        console.print_json(data=report.as_dict())
    else:
        for line in report.as_lines():
            console.print(line)
    raise typer.Exit(code=0 if report.ok else 1)


@app.command()
def schema(version: Annotated[str, typer.Option(help="Schema version")] = "v0.1") -> None:
    """Print the canonical JSON Schema."""
    path = Path(__file__).parent.parent / "schema" / f"tcgc-{version}.json"
    if not path.exists():
        console.print(f"[red]Schema version {version!r} not found at {path}[/red]")
        raise typer.Exit(code=1)
    console.print_json(data=json.loads(path.read_text()))


@app.command("score")
def score_cmd(
    predictions: Annotated[Path, typer.Argument(help="JSONL file of predictions")],
    items_dir: Annotated[Path, typer.Argument(help="Directory of item files")],
    out: Annotated[Path, typer.Option("--out")] = Path("scores.json"),
) -> None:
    """Score a predictions file against a directory of items."""
    from tcgc.score import score_predictions

    result = score_predictions(predictions, items_dir)
    out.write_text(json.dumps(result, indent=2))
    console.print(f"[green]Wrote {out}[/green]")


@app.command()
def run(
    system: Annotated[str, typer.Option("--system", help="module:callable")],
    items_dir: Annotated[Path, typer.Argument()],
    out: Annotated[Path, typer.Option("--out")],
) -> None:
    """Run a callable over every item, write predictions.jsonl."""
    import importlib

    mod_name, func_name = system.split(":")
    fn = getattr(importlib.import_module(mod_name), func_name)
    from tcgc.io import load_items, write_predictions

    preds = []
    for _, item in load_items(items_dir):
        pred = fn(item["id"], item["inputs"])
        pred.setdefault("id", item["id"])
        preds.append(pred)
    write_predictions(preds, out)
    console.print(f"[green]Wrote {len(preds)} predictions to {out}[/green]")


@app.command()
def report(scores: Annotated[Path, typer.Argument()]) -> None:
    """Pretty per-task / per-domain breakdown."""
    from tcgc.reporting.summary import render_markdown

    data = json.loads(scores.read_text())
    console.print(render_markdown(data))


@app.command()
def card(
    scores: Annotated[Path, typer.Argument()],
    out: Annotated[Path, typer.Option("--out")] = Path("SYSTEM_CARD.md"),
) -> None:
    """Emit a SYSTEM_CARD.md stub from a scores file."""
    from tcgc.reporting.card import render_card

    data = json.loads(scores.read_text())
    out.write_text(render_card(data))
    console.print(f"[green]Wrote {out}[/green]")


@app.command()
def manifest() -> None:
    """Regenerate items/manifest.json."""
    from scripts.build_manifest import main as build_manifest

    build_manifest()


if __name__ == "__main__":  # pragma: no cover
    app()
