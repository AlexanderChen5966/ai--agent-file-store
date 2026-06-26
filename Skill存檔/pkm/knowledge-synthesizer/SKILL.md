---
name: knowledge-synthesizer
description: |
  Knowledge synthesis skill. Takes multiple wiki entries of the same topic/type
  and distills them into a single high-density synthesis entry using the CAVE
  framework (Consensus / Angles / Voids / Essence).

  Trigger: knowledge-synthesizer, 精粹, synthesize, distill, 知識精粹, 合併觀點, 跨篇整合
metadata:
  version: 1.0.0
---

# knowledge-synthesizer

把同類型的多篇 wiki 條目提煉成一篇「精粹條目」。
一篇精粹條目 ≠ 摘要的摘要——它是去掉重複、保留密度、找出張力的整合知識。

## 使用方式

```
knowledge-synthesizer [主題 or 標籤 or 檔案清單]

範例：
knowledge-synthesizer PKM 方法論
knowledge-synthesizer ai/agent
knowledge-synthesizer wiki/harness-engineering.md wiki/agents-md-guide.md wiki/zerospec.md
```

輸入可以是：
- **主題關鍵字**：自動從 wiki/ 找相關條目（比對標題與 tags）
- **標籤**：例如 `ai/claude`，找所有該 tag 的 wiki 條目
- **明確檔案清單**：直接指定要整合的條目

---

## 核心框架：CAVE

四個維度決定精粹條目的結構：

### C — Consensus（共識核心）
> 多篇都支持的觀點——這是最可信、最有把握的部分

判斷標準：
- 同一論點出現在 2 篇以上
- 不同作者/來源得出相同結論
- 有具體數據或案例支撐的共同主張

輸出格式：
```
## C（共識核心）
> 出現於 N 篇來源

- [共識點 1]（來自 [[source-a]]、[[source-b]]）
- [共識點 2]（來自 [[source-a]]、[[source-c]]）
```

---

### A — Angles（獨特視角）
> 各篇的特殊貢獻——這是精粹條目的「附加價值」，摘要讀不到的部分

判斷標準：
- 只有 1 篇提到，但觀點獨特或有實作價值
- 提供不同切入角度（技術 vs 方法論 vs 案例）
- 互補而非重複

輸出格式：
```
## A（獨特視角）

| 來源 | 獨特貢獻 |
|------|---------|
| [[source-a]] | [這篇才有的洞察] |
| [[source-b]] | [這篇才有的洞察] |
```

---

### V — Voids（知識缺口）
> 所有來源都沒講清楚的地方——這是下一步研究的方向

判斷標準：
- 多篇都提到某概念但沒有深入
- 各篇互相矛盾且無法判斷哪個正確
- 理論存在但缺乏實作驗證

輸出格式：
```
## V（知識缺口）
- ❓ [待釐清的問題或缺失的知識]
- ⚠️ [各篇有分歧、需要進一步確認的地方]
```

---

### E — Essence（精粹論點）
> 整合所有來源後，最核心的一句話——比任何單篇的 T 層更濃縮

判斷標準：
- 必須是跨來源的整合觀點，不是複製某篇的論點
- 讀完所有來源後才能說出的話
- 如果只能記住一件事，是什麼？

輸出格式：
```
## E（精粹論點）
[跨越所有來源後，最核心的一句整合觀點]
```

---

## 完整執行流程

### 第一步：收集
1. 根據輸入（關鍵字/標籤/檔案清單）找出相關 wiki 條目
2. 列出候選條目清單，確認範圍（建議 3-10 篇，太少無意義，太多失焦）
3. 如有疑義，先列出清單讓用戶確認再繼續

### 第二步：萃取
對每一篇候選條目，提取：
- **T 層**：核心論點（這篇說什麼）
- **C 層**：關鍵行動（這篇要做什麼）
- **獨特點**：這篇有但其他篇沒有的觀點

### 第三步：比對
- 找**共識**：相同論點在幾篇出現？
- 找**差異**：哪些觀點只有一篇提到？
- 找**矛盾**：哪些論點互相衝突？
- 找**缺口**：什麼是所有篇都沒說清楚的？

### 第四步：合成
用 CAVE 框架組裝精粹條目，填入：
- E 層（精粹論點）— 最後才寫，必須是整合後的新論點
- C 層（共識核心）
- A 層（獨特視角）
- V 層（知識缺口）

### 第五步：輸出
1. 建立 `wiki/synthesis/synthesis-[主題].md`
2. 更新 `wiki/INDEX.md`，加入新的精粹條目

---

## 輸出模板

```yaml
---
title: [主題] 知識精粹
date: YYYY-MM-DD
tags: [繼承來源條目的 tags]
type: synthesis
status: processed
sources: [來源條目數量，例：5 篇]
asset_value: [分數]
---

[2-3 句話說明：這份精粹整合了哪些來源、解決什麼問題]

## E（精粹論點）
[跨越所有來源後，最核心的一句整合觀點]

## C（共識核心）
> 出現於 N/N 篇來源

- [共識點]（[[source-a]]、[[source-b]]）

## A（獨特視角）

| 來源 | 獨特貢獻 |
|------|---------|
| [[source-a]] | |
| [[source-b]] | |

## V（知識缺口）
- ❓
- ⚠️

## 整合行動清單
- [ ] [從所有來源的 C 層整合出最重要的行動]
- [ ] 

## 來源條目
- [[source-a]] — [一句話摘要]
- [[source-b]] — [一句話摘要]
```

---

## 精粹 vs 摘要的差異

| | 摘要 | 精粹（本 Skill） |
|--|------|----------------|
| 輸入 | 1 篇 | N 篇同類型 |
| 目標 | 濃縮單篇內容 | 找出跨篇洞察 |
| 共識 | 不判斷 | 明確標示 |
| 矛盾 | 不處理 | 明確標示 |
| 新論點 | 不產生 | 必須產生（E 層）|
| 適合時機 | 剛讀完一篇 | 同一主題累積 3 篇以上 |

---

## 參考資源

- `references/cave-template.md` — 空白 CAVE 模板
- [[knowledge-organizer]] — 單篇整理（本 Skill 的上游）
- [[wiki-health-check]] — 可發現適合精粹的主題群

---

## Changelog

### v1.0.0（2026-05-14）
- 初始版本
- CAVE 四層框架：Consensus / Angles / Voids / Essence
- 五步驟執行流程（收集 → 萃取 → 比對 → 合成 → 輸出）
- 輸出格式：`wiki/synthesis/synthesis-[主題].md`，type: synthesis
