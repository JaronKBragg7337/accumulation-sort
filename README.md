# The Accumulation Sort

Every public repo on this account, sorted by one question:

> Does it **run without you**, is it **changed by having run**, and is that change **legible when you come back**?

Continuation plus memory plus consequence. A screensaver passes the first test and fails the other two.

**Live page:** https://jaronkbragg7337.github.io/accumulation-sort/

---

## Why it rebuilds itself

A page about systems that keep their own record would be a gesture if it did not keep one. Per the
[Live-Reference Principle](https://github.com/JaronKBragg7337/live-reference-principle), a frozen
reference stops being valid the moment the thing it refers to moves on — and an account that gains
ten repos a month moves on fast. The predecessor to this page,
[Summary-Of-repos-Memory-linker](https://github.com/JaronKBragg7337/Summary-Of-repos-Memory-linker),
was verified from fresh clones on 2026-07-12 and was stale inside a month.

So this one re-reads the GitHub API on every run, and appends a line to `history.jsonl` describing
what it found. Once there are two lines, the page grows a **Drift** table showing what has moved
since it started watching. The sort becomes a time series instead of an opinion.

## Two axes and a founding question

Every repo carries three labels. The page groups by the first, orders by the second, and keeps the third as a badge.

**Kind: what it is.** The page's main sections.

| kind | meaning |
|---|---|
| `system` | Built to run, keep what happened and show it. |
| `theory/principle` | A written principle, or the experiments around one. |
| `book/writing` | Finished writing: books, essays, position papers. |
| `game/world` | A game or world, or the materials one is built from. |
| `tool` | A library, editor, bridge or asset pack. |
| `life-record` | A life written down. |
| `test/stub` | A test, exam, placeholder or empty shell. |

**Stage: how far it got.** Sorts each section, furthest first. `n/a` for books and the life record.

| stage | meaning |
|---|---|
| `accumulates` | Runs, keeps what happened, and the record is readable. |
| `runs` | Works when started; nothing yet keeps or schedules it. |
| `partial` | Some real parts, not yet a whole. |
| `spec` | Designed, not built yet. |
| `idea` | Named, outline only. |

**Tier: the founding question** (the page's original sort, kept as a secondary badge).

| | |
|---|---|
| **A · Accumulates** | Runs unattended, keeps what happened, record is readable afterward. |
| **B · Half** | Autonomous behaviour is real; cross-session retention unproven. |
| **C · Place** | A place, tool or material. The same when you return. |
| **D · Record** | Written principle or design. A timestamp, not a running system. |
| **E · Stub** | Test, stub or empty. |
| **? · Not yet judged** | Created since `tiers.json` was last edited. Listed, not guessed at. |

The month-by-month timeline colours each tile by kind.

## Files

| file | role |
|---|---|
| `tiers.json` | The judgments (kind, stage, tier and more). The only file meant to be hand-edited. |
| `build.py` | Reads the API, merges the judgments, writes `index.html`, appends `history.jsonl`. |
| `template.html` | Page shell. `build.py` substitutes the data in. |
| `history.jsonl` | Append-only. One line per change, with tier counts and (since 2026-10-14) kind counts. Never rewritten. |
| `index.html` | Generated. Do not edit by hand — it is overwritten every run. |

## Run it locally

```bash
python build.py
```

No dependencies beyond the standard library. Set `GITHUB_TOKEN` to raise the API rate limit, and
`SORT_OWNER` to point it at a different account.

## Adding a judgment

Edit `tiers.json`:

```json
"repo-name": {
  "tier": "A", "kind": "system", "stage": "accumulates", "verified": "code",
  "why": "One or two sentences on what it is and what it keeps.",
  "principle": "The idea the repo carries, in one sentence.",
  "organ": "long-term memory",
  "readme_drift": "",
  "last_commit": "2026-10-13",
  "next_stage": "What moving up one stage needs (optional)."
}
```

- `principle`: the idea the repo carries. `organ`: which part of a larger AI-built-from-parts it would be
  (core, senses, judgment, working memory, long-term memory, permanent memory, face, money, world, none).
- `readme_drift`: where the README and the code disagree; leave empty when they agree. The card shows it when present.
- `last_commit`: the latest commit the judgment was made against. If the repo is pushed after this date the card says so.
- `verified` records how far checking went: `code` (source read), `readme`, `meta` (description and size only) or `live`
  (a running deployment checked). Being honest about the depth of a claim is the discipline the sort measures.
- Where two readers disagreed, use the one that cites code or commits and add `(second reader: ...)` to `why`.
- A system at `spec` stage is written as designed, not built yet. Never as "only a document".

Judgments of 2026-10-14 come from a full code read of all 107 repos plus an independent second read.
