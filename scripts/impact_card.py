#!/usr/bin/env python3
"""Rebuild the impact card from live GitHub search counts.

Reads assets/impact-{theme}.svg as the template and writes the updated card.
Counts upstream pull requests only (repos owned by someone else).

usage: impact_card.py LOGIN TEMPLATE OUT [TEMPLATE OUT ...]
Needs the gh CLI with a token (GH_TOKEN in CI).
"""
import json
import re
import subprocess
import sys


def search(login, state):
    q = f"author:{login} type:pr {state} -user:{login}"
    out = subprocess.run(
        ["gh", "api", "-X", "GET", "search/issues", "-f", f"q={q}", "-f", "per_page=100",
         "--jq", "[.items[].repository_url]"],
        check=True, capture_output=True, text=True).stdout
    return [u.rsplit("/", 1)[1] for u in json.loads(out)]


def plural(n, one, many):
    return one if n == 1 else many


def card(template, merged, open_):
    seen = list(dict.fromkeys(merged))
    projects = sorted(seen, key=lambda p: -merged.count(p))  # most merged first, ties by recency
    names = projects[:3]
    names_line = ", ".join(names) + (f" +{len(projects) - 3}" if len(projects) > 3 else "")
    n_m, n_p, n_o = len(merged), len(projects), len(open_)
    texts = [
        str(n_m), f"merged upstream {plural(n_m, 'pull request', 'pull requests')}", names_line,
        str(n_p), f"open-source {plural(n_p, 'project', 'projects')}", "with my merged fixes",
        str(n_o), f"{plural(n_o, 'pull request', 'pull requests')} in review", "awaiting maintainer review",
    ]
    parts = re.split(r"(<text[^>]*>)[^<]*(</text>)", template)
    # re.split with two groups yields: chunk, open, close, chunk, open, close, ...
    if (len(parts) - 1) // 3 != len(texts):
        sys.exit("template has an unexpected number of <text> elements")
    out = [parts[0]]
    for i, t in enumerate(texts):
        out += [parts[1 + i * 3], t, parts[2 + i * 3], parts[3 + i * 3]]
    svg = "".join(out)
    title = (f"Impact: {texts[0]} {texts[1]}; {texts[3]} {texts[4]} {texts[5]}; "
             f"{texts[6]} {plural(n_o, 'pull request', 'pull requests')} {texts[8]}.")
    return re.sub(r'(<title id="t">)[^<]*(</title>)', lambda m: m.group(1) + title + m.group(2), svg, count=1)


def main(argv):
    login, pairs = argv[1], argv[2:]
    merged = search(login, "is:merged")
    open_ = search(login, "is:open")
    for tpl, out in zip(pairs[::2], pairs[1::2]):
        svg = card(open(tpl).read(), merged, open_)
        open(out, "w").write(svg)
        print(f"wrote {out}: {len(merged)} merged, {len(set(merged))} projects, {len(open_)} open")


if __name__ == "__main__":
    main(sys.argv)
