# 7Kolor Insights

Data-driven analytics and intelligence services — deep insights into public sentiment,
developer trends, and user demands.
数据驱动的分析与情报服务：公众情绪、开发者趋势与用户需求洞察。

🌐 Site / 站点: https://7kolor.github.io
📮 Contact / 联系: sami.wu@7kolor.com

---

## 目录结构 / Structure

${'```'}
.
├── index.html              首页（英雄区 + 数据资产 + 情报卡片）
├── about.html              关于页
├── weekly/                 每周情报内容
│   ├── index.html          周报归档页
│   └── 2026-W34/           一期周报
│       ├── index.html       双语正文（带 data-zh / data-en）
│       ├── meta.json        元数据（标题/日期/来源）
│       ├── report-zh.html   单语版（构建生成）
│       └── report-en.html   单语版（构建生成）
├── assets/                 CSS / JS / 图片
├── scripts/                构建脚本（纯 Python 标准库，零依赖）
├── tests/                  单元测试（unittest，零依赖）
├── templates/              发布工作流说明
└── .github/workflows/      CI（guard 安全门禁 + publish 自动发布）
${'```'}

## 发布新内容 / Publishing

**只需建目录 + push，剩下的全自动**（CI 自动校验、生成单语页、
更新首页卡片/归档/RSS，并提交回 main）：

${'```'}bash
# 1. 复制上一期作为模板
cp -r weekly/2026-W34 weekly/2026-W35
rm weekly/2026-W35/meta.json

# 2. 编辑正文（双语，data-zh / data-en 属性）与 meta.json
#    详见 templates/weekly-report.md

# 3. push —— CI 自动构建发布
git add weekly/2026-W35
git commit -m "feat: 2026 W35 周报"
git push
${'```'}

### 手动构建（本地预览用）

${'```'}bash
python3 scripts/publish.py            # 校验 + 全量构建
python3 scripts/publish.py --check    # 只校验，不写文件
python3 -m http.server 4000           # 本地预览
${'```'}

### meta.json 格式

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

`kind` 支持：`weekly`（每周情报）/ `analysis`（专项分析）/ `insights`（行业洞察）/ `cases`（成功案例）。
新内容类型只需把目录建在对应根文件夹下，再在首页预留对应的 `<!-- AUTO:cards-<kind> -->` 块。

## 脚本 / Scripts

| 脚本 | 职责 |
|---|---|
| `scripts/publish.py` | 一键发布：校验 meta.json → 生成单语页 → 更新首页/归档/feed（CI 同款） |
| `scripts/build_i18n.py` | 生成单语页 report-zh/en（支持单目录 / 多目录 / 全量自动扫描） |
| `scripts/build_site.py` | 更新首页卡片、归档列表、feed.xml（只动 AUTO 块，不碰手写内容） |
| `scripts/check_sanitize.py` | 安全门禁：检查历史/工作区敏感信息（guard.yml 使用） |

## 开发 / Development

${'```'}bash
python3 -m unittest discover -s tests -v   # 运行全部测试（18 个）
${'```'}

## Feedback

💬 [Discussions](https://github.com/7kolor/7kolor.github.io/discussions) · 🐛 [Issues](https://github.com/7kolor/7kolor.github.io/issues)
