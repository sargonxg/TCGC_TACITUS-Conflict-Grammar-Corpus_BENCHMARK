# Quickstart

Get running in 5 minutes.

## 1. Install

```bash
git clone https://github.com/sargonxg/TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK
cd TCGC_TACITUS-Conflict-Grammar-Corpus_BENCHMARK
pip install -e '.[dev]'
```

## 2. Validate the sample items

```bash
tcgc validate items/v0.1-sample/
```

Expected output: 5 items, 0 errors, 0 warnings.

## 3. Print the schema

```bash
tcgc schema --version v0.1 | python -m json.tool | head -30
```

## 4. Run an identity baseline (gold = prediction)

```python
import json
from pathlib import Path

items_dir = Path("items/v0.1-sample")
preds = []
for p in sorted(items_dir.glob("tcgc-*.json")):
    item = json.loads(p.read_text())
    pred = {"id": item["id"]}
    pred.update(item["gold"])
    preds.append(json.dumps(pred))

Path("predictions.jsonl").write_text("\n".join(preds))
```

```bash
tcgc score predictions.jsonl items/v0.1-sample/ --out scores.json
tcgc report scores.json
```

Expected: 4/5 scorers return 1.0; `llm_judge_anchored` returns 0.0 with a "skipped" note (set `TCGC_RUN_API=1` to enable).

## 5. Generate a system card

```bash
tcgc card scores.json --out SYSTEM_CARD.md
```

Edit `SYSTEM_CARD.md` and you're ready to submit.
