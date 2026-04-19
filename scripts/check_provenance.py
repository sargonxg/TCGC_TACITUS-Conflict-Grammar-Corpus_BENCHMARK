"""Standalone provenance linter — exits nonzero on any orphan reference."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tcgc.validate import validate_path


def main() -> int:
    items_dir = Path(__file__).parent.parent / "items"
    report = validate_path(items_dir)
    orphans = [
        (path, issue)
        for path, issues in report.by_path.items()
        for issue in issues
        if issue.code == "orphan-provenance"
    ]
    if orphans:
        for path, issue in orphans:
            print(f"ORPHAN {path}: {issue.message}", file=sys.stderr)
        return 1
    print(f"OK — {len(report.by_path)} items checked, 0 orphan provenance refs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
