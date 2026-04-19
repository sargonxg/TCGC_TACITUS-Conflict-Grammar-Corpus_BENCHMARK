from __future__ import annotations
import json
import os
from pathlib import Path
import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.environ.get("TCGC_RUN_API") != "1":
        skip = pytest.mark.skip(reason="set TCGC_RUN_API=1 to run API tests")
        for item in items:
            if item.get_closest_marker("requires_api"):
                item.add_marker(skip)


@pytest.fixture
def sample_items_dir() -> Path:
    return Path(__file__).parent.parent / "items" / "v0.1-sample"


@pytest.fixture
def tcgc_0001() -> dict:  # type: ignore[type-arg]
    path = Path(__file__).parent.parent / "items" / "v0.1-sample" / "tcgc-0001.json"
    return json.loads(path.read_text())
