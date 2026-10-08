---
name: wiki-health-check
description: |
  Monthly wiki health check skill. Scans the entire wiki for quality issues:
  contradictions between notes, unsupported claims, missing cross-links,
  outdated content, and knowledge gaps. Based on Karpathy's step 5 method.

  Trigger: wiki-health-check, 健康檢查, health check, wiki品質, 知識庫健檢, monthly review
metadata:
  version: 1.7.0
---

# wiki-health-check

每月掃描整個 wiki，找出品質問題。
對應 Karpathy 方法第五步：讓 AI 幫知識庫做「健康檢查」。

## 使用方式

```
wiki-health-check
知識庫健檢
monthly review
```

建議每月執行一次，或 wiki 超過 30 篇時開始定期執行。

---

## 檢查項目

### 1. 矛盾偵測（Contradiction Check）
> 找出 wiki 中互相矛盾的論點

掃描範圍：相同主題的多篇 wiki 條目
判斷標準：
- 同一技術/方法在不同筆記中有不同描述
- 前後期筆記的建議方向相反
- API 版本或規格前後不一致

輸出格式：
```
⚠️ 矛盾：[[note-a]] vs [[note-b]]
問題：[具體矛盾內容]
建議：[以哪篇為準 / 需要更新]
```

---

### 2. 缺乏來源（Unsupported Claims）
> 找出沒有來源支持的重要論點

判斷標準：
- frontmatter `source` 為空
- 筆記中有強烈主張但無引用
- B 層（適用場景）有具體限制但無依據

輸出格式：
```
🔍 缺乏來源：[[note-name]]
問題：[哪個論點需要來源]
建議：[補充來源 / 降低論點強度]
```

---

### 3. 缺口分析（Knowledge Gap）
> 找出應該有但尚未建立的筆記

掃描範圍：現有 wikilink 指向不存在的頁面、常被提及但無對應 wiki 條目的概念

輸出格式：
```
📭 知識缺口：[[missing-note]]
被引用於：[[note-a]]、[[note-b]]
建議：建立此條目 / 確認是否需要
```

---

### 4. 連結品質（Link Quality）
> 找出孤立筆記與斷裂連結

- 孤立筆記：沒有任何 wikilink 指入的條目
- 懸空連結：wikilink 指向不存在的頁面
- 過度集中：某些節點被太多筆記連結，可能需要拆分

⚠️ **掃描前必做的三件事（2026-09-03 新增，三者皆為實際誤報所致）：**

**① 先剝除程式碼區塊，再抽 `[[...]]`。**
Obsidian **不會**把圍籬（```／~~~）或行內 code 裡的 `[[...]]` 算成連結。不剝除的話，bash regex、
JSON、範例片段全會被當成懸空連結。2026-09-01 健檢因此把 8 個懸空連結報成 8 個，實際只有 2 個
（`[["$cmd" =~ ^(npm\ test]]` 就是 ```bash 圍籬內的 regex）。
```python
t = re.sub(r'```.*?```', '', t, flags=re.S)
t = re.sub(r'~~~.*?~~~', '', t, flags=re.S)
t = re.sub(r'`[^`\n]*`', '', t)
```

**② 解析必須同時支援「路徑寫法」與「純檔名寫法」。**
`[[synthesis/synthesis-multi-agent]]`、`[[research/xxx]]`、`[[ideas/xxx]]`、`[[sanlong/api]]` 都是
有效連結。只用純檔名比對會把它們全報成懸空（2026-09-01 首次掃描誤報 133 個，實際 8 個）。
解析順序：先試 vault 相對路徑，再試 basename；並記得 `sanlong/` `b2b-manager/` 等**外部專案 vault**
與 `my-technical-notes/` 也要納入可解析範圍。

**③ 與前一份 `outputs/health-check-*.md` 對照，再決定是否列為新問題。**
上一份報告可能已把某些項目判定為「誤報／刻意的外部參照」（例如指向 skill 名稱或記憶檔的 `[[...]]`）。
**重複列出已被判定過的項目，會讓優先清單失真**——2026-09-01 健檢就把 08-12 已排除的 6 項重新報成
「🔴 真 bug」。若判斷與前次不同，必須寫出「為何改判」。

輸出格式：
```
🏝️ 孤立：[[note-name]]（0 個入連結）
🔗 懸空：[[missing-page]]（被 [[note-a]] 引用）
```

---

### 5. 內容過時（Outdated Content）
> 找出可能已經過時的筆記

判斷標準：
- 建立日期超過 6 個月且未更新
- 筆記中提到特定版本號（如 API v11）但現在已有更新版本

輸出格式：
```
📅 可能過時：[[note-name]]
建立：YYYY-MM-DD / 上次更新：YYYY-MM-DD
建議：[更新 / 歸檔 / 確認仍有效]
```

---

### 6. 未處理素材（Unprocessed Raw）
> 找出 raw/ 中尚未轉化為 wiki 條目的素材

**判斷邏輯（frontmatter / 旁車標記分流 + cross-reference）：**

A. **`.md` 素材**（v1.6.0 起**只看 frontmatter**）：`status:` 為 `inbox` / `"inbox"` / 缺欄位 → 未處理
   掃描指令：`for f in raw/*.md; do head -15 "$f" | grep -q '^status:.*inbox' && echo "$f"; done`
   ⚠️ 限 `head -15`，否則正文提到 inbox 會誤報；舊制留下的 `.md` 旁車標記檔一律忽略，不具判斷效力

B. **非 `.md` 素材**（.pdf / 圖片 / .srt / .csv 等）：raw/ 中**不存在**同名 `.processed` 標記檔 → 未處理
   掃描指令：`find raw/ -type f ! -name "*.md" ! -name "*.processed" | while read f; do [ ! -f "${f}.processed" ] && echo "$f"; done`
   ⚠️ 不可省略 pipe 後的存在性檢查——只寫前半段 `find` 只排除標記檔本身，不會排除「已有配對 .processed」的原始檔，等於把全部非 .md 素材都當成未處理（2026-08 健檢發現此 bug，已修正）

C. **幽靈標記偵測（health-check 專屬，比 pipeline 多一層）**：
   對每個已標記為處理完的素材（`.md` 看 frontmatter `processed`，非 md 看 `.processed` 標記），
   反查 wiki/ 或 research/ 是否真有對應條目（用檔名前綴或 `source:` 比對）。
   若**已標記卻找不到對應條目** → 列為「⚠️ 待人工確認」。

   ⚠️ **此比對有先天上限，結果不可當成結論**：多篇素材常合併成一條 wiki 條目、素材可能未達存入門檻而刻意不建條目、
   來源 URL 也未必一致。2026-08-13 全庫盤點實測，即使是確定已處理的素材，URL 自動命中率也只有三到四成。
   因此「找不到對應條目」**只能列為待人工確認，絕不可自動翻回 inbox**。

> **關於 raw/ 唯讀原則：** `.md` 只改 frontmatter 的 `status:` 單一欄位、非 md 新增 `.processed` 旁車標記，
> 兩者皆屬流程元資料，在 CLAUDE.md「NEVER modify raw/」的明確例外範圍內。

**特殊情況：**
- 已標記為處理但超過 30 天仍無對應條目 → 列入待人工確認
- 多個 raw 檔對應同一 wiki 條目（合併處理）→ 各自標記完成即視為已處理，非異常

輸出格式：
```
📥 未處理素材：raw/檔案名稱.md (.pdf)
來源：（URL 或空白）
建立：YYYY-MM-DD
建議：執行 knowledge-organizer 處理此素材
```

---

### 7. 精粹過時偵測（Stale Synthesis Detection）
> 找出來源已增加、但精粹條目尚未重跑的 `wiki/synthesis/` 條目

**背景**：`knowledge-synthesizer` 產出的精粹是「快照」，一次讀取當下 N 篇來源後定稿，
不會自動感知日後新增的同主題 wiki 條目。若來源持續增長而精粹未重跑，精粹的
A 層（獨特視角）與 V 層（知識缺口）會過時，且過時會沿 synthesis → concepts 往上傳染。

**判斷邏輯（依賴 frontmatter 戳記，2026-07 起）：**

每篇精粹 frontmatter 應含：
- `source_count`：定稿當下的來源條目數（整數）
- `synthesis_snapshot_date`：該快照的基準日

對每篇 `wiki/synthesis/*.md`：
1. 解析該精粹「**## 來源條目**」段落裡的 `[[...]]`，得到**來源清單集合** `S`（不是只讀數字）
2. 找出 `date > synthesis_snapshot_date`、**且不在 `S` 內**、且主題相關的 wiki 條目 → **新增候選**
3. 有新增候選 → 標記為「精粹過時」，列出候選與其日期
4. 若精粹**缺** `source_count` 或 `synthesis_snapshot_date` → 標記為「⚠️ 缺戳記，無法偵測」，建議補上

> 🔴 **不要用「`source_count` vs glob 總數」比大小（2026-09-03 廢止此法）。**
> 該法會**假陰性**：glob 與實際來源集合可能**同時往兩個方向偏差而互相抵銷**。
> 實例——`synthesis-claude-md` 的 `source_count=5`，glob `wiki/*claude-md*` 也數到 5，判定「OK」；
> 但那 5 個裡**漏掉**來源清單內檔名不含 `claude-md` 的 `claude-5-context-engineering-rules`，
> 又**多抓**了不在來源清單內的新條目 `apple-claude-md-teardown`（av 85，高於全部既有來源）。
> 兩邊各偏一個、方向相反，總數相同 → **一篇實質嚴重過時的精粹被判成健康**。
>
> `source_count` 仍應保留為戳記（供人工核對與歷史追溯），但**判斷過時一律用步驟 1–2 的集合差**。

**主題相關性判斷**：先用檔名前綴 glob 取候選（例：`synthesis-multi-agent` → `wiki/multi-agent*.md`
＋ `wiki/*multi-agent*.md`），再由人工／模型判讀標題是否真屬該主題。
⚠️ **glob 與關鍵詞比對都會嚴重過報**——`wiki/agent-*.md` 會掃到 29 篇、`*skill*` 會掃到 45 篇，
遠多於實際來源。故本項為「提醒」而非「自動重跑」，**報告中須先剔除明顯誤抓再列出候選數**。

輸出格式：
```
🔄 精粹過時：[[synthesis-xxx]]
快照：N 篇（YYYY-MM-DD）→ 現有 M 篇
新增候選：[[new-entry-a]]、[[new-entry-b]]
建議：確認後重跑 knowledge-synthesizer <主題> 覆蓋更新
```

> **不自動重跑**：重跑會覆蓋可能經人工微調的精粹，一律列入報告等使用者確認。

---

## 執行流程

1. 讀取所有 `wiki/`（與 `research/`）目錄的 `.md` 檔案，收集 source URL 清單
2. 讀取 `raw/`：`.md` 看 frontmatter `status`，非 md 檔比對 `.processed` 旁車標記
3. **先讀前一份 `outputs/health-check-*.md`**（取得已判定為誤報／已排除的項目清單，以及上次未修的問題）
4. 依序執行七項檢查（第 1 項：矛盾偵測**必須逐項覆核前次報告列出的矛盾是否已修**；第 4 項：先剝程式碼區塊、解析路徑前綴；第 6 項：未處理 = 未標記，額外做 cross-reference 覆核；第 7 項：用來源清單集合差，不用 glob 總數）
5. 彙整結果，產出健康檢查報告（**前次未修的問題要標「連續 N 次指認」**）
6. 存入 `outputs/health-check-YYYY-MM-DD.md`
7. 提供優先處理清單（最需要修復的 3-5 個問題）
8. 執行 **5A+ 階段評估**（見下方判斷邏輯）

---

## 輸出格式

```markdown
# Wiki 健康檢查報告 — YYYY-MM-DD

## 整體評分
- wiki 條目數：N
- raw 素材數：N（.md：N / .pdf：N｜已處理 N / 未處理 N）
- 問題總數：N（嚴重 N / 警告 N / 建議 N）
- 健康指數：良好 / 待改善 / 需要處理

## 🔴 嚴重問題（需立即處理）
[矛盾 / 斷裂連結]

## 🟡 警告（建議本週處理）
[缺乏來源 / 孤立筆記 / 未處理素材]

## 🟢 建議（下次處理）
[知識缺口 / 過時內容]

## 優先處理清單
1. [最重要的修復]
2.
3.

## 🔄 5A+ 階段評估

[根據本次健康檢查結果，判斷知識庫目前處於哪個 5A+ 階段，並給出下一步建議]

**當前階段：[ACQUIRE / ATTEMPT / ADJUST / APPLY / PLUS]**

理由：[一句話說明判斷依據]

下一步：[對應該階段的具體行動]
```

---

## 5A+ 階段判斷邏輯

根據健康檢查結果，對應到 5A+ 循環的當前階段：

| 階段 | 判斷條件 | 核心建議 |
|------|---------|---------|
| **AIM** | wiki 條目 < 10 篇，知識庫剛建立 | 先定義核心主題範圍，不要急著收集素材 |
| **ACQUIRE** | raw/ 未處理素材 > 15 篇，遠多於 wiki 產出速度 | 優先消化積壓，暫停收集新素材 |
| **ATTEMPT** | wiki 有嚴重矛盾或缺口 > 3 個 | 修正品質問題，穩固現有知識再擴張 |
| **ADJUST** | 同主題有 3 篇以上 wiki 但無精粹條目 | 跑 `knowledge-synthesizer`，提煉跨篇洞察 |
| **APPLY** | 健康指數「良好」，知識庫運作順暢 | 把整理好的知識實際用於工作輸出 |
| **PLUS** | 連續兩次健康良好，主題已飽和 | 擴展新主題領域，重新進入 AIM 階段 |

> **注意**：一次可能對應多個階段（例如 ACQUIRE + ATTEMPT 同時成立），優先處理最低階段的問題。

## 參考資源

- Karpathy 方法第五步：健康檢查（矛盾偵測、缺漏補充、關聯發現）
- 5A+ 循環框架：AIM → ACQUIRE → ATTEMPT → ADJUST → APPLY → PLUS

---

## Changelog

### v1.8.0（2026-09-03）
- **第 7 項判準改為「來源清單集合差」，廢止「`source_count` vs glob 總數」比大小**——後者會因兩邊同時反向偏差而**假陰性**（實例：`synthesis-claude-md` 5→5 判成 OK，實際漏抓一篇來源又多抓一篇新條目，掩蓋了一篇嚴重過時的精粹）
- **第 4 項新增三道掃描前置**：① 先剝除圍籬與行內 code 再抽 `[[...]]`（2026-09-01 因此把 8 個懸空報成 8 個，實際 2 個）；② 解析須支援路徑寫法與外部專案 vault（首次掃描誤報 133 個，實際 8 個）；③ **與前一份報告對照，不重複列出已判定為誤報的項目**（2026-09-01 把 08-12 已排除的 6 項重報為「🔴 真 bug」）
- **執行流程新增第 1 步：先讀前一份 `outputs/health-check-*.md`**；第 1 項矛盾偵測**必須逐項覆核前次矛盾是否已修**，未修者標「連續 N 次指認」——2026-09-01 只找到 6 個既有矛盾中的 1 個，其餘 5 個仍未修卻未被列出

### v1.7.0（2026-08-13）
- 第 6 項 A 的 `.md` 判斷改為**只看 frontmatter**（廢止 v1.5.0 雙條件），對齊 `rules/inbox-detection-protocol.md` 分流制
- **幽靈標記偵測改名為「待人工確認」並加註信心上限**：2026-08-13 全庫盤點實測，確定已處理的素材其 source URL 自動命中率僅三到四成（多篇合併、未達門檻不建條目、URL 不一致所致）。明訂「找不到對應條目」不可自動翻回 inbox

### v1.6.1（2026-08-04）
- **修正第 6 項 B 非 .md 掃描指令 bug**：`find raw/ -type f ! -name "*.md" ! -name "*.processed"` 只排除標記檔本身，未過濾「已有配對 .processed」的原始檔，導致本次健檢誤報全部 24 個非 .md 素材為積壓（實際 0 篇未處理）。補上 pipe 後的存在性檢查，對齊 `rules/inbox-detection-protocol.md` 的正確版本

### v1.6.0（2026-07-24）
- **新增第 7 項檢查：精粹過時偵測（Stale Synthesis Detection）**——比對 `wiki/synthesis/*.md` frontmatter 的 `source_count` 與該主題現況條目數，`actual > source_count` 即列入報告提醒重跑 `knowledge-synthesizer`
- 配套：全部既有 synthesis 條目已補上 `source_count` + `synthesis_snapshot_date` 兩個機器可讀戳記欄位
- 設計原則：只「提醒」不「自動重跑」（避免覆蓋人工微調）；主題比對用 glob 寧可過報，由人工確認
- 執行流程由六項改七項；對應 5A+ 的 ADJUST 階段（同主題已有精粹但來源已長）

### v1.5.0（2026-07-08）
- **制度統一（批次 C 健檢 C-1 修正）**：第 6 項 A 的 `.md` 判斷改**雙條件**（frontmatter inbox 且無 `.processed` 標記）——對齊 CLAUDE.md「raw/ .md 一律旁車標記」現行規則，修正只看 frontmatter 會把已處理 56 篇誤報為積壓的問題
- 幽靈標記偵測擴及 `.md`（原僅非 md 檔）

### v1.4.0（2026-06-22）
- 第 6 項未處理素材檢查改用 `.processed` 標記檔（取代舊版「只靠 wiki source cross-reference」）
- 新增「幽靈標記偵測」：標記存在但無對應 wiki/research 條目 → 標記異常，需人工確認
- 改寫「raw/ 唯讀」說明：`.processed` 為旁車元資料，不違反唯讀原則（呼應 2026-06 確立的慣例）

### v1.3.0（2026-05-14）
- 輸出格式新增「5A+ 階段評估」區塊（當前階段 + 理由 + 下一步建議）
- 執行流程加入第 7 步：5A+ 階段評估
- 新增 5A+ 六階段判斷邏輯表（含判斷條件與核心建議）

### v1.2.0（2026-05-14）
- 第 6 項未處理素材檢查支援 `.pdf`（檔名比對 source_format: pdf 條目）
- 執行流程步驟 2 加入 `.pdf` 掃描
- 整體評分分開顯示 .md / .pdf 數量

### v1.1.0（2026-05-14）
- 新增第 6 項檢查：未處理素材（Unprocessed Raw）
- W3 判斷邏輯改為 wiki/raw cross-reference（比對 source URL），不再依賴 raw/ 的 status 欄位
- 執行流程加入 raw/ 掃描步驟
- 整體評分加入 raw 素材處理比例

### v1.0.0（2026-05-13）
- 初始版本
- 五項檢查：矛盾偵測 / 缺乏來源 / 知識缺口 / 連結品質 / 過時內容
- 健康指數評分
- 自動存入 outputs/health-check-YYYY-MM-DD.md
