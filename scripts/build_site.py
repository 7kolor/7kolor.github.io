#!/usr/bin/env python3
"""Build site index pages from content metadata.

Scans content collections (weekly/, and future modules like insights/,
cases/, analysis/) for */meta.json, then regenerates:

  - the auto blocks in index.html        (report cards per module)
  - the auto block in weekly/index.html  (archive list)
  - feed.xml                             (RSS items)

Adding a new week / report:
  1. create  weekly/2026-W35/  with index.html + meta.json
  2. run     python3 scripts/build_i18n.py weekly/2026-W35
  3. run     python3 scripts/build_site.py
  4. preview python3 -m http.server 4000

Adding a new module (e.g. 专项分析):
  mkdir analysis; drop folders with index.html + meta.json (kind: "analysis"),
  add an AUTO block for it in index.html (see MODULES below), rerun this script.

Only blocks between <!-- AUTO:<name>:begin --> and <!-- AUTO:<name>:end -->
are rewritten; everything else in the HTML is hand-authored and untouched.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://7kolor.github.io"

# module key -> (folder, homepage section title zh/en, empty-state zh/en)
MODULES = {
    "weekly":   ("weekly",   "📡 每周情报", "📡 Weekly Intelligence", None),
    "analysis": ("analysis", "🔬 专项分析", "🔬 Deep-Dive Analysis", ("赛道级深度洞察筹备中", "Track deep-dives in preparation")),
    "insights": ("insights", "🧭 赛道洞察", "🧭 Track Insights", ("赛道洞察筹备中", "Track insights in preparation")),
    "cases":    ("cases",    "🏆 成功案例详解", "🏆 Success Case Breakdowns", ("案例详解筹备中", "Case breakdowns in preparation")),
}

KIND_LABEL = {
    "weekly":   ("周报", "Weekly"),
    "analysis": ("专项", "Analysis"),
    "insights": ("洞察", "Insight"),
    "cases":    ("案例", "Case"),
}


def load_items():
    items = {k: [] for k in MODULES}
    for kind, (folder, *_rest) in MODULES.items():
        base = ROOT / folder
        if not base.is_dir():
            continue
        for meta_path in sorted(base.glob("*/meta.json")):
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            meta["url"] = f"/{folder}/{meta_path.parent.name}/"
            items[kind].append(meta)
    for kind in items:
        items[kind].sort(key=lambda m: m.get("date", ""), reverse=True)
    return items


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def report_card(m) -> str:
    kind_zh, kind_en = KIND_LABEL.get(m["kind"], (m["kind"], m["kind"]))
    title_zh = m.get("title_zh", m["id"])
    title_en = m.get("title_en", m["id"])
    label_zh = m.get("week_label_zh", title_zh)
    label_en = m.get("week_label_en", title_en)
    # 周报标题显示「2026 W34 周报：XXX」，其他模块只显示标题
    if m["kind"] == "weekly":
        title_zh = f'{label_zh}：{title_zh}' if title_zh not in label_zh else label_zh
        title_en = f'{label_en}: {title_en}' if title_en not in label_en else label_en
    return f'''                <a class="report-card" href="{m["url"]}">
                    <span class="report-kind" data-zh="{kind_zh}" data-en="{kind_en}">{kind_zh}</span>
                    <h3 data-zh="{esc(title_zh)}" data-en="{esc(title_en)}">{esc(title_zh)}</h3>
                    <p data-zh="{esc(m.get("desc_zh", ""))}" data-en="{esc(m.get("desc_en", ""))}">{esc(m.get("desc_zh", ""))}</p>
                    <div class="report-meta">
                        <span>📅 {esc(m.get("date_range", m.get("date", "")))}</span>
                        <span>📊 {esc(m.get("sources", ""))}</span>
                    </div>
                </a>'''


def empty_card(zh: str, en: str) -> str:
    return f'''                <div class="report-card report-card-soon">
                    <span class="report-kind" data-zh="筹备中" data-en="Coming Soon">筹备中</span>
                    <h3 data-zh="{zh}" data-en="{en}">{zh}</h3>
                    <p data-zh="这个模块正在筹备中，敬请期待。" data-en="This module is in preparation. Stay tuned.">这个模块正在筹备中，敬请期待。</p>
                </div>'''


# 首页每个环节板块展示的最新报告数量
STEP_HOME_COUNT = 4


def step_cards(analysis: list, step: int) -> str:
    """Renders up to STEP_HOME_COUNT analysis cards for a given step (1-6)."""
    by_step = [m for m in analysis if str(m.get("step", "")) == str(step)]
    by_step.sort(key=lambda m: m.get("date", ""), reverse=True)
    if not by_step:
        return empty_card("该环节专项报告筹备中", "Step special reports in preparation")
    cards = "\n".join(report_card(m) for m in by_step[:STEP_HOME_COUNT])
    return cards


def step_tally(analysis: list, step: int) -> str:
    """Renders the header tally badge for a step's board ('📊 N 篇报告' or a coming-soon label)."""
    count = sum(1 for m in analysis if str(m.get("step", "")) == str(step))
    if count:
        return f'<span class="step-tally-inner" data-n="{count}">📊 {count} 篇报告</span>'
    return '<span class="step-tally-in empty" data-n="0">📊 报告筹备中</span>'


def archive_item(m) -> str:
    title_zh = m.get("title_zh", m["id"])
    title_en = m.get("title_en", m["id"])
    if m["kind"] == "weekly":
        label_zh = m.get("week_label_zh", title_zh)
        label_en = m.get("week_label_en", title_en)
        title_zh = f'{label_zh}：{title_zh}' if title_zh not in label_zh else label_zh
        title_en = f'{label_en}: {title_en}' if title_en not in label_en else label_en
    return f'''            <li>
                <a class="archive-item" href="{m["url"]}">
                    <div>
                        <div class="archive-title" data-zh="{esc(title_zh)}" data-en="{esc(title_en)}">{esc(title_zh)}</div>
                        <div class="archive-desc" data-zh="{esc(m.get("desc_zh", ""))}" data-en="{esc(m.get("desc_en", ""))}">{esc(m.get("desc_zh", ""))}</div>
                    </div>
                    <span class="archive-date">{esc(m.get("date_range", m.get("date", "")))}</span>
                </a>
            </li>'''


def replace_auto(html: str, name: str, body: str) -> str:
    pat = re.compile(
        r"(<!-- AUTO:" + re.escape(name) + r":begin -->).*?(<!-- AUTO:" + re.escape(name) + r":end -->)",
        re.S,
    )
    if not pat.search(html):
        raise SystemExit(f"ERROR: AUTO block '{name}' not found")
    return pat.sub(lambda m: m.group(1) + "\n" + body + "\n            " + m.group(2), html)


def rss_item(m) -> str:
    title_zh = m.get("title_zh", m["id"])
    if m["kind"] == "weekly":
        label_zh = m.get("week_label_zh", title_zh)
        title_zh = f'{label_zh}：{title_zh}' if title_zh not in label_zh else label_zh
    from email.utils import format_datetime
    from datetime import datetime, timezone
    dt = datetime.fromisoformat(m["date"]).replace(tzinfo=timezone.utc)
    url = SITE + m["url"]
    return f"""    <item>
      <title>7Kolor Insights — {esc(title_zh)}</title>
      <link>{url}</link>
      <guid>{url}</guid>
      <pubDate>{format_datetime(dt)}</pubDate>
      <description>{esc(m.get("desc_zh", ""))}</description>
    </item>"""


def build_feed(items) -> str:
    all_items = [m for group in items.values() for m in group]
    all_items.sort(key=lambda m: m.get("date", ""), reverse=True)
    body = "\n".join(rss_item(m) for m in all_items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>7Kolor Insights</title>
    <link>{SITE}/</link>
    <description>Weekly intelligence digest on developer communities — signals, trends, and judgment. 每周开发者社区情报：信号、趋势与判断。</description>
    <language>zh-CN</language>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
{body}
  </channel>
</rss>
"""


def main():
    items = load_items()

    # --- homepage cards ---
    index_path = ROOT / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    for kind, (_folder, _tz, _te, empty) in MODULES.items():
        # 只在页面存在对应 AUTO 卡块时才填充（未预留的模块跳过）
        if not re.search(r"<!-- AUTO:cards-" + re.escape(kind) + r":begin -->", index_html):
            continue
        if items[kind]:
            cards = "\n".join(report_card(m) for m in items[kind])
        elif empty:
            cards = empty_card(*empty)
        else:
            cards = empty_card("内容筹备中", "In preparation")
        index_html = replace_auto(index_html, f"cards-{kind}", cards)

    # --- homepage: six-step boards (analysis reports by step) ---
    analysis_items = items["analysis"]
    for step in range(1, 7):
        block = f"cards-analysis-step{step}"
        if not re.search(r"<!-- AUTO:" + re.escape(block) + r":begin -->", index_html):
            continue
        index_html = replace_auto(index_html, block, step_cards(analysis_items, step))
        tally_block = f"step-count-{step}"
        if re.search(r"<!-- AUTO:" + re.escape(tally_block) + r":begin -->", index_html):
            index_html = replace_auto(index_html, tally_block, step_tally(analysis_items, step))

    index_path.write_text(index_html, encoding="utf-8")
    print(f"updated {index_path.relative_to(ROOT)}")

    # --- weekly archive ---
    arch_path = ROOT / "weekly" / "index.html"
    arch_html = arch_path.read_text(encoding="utf-8")
    arch_body = "\n".join(archive_item(m) for m in items["weekly"]) or \
        '            <li><p style="padding:20px 8px;color:var(--text-secondary)">暂无周报 / No reports yet.</p></li>'
    arch_html = replace_auto(arch_html, "archive", arch_body)
    arch_path.write_text(arch_html, encoding="utf-8")
    print(f"updated {arch_path.relative_to(ROOT)}")

    # --- feed ---
    (ROOT / "feed.xml").write_text(build_feed(items), encoding="utf-8")
    print("updated feed.xml")


if __name__ == "__main__":
    main()
