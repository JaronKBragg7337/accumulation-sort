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

## The tiers

| | |
|---|---|
| **A · Accumulates** | Runs unattended, keeps what happened, record is readable afterward. |
| **B · Half** | Autonomous behaviour is real; cross-session retention unproven. |
| **C · Place** | A place, tool or material. The same when you return. |
| **D · Record** | Written principle. A timestamp, not a system — and not meant to be one. |
| **E · Stub** | Test, stub or empty. |
| **? · Unsorted** | Created since `tiers.json` was last edited. Listed, not guessed at. |

## Files

| file | role |
|---|---|
| `tiers.json` | The judgments. The only file meant to be hand-edited. |
| `build.py` | Reads the API, merges the judgments, writes `index.html`, appends `history.jsonl`. |
| `template.html` | Page shell. `build.py` substitutes the data in. |
| `history.jsonl` | Append-only. One line per rebuild. Never rewritten. |
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
"repo-name": {"tier":"A","verified":"code","why":"One sentence on what it retains and how."}
```

`verified` records how far checking actually went — `code` (file tree or source inspected),
`readme` (README read), or `meta` (description and size only). Rows marked `meta` are the ones
most likely to be wrong, and the page says so. Being honest about the depth of a claim is the
same discipline the sort is measuring.
