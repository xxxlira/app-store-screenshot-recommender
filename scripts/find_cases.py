#!/usr/bin/env python3
"""Match candidate app-market reference images from the collected library.

Reads references/collected/manifest.json and returns up to --k diverse candidate
sets that fit the user's direction (industry / category / color / keyword). The
agent runs this in Phase 2 of the recommender workflow to pull real reference
images for the user to compare.

Usage:
  python3 scripts/find_cases.py --industry "工具/效率" --k 3
  python3 scripts/find_cases.py --category ipad --color 蓝色 --keyword 笔记
  python3 scripts/find_cases.py --k 3 --format md
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.normpath(os.path.join(HERE, "..", "references", "collected", "manifest.json"))


def load_manifest():
    if not os.path.exists(MANIFEST):
        sys.exit("manifest.json not found at " + MANIFEST +
                 " — run the collection finalize step first.")
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def norm(v):
    return (v or "").strip().lower()


def matches(c, industry, category, color, keyword):
    if industry and norm(industry) not in norm(c.get("industry")):
        return False
    if category and norm(category) not in norm(c.get("category")):
        return False
    if color and norm(color) not in norm(c.get("color")):
        return False
    if keyword and norm(keyword) not in norm(c.get("app")):
        return False
    return True


def diverse_pick(cases, k):
    """Greedily pick k cases maximizing color then category diversity."""
    if len(cases) <= k:
        return cases
    picked = []
    colors_seen, cats_seen = set(), set()
    # first pass: maximize new colors
    for c in cases:
        col = c.get("color") or ""
        if col not in colors_seen:
            picked.append(c)
            colors_seen.add(col)
            cats_seen.add(c.get("category") or "")
            if len(picked) >= k:
                return picked
    # second pass: maximize new categories
    for c in cases:
        if c in picked:
            continue
        cat = c.get("category") or ""
        if cat not in cats_seen:
            picked.append(c)
            cats_seen.add(cat)
            if len(picked) >= k:
                return picked
    # fill remaining
    for c in cases:
        if c not in picked:
            picked.append(c)
            if len(picked) >= k:
                return picked
    return picked[:k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--industry")
    ap.add_argument("--category")
    ap.add_argument("--color")
    ap.add_argument("--keyword", help="substring match against app name")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--format", choices=["json", "md"], default="json")
    args = ap.parse_args()

    manifest = load_manifest()
    cases = manifest.get("cases", [])
    filtered = [c for c in cases if matches(c, args.industry, args.category,
                                            args.color, args.keyword)]
    # if a filter narrowed too far, fall back to the full library for diversity
    if len(filtered) < args.k:
        filtered = cases
    picked = diverse_pick(filtered, args.k)

    # make file paths relative to the skill root for portability
    skill_root = os.path.normpath(os.path.join(HERE, ".."))
    for c in picked:
        c["rel_path"] = os.path.relpath(
            os.path.join(skill_root, "references", "collected", c["file"]),
            skill_root).replace(os.sep, "/")

    if args.format == "md":
        for i, c in enumerate(picked, 1):
            print(f"### 候选 {i}: {c.get('app')}  ({c.get('category')}/{c.get('industry')})")
            print(f"- 图片: `{c['rel_path']}`")
            print(f"- 分类: {c.get('category')}  行业: {c.get('industry')}  配色: {c.get('color')}")
            print()
    else:
        print(json.dumps(picked, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
