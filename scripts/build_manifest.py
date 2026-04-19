"""Regenerate items/manifest.json with SHA-256 hashes of all items."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


def _sha256(path: Path) -> str:
    canonical = json.dumps(json.loads(path.read_text()), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def main() -> None:
    repo_root = Path(__file__).parent.parent
    items_dir = repo_root / "items"
    entries = []
    for p in sorted(items_dir.rglob("tcgc-*.json")):
        rel = p.relative_to(repo_root).as_posix()
        item = json.loads(p.read_text())
        entries.append({"id": item["id"], "path": rel, "sha256": _sha256(p)})
    manifest = {
        "version": "v0.1",
        "generated": datetime.now(UTC).isoformat(),
        "items": entries,
    }
    out = items_dir / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Wrote {out} ({len(entries)} items)")


if __name__ == "__main__":
    main()
