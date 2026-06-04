---
name: knowledge-elevation
description: |
  知識昇華 Skill：三層遞進式知識提煉，適用於任何個人知識庫場景。
  從已整理的精粹條目（wiki/topic-synthesis/）出發，執行三層昇華：
  （1）自動模式偵測——同概念跨來源出現時自動合成；
  （2）E 層加深——將 CAVE 精粹的 E 層結構化為一句話洞察 + 信心等級 + 實際意義；
  （3）跨主題連結——多個精粹條目 → 更高層概念框架（wiki/concepts/）。

  Trigger: knowledge-elevation, 知識昇華, 精粹加深, 跨主題合成, meta-synthesis,
           elevate, deep essence, 概念框架, 知識提煉
metadata:
  version: 1.1.0
  target: 個人知識庫使用者（PKM）
  prerequisite: knowledge-synthesizer（需有 wiki/topic-synthesis/ 條目）
---

# knowledge-elevation

把「精粹條目」再往上提煉一層：從主題內的共識與洞察，走向跨主題的概念框架。
三層各自獨立，可單獨觸發，也可依序全跑。

## 使用方式

```
# 第一層：確認自動合成狀況
請列出 wiki/concepts/ 最近新增的合成頁面，摘要核心洞察

# 第二層：E 層加深（指定主題）
對 wiki/topic-synthesis/claude-skills.md 執行 E 層加深

# 第三層：跨主題連結（指定領域）
讀取 wiki/topic-synthesis/ 中與「AI 工作流」相關的所有精粹，執行 meta-synthesis

# 全部三層依序執行
對「AI 工作流」主題執行完整知識昇華（三層）
```

---

## 前置條件

執行本 Skill 前，確認：
- `wiki/topic-synthesis/` 已有目標主題的精粹條目（由 `knowledge-synthesizer` 產出）
- 第三層需要同領域 ≥ 3 個精粹條目

---

## 第一層：自動模式偵測（Synthesis Hook）

> 目標：讓 vault 自己發現跨來源的重複概念，不需人工指定。

### 觸發邏輯

`obsidian-second-brain` 的 Synthesis Hook 在每次寫入 vault 時自動執行：
**同一概念在 3 個以上不相關來源出現 → 自動在 `wiki/concepts/` 建立合成頁面。**

無需手動觸發。建議定期用以下指令確認產出：

```
請列出 wiki/concepts/ 最近 30 天新增的合成頁面，
每頁用一句話說明核心洞察，並列出觸發來源
```

### 手動補充觸發

若自動偵測未涵蓋某個你認為重要的跨來源概念：

```
我注意到「軟編排」在多篇 wiki 條目中多次出現，
請掃描相關條目，在 wiki/concepts/soft-orchestration.md 建立合成頁面
```

### 輸出格式

```markdown
---
title: [概念名稱]
date: YYYY-MM-DD
tags: [相關 tag]
type: concept-synthesis
sources: [觸發來源列表]
status: auto-generated
---

## 概念定義
[此概念的核心意涵，2-3 句話]

## 出現脈絡
| 來源 | 使用方式 | 位置 |
|------|---------|------|
| [[來源A]] | ... | [章節 / 段落] |
| [[來源B]] | ... | [章節 / 段落] |
| [[來源C]] | ... | [章節 / 段落] |

## 共同含意
[三個來源都在說什麼？]

## 分歧點
[各來源對此概念的不同使用或詮釋]

## 對你的意義
[這個概念對你的工作 / 知識體系有什麼潛在應用？]
```

---

## 第二層：CAVE E 層加深（Deep Essence）

> 目標：把 knowledge-synthesizer 產出的 E（精華）層從自由格式強化為結構化洞察。

### 執行步驟

```
Step 1  讀取 wiki/topic-synthesis/[主題].md
Step 2  找到現有的 E（精華）層
Step 3  依下方格式重新產出結構化 E 層
Step 4  更新原檔，原 E 層內容移至 E-original 保存
```

### 結構化 E 層格式（強制輸出）

```markdown
## E（精華—Deep Essence）

**核心洞察（一句話）**：
[去掉所有背景、脈絡、例外後，這個主題最重要的一個發現是什麼？
 必須是完整論點，不是主題標題，字數上限 40 字]

**信心等級**：stated ｜ high ｜ medium ｜ speculation
> - stated：來源文字明確陳述
> - high：多個獨立來源一致支持
> - medium：有支持但亦有反例
> - speculation：邏輯推演，尚無直接依據

**依據**：
- [[來源A]]：[支撐這個洞察的具體內容]
- [[來源B]]：[支撐這個洞察的具體內容]

**對你的實際意義**：
[為什麼這個洞察對你目前的工作 / 學習 / 專案特別重要？具體說明，不要泛泛而談]

**最大反例**：
[什麼條件下這個洞察會不成立？這是否影響你使用這個洞察的方式？]

---
*E 層加深日期：YYYY-MM-DD*
*原 E 層保存於 E-original*
```

### E-original 保存格式

```markdown
## E-original（精華—原始版本，保存於 YYYY-MM-DD）
[原始 E 層內容原文]
```

---

## 第三層：跨主題連結（Meta-Synthesis）

> 目標：讀取多個主題精粹，找出超越個別主題的上層概念框架。

### 觸發條件

同一知識領域的 `wiki/topic-synthesis/` 條目累積 ≥ 3 個。

### 執行步驟

```
Step 1  列出 wiki/topic-synthesis/ 中與目標領域相關的條目
Step 2  讀取每個條目的 C（共識）、A（爭論）、E（精華）層
Step 3  識別跨主題的共同概念、核心張力、意外連結、應用缺口
Step 4  產出 wiki/concepts/meta-[領域].md
Step 5  在每個來源條目末尾加入 [[meta-領域]] 的 wikilink
```

### Meta-Synthesis 輸出格式

```markdown
---
title: [領域] 跨主題概念框架
date: YYYY-MM-DD
tags: [領域 tag, type/concept]
type: meta-synthesis
sources:
  - [[topic-synthesis/主題A]]
  - [[topic-synthesis/主題B]]
  - [[topic-synthesis/主題C]]
status: processed
---

## 整合來源
[列出整合的精粹條目，各一句摘要]

## 共同前提
[所有主題都隱含的假設——哪些東西被視為理所當然、從未被質疑？]

## 核心張力
[主題之間最重要的對立或矛盾是什麼？這個張力有沒有被解決？]

## 上層概念
[整合後浮現的更高層框架是什麼？
 能不能用一個概念統合這些主題？]

## 應用缺口
[只有把這幾個主題放在一起看，才能看到的缺口是什麼？
 這是單看任何一個主題都看不到的]

## 下一步行動
- [ ] [具體行動一]
- [ ] [具體行動二]
- [ ] [具體行動三]
```

---

## 完整三層執行流程（依序全跑）

```
前置：確認 wiki/topic-synthesis/[主題].md 已存在

第一層  確認 wiki/concepts/ 有無自動生成的相關合成頁面
        → 若無，手動補充觸發

第二層  對目標精粹條目執行 E 層加深
        → 更新 wiki/topic-synthesis/[主題].md

第三層  若同領域有 ≥ 3 個精粹條目
        → 執行 meta-synthesis
        → 產出 wiki/concepts/meta-[領域].md
        → 回頭在各來源條目加 wikilink

收尾    更新 wiki/INDEX.md
        在 wiki/concepts/ 段落登錄新增條目
```

---

## 三層對照表

| 層次 | 觸發條件 | 觸發方式 | 輸入 | 產出位置 |
|------|---------|---------|------|---------|
| 自動模式偵測 | 同概念在 3+ 來源出現 | 自動（obsidian-second-brain）| vault 全域 | `wiki/concepts/` |
| E 層加深 | 精粹條目 E 層需強化 | 手動指定條目 | `wiki/topic-synthesis/` | 更新原條目 |
| 跨主題連結 | 同領域 ≥ 3 個精粹 | 手動指定領域 | `wiki/topic-synthesis/*` | `wiki/concepts/meta-` |

---

## 與相關 Skill 的分工

| Skill | 處理層次 | 輸入 | 輸出 |
|-------|---------|------|------|
| `knowledge-organizer` | 單篇整理 | `raw/` 素材 | `wiki/` 條目 |
| `knowledge-synthesizer` | 主題精粹 | 多篇 wiki 條目 | `wiki/topic-synthesis/`（CAVE）|
| `scientific-brainstorming` | 探索延伸 | topic-synthesis | `ideas/` 洞察與假設 |
| **`knowledge-elevation`** | **概念昇華** | **topic-synthesis** | **`wiki/concepts/`** |

知識流向：
```
raw/ → wiki/ → topic-synthesis/ → concepts/（meta）
                               ↘ ideas/（brainstorm）
```

---

## 使用注意事項

1. **信心等級誠實填寫**：`speculation` 不代表沒價值，代表「這個洞察還需要驗證才能依賴」
2. **Meta-synthesis 的邊界**：只整合同一知識脈絡的主題，跨越太遠的領域強行整合反而產生偽洞察
3. **E-original 保存**：洞察會隨時間改變，保存原始版本供回溯比較
4. **不強制頁碼**：引用來源時標注章節或段落即可，不需要嚴格的頁碼格式（學術場景例外）

---

## 參考資源

- `references/` — 本 Skill 的補充參考資料（待建立）

---

## Changelog

### v1.1.0（2026-05-18）
- 通用化為個人 PKM 版本（移除學術專用措辭）
- E 層「對你研究的意義」→「對你的實際意義」
- Meta-synthesis「研究空白」→「應用缺口」
- Meta-synthesis「研究設計的啟示」→「下一步行動」
- 第一層範例改用 PKM 場景（非學術）
- 引用來源不強制頁碼，改為「章節 / 段落」
- 移除「學術使用注意事項」，改為通用「使用注意事項」

### v1.0.0（2026-05-18）
- 初始版本（學術版）
- 三層架構：自動模式偵測 / E 層加深 / 跨主題連結
