#!/usr/bin/env python3
"""Scaffold a promo/landing page from the skill's HTML template.

Copies assets/promo-template/index.html into a target directory and replaces the
placeholder tokens with the confirmed app name, color palette, and fonts. Intended to
be run in Phase 4 of the app-store-screenshot-recommender workflow.

Usage:
    python scaffold_promo.py --app-name "My App" --output ./promo
    python scaffold_promo.py --app-name "FitPal" --headline "Move a little, daily" \
        --color-bg "#F7FBF8" --color-accent "#34C759" --font-display "Poppins"

All color/font tokens fall back to a clean light-minimal palette if omitted.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Tokens -> default values. Keys are the {{TOKEN}} names in the template.
DEFAULTS = {
    "APP_NAME": "My App",
    "CATEGORY": "效率工具",
    "HEADLINE": "一句话说清你的核心价值",
    "SUBHEAD": "用一两句话补足场景与受众，让人一眼看懂。",
    "CTA_LABEL": "立即下载",
    "COLOR_BG": "#FFFFFF",
    "COLOR_SURFACE": "#F5F5F7",
    "COLOR_TEXT": "#1D1D1F",
    "COLOR_ACCENT": "#0071E3",
    "FONT_DISPLAY": "Inter",
    "FONT_BODY": "Inter",
}


def template_path() -> Path:
    """Locate the bundled template relative to this script."""
    here = Path(__file__).resolve().parent
    return here.parent / "assets" / "promo-template" / "index.html"


def slugify(text: str) -> str:
    s = re.sub(r"[^\w一-鿿]+", "-", text.strip().lower()).strip("-")
    return s or "promo"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a promo page from the template.")
    parser.add_argument("--app-name", default=DEFAULTS["APP_NAME"], help="App / product name")
    parser.add_argument("--category", default=DEFAULTS["CATEGORY"], help="Category label badge")
    parser.add_argument("--headline", default=DEFAULTS["HEADLINE"], help="Big value statement")
    parser.add_argument("--subhead", default=DEFAULTS["SUBHEAD"], help="Supporting line")
    parser.add_argument("--cta-label", default=DEFAULTS["CTA_LABEL"], help="Call-to-action text")
    parser.add_argument("--color-bg", default=DEFAULTS["COLOR_BG"], help="Background color (hex)")
    parser.add_argument("--color-surface", default=DEFAULTS["COLOR_SURFACE"], help="Card surface color")
    parser.add_argument("--color-text", default=DEFAULTS["COLOR_TEXT"], help="Text color")
    parser.add_argument("--color-accent", default=DEFAULTS["COLOR_ACCENT"], help="Accent / CTA color")
    parser.add_argument("--font-display", default=DEFAULTS["FONT_DISPLAY"], help="Display font family")
    parser.add_argument("--font-body", default=DEFAULTS["FONT_BODY"], help="Body font family")
    parser.add_argument("--output", default=".", help="Target directory for the generated page")
    args = parser.parse_args(argv)

    src = template_path()
    if not src.exists():
        print(f"[error] template not found at {src}", file=sys.stderr)
        return 1

    out_dir = Path(args.output).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{slugify(args.app_name)}.html"

    html = src.read_text(encoding="utf-8")
    values = {
        "APP_NAME": args.app_name,
        "CATEGORY": args.category,
        "HEADLINE": args.headline,
        "SUBHEAD": args.subhead,
        "CTA_LABEL": args.cta_label,
        "COLOR_BG": args.color_bg,
        "COLOR_SURFACE": args.color_surface,
        "COLOR_TEXT": args.color_text,
        "COLOR_ACCENT": args.color_accent,
        "FONT_DISPLAY": args.font_display,
        "FONT_BODY": args.font_body,
    }
    for token, value in values.items():
        html = html.replace(f"{{{{{token}}}}}", value)

    # Warn if any placeholder survived (typo in token name, etc.)
    leftover = re.findall(r"\{\{\w+\}\}", html)
    if leftover:
        print(f"[warn] unused placeholders left in output: {set(leftover)}", file=sys.stderr)

    out_file.write_text(html, encoding="utf-8")
    print(f"[ok] promo page written to: {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
