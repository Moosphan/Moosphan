#!/usr/bin/env python3
"""Render the two dark stat cards + the local GitHub-style preview.

Left card mirrors github-readme-stats (rows + rank ring); right card mirrors
the productive-time card (commits per hour). Numbers come from data.json.

Usage:
    python3 build.py
"""
import json
import pathlib

import markdown

import kit

ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

FONT, BG, BORDER, TEXT, DIM, FAINT = (
    kit.FONT, kit.BG, kit.BORDER, kit.TEXT, kit.DIM, kit.FAINT,
)
PURPLE = "#bb9af7"
TEAL = "#73daca"
BLUE = "#7aa2f7"
GREEN = "#9ece6a"
GRID = "#262b40"

ICONS = {
    "star": '<path d="M6 .8l1.7 3.5 3.8.5-2.8 2.7.7 3.8L6 9.4l-3.4 1.9.7-3.8L.5 4.8l3.8-.5z" fill="{c}"/>',
    "clock": (
        '<circle cx="6" cy="6" r="5" fill="none" stroke="{c}" stroke-width="1.1"/>'
        '<path d="M6 3.1V6l2 1.4" stroke="{c}" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
    ),
    "pr": (
        '<circle cx="3" cy="3" r="1.7" fill="none" stroke="{c}" stroke-width="1.1"/>'
        '<circle cx="3" cy="9" r="1.7" fill="none" stroke="{c}" stroke-width="1.1"/>'
        '<path d="M3 4.7v2.6" stroke="{c}" stroke-width="1.1"/>'
        '<circle cx="9" cy="9" r="1.7" fill="none" stroke="{c}" stroke-width="1.1"/>'
        '<path d="M9 7.3V4.6a1.6 1.6 0 00-1.6-1.6H6" stroke="{c}" stroke-width="1.1" fill="none"/>'
    ),
    "issue": (
        '<circle cx="6" cy="6" r="5" fill="none" stroke="{c}" stroke-width="1.1"/>'
        '<circle cx="6" cy="6" r="1.5" fill="{c}"/>'
    ),
    "repo": (
        '<rect x="2.2" y="1.4" width="7.6" height="9.2" rx="1.2" fill="none" stroke="{c}" stroke-width="1.1"/>'
        '<path d="M4.5 1.4v9.2" stroke="{c}" stroke-width="1"/>'
    ),
}


def stats_card():
    rows = [
        ("star", "Total Stars Earned", f'{DATA["stars"]:,}'),
        ("clock", "Total Commits", f'{DATA["commits"]:,}'),
        ("pr", "Total PRs", f'{DATA["prs"]:,}'),
        ("issue", "Total Issues", f'{DATA["issues"]:,}'),
        ("repo", "Contributed to (last year)", f'{DATA["contributed_to"]:,}'),
    ]
    body = [
        f'<text x="24" y="34" font-family="{FONT}" font-size="15" font-weight="700" fill="{PURPLE}">'
        f'{DATA["display_name"]}\'s GitHub Stats</text>'
    ]
    for i, (icon, label, value) in enumerate(rows):
        y = 64 + i * 24
        body.append(
            f'<g transform="translate(24,{y - 9})">{ICONS[icon].format(c=BLUE)}</g>'
            f'<text x="46" y="{y}" font-family="{FONT}" font-size="11.5" fill="{TEAL}">{label}</text>'
            f'<text x="300" y="{y}" text-anchor="end" font-family="{FONT}" font-size="11.5" font-weight="600" fill="{PURPLE}">{value}</text>'
        )

    cx, cy, r = 368, 100, 40
    circumference = 2 * 3.141592653589793 * r
    body.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="7"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" '
        f'stroke-dasharray="{circumference * 0.72:.1f} {circumference:.1f}" '
        f'transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy + 9}" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="700" fill="{GREEN}">'
        f'{DATA["rank"]}</text>'
    )
    return kit.card(430, 190, "".join(body))


def hours_card():
    hours = DATA["hours"]
    peak = max(hours)
    ymax = 20 * ((peak + 19) // 20) or 20

    x0, x1, y0, y1 = 58, 404, 50, 148
    slot = (x1 - x0) / 24
    parts = [
        f'<text x="215" y="34" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="{PURPLE}">'
        f'Commits (UTC +8.00)</text>'
    ]
    for tick in range(0, ymax + 1, ymax // 5):
        y = y1 - (tick / ymax) * (y1 - y0)
        parts.append(
            f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>'
            f'<text x="{x0 - 8}" y="{y + 3:.1f}" text-anchor="end" font-family="{FONT}" font-size="8" fill="{DIM}">{tick}</text>'
        )
    for h in range(24):
        height = (hours[h] / ymax) * (y1 - y0)
        if height <= 0:
            continue
        parts.append(
            f'<rect x="{x0 + h * slot + (slot - 9) / 2:.1f}" y="{y1 - height:.1f}" width="9" height="{height:.1f}" '
            f'rx="1.5" fill="{PURPLE}"/>'
        )
    for h in (0, 6, 12, 18, 23):
        parts.append(
            f'<text x="{x0 + h * slot + slot / 2:.1f}" y="{y1 + 14}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="8" fill="{DIM}">{h}</text>'
        )
    parts.append(
        f'<text x="215" y="{y1 + 30}" text-anchor="middle" font-family="{FONT}" font-size="8.5" fill="{DIM}">'
        f'per day hour · {DATA["commits_sampled"]:,} sampled commits</text>'
    )
    return kit.card(430, 190, "".join(parts))


def preview(body_html):
    css = kit.GITHUB_CSS % kit.THEMES["dark"]
    header = kit.HEADER.format(
        name='Moosphan <span style="color:#9198a1;font-weight:400;font-size:22px">(Ziya)</span>',
        bio=f'{DATA["followers"]} followers · {DATA["public_repos"]} repositories · Shanghai',
    )
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>profile readme preview</title>
<style>{css}</style></head>
<body>{header}{body_html}{kit.FOOTER}</body></html>
"""


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "stats.svg").write_text(stats_card(), encoding="utf-8")
    (ROOT / "assets" / "hours.svg").write_text(hours_card(), encoding="utf-8")

    md_text = (ROOT / "README.md").read_text(encoding="utf-8")
    md_text = md_text.replace('<div align="center">', '<div align="center" markdown="1">')
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "md_in_html"])
    (ROOT / "preview.html").write_text(preview(body), encoding="utf-8")
    print("built assets/stats.svg, assets/hours.svg, preview.html")


if __name__ == "__main__":
    main()
