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
2. **匹配案例** — 从 `references/library.md` 索引的素材库中挑出若干套（数量你定，默认 3）。
3. **多轮确认** — 逐套展示参考图 + 设计说明 + 推荐理由 + 推荐样式，反复问「要不要换参考图」直到你确认。
4. **产出交付** — 设计说明文档（含配色/字体）、生成的示例图、可编辑前端脚手架。

## 目录结构

```
app-store-screenshot-recommender/
├── SKILL.md              # skill 定义与交互流程
├── references/
│   ├── library.md        # 收录案例索引（分类/风格标签/路径）
│   ├── style-guide.md    # 配色与字体方法论
│   └── cases/            # 已收录案例：brief.md + 参考图
├── assets/
│   └── promo-template/   # 前端宣传页脚手架模板（含可替换 token）
└── scripts/
    └── scaffold_promo.py # 复制模板并注入 app 名/配色/字体
```

## 安装

将本目录放入 WorkBuddy 的技能目录：

- **用户级**（跨所有项目）：`~/.workbuddy/skills/app-store-screenshot-recommender/`
- **项目级**（随仓库共享）：`<repo>/.workbuddy/skills/app-store-screenshot-recommender/`

也可直接解压 `app-store-screenshot-recommender.zip` 到对应目录。

## 扩展素材库

1. 把收集到的应用市场图片放进 `references/cases/<case-id>/`（命名为 `cover.png`）。
2. 写 `brief.md`（结构见 `cases/README.md`）。
3. 在 `references/library.md` 注册该行，供匹配使用。

## 许可

MIT
