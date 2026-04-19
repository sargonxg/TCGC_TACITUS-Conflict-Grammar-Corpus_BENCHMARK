"""SYSTEM_CARD stub renderer."""
from __future__ import annotations
from typing import Any
from tcgc.reporting.summary import render_markdown


def render_card(scores: dict[str, Any]) -> str:
    summary = render_markdown(scores)
    return f"""# SYSTEM_CARD

## System overview

- **System name:** [FILL IN]
- **Version:** [FILL IN]
- **Contact:** [FILL IN]
- **Description:** [FILL IN]

## Per-task results

{summary}

## Known limitations

[FILL IN]

## Contact

hello@tacitus.me
"""
