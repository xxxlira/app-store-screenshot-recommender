#!/usr/bin/env python3
"""build_gallery.py — 生成 uinotes 风格的应用市场图库网页。

读取 references/collected/manifest.json，按产品（app 名称）分组，
输出一个自包含、可直接双击打开、且可发布到 GitHub Pages 的图库网页：

  - 首页：卡片网格，每张卡片显示 产品 logo（头像）、产品名称、
          截图数量，以及「部分」应用市场图（预览截图）。
  - 点击头像 / 卡片：打开 lightbox，展示该产品「全部」图片。
  - 顶部筛选：搜索框 + 行业 / 分类 下拉 + 可点击「配色色板」。
  - 「🎲 随机灵感」按钮：随机打开一款产品，激发设计灵感。

产出文件（默认写在 skill 根目录，与 references/ 同级）：
  - gallery.html   本地双击可用（相对路径引用图片）
  - index.html     内容与 gallery.html 相同，作为 GitHub Pages 默认入口
  - .nojekyll      让 GitHub Pages 原样托管静态资源

图片通过相对路径 references/collected/<file> 引用，因此这些 HTML
需与 references/ 同级，线上（Pages）与本地（http.server）均可正确加载。
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)  # <skill>/scripts -> <skill>/
DEFAULT_MANIFEST = os.path.join(SKILL_ROOT, "references", "collected", "manifest.json")
DEFAULT_OUTPUT = os.path.join(SKILL_ROOT, "gallery.html")

IMG_REL = "references/collected/"  # 相对 gallery.html 的图片目录
LOGO_CATS = {"logo", "logo更新"}

# 配色名 -> 代表色（用于可视化色板）。渐变色用 CSS gradient 表示。
COLOR_HEX = {
    "多色": "linear-gradient(135deg,#ff5a8a,#ffb648,#34c759,#3b82f6,#8b5cf6)",
    "浅色/彩色": "linear-gradient(135deg,#a8edea,#fed6e3,#fff1b8)",
    "橘色": "#ff8a3d",
    "白色": "#ffffff",
    "粉色": "#ff6fa5",
    "紫色": "#8b5cf6",
    "红色": "#f4433c",
    "绿色": "#34c759",
    "蓝色": "#3b82f6",
    "黄色": "#ffcc00",
    "黑色/深色": "#1d1d1f",
}


def group_by_app(manifest):
    apps = {}
    for c in manifest.get("cases", []):
        name = (c.get("app") or "").strip()
        if not name:
            continue
        apps.setdefault(name, []).append(c)

    out = []
    for name, items in apps.items():
        # logo 头像：优先 logo / logo更新 分类，否则取首图
        logos = [c for c in items if c.get("category") in LOGO_CATS]
        logo = (logos[0] if logos else items[0])["file"]

        # 预览图：iphone / ipad 截图，最多 2 张
        shots = [c for c in items if c.get("category") in {"iphone", "ipad"}]
        previews = [c["file"] for c in shots[:2]]

        # 全部图片（logo 在前，便于 lightbox 头部展示头像）
        ordered = sorted(
            items,
            key=lambda c: (0 if c.get("category") in LOGO_CATS else 1),
        )
        images = [
            {
                "file": c["file"],
                "category": c.get("category", ""),
                "color": c.get("color", ""),
                "industry": c.get("industry", ""),
            }
            for c in ordered
        ]

        industries = sorted({c.get("industry", "") for c in items if c.get("industry")})
        colors = sorted({c.get("color", "") for c in items if c.get("color")})

        out.append(
            {
                "name": name,
                "logo": logo,
                "count": len(items),
                "previews": previews,
                "industries": industries,
                "colors": colors,
                "images": images,
            }
        )

    # 按截图数量降序（热门产品靠前，呼应 uinotes 首页）
    out.sort(key=lambda a: a["count"], reverse=True)
    return out


def build_html(apps, manifest):
    total_imgs = manifest.get("total", sum(a["count"] for a in apps))
    tags = manifest.get("tags", {})
    industries = [t for t in (tags.get("industry") or []) if t]
    categories = [t for t in (tags.get("category") or []) if t]
    colors = [t for t in (tags.get("color") or []) if t]

    # 色板：颜色名 + 代表色（未在映射表中的用中性灰）
    swatches = [{"name": c, "hex": COLOR_HEX.get(c, "#c7c7cc")} for c in colors]

    return HTML_TEMPLATE.format(
        n_apps=len(apps),
        n_imgs=total_imgs,
        img_rel=IMG_REL,
        data_js=json.dumps(apps, ensure_ascii=False),
        industries_js=json.dumps(industries, ensure_ascii=False),
        categories_js=json.dumps(categories, ensure_ascii=False),
        swatches_js=json.dumps(swatches, ensure_ascii=False),
    )


HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>应用市场图库 · App Store 宣传图灵感库</title>
<style>
  :root{{
    --bg:#f7f8fa; --card:#fff; --text:#1d1d1f; --muted:#86868b;
    --line:#e6e6ea; --accent:#ff5a8a; --shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.06);
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--text);
    font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans SC","Segoe UI",sans-serif;
    -webkit-font-smoothing:antialiased}}
  a{{color:inherit;text-decoration:none}}
  header{{max-width:1200px;margin:0 auto;padding:40px 24px 8px}}
  .title-row{{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}}
  h1{{font-size:30px;font-weight:700;margin:0 0 6px;letter-spacing:-.5px}}
  .sub{{color:var(--muted);font-size:14px;margin:0}}
  .btn-random{{border:none;background:var(--accent);color:#fff;border-radius:12px;
    padding:11px 18px;font-size:14px;font-weight:600;cursor:pointer;white-space:nowrap;
    box-shadow:0 4px 14px rgba(255,90,138,.35);transition:transform .12s,box-shadow .12s}}
  .btn-random:hover{{transform:translateY(-2px);box-shadow:0 8px 22px rgba(255,90,138,.45)}}
  .btn-random:active{{transform:translateY(0) scale(.97)}}
  .filters{{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 4px}}
  .filters input,.filters select{{
    border:1px solid var(--line);background:#fff;border-radius:10px;
    padding:9px 12px;font-size:14px;color:var(--text);outline:none}}
  .filters input{{flex:1;min-width:200px}}
  .filters input:focus,.filters select:focus{{border-color:var(--accent)}}
  /* 配色色板 */
  .palette{{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:14px 0 2px}}
  .palette .lbl{{font-size:13px;color:var(--muted);margin-right:2px}}
  .sw{{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:#fff;
    border-radius:20px;padding:4px 12px 4px 6px;font-size:13px;color:var(--text);cursor:pointer;
    transition:border-color .12s,box-shadow .12s,transform .12s}}
  .sw:hover{{transform:translateY(-1px);box-shadow:0 3px 10px rgba(0,0,0,.08)}}
  .sw .dot{{width:16px;height:16px;border-radius:50%;border:1px solid rgba(0,0,0,.12);flex:none}}
  .sw.active{{border-color:var(--accent);box-shadow:0 0 0 2px rgba(255,90,138,.18)}}
  main{{max-width:1200px;margin:0 auto;padding:18px 24px 80px}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:16px;
    padding:16px;box-shadow:var(--shadow);cursor:pointer;transition:transform .15s,box-shadow .15s}}
  .card:hover{{transform:translateY(-3px);box-shadow:0 4px 10px rgba(0,0,0,.08),0 16px 36px rgba(0,0,0,.10)}}
  .card.flash{{animation:flash 1s ease}}
  @keyframes flash{{0%{{box-shadow:0 0 0 3px var(--accent)}}100%{{box-shadow:var(--shadow)}}}}
  .card-top{{display:flex;align-items:center;gap:12px}}
  .avatar{{width:46px;height:46px;border-radius:12px;object-fit:cover;background:#f0f0f3;flex:none;
    border:1px solid var(--line);cursor:pointer}}
  .meta{{min-width:0}}
  .name{{font-size:15px;font-weight:600;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .count{{font-size:12px;color:var(--muted);margin-top:2px}}
  .previews{{display:flex;gap:8px;margin-top:14px}}
  .pv{{flex:1;aspect-ratio:9/19;object-fit:cover;border-radius:10px;background:#f0f0f3;border:1px solid var(--line)}}
  .empty{{color:var(--muted);text-align:center;padding:60px 0;grid-column:1/-1}}
  /* lightbox */
  .modal{{position:fixed;inset:0;z-index:50;display:none}}
  .modal.show{{display:block}}
  .modal-backdrop{{position:absolute;inset:0;background:rgba(0,0,0,.55);backdrop-filter:blur(2px)}}
  .modal-box{{position:absolute;inset:0;margin:auto;max-width:1100px;max-height:90vh;
    width:94%;background:var(--bg);border-radius:18px;display:flex;flex-direction:column;overflow:hidden;
    box-shadow:0 30px 80px rgba(0,0,0,.4)}}
  .modal-head{{display:flex;align-items:center;gap:14px;padding:18px 22px;border-bottom:1px solid var(--line);background:#fff}}
  .modal-head .m-logo{{width:44px;height:44px;border-radius:12px;object-fit:cover;background:#f0f0f3;border:1px solid var(--line)}}
  .modal-head h2{{font-size:18px;margin:0;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .modal-head .m-count{{font-size:13px;color:var(--muted)}}
  .close{{border:none;background:#f0f0f3;width:34px;height:34px;border-radius:50%;font-size:20px;
    line-height:1;cursor:pointer;color:#555;flex:none}}
  .close:hover{{background:#e4e4e8}}
  .modal-grid{{padding:22px;overflow:auto;display:grid;
    grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}}
  .shot{{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}}
  .shot img{{width:100%;display:block;background:#f0f0f3;cursor:zoom-in}}
  .shot .cap{{font-size:11px;color:var(--muted);padding:6px 8px}}
  .tag{{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:20px;
    padding:2px 9px;font-size:11px;color:var(--muted);margin:0 4px 4px 0}}
  @media (max-width:520px){{.grid{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}}}
</style>
</head>
<body>
<header>
  <div class="title-row">
    <div>
      <h1>应用市场图库</h1>
      <p class="sub">App Store / 应用市场宣传图灵感库 · 共 {n_apps} 款产品 · {n_imgs} 张图</p>
    </div>
    <button class="btn-random" id="btnRandom">🎲 随机灵感</button>
  </div>
  <div class="filters">
    <input id="search" type="search" placeholder="搜索产品名…">
    <select id="f-industry"><option value="">全部行业</option></select>
    <select id="f-category"><option value="">全部分类</option></select>
  </div>
  <div class="palette" id="palette"><span class="lbl">配色：</span></div>
</header>
<main><div class="grid" id="grid"></div></main>

<div class="modal" id="modal">
  <div class="modal-backdrop" data-close></div>
  <div class="modal-box">
    <div class="modal-head">
      <img class="m-logo" id="m-logo" src="" alt="">
      <h2 id="m-name"></h2>
      <span class="m-count" id="m-count"></span>
      <button class="close" data-close aria-label="关闭">×</button>
    </div>
    <div class="modal-grid" id="modalGrid"></div>
  </div>
</div>

<script>
const IMG = "{img_rel}";
const DATA = {data_js};
const INDUSTRIES = {industries_js};
const CATEGORIES = {categories_js};
const SWATCHES = {swatches_js};

// 填充下拉
function fill(sel, arr){{ arr.forEach(v=>{{ const o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }}); }}
fill(document.getElementById('f-industry'), INDUSTRIES);
fill(document.getElementById('f-category'), CATEGORIES);

const grid = document.getElementById('grid');
const search = document.getElementById('search');
const fInd = document.getElementById('f-industry');
const fCat = document.getElementById('f-category');
const palette = document.getElementById('palette');

// 配色色板（可点击，单选切换）
let activeColor = "";
SWATCHES.forEach(s => {{
  const el = document.createElement('button');
  el.className = 'sw';
  el.dataset.color = s.name;
  el.innerHTML = `<span class="dot" style="background:${{s.hex}}"></span>${{s.name}}`;
  el.addEventListener('click', () => {{
    activeColor = (activeColor === s.name) ? "" : s.name;
    document.querySelectorAll('.sw').forEach(x => x.classList.toggle('active', x.dataset.color === activeColor));
    render();
  }});
  palette.appendChild(el);
}});

function matches(a){{
  const q = search.value.trim().toLowerCase();
  if (q && !a.name.toLowerCase().includes(q)) return false;
  if (fInd.value && !a.industries.includes(fInd.value)) return false;
  if (activeColor && !a.colors.includes(activeColor)) return false;
  if (fCat.value) {{
    const has = a.images.some(i => i.category === fCat.value);
    if (!has) return false;
  }}
  return true;
}}

function cardHTML(a){{
  const previews = a.previews.map(f =>
    `<img class="pv" loading="lazy" src="${{IMG}}${{f}}" alt="${{a.name}} 预览">`).join('');
  return `<article class="card" data-name="${{a.name}}">
    <div class="card-top">
      <img class="avatar" loading="lazy" src="${{IMG}}${{a.logo}}" alt="${{a.name}}" data-avatar="1">
      <div class="meta">
        <p class="name">${{a.name}}</p>
        <div class="count">${{a.count}} 张 · ${{a.industries[0] || '—'}}</div>
      </div>
    </div>
    <div class="previews">${{previews}}</div>
  </article>`;
}}

function render(){{
  const list = DATA.filter(matches);
  if (!list.length) {{ grid.innerHTML = '<div class="empty">没有匹配的产品</div>'; return; }}
  grid.innerHTML = list.map(cardHTML).join('');
}}

grid.addEventListener('click', e => {{
  const card = e.target.closest('.card');
  if (card) openModal(card.dataset.name);
}});

// 🎲 随机灵感：在「当前筛选结果」内随机挑一款，直接打开全部图
document.getElementById('btnRandom').addEventListener('click', () => {{
  const list = DATA.filter(matches);
  if (!list.length) return;
  const pick = list[Math.floor(Math.random() * list.length)];
  openModal(pick.name);
}});

const modal = document.getElementById('modal');
const modalGrid = document.getElementById('modalGrid');
function openModal(name){{
  const a = DATA.find(x => x.name === name);
  if (!a) return;
  document.getElementById('m-logo').src = IMG + a.logo;
  document.getElementById('m-name').textContent = a.name;
  document.getElementById('m-count').textContent = a.count + ' 张';
  modalGrid.innerHTML = a.images.map(i => {{
    const tags = [];
    if (i.category) tags.push(i.category);
    if (i.color) tags.push(i.color);
    return `<div class="shot"><img loading="lazy" src="${{IMG}}${{i.file}}" alt="${{a.name}}">
      <div class="cap">${{tags.map(t=>`<span class="tag">${{t}}</span>`).join('')}}</div></div>`;
  }}).join('');
  modal.classList.add('show');
  document.body.style.overflow = 'hidden';
}}
function closeModal(){{ modal.classList.remove('show'); document.body.style.overflow=''; }}
modal.addEventListener('click', e => {{ if (e.target.hasAttribute('data-close')) closeModal(); }});
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});

[search, fInd, fCat].forEach(el => el.addEventListener('input', render));
render();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="生成 uinotes 风格的应用市场图库网页")
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST, help="manifest.json 路径")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="输出的 gallery.html 路径")
    ap.add_argument(
        "--no-pages",
        action="store_true",
        help="仅生成 gallery.html，不额外产出 index.html / .nojekyll",
    )
    args = ap.parse_args()

    if not os.path.exists(args.manifest):
        sys.exit(f"找不到 manifest: {args.manifest}")
    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)

    apps = group_by_app(manifest)
    html = build_html(apps, manifest)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已生成 {args.output}")

    if not args.no_pages:
        out_dir = os.path.dirname(os.path.abspath(args.output))
        index_path = os.path.join(out_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        nojekyll = os.path.join(out_dir, ".nojekyll")
        with open(nojekyll, "w", encoding="utf-8") as f:
            f.write("")
        print(f"已生成 {index_path}（GitHub Pages 入口）")
        print(f"已生成 {nojekyll}")

    print(f"  产品数: {len(apps)}  图片总数: {manifest.get('total')}")


if __name__ == "__main__":
    main()
