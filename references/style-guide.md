# Style Guide — Color & Typography Methodology

Used in Phase 4 to write the color/font section of the design brief, and as a
first-principles fallback when the library lacks a match. Keep recommendations
concrete and copy-pasteable (hex values, font names, sizes).

## Color

### Palette structures (pick one per brief)
- **60-30-10**: 60% dominant (background), 30% secondary (surfaces/cards), 10% accent
  (CTAs, highlights). Safest, most balanced.
- **Monochromatic**: one hue at varying lightness. Clean, premium, low risk.
- **Complementary**: two opposite hues. High energy, good for CTA contrast.
- **Analogous**: neighboring hues. Harmonious, calm, good for lifestyle/health.
- **Accent-on-neutral**: near-neutral base + one vivid accent. Modern, app-store favorite.

### Rules of thumb
- Limit to **2–3 hues** plus neutrals. More reads as chaotic on a small screenshot.
- Use the accent color **only** for the primary action / key number — scarcity = impact.
- Ensure **contrast ≥ 4.5:1** for text on background (WCAG AA).
- For dark-style promos, lift text to ≥ #E6E6E6 and use a single glowing accent.

### Suggested starter palettes (edit freely)
- Minimal light: `#FFFFFF` / `#F5F5F7` / `#1D1D1F` / accent `#0071E3`
- Premium dark: `#0B0B0F` / `#1C1C22` / `#F5F5F7` / accent `#FFD60A`
- Playful: `#FFFFFF` / `#FFE9D6` / `#2D2A32` / accent `#FF6B6B`
- Calm health: `#F7FBF8` / `#E3F0E9` / `#1F3D33` / accent `#34C759`

## Typography

### Pairing model
- **Display / Headline**: one expressive face for the big value statement.
  - Safe cross-platform: `SF Pro Display` (iOS), `Roboto` / `Inter` (Android/web).
  - Characterful: `Poppins`, `Sora`, `Clash Display` (via web font).
- **Body / Caption**: a highly legible neutral.
  - `Inter`, `SF Pro Text`, `Noto Sans SC` (Chinese), `Source Han Sans`.

### Rules of thumb
- **Max 2 families** per promo set. One for headlines, one for body.
- Headline **≥ 28px** on a 1242×2208 (iOS) canvas; body **≥ 17px**.
- For Chinese copy, prefer `Noto Sans SC` / `Source Han Sans`; avoid thin weights (<300)
  below 20px — they disappear on screenshots.
- Use **weight + size**, not color alone, to create hierarchy.
- Limit headline to **≤ 8 words / ≤ 2 lines**; screenshots are glanced, not read.

## Layout cues for promo screenshots
- Lead with a **single benefit**, not a feature list.
- Device frame optional; often a clean flat color + one UI snippet outperforms a busy
  device mockup.
- One focal point per image; whitespace is a feature, not wasted space.
