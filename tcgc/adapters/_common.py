"""Common adapter utilities."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

from tcgc.io import load_items


def load_split(split: str) -> Iterator[dict[str, Any]]:
    items_dir = Path(__file__).parent.parent.parent / "items" / split
    for _, item in load_items(items_dir):
        yield item
