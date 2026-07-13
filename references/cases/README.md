# Cases — How to add a collected app-market reference

Each case is a folder named with a stable `case-id` (hyphen-case). A case bundles the
reference image(s) the user actually collected with a short design note.

## Folder layout

```
cases/
  <case-id>/
    brief.md        # required: style analysis (template below)
    cover.png       # required: the collected reference image (your asset)
    extra-1.png     # optional: additional angles/variants
```

## brief.md template

```markdown
# <Case name>

- Category: 效率工具
- Style tags: minimal, light, editorial
- Source: <where collected, e.g. App Store CN / Google Play>
- Platform: iOS / Android / Web

## Visual style
- Composition: <how elements are arranged>
- Color: <palette summary, hex if known>
- Typography: <font(s), weights, sizes>
- Mood: <one phrase>

## Structure of the promo
- Lead message: <the headline shown>
- Supporting elements: <device frame? UI snippet? icon?>

## Why it works
- <what makes this effective for its category/audience>

## Reusable patterns
- <what another app in this category can borrow>
```

## Then register it

Add a row to `references/library.md` (Case ID, Category, Style tags, Path) so the
matching step in Phase 2 can find it.

## Note on images

Reference images are **your own collected assets** — keep them read-only. Do not modify
or delete them during a session.
