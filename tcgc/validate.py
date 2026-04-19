"""TCGC item validation: structural (JSON Schema) + semantic."""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import jsonschema
from tcgc.io import load_items
from tcgc.types import TASK_METRIC_MAP

_SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "tcgc-v0.1.json"
_ID_PATTERN = re.compile(r"^tcgc-\d{4}$")


@dataclass
class Issue:
    path: str
    level: str        # 'error' | 'warning'
    code: str
    message: str

    def as_line(self) -> str:
        marker = "✗" if self.level == "error" else "!"
        return f"  {marker} [{self.code}] {self.message}"


@dataclass
class Report:
    by_path: dict[str, list[Issue]] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not any(i.level == "error" for issues in self.by_path.values() for i in issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.level == "warning" for issues in self.by_path.values() for i in issues)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "by_path": {
                p: [{"level": i.level, "code": i.code, "message": i.message} for i in issues]
                for p, issues in self.by_path.items()
            },
        }

    def as_lines(self) -> list[str]:
        lines: list[str] = []
        for p, issues in self.by_path.items():
            if not issues:
                lines.append(f"✓ {p}"); continue
            lines.append(p)
            lines.extend(i.as_line() for i in issues)
        lines.append("")
        lines.append(f"ok={self.ok}  warnings={self.has_warnings}")
        return lines


def load_schema() -> dict[str, Any]:
    return json.loads(_SCHEMA_PATH.read_text())


def validate_path(path: Path) -> Report:
    schema = load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    report = Report()
    for item_path, item in load_items(path):
        report.by_path[str(item_path)] = _validate_item(item, validator)
    return report


def _validate_item(item: dict[str, Any], validator: jsonschema.Draft202012Validator) -> list[Issue]:
    issues: list[Issue] = []
    for err in validator.iter_errors(item):
        issues.append(Issue(
            path="/".join(str(p) for p in err.absolute_path) or "<root>",
            level="error", code="schema", message=err.message,
        ))
    if issues:
        return issues
    if not _ID_PATTERN.match(item["id"]):
        issues.append(Issue(path="id", level="error", code="id-shape",
                            message=f"id {item['id']!r} does not match ^tcgc-\\d{{4}}$"))
    expected = TASK_METRIC_MAP.get(item["task_type"])
    if expected and item["rubric"]["scoring"] != expected:
        issues.append(Issue(
            path="rubric/scoring", level="error", code="task-metric-mismatch",
            message=f"task_type={item['task_type']!r} expects metric {expected!r} but got {item['rubric']['scoring']!r}",
        ))

    input_ids = _collect_input_ids(item.get("inputs", {}))
    gold = item.get("gold", {})
    node_ids = {n.get("id") for n in gold.get("primitives", [])}
    actor_ids = {a.get("id") for a in item.get("inputs", {}).get("actors", [])} | {
        n.get("id") for n in gold.get("primitives", []) if n.get("type") == "actor"
    }

    for i, node in enumerate(gold.get("primitives", [])):
        _check_provenance(node.get("provenance"), input_ids, issues, f"gold/primitives/{i}/provenance")
    for i, edge in enumerate(gold.get("edges", [])):
        _check_provenance(edge.get("provenance"), input_ids, issues, f"gold/edges/{i}/provenance")
        for side in ("from", "to"):
            v = edge.get(side)
            if v not in node_ids and v not in actor_ids:
                issues.append(Issue(
                    path=f"gold/edges/{i}/{side}", level="error", code="edge-endpoint",
                    message=f"edge.{side}={v!r} resolves to neither a gold primitive nor an inputs actor",
                ))

    referenced: set[str] = set()
    for e in gold.get("edges", []):
        referenced.update([e.get("from", ""), e.get("to", "")])
    for i, node in enumerate(gold.get("primitives", [])):
        nid = node.get("id")
        if nid and nid not in referenced and node.get("type") != "actor":
            issues.append(Issue(
                path=f"gold/primitives/{i}", level="warning", code="dangling-node",
                message=f"primitive {nid!r} is not referenced by any edge",
            ))
    return issues


def _collect_input_ids(inputs: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for m in inputs.get("messages", []):
        if "id" in m: ids.add(m["id"])
    for d in inputs.get("documents", []):
        if "id" in d: ids.add(d["id"])
    for t in inputs.get("transcript", []):
        if "turn" in t: ids.add(f"turn:{t['turn']}")
    return ids


def _check_provenance(prov: Any, input_ids: set[str], issues: list[Issue], path: str) -> None:
    if prov is None:
        issues.append(Issue(path=path, level="error", code="missing-provenance",
                            message="provenance is missing"))
        return
    refs = prov if isinstance(prov, list) else [prov]
    for ref in refs:
        if ref in input_ids: continue
        if any(ref.startswith(f"{iid}:") for iid in input_ids): continue
        issues.append(Issue(path=path, level="error", code="orphan-provenance",
                            message=f"provenance ref {ref!r} does not resolve to any id in inputs"))
