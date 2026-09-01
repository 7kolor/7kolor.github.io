# Weekly report authoring guide / 周报写作指南

The site is now plain static HTML (no Jekyll). To add a new week:

1. Copy the latest week as a starting point:
   ```sh
   cp -r weekly/w34 weekly/w35
   ```
2. Edit `weekly/w35/index.html` — it is a single bilingual page:
   every translatable element carries `data-zh` / `data-en` attributes,
   and the in-page toggle switches languages client-side.
3. Build the single-language variants:
   ```sh
   python3 scripts/build_i18n.py weekly/w35
   ```
4. Add a card for the new week to `index.html` and an entry to
   `weekly/index.html` (prepend to the top of the archive list),
   then prepend an `<item>` to `feed.xml`.
5. Preview locally:
   ```sh
   python3 -m http.server 4000
   ```

> Signal IDs are opaque: SIG-{yy}{ww}-{seq}. Never use internal identifiers.
> 信号 ID 使用不透明编号，禁止出现任何内部标识符。

---

## Content checklist / 内容清单

- TL;DR — three one-sentence takeaways / 三句话结论
- Top Signals — what happened, why it matters, our take / 发生了什么、为什么重要、我们的判断
- Every item links to its public source / 每条信号均可回溯到公开来源
- Public content only — no private data, no paywalled sources / 只用公开内容
