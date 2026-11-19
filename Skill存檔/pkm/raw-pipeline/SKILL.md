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
  version: 1.10.0
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
  │     任務：依 tag-taxonomy 分配 tag，判斷歸屬資料夾，計算 asset_value，
  │           標出同主題群組（共用 wiki_filename）與可補充的既有條目（merge_target）
  │     輸出：/tmp/raw-classifications.md
  │
  │   Team Lead：依「建條目三條路徑」判定每篇走哪條路（含待合併清單的跨批合計）
  │
  └── Agent C：indexer（索引 Agent）
        輸入：Team Lead 的判定結果 + /tmp/raw-classifications.md + 現有 wiki/
        任務：建立獨立／合併 wiki 條目（含 TBRC）、補充既有條目、建立 wikilink、更新 INDEX.md
        輸出：wiki/ 中的新 .md 檔案 + 補充過的既有條目 + 更新後的 INDEX.md
```

---

## 建條目三條路徑（v1.10.0）

只看單篇分數會讓單篇新聞類素材幾乎全部只標記、內容流失（2026-11 連續三批各 10 篇 0 條目）。
Team Lead 在 Agent B 完成後，依序判定每篇素材走哪條路：

| 路徑 | 條件 | 動作 |
|------|------|------|
| ① 獨立條目 | 單篇 asset_value ≥ 50 | 建一個獨立 wiki 條目（原規則） |
| ② 合併條目 | 同主題多篇（共用 `wiki_filename`）各自 < 50，但**合計 ≥ 50**（可跨批，見待合併清單） | 合併建一個條目，所有篇列為來源（`source`、`source_2`、`source_3`…），`asset_value` 寫合計 |
| ③ 補充既有條目 | 低分素材與**既有** wiki／research 條目同主題（Agent B 填了 `merge_target`） | 有新內容才補進該條目「補充資料」段；只有重複資訊就不補 |
| — 只標記 | 以上皆不符合，或 `excluded` | 只標 processed；非 excluded 的低分素材記入待合併清單 |

判定順序：① → ③ → ②。單篇已過門檻的不拿去合併；能補進既有條目的優先補，不另開近似條目。

**待合併清單**：`my-knowledge-base/outputs/raw-pipeline-pending.md`
- 每批結束時，把走「只標記」路徑、且非 excluded 的素材追加進去（一行一篇：`wiki_filename｜asset_value｜raw 檔名｜一句重點｜批次日期`）
- 下一批判定路徑 ② 時，把清單中同 `wiki_filename` 的分數一起合計；合併建條目後，從清單刪掉那幾行（用 Edit 字串比對）
- 為什麼要落地成檔案：分類結果原本只存在 /tmp，換日或重開 session 就消失，跨批合計做不了
- 該檔是流程元資料，不是知識條目，不進 INDEX.md

---

## Agent 提示詞

### Agent A — summarizer

```
你是 raw-pipeline 的 summarizer。
任務：讀取 my-knowledge-base/raw/ 中所有未處理的素材。

支援格式與未處理判斷標準：
- .md（v1.8.0 起**只看 frontmatter**）：
  frontmatter 為以下任一情況即為未處理：無 frontmatter / 無 `status:` 欄位 / `status: inbox` / `status: "inbox"`
  掃描指令：`for f in raw/*.md; do head -15 "$f" | grep -q '^status:.*inbox' && echo "$f"; done`
  （限 `head -15` 避免正文提到 inbox 造成誤報；舊制留下的 `.md` 旁車標記檔一律忽略，不具判斷效力）
- 非 .md 格式（.pdf / .png / .jpg / .jpeg / .webp / .gif / .txt / .html / .csv / .srt / .vtt / .ipynb）：
  raw/ 中**不存在**同名 `.processed` 標記檔即為未處理
  例：`report.pdf` 未處理 → `report.pdf.processed` 不存在
  掃描指令：`find raw/ -type f ! -name "*.md" ! -name "*.processed" | while read f; do [ ! -f "${f}.processed" ] && echo "$f"; done` 過濾出尚無 `.processed` 配對的檔案（⚠️ 不可省略 pipe 後的存在性檢查，否則會把已處理檔案也列出）
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
2. 判斷歸屬：ideas / research / projects / wiki；明顯不屬知識庫關注方向者標 excluded 並寫一句理由
3. 計算 asset_value：頻率、耗時、複雜度**逐項**各給 1-5 分再相乘，寫出 `score: 頻率x耗時x複雜度`（不可只憑印象給總分）
4. 建議 wiki 條目的英文 kebab-case 檔名；**同主題、同系列或同一產品的多篇共用同一個 wiki_filename**（各自打分），在 note 寫明合併關係
5. 先讀 my-knowledge-base/outputs/raw-pipeline-pending.md，主題相同的沿用清單中的 wiki_filename
6. 用 grep 查 wiki/、research/ 有沒有同主題的既有條目；有的話填 merge_target（該條目路徑）

輸出格式（存入 /tmp/raw-classifications.md）：
---
file: [原始檔名]
tags: [tag1, tag2]
folder: [ideas|research|projects|wiki|excluded]
score: [頻率x耗時x複雜度]
asset_value: [分數]
wiki_filename: [kebab-case-name.md]
merge_target: [既有條目路徑；沒有就留空]
note: [系列／合併關係、文末業配等提醒]
reason: [僅 excluded 填]
---

處理完所有檔案後回報：已完成 N 篇分類。
```

---

### Agent C — indexer

```
你是 raw-pipeline 的 indexer。
任務：根據 Team Lead 的路徑判定與 /tmp/raw-classifications.md，建立／補充 wiki 條目並更新索引。

依路徑處理（見「建條目三條路徑」）：
- 路徑 ① 獨立條目：照下方步驟 1-5 建立
- 路徑 ② 合併條目：先讀完該組所有篇（含待合併清單中前幾批的 raw 原檔）再寫一個條目；
  多來源寫法沿用既有條目慣例（`source` 主要一篇，其餘 `source_2`、`source_3`…），asset_value 寫合計
- 路徑 ③ 補充既有條目：
  a. 讀目標條目的 T（核心論點），主題一致才補；不一致就找更接近的條目，都沒有就不補並回報
  b. 先比對目標條目已寫了什麼，**只補新內容**；只有重複資訊就不補，回報「無新增」
  c. 用 Edit 在「補充資料」段追加（沒有該段就在「相關連結」前新增 `## 補充資料`），
     每則以「**YYYY-MM-DD 補充（來源：標題＋網址）**」開頭，3-8 行重點，二手整理／未核對的數字要標明
  d. 目標條目有 source_N 慣例時，同時追加一個 source_N
  e. 在 INDEX.md 該條目那一列描述末尾加「📎 補充：關鍵字」（Edit 單行，不新增列）
- 每個條目建立前都要先查重複：既有條目已涵蓋核心論點 → 改走路徑 ③ 或回報 Team Lead

建立條目（路徑 ①②）的步驟：

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
7. 對本次所有來自 raw/ 的素材標記已處理（v1.8.0 起依檔案類型**分流**）：
   - **`.md`**：用 Edit 把 frontmatter 的 `status:` 改為 `status: processed`
     ⚠️ **只改 `status:` 這一行**，其餘 frontmatter 欄位與正文一律不得動
   - **非 `.md`**（無法承載 frontmatter）：`touch 'raw/<原始檔名>.processed'`
     例：`raw/report.pdf` → `touch 'raw/report.pdf.processed'`
     ⚠️ 檔名一律用**單引號**——雙引號會讓 shell 展開 `$`，檔名含 `$` 時會產生破損的孤兒標記
   - 兩者皆屬流程元資料，在 CLAUDE.md「NEVER modify raw/」的明確例外範圍內

完成後回報：已建立 N 篇 wiki 條目（獨立 N／合併 N）、補充 N 篇既有條目，更新 INDEX.md，標記 N 篇 .md（frontmatter）＋ N 個非 md（旁車標記）。
```

---

## Team Lead 執行流程

1. 確認 `raw/` 有素材（> 0 篇）；檔名以「 1.md」結尾且同名原檔存在者是重複剪存，不排入批次（回報給使用者決定是否移入 archive/）
2. 依序啟動 Agent A → 等待完成 → Agent B → 等待完成
3. 讀 `/tmp/raw-classifications.md` 與待合併清單，依「建條目三條路徑」判定每篇的路徑
4. 有路徑 ①②③ 的素材 → 啟動 Agent C；全部只標記 → Team Lead 自行標記 processed（只改 status 一行，binary 模式保留換行）
5. 把本批走「只標記」且非 excluded 的素材追加進待合併清單；已合併的從清單刪除
6. 確認都完成後，清除 `/tmp/raw-summaries.md` 和 `/tmp/raw-classifications.md`
7. 產出處理報告（格式見下方）

---

## 處理報告格式

```markdown
# raw-pipeline 處理報告 — YYYY-MM-DD HH:MM

## 處理結果
- 輸入：N 篇原始素材
- 產出 wiki 條目：N 篇（獨立 N／合併 N）
- 補充既有條目：N 篇
- 只標記：N 篇（記入待合併清單 N 篇）
- 歸入 archive/：N 篇

## 新增 wiki 條目
| 條目 | 路徑 | 來源篇數 | Tag | Asset Value |
|------|------|---------|-----|-------------|
| [[xxx]] | ① 獨立 | 1 | pkm/workflow | 75 |
| [[yyy]] | ② 合併 | 3 | ai/claude | 132（合計） |

## 補充既有條目
| 素材 | 補進條目 | 補了什麼（或為何不補） |
|------|---------|----------------------|

## 待合併清單變動
- 新增 N 篇；本批合併後移除 N 篇；清單中目前累計最高的主題：xxx（合計 N 分）

## 排除項目（非知識庫關注領域，刻意排除非遺漏）
- 檔名：一句話說明排除理由（如「遊戲發行平台，非 AI/PKM/dev 焦點」）

> 此區塊只列「Agent B 判定不屬於知識庫關注領域、僅標記 .processed 未建任何條目」的素材。與「歸入 archive/」不同——archive/ 是曾建立過 wiki 但後來停用的內容，這裡是從未建立條目。目的是讓未來回顧 raw/ 時能區分「刻意排除」與「真的遺漏積壓」，避免誤判。若本批次無排除項目，此區塊可省略。

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
| Agent C 發現重複條目 | 既有條目已涵蓋核心論點 → 改走路徑 ③ 補充；若新素材角度明顯不同、或補充會讓條目偏離 T 層，回報 Team Lead 詢問使用者 |
| 目標條目不在 wiki/、research/（如只在 ideas/） | 不補，記入待合併清單並在報告中列出 |
| raw/ 為空 | 直接回報「raw/ 無待處理素材」 |
| PDF 讀取失敗 | 跳過該檔案，在報告中標注「PDF 讀取失敗，請手動處理」|
| PDF 超過 100 頁 | 僅讀取前 5 頁 + 後 2 頁，在摘要標注「大型 PDF，僅節錄」|
| 圖片無法解析（模糊/純裝飾） | 在報告中標注「圖片內容不足以建立條目，已跳過」|
| 圖片為文章附圖 | supplementary_for 填對應文章，不建立獨立條目，補充至對應 wiki 條目 |
| .srt/.vtt 時間戳過密難以提取 | 取樣每分鐘代表性文字，標注「逐字稿節錄」|
| 不支援格式（.mp4/.mp3 等） | 在報告中列出「不支援格式：N 個，需人工處理」|

---

## Changelog

### v1.10.0（2026-11-19）
- **建條目改三條路徑**：① 單篇 ≥ 50 獨立建；② 同主題合計 ≥ 50 合併建（可跨批）；③ 低分但與既有條目同主題 → 有新內容才補進「補充資料」
- 新增**待合併清單** `outputs/raw-pipeline-pending.md`：讓跨批合計可行（/tmp 分類結果換日即消失）
- Agent B：asset_value 改逐項打分並寫出 `score`；同主題共用 wiki_filename；新增 `merge_target`、`note`、`excluded` 欄位
- Agent C：新增合併條目與補充既有條目的處理步驟（T 層對齊、只補新內容、日期標頭、INDEX 列尾「📎 補充」）
- Team Lead：Agent B 後先判定路徑；全部只標記時不派 Agent C；「 1.md」重複剪存不排入批次
- 起因：2026-11 連續三批各 10 篇 0 條目，Managed Agents（48）、ADK（36）等有具體觀點的內容只標記就流失；同主題（Whiteboards／Sheets 5 篇、AI 做 UI 驗收 4 篇、雲端排程 3 篇）合起來價值明顯過門檻

### v1.9.1（2026-08-13）
- Agent C 的 `touch` 檔名改用**單引號**：雙引號會讓 shell 展開 `$`，實際造成過一個破損的孤兒標記（`NT$15,680` → `NT,680`）

### v1.9.0（2026-08-13）
- **標記制度改分流**：`.md` 改回 Edit frontmatter `status`（僅此一行），非 `.md` 維持 `.processed` 旁車標記
- Agent A 掃描 `.md` 改為只看 frontmatter，並限 `head -15` 避免正文誤報
- 理由：旁車標記在 Obsidian / Dataview 端不可見，介面上所有 raw 檔恆顯示 inbox。全庫盤點發現 768 篇 raw .md 的兩種訊號完全反相，任一單一判準都會誤報約半數

### v1.8.0（2026-08-04）
- **修正非 .md 掃描指令 bug**：v1.6.0 起沿用的 `find raw/ -type f ! -name "*.md" ! -name "*.processed"` 只排除標記檔本身，未過濾「已有配對 .processed」的原始檔，導致每次都把全部非 .md 素材誤報為積壓（2026-08 wiki-health-check 抓到）。補上 pipe 後的存在性檢查，對齊 `rules/inbox-detection-protocol.md` 的「通用完整掃描」正確版本
- **新增「排除項目」滾動日誌習慣**：處理報告中明確列出本批次判定為「非知識庫關注領域，僅標記 .processed」的素材（如遊戲平台/音樂生成/通用資源目錄），與「遺漏未處理」區分，避免日後回顧時誤判為積壓

### v1.7.0（2026-07-08）
- **制度統一（批次 C 健檢 C-1 修正）**：raw/ `.md` 素材改用 `.processed` 旁車標記，廢止 Agent C「用 Edit 改 frontmatter」舊制——對齊 CLAUDE.md「raw/ 檔案不可修改」現行規則
- Agent A 的 .md 未處理判斷改**雙條件**（frontmatter inbox 且無 `.processed` 標記），避免把已標記處理的 56 篇誤報為積壓
- Agent C 步驟 7/8 合併為單一標記步驟（.md 與非 .md 一致）

### v1.6.0（2026-06-22）
- 非 .md 檔案的 inbox 判斷改為 `.processed` 標記檔機制（取代「同名 .md 是否存在」的脆弱判斷）
- Agent A：掃描邏輯改為 `find raw/ -type f ! -name "*.md" ! -name "*.processed"` 過濾未處理的非 md 檔
- Agent C：步驟 8 新增：非 .md 素材處理完後執行 `touch "raw/<檔名>.processed"` 建立標記
- CLAUDE.md 同步新增「非 Markdown 檔案的 inbox 判斷規則」段落

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
