# CLAUDE.md — TCGC v0.1 Build Spec

> **For Claude Code.** This single file is the complete specification for the **TACITUS Conflict Grammar Corpus (TCGC) v0.1** repository. Drop this file into an empty repo and execute it.
>
> **Maintainer:** Giulio Catanzariti · `giuliocatanzariti@gmail.com` · [tacitus.me/research/tcgc](https://www.tacitus.me/research/tcgc)
>
> **Your job:** create every file specified below, in the paths specified below, with the content specified below. Where I give you complete code, transcribe it. Where I give you a spec, implement to the spec. Where I give you open-ended instructions ("write worked examples"), use judgment. Do not reshape the architecture.

---

## 0. Prime directive

Build a public, academic-grade benchmark harness: schema, 5 sample items, 5 scorers, CLI, adapters for HELM and lm-eval-harness, tests, CI, docs, governance files. The schema, the canonical item `tcgc-0001`, the 14 task types, the 7 domains, and the 5 metrics are **fixed** by the website at `https://www.tacitus.me/research/tcgc`. Do not invent. Do not rename. Do not extend the ontology.

Python 3.11+. Typed strict (`mypy --strict`). Tested (≥ 90% coverage on `tcgc/`). Linted (`ruff`). Documented (`mkdocs-material`). Author on every file: `Giulio Catanzariti <giuliocatanzariti@gmail.com>`.

---

## 1. Ground rules

1. **Transcribe, don't improvise.** Every file below with a content block gets that content verbatim. Every file below with a spec gets an implementation to that spec.
2. **No paid API calls in CI.** Anything that calls OpenAI/Anthropic is behind `@pytest.mark.requires_api` and the env var `TCGC_RUN_API=1`. Default CI runs skip them.
3. **Conventional commits.** `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`. Imperative mood. Small commits.
4. **IDs.** Items are `tcgc-NNNN` zero-padded to four digits. Regex: `^tcgc-\d{4}$`.
5. **Per-task reporting.** Never collapse metrics into a single headline number except inside an explicitly-labeled `overall` field. The website is firm on this.
6. **Website copy.** Do not paraphrase verbatim blocks from the site without a `<!-- source: https://www.tacitus.me/research/tcgc -->` marker.
7. **Never reproduce extended quotes from other sources.** If you cite papers, paraphrase.
8. **No web UI. No training code.** This is a benchmark harness.

---

## 2. Target directory tree

Build toward exactly this. Do not add top-level directories not listed without a note in the PR description.

```
tcgc/
├── CLAUDE.md                           # this file
├── README.md
├── LICENSE                             # CC-BY-NC-SA 4.0
├── DATA_USE_AGREEMENT.md               # full-corpus DUA
├── DATASHEET.md                        # Gebru et al. (2021) structure
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md                  # Contributor Covenant 2.1
├── CITATION.cff
├── CHANGELOG.md                        # Keep a Changelog
├── pyproject.toml
├── uv.lock                             # committed after first `uv sync`
├── .gitignore
├── .editorconfig
├── .pre-commit-config.yaml
├── mkdocs.yml
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── release.yml
│   │   ├── leaderboard.yml
│   │   └── docs.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── task_type_proposal.yml
│   │   └── submission.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
├── schema/
│   ├── tcgc-v0.1.json                  # canonical
│   ├── submission-v0.1.json            # leaderboard submission shape
│   └── README.md
├── items/
│   ├── v0.1-sample/
│   │   ├── tcgc-0001.json
│   │   ├── tcgc-0002.json
│   │   ├── tcgc-0003.json
│   │   ├── tcgc-0004.json
│   │   └── tcgc-0005.json
│   ├── manifest.json
│   └── README.md
├── tcgc/
│   ├── __init__.py
│   ├── types.py
│   ├── io.py
│   ├── validate.py
│   ├── score.py
│   ├── cli.py
│   ├── ontology/
│   │   ├── __init__.py
│   │   ├── aco.py
│   │   └── edges.py
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── graph_overlap.py
│   │   ├── provenance_f1.py
│   │   ├── kendall_tau.py
│   │   ├── contradiction_pair_f1.py
│   │   ├── llm_judge_anchored.py
│   │   └── anchors/
│   │       └── v0.1.jsonl
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── _common.py
│   │   ├── helm.py
│   │   └── lm_eval.py
│   └── reporting/
│       ├── __init__.py
│       ├── card.py
│       └── summary.py
├── baselines/
│   ├── __init__.py
│   ├── zeroshot_openai.py
│   ├── zeroshot_anthropic.py
│   ├── rag_baseline.py
│   └── graphrag_baseline.py
├── tests/
│   ├── conftest.py
│   ├── test_schema.py
│   ├── test_io.py
│   ├── test_ontology.py
│   ├── test_validate.py
│   ├── test_scoring_graph_overlap.py
│   ├── test_scoring_provenance_f1.py
│   ├── test_scoring_kendall_tau.py
│   ├── test_scoring_contradiction_pair_f1.py
│   ├── test_scoring_llm_judge_anchored.py
│   ├── test_cli.py
│   ├── test_adapters_helm.py
│   └── test_adapters_lm_eval.py
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   ├── task-types.md
│   ├── domains.md
│   ├── metrics.md
│   ├── methodology.md
│   ├── agreement.md
│   ├── open-questions.md
│   ├── submission-guide.md
│   ├── leaderboard.md
│   └── roadmap.md
├── submissions/
│   └── README.md
├── leaderboard/
│   └── v0.1-sample.json
└── scripts/
    ├── build_manifest.py
    ├── check_provenance.py
    └── bootstrap.sh
```

---

## 3. The Agentic Conflict Ontology (ACO)

**Locked for v0.1.** No extensions, no aliases.

### 3.1 Primitives (8)

| Primitive | String | Definition (v0.1, do not paraphrase) |
|---|---|---|
| Actor | `"actor"` | Any party capable of holding an interest or making a claim: individuals, organizations, states, coalitions. |
| Claim | `"claim"` | An asserted fact, evaluation, or normative statement attributed to an actor. |
| Interest | `"interest"` | An underlying goal or need that motivates claims and positions (Fisher/Ury distinction). |
| Constraint | `"constraint"` | A rule, norm, or structural limit shaping feasible outcomes. |
| Leverage | `"leverage"` | A resource, dependency, or capability that shifts bargaining power. |
| Commitment | `"commitment"` | A promised future action, with a subject and typically a deadline. |
| Event | `"event"` | A dated or orderable occurrence in the world. |
| Narrative | `"narrative"` | A coherent framing across multiple claims, attributable to an actor. |

### 3.2 Edge types (18)

Closed set. Implement as a `StrEnum` in `tcgc/ontology/edges.py`:

```
ASSERTED, DENIED, ACKNOWLEDGED, ACKNOWLEDGED_AMBIGUOUSLY,
DENIES_SCOPE, COMMITS_TO, REVOKES, BLOCKS, ENABLES,
CAUSES, PRECEDES, CONTRADICTS, SUPPORTS, CITES,
HOLDS_INTEREST, FRAMES, LEVERAGES, CONSTRAINED_BY
```

Every edge carries a `provenance` field pointing at a source span. Missing provenance fails validation.

### 3.3 Partial-credit type similarity

When a predicted edge type is close to but not identical to the gold type, award partial credit per the table in `tcgc/ontology/edges.py`. All diagonal entries 1.0. Every nonzero off-diagonal is annotated with a rationale. The v0.1 values:

| Pair | Similarity | Rationale |
|---|---|---|
| `ASSERTED` ↔ `ACKNOWLEDGED` | 0.5 | Same kind, different speaker role. |
| `ACKNOWLEDGED` ↔ `ACKNOWLEDGED_AMBIGUOUSLY` | 0.75 | Same kind with hedge. |
| `DENIED` ↔ `DENIES_SCOPE` | 0.5 | Scope denial is narrower. |
| `BLOCKS` ↔ `CONSTRAINED_BY` | 0.4 | Reverse-direction near-synonym; direction matters downstream. |
| `ENABLES` ↔ `CAUSES` | 0.5 | CAUSES is strictly stronger. |
| `COMMITS_TO` ↔ `ASSERTED` | 0.5 | Commitment vs. speech act — half credit reflects the boundary this benchmark specifically tests. |

All other off-diagonal entries are 0.

---

## 4. Task types (14)

| # | `task_type` | Metric |
|---|---|---|
| 1 | `actor-resolution` | `graph_overlap` |
| 2 | `claim-extraction` | `graph_overlap` |
| 3 | `interest-extraction` | `llm_judge_anchored` |
| 4 | `constraint-extraction` | `graph_overlap` |
| 5 | `leverage-mapping` | `graph_overlap` |
| 6 | `commitment-tracking` | `graph_overlap` |
| 7 | `event-ordering` | `kendall_tau` |
| 8 | `narrative-drift` | `llm_judge_anchored` |
| 9 | `causal-chain` | `graph_overlap` |
| 10 | `contradiction-detection` | `contradiction_pair_f1` |
| 11 | `provenance-attribution` | `provenance_f1` |
| 12 | `commitment-claim-mismatch` | `graph_overlap` |
| 13 | `position-interest-separation` | `llm_judge_anchored` |
| 14 | `cross-document-synthesis` | `graph_overlap` |

Enforce the binding in `tcgc/validate.py` via `TASK_METRIC_MAP` in `tcgc/types.py`. A mismatch between `item.task_type` and `item.rubric.scoring` is a validation error.

---

## 5. Domains (7)

`workplace`, `commercial`, `governance`, `peace-process`, `policy`, `family`, `diplomatic`.

Scope statements for `docs/domains.md` (transcribe from the website verbatim, mark with the source comment):

- **workplace** — HR grievances, performance disputes, promotion blocks
- **commercial** — Contract breach, vendor dispute, joint-venture friction
- **governance** — Board disagreement, mandate conflict, committee deadlock
- **peace-process** — Ceasefire, DDR, political-track multilateral negotiation
- **policy** — Regulatory contestation, stakeholder reception, public-consultation aftermath
- **family** — Inheritance, custody arrangement, intergenerational wealth dispute
- **diplomatic** — State-to-state friction, border incident, multilateral block formation

---

## 6. Metrics (5) — implementation contracts

Every scorer in `tcgc/scoring/*.py` exports:

```python
def score(gold: dict, pred: dict) -> ScoreResult: ...
```

where `ScoreResult` is a dataclass with `value: float ∈ [0, 1]`, `components: dict[str, float]`, `notes: list[str]`. Registry in `tcgc/scoring/__init__.py`.

### 6.1 `graph_overlap`
Jaccard over the typed subgraph. Node and edge Jaccards computed separately, weighted mean (default 0.4 nodes, 0.6 edges — edges carry most of the structural signal). Near-miss edge types get partial credit via §3.3. Node equality: same `(type, id)`. Edge equality: same `(from, to)` pair; type handled via similarity. See reference implementation in §10.

### 6.2 `provenance_f1`
F1 over `(primitive_id, provenance_ref)` pairs. Exact id match = 1.0; schema allows character-span dicts (`{"doc","start","end"}`) scored by IoU for future items. Every primitive in `pred` must reference a span present in `inputs`; orphan provenance is a 0 for that primitive and a diagnostic note.

### 6.3 `kendall_tau`
`scipy.stats.kendalltau(variant='b')` over gold `order` vs. predicted `order`. Normalize `[-1, 1]` → `[0, 1]` via `(τ + 1) / 2`. Missing events in pred get worst-case rank. NaN → 0.0 with note.

### 6.4 `contradiction_pair_f1`
F1 over unordered `(claim_a, claim_b)` pairs. Materiality weighting: material = 1.0, cosmetic = 0.25, in both precision and recall. Unweighted F1 exposed in `components["f1_unweighted"]`.

### 6.5 `llm_judge_anchored`
LLM-judge with a fixed prompt, temperature 0, passed through isotonic regression fitted on an anchor set of 20+ `(raw, human_score)` triples at `tcgc/scoring/anchors/v0.1.jsonl`. Gated behind `TCGC_RUN_API=1`. Cite Zheng et al. (2023) "Judging LLM-as-a-Judge"; docstring explicitly states position/verbosity/self-preference bias as known failure modes.

---

## 7. Canonical JSON Schema — `schema/tcgc-v0.1.json`

Transcribe exactly.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tacitus.me/research/tcgc/schema/tcgc-v0.1.json",
  "title": "TACITUS Conflict Grammar Corpus item — v0.1",
  "description": "Schema for a single TCGC benchmark item. See https://www.tacitus.me/research/tcgc.",
  "type": "object",
  "required": ["id", "task_type", "domain", "inputs", "gold", "rubric"],
  "additionalProperties": false,
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^tcgc-\\d{4}$"
    },
    "task_type": {
      "type": "string",
      "enum": [
        "actor-resolution", "claim-extraction", "interest-extraction",
        "constraint-extraction", "leverage-mapping", "commitment-tracking",
        "event-ordering", "narrative-drift", "causal-chain",
        "contradiction-detection", "provenance-attribution",
        "commitment-claim-mismatch", "position-interest-separation",
        "cross-document-synthesis"
      ]
    },
    "domain": {
      "type": "string",
      "enum": ["workplace","commercial","governance","peace-process","policy","family","diplomatic"]
    },
    "license": { "type": "string" },
    "source": {
      "type": "object",
      "properties": {
        "collection": { "type": "string" },
        "collected_on": { "type": "string", "format": "date" },
        "annotators": { "type": "array", "items": { "type": "string" } },
        "inter_annotator_kappa": { "type": "number", "minimum": -1, "maximum": 1 }
      },
      "additionalProperties": false
    },
    "inputs": {
      "type": "object",
      "required": ["question"],
      "additionalProperties": false,
      "anyOf": [
        { "required": ["messages"] },
        { "required": ["documents"] },
        { "required": ["transcript"] }
      ],
      "properties": {
        "messages": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["from", "text"],
            "additionalProperties": false,
            "properties": {
              "id": {"type":"string"}, "day":{"type":"integer","minimum":0},
              "time":{"type":"string"}, "date":{"type":"string","format":"date"},
              "from":{"type":"string"}, "to":{"type":"string"}, "text":{"type":"string"}
            }
          }
        },
        "documents": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "text"],
            "additionalProperties": false,
            "properties": {
              "id":{"type":"string"}, "title":{"type":"string"}, "kind":{"type":"string"},
              "date":{"type":"string","format":"date"}, "author":{"type":"string"}, "text":{"type":"string"}
            }
          }
        },
        "transcript": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["speaker", "text"],
            "additionalProperties": false,
            "properties": {
              "turn":{"type":"integer","minimum":0}, "speaker":{"type":"string"},
              "time":{"type":"string"}, "text":{"type":"string"}
            }
          }
        },
        "actors": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "label"],
            "additionalProperties": false,
            "properties": {
              "id":{"type":"string"}, "label":{"type":"string"},
              "aliases":{"type":"array","items":{"type":"string"}}
            }
          }
        },
        "question": { "type": "string" },
        "dates_stripped": { "type": "boolean" }
      }
    },
    "gold": {
      "type": "object",
      "additionalProperties": true,
      "properties": {
        "primitives": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "type"],
            "additionalProperties": true,
            "properties": {
              "id":{"type":"string"},
              "type":{"type":"string","enum":["actor","claim","interest","constraint","leverage","commitment","event","narrative"]},
              "label":{"type":"string"}, "subject":{"type":"string"}, "deadline":{"type":"string"},
              "status":{"type":"string"}, "materiality":{"type":"string","enum":["material","cosmetic"]},
              "provenance":{"type":["string","array"],"items":{"type":"string"}},
              "attributes":{"type":"object","additionalProperties":true}
            }
          }
        },
        "edges": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["from", "to", "type", "provenance"],
            "additionalProperties": false,
            "properties": {
              "from":{"type":"string"}, "to":{"type":"string"},
              "type":{"type":"string","enum":[
                "ASSERTED","DENIED","ACKNOWLEDGED","ACKNOWLEDGED_AMBIGUOUSLY",
                "DENIES_SCOPE","COMMITS_TO","REVOKES","BLOCKS","ENABLES",
                "CAUSES","PRECEDES","CONTRADICTS","SUPPORTS","CITES",
                "HOLDS_INTEREST","FRAMES","LEVERAGES","CONSTRAINED_BY"
              ]},
              "provenance":{"type":["string","array"],"items":{"type":"string"}},
              "attributes":{"type":"object","additionalProperties":true}
            }
          }
        },
        "order": { "type": "array", "items": {"type":"string"} },
        "contradictions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["claim_a","claim_b","materiality"],
            "additionalProperties": false,
            "properties": {
              "claim_a":{"type":"string"}, "claim_b":{"type":"string"},
              "materiality":{"type":"string","enum":["material","cosmetic"]},
              "rationale":{"type":"string"}
            }
          }
        },
        "commitment_id":{"type":"string"}, "subject":{"type":"string"},
        "deadline":{"type":"string"}, "status":{"type":"string"}
      }
    },
    "rubric": {
      "type": "object",
      "required": ["scoring"],
      "additionalProperties": false,
      "properties": {
        "scoring":{"type":"string","enum":["graph_overlap","provenance_f1","kendall_tau","contradiction_pair_f1","llm_judge_anchored"]},
        "graph_overlap_target":{"type":"number","minimum":0,"maximum":1},
        "provenance_f1_target":{"type":"number","minimum":0,"maximum":1},
        "kendall_tau_target":{"type":"number","minimum":0,"maximum":1},
        "contradiction_pair_f1_target":{"type":"number","minimum":0,"maximum":1},
        "llm_judge_anchored_target":{"type":"number","minimum":0,"maximum":1},
        "node_weight":{"type":"number","minimum":0,"maximum":1,"default":0.4},
        "edge_weight":{"type":"number","minimum":0,"maximum":1,"default":0.6}
      }
    }
  }
}
```

---

## 8. The 5 sample items

Transcribe verbatim into `items/v0.1-sample/`. Item #0001 is the website's published anchor — do not alter.

### 8.1 `items/v0.1-sample/tcgc-0001.json`

```json
{
  "id": "tcgc-0001",
  "task_type": "commitment-tracking",
  "domain": "workplace",
  "license": "CC-BY-NC-SA-4.0",
  "source": {
    "collection": "v0.1-sample",
    "collected_on": "2026-03-14",
    "annotators": ["A1", "A2"],
    "inter_annotator_kappa": 0.82
  },
  "inputs": {
    "messages": [
      { "id": "msg1", "day": 1, "time": "Mon 09:14", "from": "Sam",
        "text": "So we're agreed — you own the Q4 launch deck content, I handle design. Lock it in by Thursday?" },
      { "id": "msg2", "day": 1, "time": "Mon 09:47", "from": "Alex",
        "text": "Sounds good. I'll pick it up after the Jenkins pitch." },
      { "id": "msg3", "day": 4, "time": "Thu 09:02", "from": "Alex",
        "text": "I never said I'd own it. Just help." }
    ],
    "question": "Was there a commitment on content ownership, when was it made, and who asserted it?"
  },
  "gold": {
    "commitment_id": "cm1",
    "subject": "Q4 launch deck content",
    "deadline": "Thursday",
    "status": "contested",
    "primitives": [
      { "id": "Sam",  "type": "actor", "label": "Sam",  "provenance": "msg1" },
      { "id": "Alex", "type": "actor", "label": "Alex", "provenance": "msg2" },
      { "id": "cm1", "type": "commitment",
        "subject": "Q4 launch deck content", "deadline": "Thursday", "status": "contested",
        "provenance": ["msg1","msg2","msg3"] }
    ],
    "edges": [
      { "from": "Sam",  "to": "cm1", "type": "ASSERTED",                 "provenance": "msg1" },
      { "from": "Alex", "to": "cm1", "type": "ACKNOWLEDGED_AMBIGUOUSLY", "provenance": "msg2" },
      { "from": "Alex", "to": "cm1", "type": "DENIES_SCOPE",             "provenance": "msg3" }
    ]
  },
  "rubric": {
    "scoring": "graph_overlap",
    "graph_overlap_target": 0.85,
    "provenance_f1_target": 1.0
  }
}
```

### 8.2 `items/v0.1-sample/tcgc-0002.json` — `event-ordering`, peace-process

```json
{
  "id": "tcgc-0002",
  "task_type": "event-ordering",
  "domain": "peace-process",
  "license": "CC-BY-NC-SA-4.0",
  "source": {
    "collection": "v0.1-sample",
    "collected_on": "2026-03-14",
    "annotators": ["A1","A3"],
    "inter_annotator_kappa": 0.91
  },
  "inputs": {
    "dates_stripped": true,
    "documents": [
      { "id": "doc1", "title": "Track-II summary memo", "kind": "memo",
        "text": "The Juba-based delegation returned after the preparatory consultations in Entebbe, though only once the mediation panel had circulated the revised agenda. Earlier still, both principals had met bilaterally on the margins of a regional summit — that encounter is what unblocked the panel's work in the first place. The joint communiqué was issued only after the delegation returned to Juba and briefed the Council." }
    ],
    "question": "Reconstruct the chronological order of the five events mentioned (e1..e5) from earliest to latest. Dates have been stripped from the source."
  },
  "gold": {
    "primitives": [
      { "id": "e1", "type": "event", "label": "bilateral principals meeting at regional summit", "provenance": "doc1" },
      { "id": "e2", "type": "event", "label": "mediation panel circulates revised agenda",      "provenance": "doc1" },
      { "id": "e3", "type": "event", "label": "preparatory consultations in Entebbe",           "provenance": "doc1" },
      { "id": "e4", "type": "event", "label": "Juba-based delegation returns",                  "provenance": "doc1" },
      { "id": "e5", "type": "event", "label": "joint communiqué issued",                         "provenance": "doc1" }
    ],
    "edges": [
      { "from": "e1", "to": "e2", "type": "PRECEDES", "provenance": "doc1" },
      { "from": "e2", "to": "e3", "type": "PRECEDES", "provenance": "doc1" },
      { "from": "e3", "to": "e4", "type": "PRECEDES", "provenance": "doc1" },
      { "from": "e4", "to": "e5", "type": "PRECEDES", "provenance": "doc1" }
    ],
    "order": ["e1","e2","e3","e4","e5"]
  },
  "rubric": {
    "scoring": "kendall_tau",
    "kendall_tau_target": 0.80
  }
}
```

### 8.3 `items/v0.1-sample/tcgc-0003.json` — `contradiction-detection`, governance

```json
{
  "id": "tcgc-0003",
  "task_type": "contradiction-detection",
  "domain": "governance",
  "license": "CC-BY-NC-SA-4.0",
  "source": {
    "collection": "v0.1-sample",
    "collected_on": "2026-03-14",
    "annotators": ["A2","A4"],
    "inter_annotator_kappa": 0.76
  },
  "inputs": {
    "documents": [
      { "id": "bd-minutes-q1", "title": "Board minutes, Q1", "kind": "minutes", "date": "2025-03-18",
        "text": "The Chair opened by confirming that the strategic pivot toward commercial customers had been approved unanimously at the October retreat. Director Park observed that the retreat had produced no formal resolution on customer segment." },
      { "id": "bd-minutes-q2", "title": "Board minutes, Q2", "kind": "minutes", "date": "2025-06-12",
        "text": "The Chair reported that Q1 results were ahead of plan. Director Ito noted the agenda would be distributed 72 hours in advance, consistent with the new governance protocol; Director Park noted that she had received the pack the morning of." }
    ],
    "question": "Identify contradicting claims across the two sets of minutes. Flag which are material and which are cosmetic."
  },
  "gold": {
    "primitives": [
      { "id": "c1", "type": "claim", "label": "strategic pivot approved unanimously at October retreat",   "provenance": "bd-minutes-q1" },
      { "id": "c2", "type": "claim", "label": "retreat produced no formal resolution on customer segment","provenance": "bd-minutes-q1" },
      { "id": "c3", "type": "claim", "label": "agenda distributed 72 hours in advance",                   "provenance": "bd-minutes-q2" },
      { "id": "c4", "type": "claim", "label": "pack received the morning of",                             "provenance": "bd-minutes-q2" }
    ],
    "edges": [
      { "from": "c1", "to": "c2", "type": "CONTRADICTS", "provenance": "bd-minutes-q1" },
      { "from": "c3", "to": "c4", "type": "CONTRADICTS", "provenance": "bd-minutes-q2" }
    ],
    "contradictions": [
      { "claim_a": "c1", "claim_b": "c2", "materiality": "material",
        "rationale": "Disagreement about whether a strategic decision was made bears directly on the board's authority and on downstream commitments." },
      { "claim_a": "c3", "claim_b": "c4", "materiality": "cosmetic",
        "rationale": "Procedural timing disagreement that does not affect the substance of decisions." }
    ]
  },
  "rubric": {
    "scoring": "contradiction_pair_f1",
    "contradiction_pair_f1_target": 0.85
  }
}
```

### 8.4 `items/v0.1-sample/tcgc-0004.json` — `interest-extraction`, commercial

```json
{
  "id": "tcgc-0004",
  "task_type": "interest-extraction",
  "domain": "commercial",
  "license": "CC-BY-NC-SA-4.0",
  "source": {
    "collection": "v0.1-sample",
    "collected_on": "2026-03-14",
    "annotators": ["A1","A2","A3"],
    "inter_annotator_kappa": 0.64
  },
  "inputs": {
    "transcript": [
      { "turn": 1, "speaker": "Vendor", "text": "We cannot move below the list price. It is a matter of principle for us at this stage of the quarter." },
      { "turn": 2, "speaker": "Buyer",  "text": "Then we will have to shelve the rollout. We committed internally to a per-seat cost ceiling and I am not able to go above it." },
      { "turn": 3, "speaker": "Vendor", "text": "A pilot could be structured differently. Smaller footprint, executive visibility, an expansion option." },
      { "turn": 4, "speaker": "Buyer",  "text": "Our board wants to see credible traction in this category before the next funding round." }
    ],
    "question": "Extract the underlying interests of each party, distinct from their stated positions. Interests are inferred; positions are stated."
  },
  "gold": {
    "primitives": [
      { "id": "vendor", "type": "actor", "label": "Vendor", "provenance": "turn:1" },
      { "id": "buyer",  "type": "actor", "label": "Buyer",  "provenance": "turn:2" },
      { "id": "pos_vendor", "type": "claim", "label": "position: hold list price", "provenance": "turn:1" },
      { "id": "pos_buyer",  "type": "claim", "label": "position: refuse above per-seat ceiling", "provenance": "turn:2" },
      { "id": "int_vendor_quarter", "type": "interest",
        "label": "protect quarterly revenue-recognition optics and precedent for enterprise deals",
        "provenance": ["turn:1","turn:3"] },
      { "id": "int_vendor_expand",  "type": "interest",
        "label": "open a channel for future expansion revenue", "provenance": "turn:3" },
      { "id": "int_buyer_board",    "type": "interest",
        "label": "credible category traction to support next funding round", "provenance": "turn:4" },
      { "id": "int_buyer_internal", "type": "interest",
        "label": "honor internal commitment to per-seat cost discipline", "provenance": "turn:2" }
    ],
    "edges": [
      { "from": "vendor", "to": "pos_vendor",         "type": "ASSERTED",       "provenance": "turn:1" },
      { "from": "buyer",  "to": "pos_buyer",          "type": "ASSERTED",       "provenance": "turn:2" },
      { "from": "vendor", "to": "int_vendor_quarter", "type": "HOLDS_INTEREST", "provenance": "turn:1" },
      { "from": "vendor", "to": "int_vendor_expand",  "type": "HOLDS_INTEREST", "provenance": "turn:3" },
      { "from": "buyer",  "to": "int_buyer_board",    "type": "HOLDS_INTEREST", "provenance": "turn:4" },
      { "from": "buyer",  "to": "int_buyer_internal", "type": "HOLDS_INTEREST", "provenance": "turn:2" }
    ]
  },
  "rubric": {
    "scoring": "llm_judge_anchored",
    "llm_judge_anchored_target": 0.70
  }
}
```

### 8.5 `items/v0.1-sample/tcgc-0005.json` — `provenance-attribution`, diplomatic

```json
{
  "id": "tcgc-0005",
  "task_type": "provenance-attribution",
  "domain": "diplomatic",
  "license": "CC-BY-NC-SA-4.0",
  "source": {
    "collection": "v0.1-sample",
    "collected_on": "2026-03-14",
    "annotators": ["A2","A4"],
    "inter_annotator_kappa": 0.88
  },
  "inputs": {
    "documents": [
      { "id": "press-briefing", "title": "Press briefing, Foreign Ministry of State A",
        "kind": "briefing", "date": "2026-02-03",
        "text": "The Spokesperson reiterated that State A will not accept any unilateral demarcation of the maritime boundary. A question on whether consultations with State B had resumed was declined. The Spokesperson added that cooperation with State C on fisheries remains \"unaffected by recent tensions\"." },
      { "id": "mfa-cable", "title": "Cable, Mission of State B",
        "kind": "cable", "date": "2026-02-05",
        "text": "State B's Deputy Permanent Representative stated in the corridor that \"technical contacts have continued throughout\" and characterized State A's posture as \"rhetorical\". The DPR declined to confirm a date for the next political-level meeting." }
    ],
    "question": "Extract every attributable claim in these two documents and bind it to its exact source span."
  },
  "gold": {
    "primitives": [
      { "id": "state-a-mfa", "type": "actor", "label": "State A Foreign Ministry Spokesperson", "provenance": "press-briefing" },
      { "id": "state-b-dpr", "type": "actor", "label": "State B Deputy Permanent Representative", "provenance": "mfa-cable" },
      { "id": "c1", "type": "claim", "label": "State A will not accept unilateral demarcation of the maritime boundary", "provenance": "press-briefing:spans:1" },
      { "id": "c2", "type": "claim", "label": "cooperation with State C on fisheries remains unaffected by recent tensions", "provenance": "press-briefing:spans:2" },
      { "id": "c3", "type": "claim", "label": "technical contacts have continued throughout", "provenance": "mfa-cable:spans:1" },
      { "id": "c4", "type": "claim", "label": "State A's posture characterized as rhetorical", "provenance": "mfa-cable:spans:2" }
    ],
    "edges": [
      { "from": "state-a-mfa", "to": "c1", "type": "ASSERTED", "provenance": "press-briefing:spans:1" },
      { "from": "state-a-mfa", "to": "c2", "type": "ASSERTED", "provenance": "press-briefing:spans:2" },
      { "from": "state-b-dpr", "to": "c3", "type": "ASSERTED", "provenance": "mfa-cable:spans:1" },
      { "from": "state-b-dpr", "to": "c4", "type": "ASSERTED", "provenance": "mfa-cable:spans:2" }
    ]
  },
  "rubric": {
    "scoring": "provenance_f1",
    "provenance_f1_target": 0.95
  }
}
```

---

## 9. Python package — reference implementations

### 9.1 `pyproject.toml`

```toml
[build-system]
requires = ["hatchling>=1.24"]
build-backend = "hatchling.build"

[project]
name = "tcgc"
version = "0.1.0"
description = "TACITUS Conflict Grammar Corpus — an open benchmark for conflict reasoning."
readme = "README.md"
requires-python = ">=3.11"
license = { text = "CC-BY-NC-SA-4.0" }
authors = [{ name = "Giulio Catanzariti", email = "giuliocatanzariti@gmail.com" }]
maintainers = [{ name = "Giulio Catanzariti", email = "giuliocatanzariti@gmail.com" }]
keywords = ["benchmark", "nlp", "conflict", "ontology", "neurosymbolic", "evaluation"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
dependencies = [
    "jsonschema>=4.22",
    "pydantic>=2.7",
    "typer>=0.12",
    "rich>=13.7",
    "scipy>=1.13",
    "numpy>=1.26",
    "orjson>=3.10",
]

[project.optional-dependencies]
dev = ["pytest>=8.2", "pytest-cov>=5.0", "hypothesis>=6.100", "mypy>=1.10", "ruff>=0.4", "pre-commit>=3.7"]
docs = ["mkdocs>=1.6", "mkdocs-material>=9.5", "mkdocs-gen-files>=0.5"]
baselines = ["openai>=1.30", "anthropic>=0.28", "sentence-transformers>=2.7", "scikit-learn>=1.4"]
adapters = ["lm-eval>=0.4"]

[project.urls]
Homepage = "https://www.tacitus.me/research/tcgc"
Repository = "https://github.com/tacitus-me/tcgc"
Issues = "https://github.com/tacitus-me/tcgc/issues"

[project.scripts]
tcgc = "tcgc.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["tcgc"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E","F","W","I","N","UP","B","A","C4","SIM","PL","RUF"]
ignore = ["PLR0913"]

[tool.mypy]
python_version = "3.11"
strict = true

[[tool.mypy.overrides]]
module = ["scipy.*","lm_eval.*","helm.*","sklearn.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra --strict-markers --strict-config"
testpaths = ["tests"]
markers = [
    "requires_api: test that calls a paid model API (skipped unless TCGC_RUN_API=1)",
    "slow: slow test",
]

[tool.coverage.run]
source = ["tcgc"]
omit = ["tcgc/adapters/*", "baselines/*"]

[tool.coverage.report]
fail_under = 90
exclude_lines = ["pragma: no cover","raise NotImplementedError","if TYPE_CHECKING:"]
```

### 9.2 `tcgc/__init__.py`

```python
"""TACITUS Conflict Grammar Corpus — v0.1 harness.

Author: Giulio Catanzariti <giuliocatanzariti@gmail.com>
Project: https://www.tacitus.me/research/tcgc
"""
from __future__ import annotations
__version__ = "0.1.0"
__all__ = ["__version__"]
```

### 9.3 `tcgc/ontology/aco.py`

```python
"""The Agentic Conflict Ontology (ACO) — eight primitives."""
from __future__ import annotations
from enum import StrEnum


class Primitive(StrEnum):
    ACTOR = "actor"
    CLAIM = "claim"
    INTEREST = "interest"
    CONSTRAINT = "constraint"
    LEVERAGE = "leverage"
    COMMITMENT = "commitment"
    EVENT = "event"
    NARRATIVE = "narrative"


PRIMITIVES: tuple[str, ...] = tuple(p.value for p in Primitive)

DEFINITIONS: dict[str, str] = {
    "actor":       "Any party capable of holding an interest or making a claim: individuals, organizations, states, coalitions.",
    "claim":       "An asserted fact, evaluation, or normative statement attributed to an actor.",
    "interest":    "An underlying goal or need that motivates claims and positions (Fisher/Ury distinction).",
    "constraint":  "A rule, norm, or structural limit shaping feasible outcomes.",
    "leverage":    "A resource, dependency, or capability that shifts bargaining power.",
    "commitment":  "A promised future action, with a subject and typically a deadline.",
    "event":       "A dated or orderable occurrence in the world.",
    "narrative":   "A coherent framing across multiple claims, attributable to an actor.",
}
```

### 9.4 `tcgc/ontology/edges.py`

```python
"""Typed edges of the ACO. Closed set for v0.1."""
from __future__ import annotations
from enum import StrEnum
from typing import Final


class Edge(StrEnum):
    ASSERTED = "ASSERTED"
    DENIED = "DENIED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ACKNOWLEDGED_AMBIGUOUSLY = "ACKNOWLEDGED_AMBIGUOUSLY"
    DENIES_SCOPE = "DENIES_SCOPE"
    COMMITS_TO = "COMMITS_TO"
    REVOKES = "REVOKES"
    BLOCKS = "BLOCKS"
    ENABLES = "ENABLES"
    CAUSES = "CAUSES"
    PRECEDES = "PRECEDES"
    CONTRADICTS = "CONTRADICTS"
    SUPPORTS = "SUPPORTS"
    CITES = "CITES"
    HOLDS_INTEREST = "HOLDS_INTEREST"
    FRAMES = "FRAMES"
    LEVERAGES = "LEVERAGES"
    CONSTRAINED_BY = "CONSTRAINED_BY"


EDGE_TYPES: Final[tuple[str, ...]] = tuple(e.value for e in Edge)


def _identity() -> dict[tuple[str, str], float]:
    return {(e, e): 1.0 for e in EDGE_TYPES}


# Every nonzero off-diagonal carries a rationale; see CLAUDE.md §3.3.
TYPE_SIMILARITY: dict[tuple[str, str], float] = _identity() | {
    (Edge.ASSERTED, Edge.ACKNOWLEDGED): 0.5,
    (Edge.ACKNOWLEDGED, Edge.ASSERTED): 0.5,
    (Edge.ACKNOWLEDGED, Edge.ACKNOWLEDGED_AMBIGUOUSLY): 0.75,
    (Edge.ACKNOWLEDGED_AMBIGUOUSLY, Edge.ACKNOWLEDGED): 0.75,
    (Edge.DENIED, Edge.DENIES_SCOPE): 0.5,
    (Edge.DENIES_SCOPE, Edge.DENIED): 0.5,
    (Edge.BLOCKS, Edge.CONSTRAINED_BY): 0.4,
    (Edge.CONSTRAINED_BY, Edge.BLOCKS): 0.4,
    (Edge.ENABLES, Edge.CAUSES): 0.5,
    (Edge.CAUSES, Edge.ENABLES): 0.5,
    (Edge.COMMITS_TO, Edge.ASSERTED): 0.5,
    (Edge.ASSERTED, Edge.COMMITS_TO): 0.5,
}


def similarity(a: str, b: str) -> float:
    if a == b:
        return 1.0
    return TYPE_SIMILARITY.get((a, b), 0.0)


def validate_type(t: str) -> None:
    if t not in EDGE_TYPES:
        raise ValueError(f"Unknown edge type {t!r}. Valid: {', '.join(EDGE_TYPES)}")
```

### 9.5 `tcgc/ontology/__init__.py`

```python
from tcgc.ontology.aco import DEFINITIONS, PRIMITIVES, Primitive
from tcgc.ontology.edges import EDGE_TYPES, TYPE_SIMILARITY, Edge, similarity, validate_type

__all__ = ["DEFINITIONS","EDGE_TYPES","Edge","PRIMITIVES","Primitive","TYPE_SIMILARITY","similarity","validate_type"]
```

### 9.6 `tcgc/types.py`

```python
"""StrEnums and the canonical task_type -> metric map."""
from __future__ import annotations
from enum import StrEnum


class Domain(StrEnum):
    WORKPLACE = "workplace"
    COMMERCIAL = "commercial"
    GOVERNANCE = "governance"
    PEACE_PROCESS = "peace-process"
    POLICY = "policy"
    FAMILY = "family"
    DIPLOMATIC = "diplomatic"


class TaskType(StrEnum):
    ACTOR_RESOLUTION = "actor-resolution"
    CLAIM_EXTRACTION = "claim-extraction"
    INTEREST_EXTRACTION = "interest-extraction"
    CONSTRAINT_EXTRACTION = "constraint-extraction"
    LEVERAGE_MAPPING = "leverage-mapping"
    COMMITMENT_TRACKING = "commitment-tracking"
    EVENT_ORDERING = "event-ordering"
    NARRATIVE_DRIFT = "narrative-drift"
    CAUSAL_CHAIN = "causal-chain"
    CONTRADICTION_DETECTION = "contradiction-detection"
    PROVENANCE_ATTRIBUTION = "provenance-attribution"
    COMMITMENT_CLAIM_MISMATCH = "commitment-claim-mismatch"
    POSITION_INTEREST_SEPARATION = "position-interest-separation"
    CROSS_DOCUMENT_SYNTHESIS = "cross-document-synthesis"


class Metric(StrEnum):
    GRAPH_OVERLAP = "graph_overlap"
    PROVENANCE_F1 = "provenance_f1"
    KENDALL_TAU = "kendall_tau"
    CONTRADICTION_PAIR_F1 = "contradiction_pair_f1"
    LLM_JUDGE_ANCHORED = "llm_judge_anchored"


TASK_METRIC_MAP: dict[str, str] = {
    TaskType.ACTOR_RESOLUTION:             Metric.GRAPH_OVERLAP,
    TaskType.CLAIM_EXTRACTION:             Metric.GRAPH_OVERLAP,
    TaskType.INTEREST_EXTRACTION:          Metric.LLM_JUDGE_ANCHORED,
    TaskType.CONSTRAINT_EXTRACTION:        Metric.GRAPH_OVERLAP,
    TaskType.LEVERAGE_MAPPING:             Metric.GRAPH_OVERLAP,
    TaskType.COMMITMENT_TRACKING:          Metric.GRAPH_OVERLAP,
    TaskType.EVENT_ORDERING:               Metric.KENDALL_TAU,
    TaskType.NARRATIVE_DRIFT:              Metric.LLM_JUDGE_ANCHORED,
    TaskType.CAUSAL_CHAIN:                 Metric.GRAPH_OVERLAP,
    TaskType.CONTRADICTION_DETECTION:      Metric.CONTRADICTION_PAIR_F1,
    TaskType.PROVENANCE_ATTRIBUTION:       Metric.PROVENANCE_F1,
    TaskType.COMMITMENT_CLAIM_MISMATCH:    Metric.GRAPH_OVERLAP,
    TaskType.POSITION_INTEREST_SEPARATION: Metric.LLM_JUDGE_ANCHORED,
    TaskType.CROSS_DOCUMENT_SYNTHESIS:     Metric.GRAPH_OVERLAP,
}
```

### 9.7 `tcgc/io.py`

```python
"""IO helpers for TCGC items and predictions."""
from __future__ import annotations
import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any
import orjson


def load_item(path: Path) -> dict[str, Any]:
    return orjson.loads(path.read_bytes())


def load_items(path: Path) -> Iterator[tuple[Path, dict[str, Any]]]:
    if path.is_file():
        yield path, load_item(path); return
    if not path.is_dir():
        raise FileNotFoundError(path)
    for p in sorted(path.rglob("tcgc-*.json")):
        yield p, load_item(p)


def write_predictions(predictions: Iterable[dict[str, Any]], out: Path) -> None:
    with out.open("wb") as f:
        for pred in predictions:
            f.write(orjson.dumps(pred)); f.write(b"\n")


def read_predictions(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("rb") as f:
        for line in f:
            line = line.strip()
            if line:
                yield orjson.loads(line)


def dump_json(obj: Any, path: Path, *, indent: int = 2) -> None:
    path.write_text(json.dumps(obj, indent=indent, sort_keys=True, ensure_ascii=False))
```

### 9.8 `tcgc/validate.py`

```python
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
```

### 9.9 `tcgc/scoring/graph_overlap.py`

```python
"""The `graph_overlap` scorer — Jaccard over the typed subgraph."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from tcgc.ontology.edges import similarity


@dataclass
class ScoreResult:
    value: float
    components: dict[str, float] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def _node_key(n: dict[str, Any]) -> tuple[str, str]:
    return (n.get("type", ""), n.get("id", ""))


def _edge_key(e: dict[str, Any]) -> tuple[str, str]:
    return (e.get("from", ""), e.get("to", ""))


def _jaccard(a: set[Any], b: set[Any]) -> float:
    if not a and not b: return 1.0
    if not a or not b:  return 0.0
    return len(a & b) / len(a | b)


def _edge_match_score(gold_edges: list[dict[str, Any]], pred_edges: list[dict[str, Any]]) -> float:
    gold_by_pair: dict[tuple[str, str], list[str]] = {}
    pred_by_pair: dict[tuple[str, str], list[str]] = {}
    for e in gold_edges: gold_by_pair.setdefault(_edge_key(e), []).append(e.get("type", ""))
    for e in pred_edges: pred_by_pair.setdefault(_edge_key(e), []).append(e.get("type", ""))
    union = set(gold_by_pair) | set(pred_by_pair)
    if not union: return 1.0
    total = 0.0
    for pair in union:
        g, p = gold_by_pair.get(pair, []), pred_by_pair.get(pair, [])
        if not g or not p: continue
        total += max(similarity(a, b) for a in g for b in p)
    return total / len(union)


def score(gold: dict[str, Any], pred: dict[str, Any], *,
          node_weight: float = 0.4, edge_weight: float = 0.6) -> ScoreResult:
    if abs(node_weight + edge_weight - 1.0) > 1e-9:
        raise ValueError(f"weights must sum to 1.0 (got {node_weight + edge_weight})")
    gold_nodes = {_node_key(n) for n in gold.get("primitives", [])}
    pred_nodes = {_node_key(n) for n in pred.get("primitives", [])}
    node_j = _jaccard(gold_nodes, pred_nodes)
    edge_j = _edge_match_score(gold.get("edges", []), pred.get("edges", []))
    value = node_weight * node_j + edge_weight * edge_j
    notes: list[str] = []
    if not gold.get("edges"): notes.append("gold has no edges — score reduces to node overlap")
    if not pred.get("edges") and gold.get("edges"): notes.append("pred has no edges — edge_jaccard is 0")
    return ScoreResult(value=value, components={"node_jaccard": node_j, "edge_jaccard": edge_j}, notes=notes)
```

### 9.10 `tcgc/scoring/provenance_f1.py`

```python
"""The `provenance_f1` scorer — F1 over (primitive_id, provenance_ref) pairs."""
from __future__ import annotations
from typing import Any
from tcgc.scoring.graph_overlap import ScoreResult


def _norm(p: Any) -> list[str]:
    if p is None: return []
    if isinstance(p, str): return [p]
    if isinstance(p, list): return [str(x) for x in p]
    return []


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    gold_pairs: set[tuple[str, str]] = set()
    pred_pairs: set[tuple[str, str]] = set()
    for n in gold.get("primitives", []):
        for r in _norm(n.get("provenance")): gold_pairs.add((n.get("id", ""), r))
    for e in gold.get("edges", []):
        k = f"edge:{e.get('from')}->{e.get('to')}:{e.get('type')}"
        for r in _norm(e.get("provenance")): gold_pairs.add((k, r))
    for n in pred.get("primitives", []):
        for r in _norm(n.get("provenance")): pred_pairs.add((n.get("id", ""), r))
    for e in pred.get("edges", []):
        k = f"edge:{e.get('from')}->{e.get('to')}:{e.get('type')}"
        for r in _norm(e.get("provenance")): pred_pairs.add((k, r))
    if not gold_pairs and not pred_pairs:
        return ScoreResult(value=1.0, components={"precision": 1.0, "recall": 1.0})
    if not pred_pairs:
        return ScoreResult(value=0.0, components={"precision": 0.0, "recall": 0.0},
                           notes=["pred has no provenance-bearing primitives"])
    if not gold_pairs:
        return ScoreResult(value=0.0, components={"precision": 0.0, "recall": 0.0})
    tp = len(gold_pairs & pred_pairs)
    p = tp / len(pred_pairs)
    r = tp / len(gold_pairs)
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return ScoreResult(value=f1, components={"precision": p, "recall": r, "tp": float(tp)})
```

### 9.11 `tcgc/scoring/kendall_tau.py`

```python
"""The `kendall_tau` scorer — τ-b normalized to [0, 1]."""
from __future__ import annotations
from typing import Any
from scipy.stats import kendalltau
from tcgc.scoring.graph_overlap import ScoreResult


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    gold_order = list(gold.get("order", []))
    pred_order = list(pred.get("order", []))
    if not gold_order:
        return ScoreResult(value=1.0, components={"tau": 1.0}, notes=["gold has no order"])
    if not pred_order:
        return ScoreResult(value=0.0, components={"tau": -1.0}, notes=["pred has no order"])
    gold_rank = {eid: i for i, eid in enumerate(gold_order)}
    pred_rank = {eid: i for i, eid in enumerate(pred_order)}
    missing = [eid for eid in gold_order if eid not in pred_rank]
    x = [gold_rank[eid] for eid in gold_order]
    y = [pred_rank.get(eid, len(pred_order)) for eid in gold_order]
    tau, _ = kendalltau(x, y, variant="b")
    if tau is None or tau != tau:
        return ScoreResult(value=0.0, components={"tau": 0.0}, notes=["kendalltau returned NaN"])
    norm = (float(tau) + 1.0) / 2.0
    notes = [f"{len(missing)} gold events missing from prediction"] if missing else []
    return ScoreResult(value=norm,
                       components={"tau": float(tau), "normalized": norm, "missing": float(len(missing))},
                       notes=notes)
```

### 9.12 `tcgc/scoring/contradiction_pair_f1.py`

```python
"""The `contradiction_pair_f1` scorer — materiality-weighted F1."""
from __future__ import annotations
from typing import Any
from tcgc.scoring.graph_overlap import ScoreResult

_WEIGHT = {"material": 1.0, "cosmetic": 0.25}


def _pair(a: str, b: str) -> frozenset[str]:
    return frozenset({a, b})


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    gm: dict[frozenset[str], str] = {
        _pair(g["claim_a"], g["claim_b"]): g.get("materiality", "material")
        for g in gold.get("contradictions", [])
    }
    pp: set[frozenset[str]] = {_pair(p["claim_a"], p["claim_b"]) for p in pred.get("contradictions", [])}
    if not gm and not pp:
        return ScoreResult(value=1.0, components={"f1_weighted": 1.0, "f1_unweighted": 1.0})
    if not gm:
        return ScoreResult(value=0.0, components={"f1_weighted": 0.0, "f1_unweighted": 0.0,
                                                   "precision": 0.0, "recall": 0.0})
    if not pp:
        return ScoreResult(value=0.0, components={"f1_weighted": 0.0, "f1_unweighted": 0.0,
                                                   "precision": 0.0, "recall": 0.0},
                           notes=["pred has no contradictions"])
    tp_w = sum(_WEIGHT[gm[p]] for p in pp if p in gm)
    fp_w = sum(1.0 for p in pp if p not in gm)
    fn_w = sum(_WEIGHT[gm[p]] for p in gm if p not in pp)
    prec_w = tp_w / (tp_w + fp_w) if (tp_w + fp_w) else 0.0
    rec_w  = tp_w / (tp_w + fn_w) if (tp_w + fn_w) else 0.0
    f1_w   = 2 * prec_w * rec_w / (prec_w + rec_w) if (prec_w + rec_w) else 0.0
    tp = len(pp & set(gm.keys()))
    prec_u = tp / len(pp) if pp else 0.0
    rec_u  = tp / len(gm) if gm else 0.0
    f1_u   = 2 * prec_u * rec_u / (prec_u + rec_u) if (prec_u + rec_u) else 0.0
    return ScoreResult(value=f1_w,
                       components={"f1_weighted": f1_w, "f1_unweighted": f1_u,
                                   "precision": prec_w, "recall": rec_w})
```

### 9.13 `tcgc/scoring/llm_judge_anchored.py`

```python
"""The `llm_judge_anchored` scorer — isotonic-calibrated LLM judge.

Gated behind TCGC_RUN_API=1. Cite Zheng et al. (2023) "Judging LLM-as-a-Judge".
Known failure modes: position bias, verbosity bias, self-preference bias.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from tcgc.scoring.graph_overlap import ScoreResult

_ANCHOR_PATH = Path(__file__).parent / "anchors" / "v0.1.jsonl"

_DEFAULT_JUDGE_PROMPT = """You are an expert annotator evaluating conflict-analysis outputs.
You will be shown an INPUT (source material plus a question), a GOLD reference
answer structured as a typed subgraph, and a PREDICTED answer in the same shape.
Score the PREDICTED answer on a scale from 0.0 to 1.0.
Return ONLY a single floating-point number.
"""


def _load_anchors() -> list[dict[str, Any]]:  # pragma: no cover
    if not _ANCHOR_PATH.exists(): return []
    import orjson
    return [orjson.loads(line) for line in _ANCHOR_PATH.read_bytes().splitlines() if line.strip()]


def _call_judge(input_obj: dict[str, Any], gold: dict[str, Any], pred: dict[str, Any],
                *, model: str | None = None) -> float:  # pragma: no cover
    raise NotImplementedError(
        "llm_judge_anchored requires a model backend. Implement _call_judge in this module."
    )


def _isotonic(raw: float, anchors: list[dict[str, Any]]) -> float:
    if len(anchors) < 2: return raw
    try:
        from sklearn.isotonic import IsotonicRegression  # type: ignore[import-not-found]
    except ImportError:  # pragma: no cover
        return raw
    xs = [a["raw"] for a in anchors]
    ys = [a["human_score"] for a in anchors]
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    iso.fit(xs, ys)
    return float(iso.predict([raw])[0])


def score(gold: dict[str, Any], pred: dict[str, Any]) -> ScoreResult:
    if os.environ.get("TCGC_RUN_API") != "1":
        return ScoreResult(value=0.0, components={"raw": 0.0, "calibrated": 0.0},
                           notes=["llm_judge_anchored skipped: set TCGC_RUN_API=1 to enable"])
    input_obj = pred.get("_inputs", {})
    raw = _call_judge(input_obj, gold, pred)  # pragma: no cover
    raw = max(0.0, min(1.0, float(raw)))
    calibrated = _isotonic(raw, _load_anchors())
    return ScoreResult(value=calibrated, components={"raw": raw, "calibrated": calibrated})
```

### 9.14 `tcgc/scoring/__init__.py`

```python
"""Scorer registry."""
from __future__ import annotations
from collections.abc import Callable
from typing import Any
from tcgc.scoring.graph_overlap import ScoreResult, score as graph_overlap_score
from tcgc.scoring.provenance_f1 import score as provenance_f1_score
from tcgc.scoring.kendall_tau import score as kendall_tau_score
from tcgc.scoring.contradiction_pair_f1 import score as contradiction_pair_f1_score
from tcgc.scoring.llm_judge_anchored import score as llm_judge_anchored_score

Scorer = Callable[[dict[str, Any], dict[str, Any]], ScoreResult]

REGISTRY: dict[str, Scorer] = {
    "graph_overlap": graph_overlap_score,
    "provenance_f1": provenance_f1_score,
    "kendall_tau": kendall_tau_score,
    "contradiction_pair_f1": contradiction_pair_f1_score,
    "llm_judge_anchored": llm_judge_anchored_score,
}


def get(name: str) -> Scorer:
    if name not in REGISTRY:
        raise KeyError(f"Unknown scorer {name!r}. Known: {', '.join(sorted(REGISTRY))}")
    return REGISTRY[name]


__all__ = ["REGISTRY", "ScoreResult", "Scorer", "get"]
```

### 9.15 `tcgc/scoring/anchors/v0.1.jsonl`

Twenty calibration triples. Transcribe as-is.

```jsonl
{"id":"anchor-001","task_type":"interest-extraction","raw":0.95,"human_score":0.92,"note":"near-perfect interest separation, minor actor attribution error"}
{"id":"anchor-002","task_type":"interest-extraction","raw":0.80,"human_score":0.75,"note":"interests identified but one position mislabeled as interest"}
{"id":"anchor-003","task_type":"interest-extraction","raw":0.60,"human_score":0.55,"note":"two of four interests captured"}
{"id":"anchor-004","task_type":"interest-extraction","raw":0.40,"human_score":0.30,"note":"surface positions only, no inferred interests"}
{"id":"anchor-005","task_type":"interest-extraction","raw":0.20,"human_score":0.10,"note":"confused parties and positions"}
{"id":"anchor-006","task_type":"narrative-drift","raw":0.90,"human_score":0.88,"note":"drift correctly attributed to party and temporally ordered"}
{"id":"anchor-007","task_type":"narrative-drift","raw":0.70,"human_score":0.65,"note":"drift detected, party attribution weak"}
{"id":"anchor-008","task_type":"narrative-drift","raw":0.50,"human_score":0.40,"note":"partial drift detection, no temporal structure"}
{"id":"anchor-009","task_type":"narrative-drift","raw":0.30,"human_score":0.20,"note":"flagged cosmetic variation as drift"}
{"id":"anchor-010","task_type":"narrative-drift","raw":0.10,"human_score":0.05,"note":"no drift detected where one clearly exists"}
{"id":"anchor-011","task_type":"position-interest-separation","raw":0.95,"human_score":0.90,"note":"separation clean across both parties"}
{"id":"anchor-012","task_type":"position-interest-separation","raw":0.85,"human_score":0.80,"note":"separation clean for one party, mixed for other"}
{"id":"anchor-013","task_type":"position-interest-separation","raw":0.65,"human_score":0.60,"note":"one interest inferred plausibly, one confused with position"}
{"id":"anchor-014","task_type":"position-interest-separation","raw":0.45,"human_score":0.35,"note":"partial separation, attribution errors"}
{"id":"anchor-015","task_type":"position-interest-separation","raw":0.25,"human_score":0.15,"note":"positions restated as interests"}
{"id":"anchor-016","task_type":"interest-extraction","raw":0.75,"human_score":0.70,"note":"good vendor interests, buyer interests partial"}
{"id":"anchor-017","task_type":"narrative-drift","raw":0.80,"human_score":0.72,"note":"drift attributed to wrong actor but correctly typed"}
{"id":"anchor-018","task_type":"position-interest-separation","raw":0.55,"human_score":0.45,"note":"one side's interests plausible, other side's hallucinated"}
{"id":"anchor-019","task_type":"interest-extraction","raw":0.10,"human_score":0.08,"note":"uninformative output"}
{"id":"anchor-020","task_type":"narrative-drift","raw":0.00,"human_score":0.02,"note":"empty output"}
```

### 9.16 `tcgc/score.py`

```python
"""Scoring driver — dispatches by rubric.scoring and aggregates."""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
from tcgc.io import load_items, read_predictions
from tcgc.scoring import get as get_scorer


def score_predictions(predictions_path: Path, items_dir: Path) -> dict[str, Any]:
    preds_by_id = {p["id"]: p for p in read_predictions(predictions_path)}
    per_item: list[dict[str, Any]] = []
    for _, item in load_items(items_dir):
        if item["id"] not in preds_by_id:
            per_item.append({"id": item["id"], "task_type": item["task_type"],
                             "domain": item["domain"], "metric": item["rubric"]["scoring"],
                             "value": 0.0, "notes": ["no prediction submitted"]})
            continue
        scorer = get_scorer(item["rubric"]["scoring"])
        r = scorer(item["gold"], preds_by_id[item["id"]])
        per_item.append({
            "id": item["id"], "task_type": item["task_type"], "domain": item["domain"],
            "metric": item["rubric"]["scoring"], "value": float(r.value),
            "components": r.components, "notes": r.notes,
        })
    tb: dict[str, list[float]] = defaultdict(list)
    db: dict[str, list[float]] = defaultdict(list)
    for row in per_item:
        tb[row["task_type"]].append(row["value"])
        db[row["domain"]].append(row["value"])
    return {
        "per_item": per_item,
        "per_task_type": {k: float(mean(v)) for k, v in tb.items()},
        "per_domain":    {k: float(mean(v)) for k, v in db.items()},
        "overall":       float(mean([r["value"] for r in per_item])) if per_item else 0.0,
    }
```

### 9.17 `tcgc/cli.py`

```python
"""The `tcgc` command-line interface (Typer)."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Annotated
import typer
from rich.console import Console

app = typer.Typer(name="tcgc", help="TACITUS Conflict Grammar Corpus CLI.",
                  no_args_is_help=True, add_completion=False)
console = Console()


@app.command()
def validate(
    path: Annotated[Path, typer.Argument(help="Item file or directory")],
    fmt: Annotated[str, typer.Option("--format", help="'pretty' or 'json'")] = "pretty",
) -> None:
    """Validate one or more TCGC items."""
    from tcgc.validate import validate_path
    report = validate_path(path)
    if fmt == "json":
        console.print_json(data=report.as_dict())
    else:
        for line in report.as_lines(): console.print(line)
    raise typer.Exit(code=0 if report.ok else 1)


@app.command()
def schema(version: Annotated[str, typer.Option(help="Schema version")] = "v0.1") -> None:
    """Print the canonical JSON Schema."""
    path = Path(__file__).parent.parent / "schema" / f"tcgc-{version}.json"
    if not path.exists():
        console.print(f"[red]Schema version {version!r} not found at {path}[/red]")
        raise typer.Exit(code=1)
    console.print_json(data=json.loads(path.read_text()))


@app.command("score")
def score_cmd(
    predictions: Annotated[Path, typer.Argument(help="JSONL file of predictions")],
    items_dir: Annotated[Path, typer.Argument(help="Directory of item files")],
    out: Annotated[Path, typer.Option("--out")] = Path("scores.json"),
) -> None:
    """Score a predictions file against a directory of items."""
    from tcgc.score import score_predictions
    result = score_predictions(predictions, items_dir)
    out.write_text(json.dumps(result, indent=2))
    console.print(f"[green]Wrote {out}[/green]")


@app.command()
def run(
    system: Annotated[str, typer.Option("--system", help="module:callable")],
    items_dir: Annotated[Path, typer.Argument()],
    out: Annotated[Path, typer.Option("--out")],
) -> None:
    """Run a callable over every item, write predictions.jsonl."""
    import importlib
    mod_name, func_name = system.split(":")
    fn = getattr(importlib.import_module(mod_name), func_name)
    from tcgc.io import load_items, write_predictions
    preds = []
    for _, item in load_items(items_dir):
        pred = fn(item["id"], item["inputs"])
        pred.setdefault("id", item["id"])
        preds.append(pred)
    write_predictions(preds, out)
    console.print(f"[green]Wrote {len(preds)} predictions to {out}[/green]")


@app.command()
def report(scores: Annotated[Path, typer.Argument()]) -> None:
    """Pretty per-task / per-domain breakdown."""
    from tcgc.reporting.summary import render_markdown
    data = json.loads(scores.read_text())
    console.print(render_markdown(data))


@app.command()
def card(scores: Annotated[Path, typer.Argument()],
         out: Annotated[Path, typer.Option("--out")] = Path("SYSTEM_CARD.md")) -> None:
    """Emit a SYSTEM_CARD.md stub from a scores file."""
    from tcgc.reporting.card import render_card
    data = json.loads(scores.read_text())
    out.write_text(render_card(data))
    console.print(f"[green]Wrote {out}[/green]")


@app.command()
def manifest() -> None:
    """Regenerate items/manifest.json."""
    from scripts.build_manifest import main as build_manifest
    build_manifest()


if __name__ == "__main__":  # pragma: no cover
    app()
```

### 9.18 Reporting modules

Implement `tcgc/reporting/summary.py` with a `render_markdown(scores_dict) -> str` that produces:

1. A per-task-type table (columns: task_type, n, mean).
2. A per-domain table (columns: domain, n, mean).
3. A trailing one-line "overall: X.XXX (n=N)".

Implement `tcgc/reporting/card.py` with `render_card(scores_dict) -> str` that produces a Markdown SYSTEM_CARD stub with sections: *System overview* (placeholders), *Per-task results* (from the summary), *Known limitations* (placeholder), *Contact*.

### 9.19 Adapters

- `tcgc/adapters/_common.py` — one function, `load_split(split: str) -> Iterator[Item]`, reading from `items/<split>/`.
- `tcgc/adapters/helm.py` — a minimal HELM `Scenario` subclass that emits one `Instance` per TCGC item, with `input` from `item.inputs` and `references` from `item.gold`.
- `tcgc/adapters/lm_eval.py` — register tasks `tcgc_<task_type>` via `ConfigurableTask`; `process_results` dispatches to `tcgc.scoring.REGISTRY`.

Both adapter files begin with a `try: import ... except ImportError: raise ImportError("Install tcgc[adapters]") from None` guard, so importing the package doesn't require HELM/lm-eval.

---

## 10. Tests

Target ≥ 90% line coverage on `tcgc/` (exclude `adapters/` and `baselines/`).

### 10.1 `tests/conftest.py`

```python
from __future__ import annotations
import json
from pathlib import Path
import pytest


@pytest.fixture
def sample_items_dir() -> Path:
    return Path(__file__).parent.parent / "items" / "v0.1-sample"


@pytest.fixture
def tcgc_0001() -> dict:
    path = Path(__file__).parent.parent / "items" / "v0.1-sample" / "tcgc-0001.json"
    return json.loads(path.read_text())
```

### 10.2 Required tests

For each of these, write the file at the indicated path. Each test file should be self-contained.

- `tests/test_schema.py` — every file in `items/v0.1-sample/` validates against the schema. The schema itself is a well-formed Draft 2020-12 schema (`jsonschema.Draft202012Validator.check_schema`).
- `tests/test_io.py` — round-trip `load_item`, `load_items`, `write_predictions`, `read_predictions` against a tmp_path.
- `tests/test_ontology.py` — `Primitive`, `Edge` enums export the expected members; `similarity("ASSERTED","ASSERTED") == 1.0`; `similarity("FOO","BAR") == 0.0`; `validate_type` raises on unknown.
- `tests/test_validate.py` — all 5 sample items validate clean (`report.ok == True`, `report.has_warnings == False`). Constructed items that break each semantic rule trigger the expected `code`.
- `tests/test_scoring_graph_overlap.py` — identity (gold→gold = 1.0); worst case (gold→{} = 0.0); near-miss edge types yield partial credit; `node_weight + edge_weight != 1.0` raises. Include a `hypothesis` property test: random subgraph deletion monotonically decreases the score.
- `tests/test_scoring_provenance_f1.py` — identity, worst case, partial P/R arithmetic on a 3-true-1-fp-1-fn fixture.
- `tests/test_scoring_kendall_tau.py` — identity returns 1.0; fully reversed returns ~0.0; `hypothesis` property: reversing a sequence gives normalized value ≤ 0.5.
- `tests/test_scoring_contradiction_pair_f1.py` — identity; unordered pair equivalence; material pair contributes more than cosmetic.
- `tests/test_scoring_llm_judge_anchored.py` — with `TCGC_RUN_API` unset, returns 0.0 and a note containing "skipped". Real-API test is marked `@pytest.mark.requires_api`.
- `tests/test_cli.py` — `typer.testing.CliRunner` against `validate`, `schema`, `score`; `tcgc validate items/v0.1-sample/` exits 0.
- `tests/test_adapters_helm.py`, `tests/test_adapters_lm_eval.py` — skip if the respective library is not installed; otherwise, smoke test that the adapter enumerates all 5 sample items.

---

## 11. Governance files

### 11.1 `README.md`

```markdown
# TCGC — TACITUS Conflict Grammar Corpus

*An open benchmark for conflict reasoning, grounded in the Agentic Conflict Ontology.*

**Version** `v0.1-sample` (public) · **Full** in development · **Homepage** <https://www.tacitus.me/research/tcgc>

The TCGC measures what generic language models fail at in the conflict-analysis setting — time, causality, provenance, commitment tracking, interest/position separation, narrative drift. Items are short, structured, and scored on a typed subgraph, not on free text. Every extracted primitive must cite the source span it came from.

This repository ships: the JSON Schema (`schema/tcgc-v0.1.json`), five public sample items (`items/v0.1-sample/`), a reference harness (`tcgc/`), a CLI (`tcgc`), and adapters for HELM and `lm-evaluation-harness`. The full corpus (~480+ items) is under the Data Use Agreement.

## Quickstart

    git clone https://github.com/tacitus-me/tcgc && cd tcgc
    pip install -e '.[dev]'
    tcgc validate items/v0.1-sample/
    tcgc schema --version v0.1 | jq .
    tcgc score predictions.jsonl items/v0.1-sample/ --out scores.json
    tcgc report scores.json

## Task types and metrics

14 task types, 7 domains, 5 metrics. Per-task numbers are reported separately; no single headline score. See `docs/task-types.md`, `docs/domains.md`, `docs/metrics.md`.

## Submit

Fork, add `predictions.jsonl` and `SYSTEM_CARD.md` under `submissions/<name>/<date>/`, open a PR. The leaderboard workflow re-runs your predictions against the canonical scorer and posts the table back on the PR. Alternatively: email the per-metric CSV plus system card to <hello@tacitus.me>.

## Cite

See `CITATION.cff`. Full BibTeX in the dataset paper (Q4 2026, forthcoming).

## License

- Sample items and harness: CC-BY-NC-SA 4.0 (`LICENSE`).
- Full corpus: `DATA_USE_AGREEMENT.md`.

---

*Maintainer: Giulio Catanzariti · <giuliocatanzariti@gmail.com> · Building in public · NYC*
*TACITUS — making conflict legible. Member of Google Cloud for Startups · Neo4j · Databricks.*
```

### 11.2 `LICENSE`

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. Copyright `2026 Giulio Catanzariti / TACITUS`. Include the standard CC-BY-NC-SA 4.0 notice with a pointer to `https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode`. Contact line: `hello@tacitus.me`.

### 11.3 `CITATION.cff`

```yaml
cff-version: 1.2.0
title: "TCGC: The TACITUS Conflict Grammar Corpus"
message: "If you use this corpus or the harness, please cite it as below."
type: dataset
authors:
  - given-names: Giulio
    family-names: Catanzariti
    email: giuliocatanzariti@gmail.com
    affiliation: TACITUS
repository-code: "https://github.com/tacitus-me/tcgc"
url: "https://www.tacitus.me/research/tcgc"
license: CC-BY-NC-SA-4.0
version: "0.1.0"
date-released: "2026-04-18"
keywords:
  - benchmark
  - natural language processing
  - conflict analysis
  - ontology
  - neurosymbolic AI
  - evaluation
```

### 11.4 `CHANGELOG.md`

Keep a Changelog 1.1.0 format. First entry:

```markdown
# Changelog

All notable changes to the TCGC harness and sample are documented here.
The format is based on Keep a Changelog; the project adheres to Semantic Versioning.

## [0.1.0] — 2026-04-18

### Added
- Initial public release of the v0.1-sample (5 items).
- Canonical JSON Schema (`schema/tcgc-v0.1.json`).
- ACO ontology module (8 primitives, 18 edge types, partial-credit similarity).
- Five reference scorers (`graph_overlap`, `provenance_f1`, `kendall_tau`, `contradiction_pair_f1`, `llm_judge_anchored`).
- `tcgc` CLI: `validate`, `schema`, `run`, `score`, `report`, `card`, `manifest`.
- HELM and lm-evaluation-harness adapters.
- mkdocs-material documentation scaffold.
- 20-entry calibration anchor set for the LLM judge.
- GitHub Actions workflows for CI, release, and leaderboard intake.
```

### 11.5 `CONTRIBUTING.md`

Four tiers mirroring the website's "How to contribute":

- **Tier 01 — Run v0.1 sample.** Instructions for running a system over the 5-item sample and submitting via PR or email.
- **Tier 02 — Read the protocol.** Pointer to `docs/methodology.md` and `docs/task-types.md`; invite comments via issues.
- **Tier 03 — Request full-corpus access.** Pointer to `DATA_USE_AGREEMENT.md`.
- **Tier 04 — Propose a new task type.** Use `.github/ISSUE_TEMPLATE/task_type_proposal.yml`.

Plus a short "Developer setup" section: clone, `pip install -e '.[dev]'`, `pre-commit install`, how to run tests, how to run `tcgc validate`.

### 11.6 `CODE_OF_CONDUCT.md`

Transcribe the Contributor Covenant 2.1 (available at https://www.contributor-covenant.org/version/2/1/code_of_conduct.txt). Point-of-contact: `hello@tacitus.me`.

### 11.7 `DATA_USE_AGREEMENT.md`

Draft DUA with these sections: Parties (Provider: TACITUS / Giulio Catanzariti; Recipient: name + institution), Permitted use (academic research, pilot partnership), Restrictions (no redistribution, no generative training without consent, no re-identification, no profiling/surveillance), Obligations (access controls, incident notification within 14 days, citation, return/destroy on termination), No warranty, Attribution, Term & termination, Governing law (New York). Signature block at the bottom with Provider pre-filled and Recipient fields blank.

### 11.8 `DATASHEET.md`

Gebru et al. (2021) structure. Populate each section for v0.1-sample:

- **Motivation** — measure what generic RAG fails at in conflict analysis.
- **Composition** — 5 public items across 5 task types, 5 domains, 3 input modalities (messages / documents / transcript).
- **Collection process** — expert authoring from the Conflict Grammar; no personal data; synthetic and/or anonymized.
- **Preprocessing / cleaning / labeling** — three-pass annotation (primitive tagging, edge labeling, ground-truth QA); IAA reported per-item.
- **Uses** — benchmark evaluation of conflict-analysis systems; not for generative training.
- **Distribution** — GitHub, CC-BY-NC-SA 4.0 for the sample; full corpus under DUA.
- **Maintenance** — maintained by Giulio Catanzariti (`giuliocatanzariti@gmail.com`); versioned via SemVer; issues via GitHub.

---

## 12. CI / CD

### 12.1 `.github/workflows/ci.yml`

```yaml
name: ci
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}", cache: pip }
      - run: pip install -e '.[dev]'
      - run: ruff check .
      - run: ruff format --check .
      - run: mypy --strict tcgc
      - run: pytest -q --cov=tcgc --cov-report=term-missing --cov-fail-under=90
      - run: tcgc validate items/v0.1-sample/

  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12", cache: pip }
      - run: pip install -e '.[docs]'
      - run: mkdocs build --strict
```

### 12.2 `.github/workflows/release.yml`

Trigger on `v*` tags. Build the wheel, publish to PyPI via trusted publishing (`pypa/gh-action-pypi-publish@release/v1`), draft a GitHub Release whose body is the matching `CHANGELOG.md` section.

### 12.3 `.github/workflows/leaderboard.yml`

Trigger on PRs touching `submissions/**`. Validate against `schema/submission-v0.1.json`, run `tcgc score` on the submitted predictions against `items/v0.1-sample/`, post the per-task-type markdown table back as a PR comment using `peter-evans/create-or-update-comment@v4`.

### 12.4 `.github/workflows/docs.yml`

Deploy mkdocs-material to GitHub Pages on push to `main`.

---

## 13. Docs

### 13.1 `mkdocs.yml`

```yaml
site_name: TCGC
site_description: The TACITUS Conflict Grammar Corpus
site_url: https://tacitus-me.github.io/tcgc/
repo_url: https://github.com/tacitus-me/tcgc
repo_name: tacitus-me/tcgc

theme:
  name: material
  palette:
    - scheme: default
      primary: black
      accent: deep orange
  features:
    - navigation.sections
    - navigation.expand
    - content.code.copy
    - content.code.annotate

markdown_extensions:
  - admonition
  - attr_list
  - tables
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.inlinehilite
  - pymdownx.details

nav:
  - Home: index.md
  - Quickstart: quickstart.md
  - Task types: task-types.md
  - Domains: domains.md
  - Metrics: metrics.md
  - Methodology: methodology.md
  - Agreement: agreement.md
  - Open questions: open-questions.md
  - Submission guide: submission-guide.md
  - Leaderboard: leaderboard.md
  - Roadmap: roadmap.md
```

### 13.2 `docs/*.md`

For each, write tight, declarative prose (second person, no hedging). The authoritative content sources:

- **`index.md`** — one paragraph restating the mission + a link matrix to every other docs page.
- **`quickstart.md`** — the README's quickstart, expanded: installing dev extras, running the validator, running a trivial identity baseline (pred = gold) and seeing 4/5 scorers hit 1.0.
- **`task-types.md`** — all 14 task types: one-paragraph definition, expected input shape, expected output shape, failure modes, one worked mini-example each. Cross-reference §4 of this file.
- **`domains.md`** — each of the 7 domains: verbatim scope statement (marked with source comment), typical document types, typical actor structure, two or three conflict archetypes.
- **`metrics.md`** — each of the 5 metrics: formula, worked example, edge cases, when it can mislead.
- **`methodology.md`** — three-pass annotation protocol (primitives → edges → QA); IAA targets per task type; how to bulk-import into the platform.
- **`agreement.md`** — an IAA report stub. For v0.1-sample, use the κ values on each item's `source.inter_annotator_kappa`.
- **`open-questions.md`** — transcribe the 6 open questions from the website verbatim (mark with source comment) and under each add a "current thinking" subsection.
- **`submission-guide.md`** — step-by-step for the leaderboard PR flow: fork → add files under `submissions/<name>/<date>/` → CI validates → PR comment with scores.
- **`leaderboard.md`** — rendered from `leaderboard/v0.1-sample.json` via an mkdocs hook (or a static table if the hook is too much).
- **`roadmap.md`** — mirror the website's publication plan: Q4 2026 dataset paper, Q1 2027 OAG methodology, Q2 2027 v2.

---

## 14. Misc config

### 14.1 `.gitignore`

Standard Python ignore: `__pycache__/`, `*.py[cod]`, `.venv/`, `build/`, `dist/`, `*.egg-info/`, `.pytest_cache/`, `.coverage`, `.hypothesis/`, `.mypy_cache/`, `.ruff_cache/`, `site/`, `.vscode/`, `.idea/`, `.DS_Store`.

### 14.2 `.editorconfig`

```
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{yml,yaml,json,md}]
indent_size = 2

[Makefile]
indent_style = tab
```

### 14.3 `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-json
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
        args: ["--maxkb=1024"]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8
    hooks:
      - id: ruff
      - id: ruff-format
```

### 14.4 Issue templates

- `.github/ISSUE_TEMPLATE/bug_report.yml` — standard bug form (what happened, what you expected, reproduction, version).
- `.github/ISSUE_TEMPLATE/task_type_proposal.yml` — matches the website's Tier 04 ask: motivation (1 paragraph), worked example, suggested metric, domain(s).
- `.github/ISSUE_TEMPLATE/submission.yml` — for leaderboard submission intake: system name, version, contact email, one-paragraph system description, attested scorer commit SHA.

### 14.5 `.github/PULL_REQUEST_TEMPLATE.md`

Checklist: linked issue, tests added/updated, docs updated, `tcgc validate` clean, `pytest` green, `mkdocs build --strict` clean.

### 14.6 `.github/CODEOWNERS`

```
*                @giuliocatanzariti
/schema/         @giuliocatanzariti
/items/          @giuliocatanzariti
/tcgc/scoring/   @giuliocatanzariti
/docs/           @giuliocatanzariti
```

### 14.7 `schema/submission-v0.1.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tacitus.me/research/tcgc/schema/submission-v0.1.json",
  "title": "TCGC leaderboard submission",
  "type": "object",
  "required": ["system_name","system_version","contact_email","predictions_path","system_card_path","scorer_commit"],
  "additionalProperties": false,
  "properties": {
    "system_name":      {"type":"string"},
    "system_version":   {"type":"string"},
    "contact_email":    {"type":"string","format":"email"},
    "predictions_path": {"type":"string"},
    "system_card_path": {"type":"string"},
    "scorer_commit":    {"type":"string","pattern":"^[a-f0-9]{7,40}$"}
  }
}
```

### 14.8 `leaderboard/v0.1-sample.json`

Initial stub (systems from the website, all pending):

```json
{
  "schema": "submission-v0.1",
  "updated": "2026-04-18",
  "entries": [
    {"system_name":"TACITUS Dialectica (reference)","status":"pending","v0.1_sample":null,"full":null,"card":null},
    {"system_name":"GPT-4-class zero-shot","status":"pending","v0.1_sample":null,"full":null,"card":null},
    {"system_name":"Claude 3-class zero-shot","status":"pending","v0.1_sample":null,"full":null,"card":null},
    {"system_name":"Strong RAG baseline","status":"pending","v0.1_sample":null,"full":null,"card":null},
    {"system_name":"GraphRAG baseline","status":"pending","v0.1_sample":null,"full":null,"card":null}
  ]
}
```

---

## 15. Baselines (stubs — optional for v0.1)

Each baseline at `baselines/*.py` exposes:

```python
def predict(item_id: str, inputs: dict) -> dict:
    """Return a prediction matching the `gold` shape for the item's task_type."""
```

- `baselines/zeroshot_openai.py` — one-shot prompt, no tools, temperature 0. Reads `OPENAI_API_KEY`.
- `baselines/zeroshot_anthropic.py` — same for Claude. Reads `ANTHROPIC_API_KEY`.
- `baselines/rag_baseline.py` — chunk → embed (sentence-transformers) → retrieve top-k → extract. Reads `OPENAI_API_KEY` for the extractor.
- `baselines/graphrag_baseline.py` — LLM-driven graph construction, then query.

All baselines are skipped in CI unless `TCGC_RUN_BASELINES=1`. Each module begins with:

```python
import os
if os.environ.get("TCGC_RUN_BASELINES") != "1":  # pragma: no cover
    raise RuntimeError("Set TCGC_RUN_BASELINES=1 to enable this baseline.")
```

---

## 16. Scripts

- `scripts/build_manifest.py` — walk `items/`, hash each JSON file (SHA-256 of sorted-keys canonical JSON), write `items/manifest.json` as `{"version":"v0.1","generated":"<iso>","items":[{"id":"tcgc-0001","path":"items/v0.1-sample/tcgc-0001.json","sha256":"..."}]}`.
- `scripts/check_provenance.py` — standalone linter: for every item, ensure every `provenance` ref resolves to an id in `inputs`. Exits nonzero on any orphan.
- `scripts/bootstrap.sh` — new-contributor one-shot: installs uv, runs `uv sync --all-extras --dev`, installs pre-commit, runs the test suite once, prints a success banner with a link to CONTRIBUTING.md.

Also: `items/manifest.json` should be generated by running `scripts/build_manifest.py` after creating all 5 sample items, so it's regenerable. Do not hand-write it.

---

## 17. Definition of done for v0.1

Every one of these must hold before tagging `v0.1.0`:

1. `tcgc validate items/v0.1-sample/` → 0 errors, 0 warnings.
2. `pytest -q` green. `--cov-fail-under=90` passes on `tcgc/`.
3. `mypy --strict tcgc` clean.
4. `ruff check` and `ruff format --check` clean.
5. `mkdocs build --strict` clean.
6. `tcgc score` with a gold-as-prediction run returns 1.0 for every scorer except `llm_judge_anchored` (which correctly returns 0 with a "skipped" note under `TCGC_RUN_API=0`).
7. `README.md` quickstart works from a fresh clone.
8. `CHANGELOG.md` has a dated `0.1.0` entry.
9. `CITATION.cff` validates as well-formed YAML against the CFF 1.2.0 shape.
10. GitHub Actions `ci.yml` green on both 3.11 and 3.12.

---

## 18. Execution order

Do the work in this order. Do not skip ahead.

1. Create the directory tree (§2).
2. Transcribe `schema/tcgc-v0.1.json` (§7).
3. Transcribe the five items in `items/v0.1-sample/` (§8).
4. Create `pyproject.toml` (§9.1). Run `pip install -e '.[dev]'` to establish the env.
5. Transcribe `tcgc/__init__.py`, `tcgc/types.py`, `tcgc/ontology/`, `tcgc/io.py` (§9.2–§9.7).
6. Transcribe `tcgc/validate.py` (§9.8). Write `tests/test_validate.py`. Run `tcgc validate items/v0.1-sample/` — must exit 0 with zero warnings before moving on.
7. Transcribe `tcgc/scoring/graph_overlap.py` (§9.9). Write `tests/test_scoring_graph_overlap.py`. Run `pytest tests/test_scoring_graph_overlap.py` — must be green.
8. Transcribe the remaining scorers (§9.10–§9.13), the anchor set (§9.15), and `tcgc/scoring/__init__.py` (§9.14). Write matching tests.
9. Transcribe `tcgc/score.py` (§9.16) and `tcgc/cli.py` (§9.17). Write `tests/test_cli.py`.
10. Implement `tcgc/reporting/` (§9.18) and `tcgc/adapters/` (§9.19). Write their tests.
11. Write governance files (§11): `README.md`, `LICENSE`, `CITATION.cff`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `DATA_USE_AGREEMENT.md`, `DATASHEET.md`.
12. Write CI (§12) and mkdocs config + all `docs/*.md` pages (§13).
13. Write misc config (§14): `.gitignore`, `.editorconfig`, `.pre-commit-config.yaml`, issue templates, PR template, CODEOWNERS, `schema/submission-v0.1.json`, `leaderboard/v0.1-sample.json`.
14. Write baseline stubs (§15) and scripts (§16). Run `python scripts/build_manifest.py` to generate `items/manifest.json`.
15. Verify the definition of done (§17). Open an initial PR titled `feat: initial v0.1-sample release`.

---

## 19. If you're unsure

Re-read §0. Then re-read the relevant section. Then implement.

If a tool I've specified is not available in your environment, use the closest standard equivalent and note the substitution in `CHANGELOG.md`.

If you find a genuine contradiction between this file and the website, the website wins — and open an issue tagged `spec-drift` so I can fix this file.

---

*Maintainer: Giulio Catanzariti · `giuliocatanzariti@gmail.com` · TACITUS · `https://www.tacitus.me/research/tcgc`*
