---
name: wiki-health-check
description: |
  Monthly wiki health check skill. Scans the entire wiki for quality issues:
  contradictions between notes, unsupported claims, missing cross-links,
  outdated content, and knowledge gaps. Based on Karpathy's step 5 method.

  Trigger: wiki-health-check, 健康檢查, health check, wiki品質, 知識庫健檢, monthly review
metadata:
  version: 1.3.0
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

**判斷邏輯（cross-reference 方式）：**
1. 掃描 `raw/` 所有 `.md` 和 `.pdf` 檔，提取每篇的 `source:` URL（PDF 無 frontmatter 則 source 視為空白）
2. 掃描 `wiki/` 所有 `.md` 檔，收集所有 `source:` URL 成清單
3. 對每個 raw 檔：若其 `source:` URL **已出現在** wiki/ 某條目 → 視為已處理，跳過
4. `.pdf` 額外判斷：若 wiki/ 存在 `source_format: pdf` 且檔名相符的條目 → 視為已處理
5. 若 raw 檔的 `source:` URL **未出現在任何** wiki 條目，且建立超過 30 天 → 標記為未處理

> **為什麼不看 raw/ 的 status 欄位：** raw/ 是唯讀輸入區，AI 不應修改原始素材；「是否已處理」的真實狀態應由 wiki/ 是否存在對應條目來判斷。

**特殊情況：**
- raw `.md` 的 `source:` 為空 → 無法比對，單獨列出，手動確認
- raw `.pdf` → 無 frontmatter 屬正常，改用檔名比對 wiki/ 的 `source_format: pdf` 條目
- 多個 raw 檔對應同一 wiki 條目（合併處理）→ 視為已處理，不報告

輸出格式：
```
📥 未處理素材：raw/檔案名稱.md (.pdf)
來源：（URL 或空白）
建立：YYYY-MM-DD
建議：執行 knowledge-organizer 處理此素材
```

---

## 執行流程

1. 讀取所有 `wiki/` 目錄的 `.md` 檔案，收集 source URL 清單
2. 讀取所有 `raw/` 目錄的 `.md` 和 `.pdf` 檔案，提取 source URL 與建立日期
3. 依序執行六項檢查（第 6 項需 wiki/raw cross-reference）
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
