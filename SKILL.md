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

1. Read `references/library.md` to understand the curated case categories and tags.
2. Decide the set count: use the number the user specified; otherwise default to **3**.
3. Select that many candidate sets from the library that best fit the direction plus the
   user's stated preferences. For each set, assemble:
   - **Reference image(s)** — collected files under `references/cases/` (present or link
     them so the user can see real examples).
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

The curated library is **partially populated** and meant to grow. To add a case:

1. Drop the collected app-market image(s) into `references/cases/<case-id>/`.
2. Add a per-case design note (`references/cases/<case-id>/brief.md`) describing style,
   structure, color, typography, and what makes it effective.
3. Register the case in `references/library.md` with its category tags and path so future
   runs can match it.

When the library lacks a good match for the user's direction, say so explicitly and
either (a) propose the closest available sets, or (b) generate a style from first
principles using `references/style-guide.md`.

## Resources

### references/
- `library.md` — index of collected app-market cases with category/style tags and paths.
  Load this first to drive matching in Phase 2.
- `style-guide.md` — methodology for color palettes and typography; used for the
  brief's color/font recommendations.
- `cases/<case-id>/` — collected reference images + per-case design notes. Not loaded
  wholesale; read the specific case the user is shown.

### assets/
- `promo-template/` — HTML/CSS scaffold for a promo/landing page with replaceable app
  name, color tokens, and font variables. Copied into the user's workspace in Phase 4.

### scripts/
- `scaffold_promo.py` — copies `assets/promo-template/` into a target directory, injects
  the app name and color/font tokens, and reports the output path.

## Notes

- Keep the confirmation loop genuinely interactive; resist the urge to dump all options
  and stop. The value of this skill is the back-and-forth.
- Reference images are the user's own collected assets — treat them as read-only context,
  never modify or delete them.
