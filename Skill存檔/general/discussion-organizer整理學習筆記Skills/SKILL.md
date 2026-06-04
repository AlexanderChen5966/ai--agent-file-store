---
name: discussion-organizer
version: "1.0.0"
description: Organizes notes, articles, transcripts, and personal reflections into structured knowledge documents. Supports multiple output frameworks (TBRC, SCQA, material library, roleplay scripts). Use when the user says "整理", "結構化", "幫我整理這篇文章/筆記/想法/逐字稿/字幕", "用TBRC/SCQA整理", "建立素材庫", "整理成腳本".
---

# Discussion Organizer

Transforms raw content — notes, articles, transcripts, subtitles, or reflections — into structured knowledge documents.

## Two-axis detection

Before processing, identify both axes. They are independent.

### Axis 1: Input type → determines pre-processing

| Type | Signals | Pre-processing |
|------|---------|----------------|
| 直播/逐字稿 | 大量口語、重複、說話者標記、無段落 | See sop-complete.md → 逐字稿前處理 |
| 字幕檔 | 時間戳（00:01:23）、短句斷行 | 剔除時間戳、合併斷句後再處理 |
| 網頁文章 | 導覽列文字、廣告語、「相關文章」區塊 | 識別正文邊界、剔除非正文區塊 |
| 純文字筆記 | 已相對乾淨，有段落或條列 | 直接進入四層判斷，無需前處理 |

### Axis 2: Output framework → determines structure

| Framework | Best for | Template |
|-----------|----------|----------|
| TBRC | 學習筆記、技術文章、有明確論點的內容 | See templates.md → TBRC |
| SCQA | 問題分析、Bug記錄、案例、有衝突的敘事 | See templates.md → SCQA |
| 素材庫 | 直播/逐字稿、內容密度高、不需套框架 | See templates.md → MATERIAL |
| 情境腳本 | 角色扮演訓練素材、情境對話、教學演示 | See templates.md → SCRIPT |

**Framework selection rule:**
- User specifies → use that framework
- User does not specify → infer from input type:
  - 技術文章/學習筆記 → TBRC
  - 問題/案例/Bug記錄 → SCQA
  - 逐字稿/字幕/高密度口語 → 素材庫
  - 教學示範/對話情境 → 情境腳本
- If still unclear → ask: "你希望輸出成哪種格式？TBRC知識架構、SCQA問題分析、素材標籤庫、還是情境腳本？"

## Four-layer judgment (apply to every content item)

After pre-processing, run each item through all four layers.

### Layer 1: Value

```
⭐⭐⭐⭐⭐  Core insight / main claim     → primary position in framework
⭐⭐⭐⭐    Important supporting detail   → secondary position
⭐⭐⭐      Useful example or case        → examples / R3-R4 / case detail
⭐⭐        Background or reference       → appendix / C3 / tag only
⭐ / ❌    Filler / repeat / pure emotion → discard
```

Discard if: 「太棒了！」「我覺得很有趣」「嗯嗯對對」and similar filler with no information value.

### Layer 2: Credibility

```
✅  Has source: official docs, data, speaker's direct experience
⚠️  Reasonable inference, no stated source
❌  Contradicts known facts or internal logic
```

Rule: Personal reflections and roleplay material → always ⚠️ by default.

### Layer 3: Extraction granularity

```
🔥  Quote directly   — original phrasing has unique value (金句、精準定義)
📝  Rewrite          — correct idea, needs removing colloquial/emotional tone
🗂️  Tag only         — topic mentioned, not substantive enough to expand
```

### Layer 4: Tone normalization (apply to all 📝 items)

```
口語 → 書面語：「搞定」→「完成」、「超強」→「效能顯著」
統一術語：全文選定一個詞，不混用（Agent / 智能體 選一個）
刪除情緒填充詞：「太棒了」「真的假的」「對對對」
時態：主動語態、現在式
```

## Workflow

```
1. Detect input type (Axis 1) → apply pre-processing if needed
2. Detect or confirm output framework (Axis 2)
3. Break content into individual items (one claim = one item)
4. Run four-layer judgment on each item
5. Map items to framework positions (see templates.md)
6. Apply tone normalization to all 📝 items
7. Self-check (below)
8. Output + summary (3 lines max)
```

## Self-check before output

```
Pre-processing
- [ ] Time stamps removed (subtitle input)
- [ ] Non-content blocks removed (web article input)
- [ ] Filler / noise discarded before framework mapping

Framework
- [ ] Correct framework applied (or user confirmed)
- [ ] All ⭐⭐⭐⭐⭐ items placed in primary positions
- [ ] No framework section left completely empty without note

Quality
- [ ] No vague hedging in output: 可能、也許、感覺 (except inside 🔥 quotes)
- [ ] All ⚠️ items explicitly marked
- [ ] Consistent terminology throughout
- [ ] No duplicate content across sections
```

## Output summary format

Append after every output:

```
📊 整理摘要
輸入類型：[逐字稿 / 字幕 / 網頁文章 / 純文字筆記]
輸出框架：[TBRC / SCQA / 素材庫 / 情境腳本]
處理 N 條，保留 X 條，丟棄 Y 條（噪音/重複）
⚠️ 待驗證：N 條
建議下一步：[1 具體行動]
```

## Edge cases

| Situation | Action |
|-----------|--------|
| < 5 items after filtering | Proceed; note "內容密度較低，建議補充來源" |
| Input > 5000 chars | Split by natural sections, process each, merge at self-check |
| Mixed languages | Keep technical terms in source language; output prose in 繁體中文 |
| All items ⭐ or below | Output what exists; tell user "此內容知識密度較低" |
| User requests specific tags | Apply user tags in 素材庫 mode; do not invent tag taxonomy |

For detailed framework rules and pre-processing SOPs see sop-complete.md.
For all output templates see templates.md.
