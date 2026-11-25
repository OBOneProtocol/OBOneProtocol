#!/usr/bin/env python3
"""Build the headline stats card from live GitHub data.

Four tiles: merged upstream pull requests, projects with my merged fixes,
GitHub stars on those projects, and fixes in review (authored or co-authored).
Counts come from contributions.collect(), the same data as the README table.

usage: impact_card.py LOGIN light OUT.svg [dark OUT.svg ...]
Needs the gh CLI with a token (GH_TOKEN in CI).
"""
import sys

from contributions import collect

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
THEMES = {
    "dark": dict(bg="#0d1117", tile="#161b22", border="#30363d", text="#e6edf3", muted="#9da7b3",
                 accents=["#58a6ff", "#3fb950", "#e3b341", "#d2a8ff"]),
    "light": dict(bg="#ffffff", tile="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  accents=["#0969da", "#1a7f37", "#9a6700", "#8250df"]),
}
W, H, PAD, GAP = 880, 124, 20, 16


def plural(n, one, many):
    return one if n == 1 else many


def short(n):
    if n >= 10_000:
        return f"{n // 1000}K"
    if n >= 1000:
        return f"{n / 1000:.1f}K".replace(".0K", "K")
    return str(n)


def stats(prs, stars):
    merged = [p for p in prs if p["status"] == "merged" or (p["status"] == "coauthored" and p.get("merged"))]
    pending = [p for p in prs if p not in merged]
    projects = list(dict.fromkeys(p["repo"] for p in merged))
    projects.sort(key=lambda r: -sum(p["repo"] == r for p in merged))
    names = [r.split("/")[1] for r in projects]
    names_line = ", ".join(names[:3]) + (f" +{len(names) - 3}" if len(names) > 3 else "")
    total_stars = sum(stars[r] for r in projects)
    n_auth = sum(p["status"] == "open" for p in pending)
    n_co = len(pending) - n_auth
    parts = [f"{n_auth} authored"] if n_auth else []
    parts += [f"{n_co} co-authored"] if n_co else []
    return [
        (str(len(merged)), f"upstream {plural(len(merged), 'PR', 'PRs')} merged", names_line or "none yet"),
        (str(len(projects)), f"open-source {plural(len(projects), 'project', 'projects')}", "with my merged fixes"),
        (short(total_stars), "GitHub stars", "on those projects"),
        (str(len(pending)), f"{plural(len(pending), 'fix', 'fixes')} in review", ", ".join(parts) or "none open"),
    ]


def card(tiles, theme):
    t = THEMES[theme]
    tw = (W - 2 * PAD - 3 * GAP) / 4
    title = "; ".join(f"{a} {b} ({c})" for a, b, c in tiles)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
        f'<title id="t">Impact, from live GitHub data: {title}.</title>',
        "<style>.tile{animation:up .6s ease-out both}@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
        ".bar{animation:grow .8s ease-out both;transform-box:fill-box;transform-origin:left}@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@media (prefers-reduced-motion:reduce){.tile,.bar{animation:none}}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
    ]
    for i, (big, label, sub) in enumerate(tiles):
        x = PAD + i * (tw + GAP)
        cx = x + tw / 2
        a = t["accents"][i]
        out.append(
            f'<g class="tile" style="animation-delay:{0.15 + i * 0.2:.2f}s">'
            f'<rect x="{x:.1f}" y="16" width="{tw:.1f}" height="{H - 32}" rx="10" fill="{t["tile"]}" stroke="{t["border"]}"/>'
            f'<rect class="bar" style="animation-delay:{0.45 + i * 0.2:.2f}s" x="{x + 14:.1f}" y="16" width="{tw - 28:.1f}" height="3" rx="1.5" fill="{a}"/>'
            f'<text x="{cx:.1f}" y="54" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="{a}">{big}</text>'
            f'<text x="{cx:.1f}" y="77" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="{t["text"]}">{label}</text>'
            f'<text x="{cx:.1f}" y="95" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{t["muted"]}">{sub}</text></g>'
        )
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main(argv):
    login, pairs = argv[1], argv[2:]
    prs, stars = collect(login)
    tiles = stats(prs, stars)
    for theme, path in zip(pairs[::2], pairs[1::2]):
        open(path, "w").write(card(tiles, theme))
        print(f"wrote {path}: " + " | ".join(f"{a} {b}" for a, b, _ in tiles))


if __name__ == "__main__":
    main(sys.argv)
