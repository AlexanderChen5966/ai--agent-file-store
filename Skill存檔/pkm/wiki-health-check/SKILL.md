---
name: wiki-health-check
description: |
  Monthly wiki health check skill. Scans the entire wiki for quality issues:
  contradictions between notes, unsupported claims, missing cross-links,
  outdated content, and knowledge gaps. Based on Karpathy's step 5 method.

  Trigger: wiki-health-check, 健康檢查, health check, wiki品質, 知識庫健檢, monthly review
metadata:
  version: 1.6.0
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

**判斷邏輯（標記檔 + cross-reference 雙軌）：**

A. **`.md` 素材**（v1.5.0 起**雙條件**）：frontmatter `status:` 為 `inbox` / `"inbox"` / 缺欄位，**且** raw/ 中**不存在**同名 `.processed` 標記檔 → 才視為未處理
   掃描指令：`for f in raw/*.md; do grep -q 'status:.*inbox' "$f" 2>/dev/null && [ ! -f "${f}.processed" ] && echo "$f"; done`
   ⚠️ 不可只看 frontmatter——raw/ 一律唯讀，已處理的 .md 其 frontmatter 仍會停留在 inbox，僅靠旁車標記辨識

B. **非 `.md` 素材**（.pdf / 圖片 / .srt / .csv 等）：raw/ 中**不存在**同名 `.processed` 標記檔 → 未處理
   掃描指令：`find raw/ -type f ! -name "*.md" ! -name "*.processed"`

C. **幽靈標記偵測（health-check 專屬，比 pipeline 多一層）**：
   對每個有 `.processed` 標記的檔案（v1.5.0 起**含 .md 與非 md**），反查 wiki/ 或 research/ 是否真有對應條目
   （用檔名前綴或 `source:` 比對）。若**標記存在但找不到對應條目** → 標記為「⚠️ 幽靈標記」，
   代表當初標記了卻沒真的建立條目，需人工確認。

> **關於 raw/ 唯讀原則：** `.processed` 是旁車標記檔（新增元資料），不修改原始素材內容，
> 不違反「NEVER modify raw/」。這是 2026-06 後確立的慣例（取代舊版「只靠 wiki cross-reference」判斷）。

**特殊情況：**
- `.processed` 標記（含 .md 與非 md）存在但建立超過 30 天仍無對應條目 → 列入幽靈標記
- 多個 raw 檔對應同一 wiki 條目（合併處理）→ 各自有 `.processed` 標記即視為已處理

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
1. 讀取 frontmatter 的 `source_count`
2. 依主題比對規則（見下表）數出**目前** wiki/ 中該主題實際條目數 `actual`
3. 若 `actual > source_count` → 標記為「精粹過時」，列出新增的候選條目
4. 若精粹**缺** `source_count` 欄位 → 標記為「⚠️ 缺戳記，無法偵測」，建議補上

**主題比對規則**：以精粹的「來源條目」段落所列的 `[[...]]` 為基準集合，
再用該主題的檔名前綴 glob 掃出現況（例：`synthesis-multi-agent` → `wiki/multi-agent*.md`
＋ `wiki/*multi-agent*.md`；`synthesis-claude-md` → `wiki/claude-md*.md`）。
glob 判準可能誤抓，故本項為「提醒」而非「自動重跑」——寧可過報，由人工確認後再決定是否重跑。

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
2. 讀取 `raw/`：`.md` 與非 md 檔**一律**比對 `.processed` 旁車標記（.md 另加 frontmatter inbox 雙條件）
3. 依序執行七項檢查（第 6 項：未處理 = 缺標記；額外做幽靈標記偵測。第 7 項：比對 synthesis 的 source_count 與現況）
4. 彙整結果，產出健康檢查報告
5. 存入 `outputs/health-check-YYYY-MM-DD.md`
6. 提供優先處理清單（最需要修復的 3-5 個問題）
7. 執行 **5A+ 階段評估**（見下方判斷邏輯）

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
