---
name: app-store-screenshot-recommender
description: "Recommend app-store / promotional screenshot design styles. This skill should be used when a user wants design references and style recommendations for app store screenshots, promo images, or marketing visuals, triggered by a natural-language description of their app or product or by uploading a reference image. It analyzes the input, asks the user about their preferences, matches several candidate sets from a curated library of collected app-market images and design notes (count specified by the user, default 3), presents each with reference images, a design brief, recommendation rationale, and a suggested visual style, then iterates by asking whether to swap any reference image until the user confirms. Finally it delivers a design brief document, generated example images, and a frontend code scaffold."
agent_created: true
---

# App Store Screenshot Recommender

## Overview

A design-advisory skill that turns a vague brief — a sentence about an app, or an
uploaded image — into **several concrete promotional-image design directions**, each
backed by collected real-world app-market references. Its signature behavior is a
**multi-turn confirmation loop**: it keeps asking "want to swap any reference image?"
until the user is satisfied, then materializes the chosen direction into a brief,
sample images, and a code scaffold.

## When To Use

Trigger on requests such as:

- "帮我想几套 App Store 宣传图风格"
- "我的 App 是 XX 类型，给点设计参考"
- "分析这张截图，推荐类似的设计样式"
- "给我配色和字体建议 + 可编辑设计稿"
- Any natural-language ask for app-store / promo / marketing screenshot style help,
  with or without an attached image.

Do **not** use this for: generating a single finished asset with no style exploration,
pure copywriting, or non-promotional UI work.

## Input Modes

Determine the mode from the user's first message:

- **Image attached** → *Image Analysis mode*: analyze the visual style of what they
  uploaded, then treat it as the starting point for matching.
- **Text only** → *Text Brief mode*: infer the app category, audience, tone, and target
  platform (iOS App Store / Google Play / web landing), then proceed.

## Workflow — Interactive Design Recommendation

Follow these phases in order. The loop in Phase 3 is the core of the skill; do not
collapse it into a single response.

### Phase 1 — Understand the direction

1. If an image was provided, analyze its visual style in 1–2 sentences: composition,
   color temperature, typography, mood, and apparent category. State this back to the
   user so they can correct you.
2. If only text, infer: app category, target audience, desired tone (e.g. playful /
   premium / minimal), and platform.
3. **Ask the user one focused question** about their preferences or constraints
   (audience, tone, must-have elements, platform, competitor references). Their answer
   shapes the matching — never skip this step.

### Phase 2 — Match candidate sets

1. Infer filters from the direction plus the user's Phase-1 answer:
   - `--industry` (e.g. 工具/效率 / 社交 / 游戏) — valid values live under
     `references/collected/manifest.json` → `tags.industry`.
   - `--category` (logo / logo更新 / iphone / ipad).
   - `--color` (配色 tag, e.g. 蓝色 / 多色 / 黑色/深色).
   - `--keyword` (substring of the app name, optional).
2. Run the matcher (set count = the number the user specified, else default **3**):
   ```bash
   python3 scripts/find_cases.py --industry "<行业>" --category "<分类>" \
       --color "<配色>" --keyword "<可选>" --k <N>
   ```
   It returns diverse candidate images from `references/collected/` together with
   their metadata (`app` / `industry` / `category` / `color` / `rel_path`). Omit any
   filter you don't have; when a filter narrows too far it falls back to the full
   library for diversity.
3. For each returned candidate, assemble a set with:
   - **Reference image** — the file at `references/collected/<file>` (show it to the
     user so they see a real example).
   - **Design brief (设计说明)** — what the style is, its structure, and key elements.
   - **Recommendation rationale (推荐理由)** — why it fits *this* app.
   - **Suggested image design style (推荐样式)** — layout, color, typography, and copy
     guidance.

### Phase 3 — Present & confirm (iterate)

1. Present the sets clearly, one block each, so the user can compare.
2. Ask: **"以上参考图中，有哪一套你想更换或调整吗？还是就此确定？"**
3. Branch:
   - **Wants changes** → refine the affected set(s), pull alternative cases from the
     library if needed, and re-present. Return to step 2 of this phase.
   - **Confirms (no more changes)** → proceed to Finalize.
4. Repeat until the user explicitly says they no longer want to change references.

### Phase 4 — Finalize & deliver

Produce the final deliverables:

1. **Design brief document (Markdown)** — the confirmed plan(s) with color palette and
   typography. Draw color/font methodology from `references/style-guide.md`.
2. **Generated example images** — use the ImageGen tool to produce sample promo images
   for each confirmed style (collected references are shown as references; generated
   ones are new samples). If ImageGen is unavailable, output detailed image-generation
   prompts the user can run elsewhere.
3. **Frontend code scaffold** — copy `assets/promo-template/` (or run
   `scripts/scaffold_promo.py`) to produce an HTML/CSS promo page populated with the
   confirmed app name, color tokens, and font variables.

## Reference Library Management

The library is a **flat, programmatically-indexed collection** under
`references/collected/`:

- `manifest.json` — the single source of truth. Registers every image with
  `record_id`, `file`, `app`, `industry`, `category`, `color`, `original_name`,
  `size`. Also lists all valid tag values under `tags` (industry / category / color).
  Phase 2 matching reads this via `scripts/find_cases.py`.
- `*.jpg` / `*.png` / ... — the actual reference images, named by their Feishu
  `record_id`.

It was imported from the user's Feishu wiki "APP应用市场宣传图". To refresh or extend
it, re-run the collection pipeline (gather → download → finalize) and commit the
result. Optional hand-curated deep-dives can still live in `references/cases/<case-id>/`.

When the library lacks a good match for the user's direction, say so explicitly and
either (a) propose the closest available sets, or (b) generate a style from first
principles using `references/style-guide.md`.

## Resources

### references/
- `collected/manifest.json` — index of all collected app-market images with
  industry/category/color tags and file paths. Primary input for Phase 2 matching.
- `collected/` — the reference image files (named by Feishu `record_id`).
- `style-guide.md` — methodology for color palettes and typography; used for the
  brief's color/font recommendations.
- `cases/<case-id>/` — optional hand-curated deep-dive cases (brief.md + image). Not
  loaded wholesale; read the specific case the user is shown.
- `library.md` — human-readable overview of the collection and the tag vocabulary.

### assets/
- `promo-template/` — HTML/CSS scaffold for a promo/landing page with replaceable app
  name, color tokens, and font variables. Copied into the user's workspace in Phase 4.

### scripts/
- `find_cases.py` — matches `references/collected/manifest.json` by industry / category /
  color / keyword and returns diverse candidate reference images for Phase 2.
- `scaffold_promo.py` — copies `assets/promo-template/` into a target directory, injects
  the app name and color/font tokens, and reports the output path.

## Notes

- Keep the confirmation loop genuinely interactive; resist the urge to dump all options
  and stop. The value of this skill is the back-and-forth.
- Reference images are the user's own collected assets — treat them as read-only context,
  never modify or delete them.
