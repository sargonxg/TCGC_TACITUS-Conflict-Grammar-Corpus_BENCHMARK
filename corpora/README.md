# `corpora/` — public-domain text fixtures for TCGC

This directory holds **manifests**, not text. Each manifest points to an immutable, freely licensed source (mostly Project Gutenberg) and describes:

- which character spans matter,
- which TCGC task types the text exercises,
- which ACO primitives are dense in it,
- one or more anchor questions, with the typed-subgraph answer we expect a good system to produce.

The goal is to make the benchmark **reproducible without redistributing the source**, and to ground it in texts that:

1. Every modern frontier model has seen during pre-training (so the benchmark is *not* a memorisation test — it is a structural-reasoning test).
2. Have stable canonical references — Project Gutenberg URLs, Wikisource editions, public-domain academic translations.
3. Are dense in conflict-grammar primitives (actors with overlapping interests, time-stamped commitments, contested narratives, leverage asymmetries, contradicting accounts).

## Why public-domain classics?

A benchmark on conflict reasoning is more useful when the *facts* are not in dispute and only the *structural reading* is. Classical political philosophy and historiography give us thousands of years of densely-typed source material with stable citation conventions:

- **Federalist Papers** (Hamilton / Madison / Jay vs Anti-Federalists) — commitments, counter-claims, constitutional negotiation.
- **Melian Dialogue** (Thucydides, V.84–116) — leverage asymmetry, position vs interest, ultimatum, commitment breach.
- **Leviathan** (Hobbes) vs **The Prince** (Machiavelli) — narrative drift on the same primitive ("the sovereign", "the prince").
- **Caesar's Commentaries on the Gallic War** — actor disambiguation across dozens of tribes, alliance dynamics.
- **The Art of War** (Sun Tzu, Giles translation) — leverage classification, narrative framing, deception as a typed move.
- **Athenian Constitution** (Aristotle) — institutional commitment vs lapsed practice.
- **Discourses on Livy** (Machiavelli) — long-horizon causal chains, retrospective analysis.

These texts are not soft humanities scaffolding. They are dense in the *exact* primitives we test: who said what to whom under what constraint with what leverage and what commitment. The Melian Dialogue alone has more typed structure per paragraph than most modern policy memos.

## Manifest format

```jsonc
{
  "id": "<short-slug>",
  "title": "<work>",
  "author": "<author>",
  "translator": "<if applicable>",
  "license": "Public Domain",
  "source": {
    "kind": "gutenberg | wikisource | internet-archive | perseus | other",
    "url": "https://...",
    "edition": "<edition identifier>",
    "retrieved": "ISO-8601 date"
  },
  "anchors": [
    {
      "id": "<anchor-id>",
      "span": { "start": 12345, "end": 13456 },      // character offsets into the canonical URL body
      "primitives_dense": ["actor", "claim", "commitment"],
      "task_types": ["actor-resolution", "commitment-tracking"],
      "question": "<the analyst-style question>",
      "expected_subgraph_summary": "<one-paragraph human-readable summary>"
    }
  ],
  "notes": "<editorial notes, including known translation quirks>"
}
```

## Reproducibility

We do **not** vendor the source text in this repo. Reasons:

- The canonical URL is the citation; that is the point.
- Storing the bytes here introduces a copyright-adjacent question for translations (some are PD; some are not in every jurisdiction).
- Character offsets against a stable Gutenberg URL are robust enough; if the source ever changes, we treat it as a corpus version bump and refresh manifests.

A small fetcher utility (`scripts/fetch_corpora.py`) downloads sources locally for evaluation runs and verifies content hashes against the manifest.

## Adding a new manifest

1. Pick a public-domain text dense in conflict primitives.
2. Identify 1–4 anchor passages.
3. Write the manifest using the format above.
4. Open a PR. The validator (`tcgc validate-corpora`) checks the JSON shape and the URL liveness.
