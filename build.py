#!/usr/bin/env python3
"""Regenerate index.html from the live GitHub account, and append one line to history.jsonl.

The page is a live reference: it re-reads the account every run rather than trusting
a snapshot. See https://github.com/JaronKBragg7337/live-reference-principle
"""
import json, os, sys, urllib.request, datetime, html, pathlib

OWNER = os.environ.get("SORT_OWNER", "JaronKBragg7337")
ROOT = pathlib.Path(__file__).parent
ORDER = ["A", "B", "C", "D", "E", "?"]


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
VERIF = {"code": "source read", "readme": "README read", "meta": "metadata only"}


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
            "verified": j.get("verified", ""),
            "why": j.get("why", r.get("description") or "No description on GitHub and not yet sorted."),
        })

    today = datetime.date.today().isoformat()
    counts = {k: sum(1 for x in rows if x["tier"] == k) for k in ORDER}

    hist_path = ROOT / "history.jsonl"
    history = []
    if hist_path.exists():
        history = [json.loads(l) for l in hist_path.read_text("utf-8").splitlines() if l.strip()]
    if not history or history[-1]["date"] != today:
        entry = {"date": today, "total": len(rows), "counts": counts}
        history.append(entry)
        with hist_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    tpl = (ROOT / "template.html").read_text("utf-8")
    page = (tpl
            .replace("/*__ROWS__*/null", json.dumps(rows, ensure_ascii=False))
            .replace("/*__TIERS__*/null", json.dumps(TIERS, ensure_ascii=False))
            .replace("/*__VERIF__*/null", json.dumps(VERIF, ensure_ascii=False))
            .replace("/*__HISTORY__*/null", json.dumps(history, ensure_ascii=False))
            .replace("__OWNER__", html.escape(OWNER))
            .replace("__TOTAL__", str(len(rows)))
            .replace("__FIRST__", rows[0]["created"] if rows else "")
            .replace("__BUILT__", today))
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    print(f"{len(rows)} repos -> " + "  ".join(f"{k}:{counts[k]}" for k in ORDER))
    if counts["?"]:
        print("UNSORTED:", ", ".join(x["name"] for x in rows if x["tier"] == "?"))


if __name__ == "__main__":
    build()
