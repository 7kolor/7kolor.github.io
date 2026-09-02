# 发布工作流 / Publishing workflow

站点是纯静态 HTML + 元数据驱动的自动生成。**发布新内容只需建文件夹 + 跑一条命令。**

## 新增一期周报（如 2026 W35）

1. 复制模板为本周目录：
   ```sh
   cp -r weekly/2026-W34 weekly/2026-W35
   rm weekly/2026-W35/meta.json
   ```
2. 编辑 `weekly/2026-W35/index.html` —— 双语单页：可翻译元素带 `data-zh` / `data-en` 属性。
3. 新建 `weekly/2026-W35/meta.json`，格式见下方。
4. 生成单语页 + 自动填充全站：
   ```sh
   python3 scripts/build_i18n.py weekly/2026-W35   # 生成 report-zh/en.html
   python3 scripts/build_site.py                     # 自动更新 首页卡片 / 周报归档 / feed.xml
   ```
5. 本地预览：
   ```sh
   python3 -m http.server 4000
   ```

> 第 4 步的 build_site.py 会自动扫描 `weekly/*/meta.json`，把新周报**自动填充**到首页「每周情报」卡片区和周报归档列表，并写入 RSS —— 无需手动改任何列表。

## meta.json 格式

```json
{
  "kind": "weekly",
  "id": "2026-W35",
  "week_label_zh": "2026 W35 周报",
  "week_label_en": "2026 W35 Weekly Report",
  "title_zh": "一句话中文标题",
  "title_en": "One-line English title",
  "desc_zh": "卡片上的中文摘要",
  "desc_en": "Card summary in English",
  "date_range": "2026-08-30 ~ 09-05",
  "date": "2026-09-05",
  "sources": "Reddit · HN · IH · PH"
}
```

## 新增其他模块（专项分析 / 赛道洞察 / 成功案例详解）

系统已预留模块位置（首页对应标题区在 build_site.py 的 MODULES，按需启用）。
新增一个模块（如「专项分析」）：

1. 建顶层目录 `analysis/`，每个分析一个子目录，同样放 `index.html` + `meta.json`，其中 `"kind": "analysis"`。
2. 在 `scripts/build_site.py` 的 `MODULES` 里确认 `analysis` 已启用。
3. 跑 `python3 scripts/build_site.py`，自动填充首页「专项分析」卡片区。
4. 若某模块暂无内容，首页会显示「筹备中」占位卡。

> 兼容 markdown：大多数字段其实来自 HTML 内的 `data-zh`/`data-en`；meta.json 里的 title/desc 主要用于卡片与 RSS。若你偏好用 `.md` 写正文，可在子目录里同时放 `index.html`（外壳）和把 markdown 渲染好的 HTML 正文并入其中。

## 命名约定

- 周报目录用连字符：`2026-W35`（URL 干净：`/weekly/2026-W35/`），不用空格。
- 新增周报在 `weekly/` 下按日期命名即可。

> Signal IDs are opaque: SIG-{yy}{ww}-{seq}. Never use internal identifiers.
> 信号 ID 使用不透明编号，禁止出现任何内部标识符。

## Content checklist / 内容清单

- TL;DR —— 三句话结论
- 每条信号链接到公开来源
- 只使用公开内容，不涉及私有数据 / 付费墙来源
