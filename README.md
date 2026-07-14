# app-store-screenshot-recommender

> 应用市场宣传图 / 截图设计推荐顾问

通过一段文字描述（你的 App / 产品）或一张参考图片，从**已收录的应用市场图片与设计说明素材库**中匹配出若干套设计方向，每套包含：参考图、设计说明、推荐理由、推荐的图片设计样式。它会**多轮追问**「要不要换参考图」，直到你确认，再产出设计说明文档、生成的示例图与前端代码脚手架。

## 触发方式

自然语言或图片即可触发，例如：

- “帮我想几套 App Store 宣传图风格”
- “我的 App 是 XX 类型，给点设计参考”
- “分析这张截图，推荐类似的设计样式”
- “给我配色和字体建议 + 可编辑设计稿”

## 核心流程

1. **理解方向** — 分析图片风格或推断 App 品类/受众/调性，并追问你的偏好。
2. **匹配案例** — 从 `references/collected/manifest.json`（约 1400+ 张真实应用市场图，按 行业/分类/配色 标签索引）中，由 `scripts/find_cases.py` 挑出若干套多样化候选（数量你定，默认 3）。
3. **多轮确认** — 逐套展示参考图 + 设计说明 + 推荐理由 + 推荐样式，反复问「要不要换参考图」直到你确认。
4. **产出交付** — 设计说明文档（含配色/字体）、生成的示例图、可编辑前端脚手架。

## 目录结构

```
app-store-screenshot-recommender/
├── SKILL.md                 # skill 定义与交互流程
├── references/
│   ├── library.md           # 素材库概览与标签词表
│   ├── style-guide.md       # 配色与字体方法论
│   ├── collected/           # 已收录的成片库（来自飞书知识库）
│   │   ├── manifest.json    # 索引：每张图的 行业/分类/配色/路径
│   │   └── <record_id>.jpg  # 参考图（以飞书 record_id 命名）
│   └── cases/               # 可选：手工精编的深层案例（brief.md + 图）
├── assets/
│   └── promo-template/      # 前端宣传页脚手架模板（含可替换 token）
└── scripts/
    ├── find_cases.py        # 按标签从 manifest 匹配多样化候选参考图
    └── scaffold_promo.py    # 复制模板并注入 app 名/配色/字体
```

## 安装

将本目录放入 WorkBuddy 的技能目录：

- **用户级**（跨所有项目）：`~/.workbuddy/skills/app-store-screenshot-recommender/`
- **项目级**（随仓库共享）：`<repo>/.workbuddy/skills/app-store-screenshot-recommender/`

也可直接解压 `app-store-screenshot-recommender.zip` 到对应目录。

## 素材库来源与扩展

`references/collected/` 中的约 1400+ 张图片是从作者的飞书知识库
**「APP应用市场宣传图」** 批量导入的真实应用市场宣传图，每条带 行业 / 分类 / 配色
标签，记录在 `manifest.json`。

- 想看全部标签词表：`python3 -c "import json;print(json.load(open('references/collected/manifest.json'))['tags'])"`
- 想刷新/扩充：重新跑「抓取 → 下载 → 落盘索引」流水线，提交新的 `manifest.json` 与图片即可。
- 也可在 `references/cases/<case-id>/` 放手工精编的深层案例（`brief.md` + `cover.png`）。

## 许可

MIT
