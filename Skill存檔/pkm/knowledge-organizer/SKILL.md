---
name: knowledge-organizer
description: |
  Knowledge organization skill using TBRC framework.
  Processes raw materials from vault's raw/ folder: evaluates asset value,
  structures notes into T/B/R/C layers, assigns tags, routes to correct folder,
  builds wikilinks, and updates INDEX.md.

  Trigger: knowledge-organizer, 整理筆記, 處理raw, process raw, organize notes, 知識整理
metadata:
  version: 1.1.0
---

# knowledge-organizer

把「整理一篇筆記」的判斷邏輯封裝成可重複執行的 AI 指令。
每次處理 `raw/` 中的新素材，都用同樣的四層判斷：T → B → R → C。

## 使用方式

```
請用 knowledge-organizer Skill 處理 raw/ 中的所有新素材
請用 knowledge-organizer Skill 處理這篇：raw/xxx.md
請用 knowledge-organizer Skill 處理這篇：raw/xxx.pdf
```

---

## 核心邏輯：TBRC 四層判斷

### T — Thesis（核心論點）
> 這篇文章/筆記最重要的一句話是什麼？

判斷標準：
- 去掉所有例子、背景、說明後，剩下的核心主張
- 必須是一個完整的論點，不是主題標題
- 長度限制：1-2 句話

輸出格式：
```
## T（核心論點）
[一句話總結核心主張]
```

---

### B — Background（適用場景與限制）
> 這個知識在什麼情況下有用？什麼情況下不適用？

判斷標準：
- 適用：明確的使用情境（角色、問題類型、前提條件）
- 不適用：已知的例外、邊界條件、反例

輸出格式：
```
## B（適用場景）
**適用：** [具體情境]
**不適用 / 注意：** [例外或限制]
```

---

### R — Recipe（具體操作步驟）
> 如果要執行這個知識，步驟是什麼？

判斷標準：
- 可操作的具體動作，不是抽象原則
- 步驟要有順序性
- 每步驟一個動作

輸出格式：
```
## R（操作步驟）
1. [第一步]
2. [第二步]
3. [第三步]
```

---

### C — Checklist（關鍵行動）
> 下次遇到這個情境，第一件要確認的事是什麼？

判斷標準：
- 最容易忘記或出錯的地方
- 可以是 check item 或 warning
- 3 項以內

輸出格式：
```
## C（關鍵行動）
- [ ] [最重要的確認事項]
- [ ] [次要確認]
```

---

## 完整執行流程

處理每一篇 `raw/` 素材時，依序執行：

1. **讀取**原始內容：
   - `.md`：直接讀取全文
   - `.pdf`（≤ 10 頁）：讀取全文
   - `.pdf`（> 10 頁）：讀取前 5 頁 + 後 2 頁，在輸出的「原始摘要」區塊標注「PDF 節錄，建議人工補充完整內容」
2. **判斷資產化價值**（用下方公式，< 30 分可跳過詳細處理）
3. **生成 TBRC 結構**
4. **指定 tag**（參考 `references/tag-taxonomy.md`）
5. **判斷歸屬**：ideas / research / projects / wiki
6. **建立整理後的筆記**（含完整 frontmatter + TBRC）
7. **建立 wikilink** 到相關現有筆記
8. **更新** `wiki/INDEX.md`
9. **標記已處理**：若原始素材為 `raw/` 中的 `.md` 檔案，用 Edit 工具更新其 frontmatter：
   - 若已有 `status:` 欄位（無論值是 `inbox`、`"inbox"` 或其他）→ 整行替換為 `status: processed`
   - 若無 `status:` 欄位 → 在 frontmatter 結尾 `---` 前插入 `status: processed`
   **注意**：一律寫入不帶引號的格式 `status: processed`，不要寫成 `status: "processed"`
   （防止下次重複處理）

---

## 資產化價值公式

```
資產化價值 = 頻率 × 耗時 × 複雜度

頻率：這個知識會重複用到嗎？（1-5）
耗時：每次用到需要多久重新想？（1-5）
複雜度：需要專業判斷嗎？（1-5）

≥ 50 分 → 完整 TBRC 處理，歸入 wiki/
20-49 分 → 簡單摘要，歸入 research/ 或 ideas/
< 20 分  → 只存 frontmatter，歸入 archive/
```

---

## 輸出模板

```yaml
---
title: [標題]
date: [YYYY-MM-DD]
tags: [tag1, tag2]
source: [來源，PDF 填 local-pdf]
source_format: pdf          # 僅 PDF 來源時加此欄位
type: article | note | idea | reference
status: processed
asset_value: [分數]
---

## T（核心論點）


## B（適用場景）
**適用：**
**不適用 / 注意：**

## R（操作步驟）
1.
2.
3.

## C（關鍵行動）
- [ ]
- [ ]

## 原始摘要


## 相關連結
- [[相關筆記]]
```

---

## 參考資源

- `references/tbrc-template.md` — 空白 TBRC 模板
- `references/tag-taxonomy.md` — 標籤分類表
- `references/examples/` — 輸入輸出範例

---

## Changelog

### v1.3.0（2026-05-28）
- 步驟 9 修正：同時處理「有 status 欄位」與「無 status 欄位」兩種情況（Obsidian Web Clipper 下載的文章預設無 status）

### v1.2.0（2026-05-28）
- 步驟 9：處理完 raw/ .md 檔案後，將其 status 從 inbox 更新為 processed，防止重複處理

### v1.1.0（2026-05-14）
- 支援 `.pdf` 輸入（自動判斷頁數，> 10 頁節錄首尾）
- 輸出模板新增 `source_format: pdf` 欄位（僅 PDF 來源時加入）
- 大型 PDF 在「原始摘要」區塊標注人工補充提示

### v1.0.0（2026-05-13）
- 初始版本
- TBRC 四層判斷邏輯
- 資產化價值公式（頻率 × 耗時 × 複雜度）
- 完整執行流程（8 步驟）
- 輸出模板與參考資源
