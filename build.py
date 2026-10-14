#!/usr/bin/env python3
"""Regenerate index.html from the live GitHub account, and append one line to history.jsonl.

The page is a live reference: it re-reads the account every run rather than trusting
a snapshot. See https://github.com/JaronKBragg7337/live-reference-principle
"""
import json, os, sys, urllib.request, datetime, html, pathlib

OWNER = os.environ.get("SORT_OWNER", "JaronKBragg7337")
ROOT = pathlib.Path(__file__).parent
ORDER = ["A", "B", "C", "D", "E", "?"]
# Second axis: what a repo IS (kind) and how far it got (stage). Tier stays as the
# founding question. "?" kind = created since tiers.json was last edited.
KINDS = {
    "system": ("Systems", "Built to run, keep and show",
               "Things meant to run on their own, keep what happened and show it afterward. Furthest along first. "
               "Anything at the designed stage is marked designed, not built yet: a system on paper, not a lesser one."),
    "theory/principle": ("Theories & principles", "Ideas that carry the other work",
               "Written principles and the experiments around them. These are specification for the systems above, not systems."),
    "book/writing": ("Books & writing", "Finished writing",
               "Books, essays and position papers. Stage does not apply: finished writing is judged as writing."),
    "game/world": ("Games & worlds", "Places to be in",
               "Games, worlds and the materials they are built from. Furthest along first."),
    "tool": ("Tools", "Instruments and materials",
               "Libraries, editors, bridges and asset packs. The same when you return, by design."),
    "life-record": ("Life record", "A life, written down",
               "Written record of a life. Stage does not apply."),
    "test/stub": ("Tests & stubs", "Tests, placeholders and empty shells",
               "Connector checks, exams, placeholders and abandoned shells. Listed for completeness."),
    "?": ("Not yet judged", "Created since the last judgment",
               "Created since tiers.json was last edited. Listed here rather than guessed at."),
}
KIND_ORDER = ["system", "theory/principle", "book/writing", "game/world", "tool", "life-record", "test/stub", "?"]
# Furthest first. spec = designed, not built yet.
STAGES = {
    "accumulates": "accumulates", "runs": "runs", "partial": "partial",
    "spec": "designed, not built yet", "idea": "idea", "n/a": "n/a", "": "not judged",
}


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "accumulation-sort"},
    )
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fetch_repos():
    out, page = [], 1
    while True:
        batch = api(f"/users/{OWNER}/repos?per_page=100&page={page}")
        if not batch:
            break
        out += batch
        if len(batch) < 100:
            break
        page += 1
    return out


TIERS = {
    "A": ("Accumulates", "Substrate — built to retain",
          "Passes all three tests: runs unattended, keeps what happened, and the record is readable afterward. "
          "This is the line the account keeps returning to and keeps dropping."),
    "B": ("Half", "Living world — runs without you, retention unproven",
          "Autonomous behaviour is real: agents act with no player present. What is not established is whether the "
          "world is different tomorrow because of what happened today. One persistence layer from the tier above."),
    "C": ("Place", "Place, tool or material — the same when you return",
          "The largest group, and the best-looking work here. None of it accumulates and none of it is meant to. "
          "This is where the render problem got solved; it should now be a supply of parts, not a source of projects."),
    "D": ("Record", "Written principle — a timestamp, not a system",
          "Not supposed to accumulate; these are the extracted principles themselves. The Live-Reference Principle "
          "and ECIH are load-bearing for the top two tiers and should be read as specification, not as essays."),
    "E": ("Stub", "Test, stub or empty", "Connector checks and abandoned shells. Listed for completeness."),
    "?": ("Unsorted", "Not yet judged",
          "Created since the last time tiers.json was updated. Listed here rather than guessed at."),
}
VERIF = {"live": "live system checked", "code": "source read",
         "readme": "README read", "meta": "metadata only"}


def build():
    repos = [r for r in fetch_repos() if not r.get("archived")]
    tiers = {k: v for k, v in json.loads((ROOT / "tiers.json").read_text("utf-8")).items()
             if not k.startswith("_")}

    rows = []
    for r in sorted(repos, key=lambda x: x["created_at"]):
        j = tiers.get(r["name"], {})
        rows.append({
            "name": r["name"],
            "created": r["created_at"][:10],
            "pushed": r["pushed_at"][:10],
            "size": r["size"],
            "tier": j.get("tier", "?"),
            "kind": j.get("kind", "?"),
            "stage": j.get("stage", ""),
            "principle": j.get("principle", ""),
            "organ": j.get("organ", ""),
            "drift": j.get("readme_drift", ""),
            "judged_at": j.get("last_commit", ""),
            "next": j.get("next_stage", ""),
            "verified": j.get("verified", ""),
            "why": j.get("why", r.get("description") or "No description on GitHub and not yet sorted."),
        })

    today = datetime.date.today().isoformat()
    counts = {k: sum(1 for x in rows if x["tier"] == k) for k in ORDER}

    # Append-only: a line is never rewritten. If the numbers for today have not
    # moved, no line is added — an unchanged day is not an event. When they have,
    # a second line for the same date is appended and the reader below keeps the
    # latest one per date, so the record stays honest without being edited.
    hist_path = ROOT / "history.jsonl"
    raw = []
    if hist_path.exists():
        raw = [json.loads(l) for l in hist_path.read_text("utf-8").splitlines() if l.strip()]
    kinds = {k: sum(1 for x in rows if x["kind"] == k) for k in KIND_ORDER}
    entry = {"date": today, "total": len(rows), "counts": counts, "kinds": kinds}
    # Old lines (tier counts only) are never touched; the first line with kind counts
    # is simply the next line appended.
    if (not raw or raw[-1]["total"] != entry["total"] or raw[-1]["counts"] != entry["counts"]
            or raw[-1].get("kinds") != entry["kinds"]):
        with hist_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        raw.append(entry)

    by_date = {}
    for e in raw:
        by_date[e["date"]] = e
    history = [by_date[d] for d in sorted(by_date)]

    tpl = (ROOT / "template.html").read_text("utf-8")
    page = (tpl
            .replace("/*__ROWS__*/null", json.dumps(rows, ensure_ascii=False))
            .replace("/*__TIERS__*/null", json.dumps(TIERS, ensure_ascii=False))
            .replace("/*__KINDS__*/null", json.dumps(KINDS, ensure_ascii=False))
            .replace("/*__KINDORDER__*/null", json.dumps(KIND_ORDER))
            .replace("/*__STAGES__*/null", json.dumps(STAGES, ensure_ascii=False))
            .replace("/*__VERIF__*/null", json.dumps(VERIF, ensure_ascii=False))
            .replace("/*__HISTORY__*/null", json.dumps(history, ensure_ascii=False))
            .replace("__OWNER__", html.escape(OWNER))
            .replace("__TOTAL__", str(len(rows)))
            .replace("__FIRST__", rows[0]["created"] if rows else "")
            .replace("__BUILT__", today))
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    print(f"{len(rows)} repos -> tiers " + "  ".join(f"{k}:{counts[k]}" for k in ORDER))
    print("kinds " + "  ".join(f"{k}:{kinds[k]}" for k in KIND_ORDER))
    unsorted = [x["name"] for x in rows if x["tier"] == "?" or x["kind"] == "?"]
    if unsorted:
        print("NOT YET JUDGED:", ", ".join(unsorted))


if __name__ == "__main__":
    build()
