# 7Kolor 开发规范

> 本文档供开发者和 AI 助手参考，包含内部技术规范、发布流程和目录结构。

---

## 技术栈

- **前端**: 纯 HTML/CSS/JS，无框架依赖
- **构建**: Python 3 标准库（零外部依赖）
- **部署**: GitHub Pages + GitHub Actions
- **测试**: unittest（18 个测试用例）
- **CI**: guard（安全门禁）+ publish（自动发布）

---

## 目录结构

```
.
├── index.html               # 首页（英雄区 + 数据资产 + 情报卡片）
├── about.html               # 关于页
├── weekly/                  # 每周情报内容
│   ├── index.html           # 周报归档页
│   └── 2026-W34/            # 一期周报
│       ├── index.html       # 双语正文（带 data-zh / data-en 属性）
│       ├── meta.json        # 元数据（标题/日期/来源）
│       ├── report-zh.html   # 单语版（构建生成）
│       └── report-en.html   # 单语版（构建生成）
├── assets/                  # CSS / JS / 图片
├── scripts/                 # 构建脚本
├── tests/                   # 单元测试
├── templates/               # 发布工作流说明
└── .github/workflows/       # CI/CD
```

---

## 核心脚本

| 脚本 | 职责 | 使用场景 |
|------|------|---------|
| `scripts/publish.py` | 一键发布：校验 meta.json → 生成单语页 → 更新首页/归档/feed | CI 或本地发布 |
| `scripts/build_i18n.py` | 生成单语页 report-zh/en | 双语内容分离 |
| `scripts/build_site.py` | 更新首页卡片、归档列表、feed.xml | 只动 AUTO 块，不碰手写内容 |
| `scripts/check_sanitize.py` | 安全门禁 | 检查历史/工作区敏感信息 |

---

## 发布流程

### 自动发布（推荐）

```bash
# 1. 复制上一期作为模板
cp -r weekly/2026-W34 weekly/2026-W35
rm weekly/2026-W35/meta.json

# 2. 编辑正文（双语，data-zh / data-en 属性）与 meta.json
#    详见 templates/weekly-report.md

# 3. push —— CI 自动构建发布
git add weekly/2026-W35
git commit -m "feat: 2026 W35 周报"
git push
```

### 手动构建（本地预览）

```bash
python3 scripts/publish.py            # 校验 + 全量构建
python3 scripts/publish.py --check    # 只校验，不写文件
python3 -m http.server 4000           # 本地预览
```

---

## meta.json 格式

```json
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
```

### kind 类型

| kind | 说明 |
|------|------|
| `weekly` | 每周情报 |
| `analysis` | 专项分析 |
| `insights` | 行业洞察 |
| `cases` | 成功案例 |

新内容类型只需把目录建在对应根文件夹下，再在首页预留对应的 `<!-- AUTO:cards-<kind> -->` 块。

---

## 开发命令

```bash
# 运行全部测试（18 个）
python3 -m unittest discover -s tests -v

# 本地预览
python3 -m http.server 4000
```

---

## 内容编辑规范

1. **双语内容**：使用 `data-zh` / `data-en` 属性标记
2. **模板参考**：`templates/weekly-report.md`
3. **AUTO 块**：首页/归档/feed 有 `<!-- AUTO:xxx -->` 标记，构建脚本只修改这些区域
4. **安全门禁**：CI 会自动扫描敏感信息，避免泄露
