# 发布工作流 / Publishing workflow

站点是纯静态 HTML + 元数据驱动的自动生成。**发布新内容 = 建文件夹 + 提交 push，
其余全部由 CI（publish.yml）自动完成。**

## 新增一期周报（如 2026 W35）

1. 复制上一期作为模板：
   ${'```'}sh
   cp -r weekly/2026-W34 weekly/2026-W35
   rm weekly/2026-W35/meta.json
   ${'```'}
2. 编辑 `weekly/2026-W35/index.html` —— 双语单页：可翻译元素带 `data-zh` / `data-en` 属性。
3. 新建 `weekly/2026-W35/meta.json`，格式见下方。
4. 提交并推送 —— CI 自动完成以下全部工作：
   - 校验 meta.json（必填字段、kind、日期格式，失败则中止并通知你）
   - 为每个新目录生成 `report-zh.html` / `report-en.html`
   - 更新首页「每周情报」卡片区、周报归档列表、feed.xml
   - 自动提交生成内容回 main（`[skip ci]` 防循环），GitHub Pages 随即上线

## 本地手动构建（可选）

   ${'```'}sh
   python3 scripts/publish.py            # 校验 + 全量构建（与 CI 完全一致）
   python3 scripts/publish.py --check    # 只校验不写文件
   python3 scripts/build_i18n.py weekly/2026-W35   # 只生成某期单语页
   python3 -m unittest discover -s tests -v        # 运行全部测试
   ${'```'}

> `build_site.py` 会自动扫描 `weekly/*/meta.json`（以及其他内容根目录），把新周报
> **自动填充**到首页卡片区和归档列表，并写入 RSS —— 无需手动改任何列表。

## meta.json 格式

   ${'```'}json
   {
     "kind": "weekly",
     "id": "2026-W35",
     "week_label_zh": "2026 W35 周报",
     "week_label_en": "2026 W35 Weekly Report",
     "title_zh": "本期中文标题",
     "title_en": "English title",
     "desc_zh": "中文摘要（首页卡片 + RSS 用）",
     "desc_en": "English summary",
     "date_range": "2026-08-30 ~ 09-05",
     "date": "2026-09-05",
     "sources": "Reddit · HN · IH · PH"
   }
   ${'```'}

### 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `kind` | ✅ | `weekly` / `analysis` / `insights` / `cases` |
| `id` | ✅ | 唯一标识（如 `2026-W35`） |
| `title_zh` / `title_en` | ✅ | 本期标题 |
| `date` | ✅ | ISO 日期（`YYYY-MM-DD`），用于排序 |
| `week_label_zh` / `week_label_en` | weekly | 周报标签（拼在标题前的「2026 W35 周报」） |
| `date_range` | weekly | 数据覆盖范围（卡片显示） |
| `sources` | weekly | 数据来源（卡片显示） |
| `desc_zh` / `desc_en` | ✅ | 摘要（首页卡片 + RSS） |

### 内容类型扩展

新增内容类型（如 `cases/`）时：
1. 在对应根目录下建 `<type>/<id>/index.html + meta.json`
2. 在首页为 `<!-- AUTO:cards-<type> -->` 预留 AUTO 块（build_site 自动填充）
3. 在 `.github/workflows/publish.yml` 的 `paths` 中加入该根目录
