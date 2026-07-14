# Reference Library — Collected App-Market Images

This library is a flat, programmatically-indexed collection of real-world
app-store / promo images imported from the user's Feishu wiki
**"APP应用市场宣传图"**. Read it (via `scripts/find_cases.py`) first in Phase 2 to
pick candidate sets that match the user's direction.

## Layout

```
references/collected/
  manifest.json      # the index: every image + its tags + valid tag vocabulary
  <record_id>.jpg    # actual reference images, named by Feishu record_id
  <record_id>.png
```

- `manifest.json.cases[]` — one entry per image: `record_id`, `file`, `app`,
  `industry`, `category`, `color`, `original_name`, `size`.
- `manifest.json.tags` — the authoritative list of valid values for
  `industry` / `category` / `color` (use these when calling `find_cases.py`).

## How matching works (Phase 2)

1. Infer `industry` / `category` / `color` / `keyword` from the user's direction.
2. Run the matcher:

   ```bash
   python3 scripts/find_cases.py --industry "工具/效率" --category iphone \
       --color 蓝色 --k 3
   ```

3. It returns diverse candidates (varied color/category) with `rel_path` so you can
   show the user a real reference image per set.

## Tag vocabulary (from the collection)

Use `python3 -c "import json;print(json.load(open('references/collected/manifest.json'))['tags'])"`
for the live, complete list. Common values:

- **industry (行业)**: 社交, 工具/效率, 购物/买卖/生活, AI相关, 待办/专注/清单,
  视频/漫画/小说, 游戏, 儿童游戏/幼教, 工具/教育, 工具/阅读, 社交/播客, 工具/影像,
  工具/修图, ...
- **category (分类)**: logo, logo更新, iphone, ipad
- **color (配色)**: 多色, 浅色/彩色, 黑色/深色, 白色, 蓝色, 绿色, 红色, 橘色, 黄色,
  紫色, 粉色

## Notes

- When no registered case fits well, say so and either propose the closest sets or
  build a style from first principles using `style-guide.md`.
- Reference images are the user's own collected assets — treat them as read-only
  context, never modify or delete them.
- To refresh/extend the collection, re-run the gather → download → finalize pipeline
  against the Feishu wiki and commit the new `manifest.json` + images.
