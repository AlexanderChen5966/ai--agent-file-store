---
name: requirements
metadata:
  version: 1.2.0
description: 將模糊需求轉換為標準化任務文件，存入 docs/shared/。自動分析影響範圍、拆解實作任務、確認風險清單，產出可直接交給 AI agent 實作的任務文件。觸發時機：/requirements、討論作法、需求分析、寫任務文件、規劃功能、我想要新增/修改功能時。只要使用者描述想做的功能變更，就應主動使用此 skill。
---

# Requirements Analysis

將使用者的需求描述轉換為標準化任務文件，存入 `docs/shared/`。

## 工作流程

### Step 1：理解需求

先確認以下資訊（若使用者描述不夠完整，逐一詢問）：

1. **功能描述**：要做什麼？改什麼行為？
2. **目標頁面/模組**：影響哪個頁面？路由是什麼？
3. **觸發條件**：什麼情況下觸發這個行為？
4. **預期結果**：使用者操作後應該看到什麼？
5. **邊界條件**：例外情況如何處理？（空值、錯誤狀態等）

若需求已夠清楚，直接進入 Step 2，不要不必要地多問。

### Step 2：探索相關程式碼

根據需求描述的頁面/功能，探索現有實作：

```bash
# 找到目標頁面
ls lib/page/[模組]/

# 搜尋相關關鍵字
grep -r "關鍵字" lib/page/[模組]/ --include="*.dart" -l
```

重點理解：
- 目前實作方式（State、API、Widget 結構）
- 需要修改的具體檔案與函式
- 現有類似功能的作法（作為新實作的參考）

### Step 3：風險評估

依照 CLAUDE.md 的風險清單，逐一確認：

| 風險項目 | 是否影響 |
|---------|---------|
| OAuth2 / TaskManager | 是否涉及認證流程？ |
| API / build_runner | 是否新增或修改 API 端點？ |
| 路由配置 | 是否新增頁面或修改路由？ |
| 狀態管理結構 | 是否改動 StateNotifier？ |
| DataCell 游標規則 | 是否修改 DataCell.onTap？ |
| DataTable 排序 | 是否修改 sortColumnIndex？ |
| 欄位寬度配置 | 是否修改 fixedWidth / ColumnSize？ |

### Step 4：確認 docs/shared/ 存在

```bash
ls docs/shared/ 2>/dev/null || echo "不存在"
```

若目錄不存在，建立它：

```bash
mkdir -p docs/shared
```

並建立 `docs/shared/readme.md`（使用 [references/readme-template.md](references/readme-template.md) 的格式）。

### Step 5：檢查同名文件是否已存在

根據 Step 1-3 的分析結果決定檔名後，先檢查是否已有同名文件：

```bash
ls docs/shared/[預定檔名].md 2>/dev/null
```

**若文件已存在，讀取其狀態欄位：**

| 現有狀態 | 行為 |
|---------|------|
| ⏳ 待實作 | 直接覆寫更新，狀態維持「待實作」 |
| 🔄 進行中 | 直接覆寫更新，狀態維持「進行中」 |
| ✅ 已完成 | **⚠️ 必須先提示使用者確認**（見下方） |

**已完成文件的處理流程：**

```
偵測到 docs/shared/[檔名].md 狀態為「✅ 已完成」
    ↓
提示使用者：
  「⚠️ 此任務文件已標記為 ✅ 已完成。
   重新修改將把狀態改為 🔄 進行中。
   是否繼續？」
    ↓
使用者拒絕 → 停止，不修改任何檔案
使用者確認 → 繼續 Step 6，狀態設為「🔄 進行中」
```

**若文件不存在：** 直接進入 Step 6（新建文件）。

### Step 6：產出任務文件

使用 [references/task-doc-template.md](references/task-doc-template.md) 為模板，依照探索結果填寫所有欄位。

**狀態設定規則：**
- 新建文件 → `**⏳ 待實作**`
- 覆寫「待實作」文件 → `**⏳ 待實作**`
- 覆寫「進行中」文件 → `**🔄 進行中**`
- 重新開啟「已完成」文件（經使用者確認）→ `**🔄 進行中**`

**檔案命名規則：**
- 全小寫，以底線連接
- 描述功能，不超過 5 個詞
- 範例：`order_fuel_type_ellipsis_tooltip.md`、`invoice_status_update_task.md`

**文件頂部 metadata header 格式（必須遵守，與 sort_data_tables.md 等既有文件統一）：**

```markdown
**優先級：** High / Medium / Low
**建立日期：** YYYY-MM-DD
**完成日期：** —
**分支編號：** SSGS-XXXXX（若已知）
**狀態：** ⏳ 待實作
**影響路徑：** `[主要影響的檔案或模組路徑]`
```

- 狀態與 metadata 集中在頂部 header block，**不在文件底部重複**
- `**完成日期：**` 新建時填 `—`，由 `/doc-update` 填入實際日期
- `**分支編號：**` 若尚未建立分支可省略該行

**寫作原則：**
- 實作任務要具體到「貼近可執行的程式碼」，包含修改前後的 code snippet
- 步驟要有手動驗證清單（`[ ]` checkboxes）
- 若需要 build_runner，在 metadata header 的影響路徑後補充說明

### Step 7：更新 docs/shared/readme.md

**新建文件時：** 在狀態索引表格新增一行：

```markdown
| [filename.md](./filename.md) | 功能一句話說明 | ⏳ 待實作 |
```

**重新開啟已完成文件時：** 修改既有行的狀態：

```markdown
| [filename.md](./filename.md) | 功能一句話說明 | 🔄 進行中 |
```

同時將「實作記錄」表格中對應的已完成記錄移回「任務文件狀態索引」表格。

若 readme.md 不存在，根據 [references/readme-template.md](references/readme-template.md) 建立。

### Step 8：更新 CHANGELOG.md（僅限重新開啟時）

**僅在「已完成 → 進行中」狀態變更時執行此步驟。新建文件時跳過。**

在 `[Unreleased]` 區塊的 `Changed` 分類下新增：

```markdown
### Changed
- 重新開啟任務文件 `[檔名]`：[簡述需求變更原因]
```

若 CHANGELOG.md 不存在或無 `[Unreleased]` 區塊，跳過此步驟。

---

## 注意事項

- **先探索再寫文件**，不要根據假設寫任務，確認過目前程式碼後才描述修改方式
- **任務文件要夠具體**，讓另一個 AI agent 讀完後不需要再問問題就能實作
- **不要過度設計**，只描述必要的最小變更
- **技術術語保留英文**（Flutter、Riverpod、DataCell 等），說明文字用繁體中文
