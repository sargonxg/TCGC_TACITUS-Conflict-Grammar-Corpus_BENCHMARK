"""IO helpers for TCGC items and predictions."""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any, cast

import orjson


def load_item(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], orjson.loads(path.read_bytes()))


def load_items(path: Path) -> Iterator[tuple[Path, dict[str, Any]]]:
    if path.is_file():
        yield path, load_item(path)
        return
    if not path.is_dir():
        raise FileNotFoundError(path)
    for p in sorted(path.rglob("tcgc-*.json")):
        yield p, load_item(p)


def write_predictions(predictions: Iterable[dict[str, Any]], out: Path) -> None:
    with out.open("wb") as f:
        for pred in predictions:
            f.write(orjson.dumps(pred))
            f.write(b"\n")


def read_predictions(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("rb") as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if stripped:
                yield cast(dict[str, Any], orjson.loads(stripped))


def dump_json(obj: Any, path: Path, *, indent: int = 2) -> None:
    path.write_text(json.dumps(obj, indent=indent, sort_keys=True, ensure_ascii=False))
