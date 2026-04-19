"""Tests for tcgc.adapters.helm — skipped if HELM not installed."""
from __future__ import annotations
import pytest

helm = pytest.importorskip("helm", reason="HELM not installed; skipping adapter test")


def test_helm_scenario_enumerates_5_items() -> None:
    from tcgc.adapters.helm import TCGCScenario
    scenario = TCGCScenario(split="v0.1-sample")
    instances = scenario.get_instances(output_path="")
    assert len(instances) == 5
