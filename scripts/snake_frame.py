#!/usr/bin/env python3
"""Frame the Platane/snk snake so it reads like GitHub's contribution graph.

Adds the "N contributions in the last year" line, month and weekday labels,
and a Less-More legend, and holds the full graph on screen for a few seconds
before the snake starts eating.

usage: snake_frame.py CALENDAR_JSON SVG THEME [SVG THEME ...]
  CALENDAR_JSON  output of the GraphQL contributionCalendar query
  THEME          dark | light
"""
import json
import re
import sys
from datetime import date

HOLD_MS = 3000           # full graph on screen before the snake moves
CELL = 16                # snk grid pitch
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
THEMES = {
    "dark": {"text": "#e6edf3", "muted": "#9da7b3", "snake": "#d2a8ff"},
    "light": {"text": "#1f2328", "muted": "#59636e", "snake": "#8250df"},
}
# new viewBox: room on the left for weekday labels, above for the header and
# month labels (the snake parks in the row just above the grid), below for the legend
VB_X, VB_Y, VB_W, VB_H = -36, -58, 900, 246
OUT_W = 880


def load_calendar(path):
    cal = json.load(open(path))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], [date.fromisoformat(w["firstDay"]) for w in cal["weeks"]]


def stretch_keyframes(css, old_ms, hold_ms):
    """Prepend a hold to every animation: p% -> H + p*(1-H), 0% also covers H."""
    new_ms = old_ms + hold_ms
    h = hold_ms / new_ms * 100

    def fix_sel(sel):
        out = []
        for p in sel.split(","):
            v = float(p.strip().rstrip("%"))
            if v == 0:
                out += ["0%", f"{h:.2f}%"]
            else:
                out.append(f"{h + v * (1 - h / 100):.2f}%")
        return ",".join(out)

    def fix_block(m):
        body = re.sub(r"([0-9.,%\s]+)\{", lambda s: fix_sel(s.group(1)) + "{", m.group(2))
        return m.group(1) + body

    css = re.sub(r"(@keyframes [\w-]+\{)((?:[0-9.,%\s]+\{[^}]*\})+)", fix_block, css)
    return css.replace(f"{old_ms}ms", f"{new_ms}ms")


def month_labels(weeks, cols):
    """GitHub-style: label a column when its week starts a new month; skip crowded ones."""
    weeks = weeks[-cols:]
    offset = cols - len(weeks)
    labels, last = [], -99
    for i, d in enumerate(weeks):
        prev = weeks[i - 1] if i else None
        if prev is None or d.month != prev.month:
            col = i + offset
            if col - last >= 3:
                labels.append((col, d.strftime("%b")))
                last = col
    # drop a first label that would collide with the second
    if len(labels) > 1 and labels[1][0] - labels[0][0] < 3:
        labels.pop(0)
    return labels


def frame(svg, theme, total, weeks):
    t = THEMES[theme]
    m = re.search(r"<style>(.*?)</style>", svg, re.S)
    css = m.group(1)
    old_ms = int(re.search(r"(\d+)ms", css).group(1))
    css = stretch_keyframes(css, old_ms, HOLD_MS)
    css = re.sub(r"--cs:[^;]+;", f"--cs:{t['snake']};", css)
    css += (f".lbl{{font-family:{FONT};font-size:10px;fill:{t['muted']}}}"
            f".hdr{{font-family:{FONT};font-size:13px;fill:{t['text']}}}")
    svg = svg[:m.start(1)] + css + svg[m.end(1):]

    xs = [int(x) for x in re.findall(r'<rect class="c[^"]*" x="(\d+)"', svg)]
    cols = (max(xs) - 2) // CELL + 1
    grid_w = cols * CELL

    extra = [f'<text class="hdr" x="0" y="-38">{total:,} contributions in the last year</text>']
    for col, name in month_labels(weeks, cols):
        extra.append(f'<text class="lbl" x="{2 + col * CELL}" y="-20">{name}</text>')
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        extra.append(f'<text class="lbl" x="-8" y="{2 + row * CELL + 10}" text-anchor="end">{name}</text>')
    # legend, right-aligned under the progress bar
    lx = grid_w - 2 - 5 * 14 - 26
    extra.append(f'<text class="lbl" x="{lx - 6}" y="{176}" text-anchor="end">Less</text>')
    for i in range(5):
        extra.append(f'<rect x="{lx + i * 14}" y="167" width="10" height="10" rx="2" '
                     f'fill="var(--c{i})" stroke="var(--cb)"/>')
    extra.append(f'<text class="lbl" x="{lx + 5 * 14 + 2}" y="176">More</text>')

    out_h = round(OUT_W * VB_H / VB_W)
    svg = re.sub(r'<svg viewBox="[^"]*" width="\d+" height="\d+"',
                 f'<svg viewBox="{VB_X} {VB_Y} {VB_W} {VB_H}" width="{OUT_W}" height="{out_h}"', svg, count=1)
    return svg.replace("</svg>", "".join(extra) + "</svg>")


def main(argv):
    total, weeks = load_calendar(argv[1])
    pairs = argv[2:]
    for path, theme in zip(pairs[::2], pairs[1::2]):
        src = open(path).read()
        if "contributions in the last year" in src:
            sys.exit(f"{path}: already framed")
        open(path, "w").write(frame(src, theme, total, weeks))
        print(f"framed {path} ({theme})")


if __name__ == "__main__":
    main(sys.argv)
