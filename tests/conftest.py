from __future__ import annotations
import json
from pathlib import Path
import pytest


@pytest.fixture
def sample_items_dir() -> Path:
    return Path(__file__).parent.parent / "items" / "v0.1-sample"


@pytest.fixture
def tcgc_0001() -> dict:  # type: ignore[type-arg]
    path = Path(__file__).parent.parent / "items" / "v0.1-sample" / "tcgc-0001.json"
    return json.loads(path.read_text())
