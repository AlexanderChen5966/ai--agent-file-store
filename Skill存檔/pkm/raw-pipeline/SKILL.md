---
name: raw-pipeline
description: |
  Soft orchestration pipeline for processing raw materials.
  Coordinates three sequential agents: Agent A summarizes raw content,
  Agent B classifies and tags, Agent C updates wiki index and builds wikilinks.
  Designed for batch processing when raw/ accumulates 10+ files.
  Supports all Claude Code readable formats: .md .txt .html .pdf .png .jpg .jpeg .webp .gif .srt .vtt .ipynb .csv

  Trigger: raw-pipeline, 批次處理, batch process, pipeline, 自動整理流程
metadata:
  version: 1.3.0
---

# raw-pipeline

軟編排型 Skill，調度三個子 Agent 協作處理 raw/ 素材。
適合 raw/ 積壓 10 篇以上時的批次處理場景。

單篇處理請用 `knowledge-organizer`。

## 使用方式

```
raw-pipeline
批次處理 raw/
```

---

## Agent 分工

```
Team Lead（當前 Claude 工作階段）
  │  負責：統籌、錯誤處理、產出最終報告
  │
  ├── Agent A：summarizer（摘要 Agent）
  │     輸入：raw/ 所有未處理 .md 和 .pdf 檔案
  │     任務：讀取每篇原始內容，產出摘要清單
  │     輸出：/tmp/raw-summaries.md
  │
  ├── Agent B：classifier（分類 Agent）
  │     輸入：/tmp/raw-summaries.md
  │     任務：依 tag-taxonomy 分配 tag，判斷歸屬資料夾，計算 asset_value
  │     輸出：/tmp/raw-classifications.md
  │
  └── Agent C：indexer（索引 Agent）
        輸入：/tmp/raw-classifications.md + 現有 wiki/
        任務：建立 wiki 條目（含 TBRC）、建立 wikilink、更新 INDEX.md
        輸出：wiki/ 中的新 .md 檔案 + 更新後的 INDEX.md
```

---

## Agent 提示詞

### Agent A — summarizer

```
你是 raw-pipeline 的 summarizer。
任務：讀取 my-knowledge-base/raw/ 中所有未處理的素材。

支援格式與未處理判斷標準：
- .md：以下任一情況視為未處理：
  - 無 frontmatter
  - 無 `status:` 欄位（Obsidian Web Clipper 舊版預設行為）
  - `status: inbox`（標準格式）
  - `status: "inbox"`（Web Clipper 模板加引號時的格式）
- .txt / .html / .csv：尚未有對應的同名 .md 出現在 wiki/ 或 research/
- .pdf：尚未有對應的同名 .md 出現在 wiki/ 或 research/
- .png / .jpg / .jpeg / .webp / .gif：尚未有對應的同名 .md 出現在 wiki/ 或 research/
- .srt / .vtt：尚未有對應的同名 .md 出現在 wiki/ 或 research/
- .ipynb：尚未有對應的同名 .md 出現在 wiki/ 或 research/
- 其他格式（如 .mp4 / .mp3）：跳過，標注於報告

讀取規則（依格式）：

**文字類（.md / .txt / .html）**
- 直接讀取全文，.html 忽略導覽列與廣告區塊，只提取正文

**PDF（.pdf）**
- ≤ 10 頁：讀取全文（pages: "1-10"）
- > 10 頁：先讀第 1-5 頁取得摘要與結構，再讀最後 1-2 頁取得結論
- 在 summary 中標注「(PDF, N 頁，已節錄)」

**截圖／圖表（.png / .jpg / .jpeg / .webp / .gif）**
- 使用 Read 工具讀取圖片（Claude 具備視覺能力）
- 描述：圖片類型（截圖/架構圖/流程圖/圖表）、主要內容、可識別的文字
- 判斷是否為某篇文章的附圖（檔名前綴相同）→ 若是，標記為 supplementary，建議合併入對應條目
- 若為獨立知識（如完整架構圖），視為獨立素材處理

**逐字稿／字幕（.srt / .vtt）**
- 去除時間戳記（00:00:00,000 --> 00:00:05,000 格式），只保留文字
- 識別說話者標記（如有）
- 提取核心討論主題與關鍵論點，忽略過場語（嗯、啊、對對對等）

**Jupyter Notebook（.ipynb）**
- Read 工具原生支援 .ipynb，會顯示所有 cell 與 output
- 提取：標題（第一個 Markdown cell）、敘事說明（Markdown cells）、核心演算法/邏輯（Code cells）
- 忽略純輸出結果（數字/圖表描述）

**資料表格（.csv）**
- 讀取前 20 行，了解欄位結構
- 摘要：資料主題、欄位清單、筆數（如可判斷）、主要用途

對每一個素材：
1. 用 1-2 句話總結核心論點或內容（T 層）
2. 記錄原始檔名、來源（從 frontmatter 或檔名推斷）、建立日期
3. 標注格式類型與特殊屬性（頁數/解析度/片長等）

輸出格式（存入 /tmp/raw-summaries.md）：
---
file: [檔名（含副檔名）]
type: md | pdf | image | transcript | html | notebook | csv
supplementary_for: [若為附圖，填對應主文章檔名；否則留空]
pages: [頁數，僅 pdf 填寫]
source: [來源]
date: [日期]
summary: [1-2 句話核心論點或內容描述]
---

處理完所有素材後回報：已完成 N 個素材摘要（依格式分類列出數量）。
```

---

### Agent B — classifier

```
你是 raw-pipeline 的 classifier。
任務：讀取 /tmp/raw-summaries.md，對每篇素材進行分類。

參考 skills/knowledge-organizer/references/tag-taxonomy.md 選擇 tag。

對每一篇：
1. 分配 1-3 個 tag
2. 判斷歸屬：ideas / research / projects / wiki
3. 計算 asset_value（頻率 × 耗時 × 複雜度，各 1-5 分）
4. 建議 wiki 條目的英文 kebab-case 檔名

輸出格式（存入 /tmp/raw-classifications.md）：
---
file: [原始檔名]
tags: [tag1, tag2]
folder: [ideas|research|projects|wiki]
asset_value: [分數]
wiki_filename: [kebab-case-name.md]
---

處理完所有檔案後回報：已完成 N 篇分類。
```

---

### Agent C — indexer

```
你是 raw-pipeline 的 indexer。
任務：根據 /tmp/raw-classifications.md 建立 wiki 條目並更新索引。

對每一個素材（asset_value ≥ 50 才建立完整 wiki 條目）：

1. 讀取原始 raw/ 檔案內容（依格式使用對應讀取規則，同 Agent A）

2. 根據 supplementary_for 欄位判斷處理方式：
   - supplementary_for 為空 → 建立獨立 wiki 條目
   - supplementary_for 有值 → 補充前先讀取目標條目的 T（核心論點），確認補充內容的主題與 T 層一致：
     - 一致 → 將內容補充進對應條目的「補充資料」段落
     - 不一致 → 掃描其他現有 wiki 條目，改補充至主題更接近的條目；若無適合條目且 asset_value ≥ 50，改建立獨立條目

3. 用 TBRC 模板（skills/knowledge-organizer/references/tbrc-template.md）建立 wiki 條目，
   並在 frontmatter 加上 source_format 欄位標注來源格式：
   - `source_format: pdf`（PDF 節錄時另標注「建議人工補充完整內容」）
   - `source_format: image`（截圖/圖表，說明圖片描述來源）
   - `source_format: transcript`（逐字稿/字幕，說明原始影音來源）
   - `source_format: notebook`（Jupyter，標注語言與主要函式庫）
   - `source_format: csv`（資料表格，標注欄位數與筆數）
   - .md / .txt / .html 不需要 source_format 欄位

4. 掃描現有 wiki/ 找相關筆記，建立 [[wikilink]]

5. 將檔案存入對應資料夾

完成所有條目後：
6. 更新 my-knowledge-base/wiki/INDEX.md（新增條目列）
7. 對本次所有來自 raw/ 的 .md 素材，用 Edit 工具更新其 frontmatter：
   - 若已有 `status:` 欄位（無論值是 `inbox`、`"inbox"` 或其他）→ 整行替換為 `status: processed`
   - 若無 `status:` 欄位 → 在 frontmatter 結尾 `---` 前插入 `status: processed`
   **注意**：寫入時一律使用不帶引號的格式 `status: processed`，不要寫成 `status: "processed"`
   （防止下次 Agent A 重複處理）

完成後回報：已建立 N 篇 wiki 條目，更新 INDEX.md，標記 N 篇 raw/ .md 為 processed。
```

---

## Team Lead 執行流程

1. 確認 `raw/` 有素材（> 0 篇）
2. 依序啟動 Agent A → 等待完成 → Agent B → 等待完成 → Agent C
3. 確認三個 Agent 都完成後，清除 `/tmp/raw-summaries.md` 和 `/tmp/raw-classifications.md`
4. 產出處理報告（格式見下方）

---

## 處理報告格式

```markdown
# raw-pipeline 處理報告 — YYYY-MM-DD HH:MM

## 處理結果
- 輸入：N 篇原始素材
- 產出 wiki 條目：N 篇（asset_value ≥ 50）
- 歸入 research/：N 篇
- 歸入 ideas/：N 篇
- 歸入 archive/：N 篇

## 新增 wiki 條目
| 條目 | Tag | Asset Value |
|------|-----|-------------|
| [[xxx]] | pkm/workflow | 75 |

## 耗時
- Agent A（摘要）：~N 秒
- Agent B（分類）：~N 秒
- Agent C（索引）：~N 秒
```

---

## 錯誤處理

| 情況 | 處理方式 |
|------|----------|
| Agent A 失敗 | 中止，回報失敗的檔案，其餘繼續 |
| Agent B 分類不確定 | 預設歸入 `research/`，asset_value 設 30 |
| Agent C 發現重複條目 | 詢問使用者是否合併或跳過 |
| raw/ 為空 | 直接回報「raw/ 無待處理素材」 |
| PDF 讀取失敗 | 跳過該檔案，在報告中標注「PDF 讀取失敗，請手動處理」|
| PDF 超過 100 頁 | 僅讀取前 5 頁 + 後 2 頁，在摘要標注「大型 PDF，僅節錄」|
| 圖片無法解析（模糊/純裝飾） | 在報告中標注「圖片內容不足以建立條目，已跳過」|
| 圖片為文章附圖 | supplementary_for 填對應文章，不建立獨立條目，補充至對應 wiki 條目 |
| .srt/.vtt 時間戳過密難以提取 | 取樣每分鐘代表性文字，標注「逐字稿節錄」|
| 不支援格式（.mp4/.mp3 等） | 在報告中列出「不支援格式：N 個，需人工處理」|

---

## Changelog

### v1.5.0（2026-05-28）
- Agent C 步驟 7 修正：同時處理「有 status 欄位」與「無 status 欄位」兩種情況（Obsidian Web Clipper 下載的文章預設無 status）

### v1.4.0（2026-05-28）
- Agent C 新增步驟 7：處理完畢後將 raw/ .md 的 status 更新為 processed，修正重複處理 bug

### v1.3.0（2026-05-20）
- Agent C 補充規則新增「T 層對齊驗證」：補充前先讀目標條目 T 層，確認主題一致才補充；不一致則找更合適的目標條目或改建獨立條目
- 對應 alignment-check Skill 的設計理念，在 pipeline 階段就預防歸屬錯誤

### v1.2.0（2026-05-14）
- 全面擴充格式支援：新增圖片（.png/.jpg/.jpeg/.webp/.gif）、逐字稿（.srt/.vtt）、網頁存檔（.html）、Jupyter Notebook（.ipynb）、資料表格（.csv）
- Agent A：新增各格式專屬讀取規則（視覺解析、去時間戳、ipynb cell 提取等）
- Agent A：新增 supplementary_for 欄位，識別文章附圖避免建立無意義獨立條目
- Agent C：依 supplementary_for 決定建立獨立條目或補充至既有條目
- Agent C：新增 source_format 欄位標注各格式來源
- 錯誤處理：新增圖片解析失敗、附圖識別、字幕節錄、不支援格式等情境
- CLAUDE.md 同步新增「raw/ 支援的輸入格式」對照表

### v1.1.0（2026-05-14）
- Agent A 支援 .pdf 讀取（自動判斷頁數，超過 10 頁節錄首尾）
- Agent C 支援 .pdf 來源條目（加 source_format: pdf，大型 PDF 標注人工補充提示）
- 錯誤處理新增 PDF 失敗與大型 PDF 兩個情境

### v1.0.0（2026-05-13）
- 初始版本
- 三 Agent 軟編排架構（summarizer → classifier → indexer）
- 完整 Agent 提示詞
- 處理報告格式與錯誤處理規則
