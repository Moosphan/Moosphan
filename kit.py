#!/usr/bin/env python3
"""Shared kit for the profile-README variants: palette, SVG card shell, GitHub-like CSS."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif,sans-serif"
BG = "#1a1b27"
BORDER = "#2f334d"
TEXT = "#c0caf5"
DIM = "#565f89"
FAINT = "#3b4261"
ACCENT = "#7aa2f7"

LANG_COLORS = {
    "Kotlin": "#A97BFF",
    "Java": "#b07219",
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "Dart": "#00B4AB",
    "TypeScript": "#3178c6",
    "Swift": "#F05138",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
}


def card(width, height, body):
    """Dark rounded panel that wraps a card body."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="9" fill="{BG}" stroke="{BORDER}"/>
  {body}
</svg>
"""


GITHUB_CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: %(page_bg)s; color: %(fg)s;
  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;
  font-size: 16px; line-height: 1.5; -webkit-font-smoothing: antialiased; }
a { color: %(link)s; text-decoration: none; }
a:hover { text-decoration: underline; }
.page { max-width: 1012px; margin: 0 auto; padding: 24px 16px 48px; }
.profile-head { display: flex; gap: 16px; align-items: center; padding: 8px 8px 20px; }
.profile-head img { width: 64px; height: 64px; border-radius: 50%%; border: 1px solid %(border)s; }
.profile-head h2 { margin: 0; font-size: 24px; font-weight: 400; line-height: 1.25; }
.profile-head p { margin: 4px 0 0; font-size: 14px; color: %(dim)s; }
.tabs { display: flex; gap: 8px; padding: 0 8px; border-bottom: 1px solid %(border)s; margin-bottom: 24px; }
.tabs span { padding: 8px 8px 10px; font-size: 14px; color: %(dim)s; }
.tabs span.active { color: %(fg)s; font-weight: 600; border-bottom: 2px solid %(accent)s; margin-bottom: -1px; }
.markdown-body { border: 1px solid %(border)s; border-radius: 6px; padding: 32px 40px; background: %(card_bg)s; }
.markdown-body > :first-child { margin-top: 0 !important; }
.markdown-body h1 { font-size: 2em; font-weight: 600; border-bottom: 1px solid %(border)s;
  padding-bottom: .3em; margin: 24px 0 16px; }
.markdown-body h2 { font-size: 1.5em; font-weight: 600; border-bottom: 1px solid %(border)s;
  padding-bottom: .3em; margin: 24px 0 16px; }
.markdown-body p, .markdown-body ul, .markdown-body ol { margin: 0 0 16px; }
.markdown-body img { max-width: 100%%; vertical-align: middle; }
.markdown-body hr { height: .25em; padding: 0; margin: 24px 0; background: %(border)s; border: 0; }
.markdown-body table { display: block; width: max-content; max-width: 100%%; overflow: auto;
  border-collapse: collapse; margin: 0 0 16px; }
.markdown-body th, .markdown-body td { padding: 6px 13px; border: 1px solid %(border)s; }
.markdown-body th { font-weight: 600; background: %(thead_bg)s; }
.markdown-body tr:nth-child(2n) { background: %(striped)s; }
.markdown-body blockquote { margin: 0 0 16px; padding: 0 1em; color: %(dim)s;
  border-left: .25em solid %(border)s; }
.markdown-body code { padding: .2em .4em; font-size: 85%%; background: %(code_bg)s; border-radius: 6px; }
.markdown-body div[align="center"] { text-align: center; }
.markdown-body div[align="center"] img { display: inline-block; }
.markdown-body sub { font-size: 11px; color: %(dim)s; }
"""

THEMES = {
    "light": dict(
        page_bg="#ffffff", card_bg="#ffffff", fg="#1f2328", link="#0969da", dim="#59636e",
        border="#d1d9e0", thead_bg="#f6f8fa", striped="#f6f8fa", code_bg="rgba(175,184,193,.2)",
        accent="#fd8c73",
    ),
    "dark": dict(
        page_bg="#0d1117", card_bg="#0d1117", fg="#e6edf3", link="#4493f8", dim="#9198a1",
        border="#3d444d", thead_bg="#151b23", striped="#151b23", code_bg="rgba(101,108,118,.2)",
        accent="#f78166",
    ),
}

HEADER = """
<div class="page">
  <div class="profile-head">
    <img src="https://avatars.githubusercontent.com/u/31280310?v=4" alt="avatar" />
    <div>
      <h2>{name}</h2>
      <p>{bio}</p>
    </div>
  </div>
  <div class="tabs"><span class="active">Overview</span><span>Repositories</span><span>Stars</span></div>
  <article class="markdown-body">
"""

FOOTER = "</article></div>"
