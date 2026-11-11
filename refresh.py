#!/usr/bin/env python3
"""Refresh data.json from the GitHub API + the public profile pages.

Usage:
    python3 refresh.py && python3 build.py
"""
import datetime
import json
import os
import pathlib
import re
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
USER = "Moosphan"
TOKEN = os.environ.get("GITHUB_TOKEN", "")  # 有 token 时算认证请求，额度 5000/h
TZ = datetime.timezone(datetime.timedelta(hours=8))


def get_json(url):
    headers = {"User-Agent": "profile-card-builder"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-card-builder"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def contributions():
    """Public contribution calendar: (total, [[date, level], ...])."""
    html = get_text(f"https://github.com/users/{USER}/contributions")
    # 页面里图表 DOM 会出现两份，按 tooltip 逐个计数
    total = sum(int(m.group(1)) for m in re.finditer(r"<tool-tip[^>]*>\s*(\d+)\s+contribution", html))
    rows = re.findall(r'data-date="([0-9-]+)"[\s\S]{0,120}?data-level="(\d)"', html)
    return total, [[d, int(lvl)] for d, lvl in sorted(set(rows))]


def search_count(query, kind="issues"):
    url = (
        f"https://api.github.com/search/{kind}?q={urllib.parse.quote(query)}&per_page=1"
    )
    return get_json(url)["total_count"]


def commit_sample(repos, limit=40):
    """Author commit timestamps from public repos → hour histogram (UTC+8)."""
    hours = [0] * 24
    recent = set()
    sampled = 0
    cut = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365)
    for repo in repos[:limit]:
        try:
            commits = get_json(
                f"https://api.github.com/repos/{repo['full_name']}/commits"
                f"?author={USER}&per_page=100"
            )
        except Exception:
            continue
        for c in commits:
            when = datetime.datetime.fromisoformat(
                c["commit"]["author"]["date"].replace("Z", "+00:00")
            ).astimezone(TZ)
            hours[when.hour] += 1
            sampled += 1
            if when >= cut.astimezone(TZ):
                recent.add(repo["full_name"])
    return hours, len(recent), sampled


def rank_letter(stats):
    """Rough letter grade over a weighted activity score (github-readme-stats weights)."""
    score = (
        stats["commits"] * 2
        + stats["prs"] * 3
        + stats["issues"] * 2
        + stats["stars"] * 3
        + stats["followers"] * 1
        + stats["contributed_to"] * 1
    )
    for threshold, letter in ((60000, "S"), (35000, "A+"), (15000, "A"), (7000, "B+"), (3000, "B")):
        if score >= threshold:
            return letter
    return "C"


def main():
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    # 城市名沿用 data.json 里的写法（API 返回的是 "ShangHai" 这种大小写）
    user = get_json(f"https://api.github.com/users/{USER}")
    repos = get_json(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed")
    total, days = contributions()

    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1

    hours, contributed_to, sampled = commit_sample(own)
    stats = {
        "stars": sum(r["stargazers_count"] for r in own),
        "followers": user["followers"],
        "commits": search_count(f"author:{USER}", kind="commits"),
        "prs": search_count(f"author:{USER} type:pr"),
        "issues": search_count(f"author:{USER} type:issue"),
        "contributed_to": contributed_to,
    }

    data.update({
        "username": USER,
        "public_repos": user["public_repos"],
        "own_repos": len(own),
        "forks": sum(r["forks_count"] for r in own),
        "contributions": total,
        "since": int(user["created_at"][:4]),
        "languages": dict(sorted(langs.items(), key=lambda kv: -kv[1])),
        "days": days,
        "hours": hours,
        "commits_sampled": sampled,
        "rank": rank_letter(stats),
        "updated": datetime.date.today().isoformat(),
        **stats,
    })
    (ROOT / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(
        f"refreshed: {data['stars']} stars · {data['commits']} commits · "
        f"{data['contributions']} contributions · {data['contributed_to']} repos touched"
    )


if __name__ == "__main__":
    main()
