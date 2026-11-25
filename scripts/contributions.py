#!/usr/bin/env python3
"""Rebuild the upstream contributions table in README.md from live GitHub data.

Finds my merged and open pull requests in repos I don't own, adds the
co-authored PRs listed in contributions.json, and rewrites the block between
<!-- contributions:start --> and <!-- contributions:end -->. Closed-unmerged
PRs never appear. Star counts and PR states are live shields.io badges, so
the markdown only changes when the set of PRs or their status changes.

usage: contributions.py LOGIN README [--check]
  --check  exit 1 if README would change, write nothing
Needs the gh CLI with a token (GH_TOKEN in CI).
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
START, END = "<!-- contributions:start -->", "<!-- contributions:end -->"
RANK = {"merged": 0, "coauthored": 1, "open": 2}


def gh(*args):
    out = subprocess.run(["gh", "api", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def search(login, state):
    q = f"author:{login} type:pr {state} -user:{login}"
    data = gh("-X", "GET", "search/issues", "-f", f"q={q}", "-f", "per_page=100")
    rows = []
    for it in data["items"]:
        repo = it["repository_url"].split("/repos/", 1)[1]
        rows.append({
            "repo": repo, "number": it["number"], "title": it["title"],
            "url": it["html_url"],
            "date": (it.get("pull_request") or {}).get("merged_at") or it["created_at"],
        })
    return rows


def collect(login, config=None):
    """Return (prs, stars). Each PR: repo, number, url, status, impact, from_pr."""
    if config is None:
        config = json.load(open(os.path.join(HERE, "contributions.json")))
    prs = []
    for state, status in (("is:merged", "merged"), ("is:open", "open")):
        for p in search(login, state):
            p["status"] = status
            prs.append(p)
    for co in config.get("coauthored", []):
        repo, num = co["pr"].split("#")
        pr = gh(f"repos/{repo}/pulls/{num}")
        if pr["state"] == "closed" and not pr.get("merged_at"):
            continue  # folded PR was closed without merging: nothing to show
        prs.append({
            "repo": repo, "number": int(num), "title": pr["title"], "url": pr["html_url"],
            "date": pr.get("merged_at") or pr["created_at"],
            "status": "coauthored", "merged": bool(pr.get("merged_at")),
            "from_pr": co.get("mine"),
        })
    for p in prs:
        p["impact"] = config.get("prs", {}).get(f"{p['repo']}#{p['number']}", p["title"])
    stars = {r: gh(f"repos/{r}")["stargazers_count"] for r in dict.fromkeys(p["repo"] for p in prs)}
    return prs, stars


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table(prs, stars, notes):
    by_repo = {}
    for p in prs:
        by_repo.setdefault(p["repo"], []).append(p)
    for rows in by_repo.values():
        rows.sort(key=lambda p: (RANK[p["status"]], -_ts(p["date"])))
    order = sorted(by_repo, key=lambda r: (min(RANK[p["status"]] for p in by_repo[r]), -stars[r]))

    out = ["<table>",
           '<tr><th align="left">Project</th><th align="left">Pull request</th>'
           '<th align="left">What changed for users</th></tr>']
    for repo in order:
        owner, name = repo.split("/")
        rows = by_repo[repo]
        note = notes.get(repo)
        project = (
            f'<img src="https://github.com/{owner}.png?size=40" width="20" height="20" alt="{owner} avatar">'
            f' <a href="https://github.com/{repo}"><b>{name}</b></a><br>'
            f'<img src="https://img.shields.io/github/stars/{repo}?style=flat&label=stars&logo=github&color=555"'
            f' height="20" alt="{name} GitHub stars">'
            + (f"<br><sub>{esc(note)}</sub>" if note else "")
        )
        for i, p in enumerate(rows):
            n = p["number"]
            badge = (f'<img src="https://img.shields.io/github/pulls/detail/state/{repo}/{n}?style=flat&label=PR"'
                     f' height="20" alt="PR #{n} live state">')
            cell = f'<a href="{p["url"]}"><b>#{n}</b></a><br>{badge}'
            if p["status"] == "coauthored":
                mine = p.get("from_pr", "")
                mine_n = mine.split("#")[1] if "#" in mine else ""
                cell += "<br><sub>co-author" + (
                    f', from my <a href="https://github.com/{repo}/pull/{mine_n}">#{mine_n}</a>' if mine_n else "") + "</sub>"
            tds = []
            if i == 0:
                span = f' rowspan="{len(rows)}"' if len(rows) > 1 else ""
                tds.append(f'<td{span} valign="top">{project}</td>')
            tds.append(f'<td valign="top" nowrap>{cell}</td>')
            tds.append(f'<td valign="top">{esc(p["impact"])}</td>')
            out.append("<tr>" + "".join(tds) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def _ts(iso):
    return int(re.sub(r"\D", "", iso)[:14] or 0)


def render(readme_text, block):
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pat.search(readme_text):
        sys.exit("README has no contributions markers")
    return pat.sub(lambda m: f"{START}\n{block}\n{END}", readme_text, count=1)


def main(argv):
    login, readme = argv[1], argv[2]
    config = json.load(open(os.path.join(HERE, "contributions.json")))
    prs, stars = collect(login, config)
    text = open(readme).read()
    new = render(text, table(prs, stars, config.get("notes", {})))
    if "--check" in argv:
        sys.exit(0 if new == text else 1)
    if new != text:
        open(readme, "w").write(new)
    counts = {s: sum(p["status"] == s for p in prs) for s in RANK}
    print(f"{readme}: {'updated' if new != text else 'unchanged'} {counts}")


if __name__ == "__main__":
    main(sys.argv)
