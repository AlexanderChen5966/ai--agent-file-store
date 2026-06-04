# 小型專案範例：個人部落格 API

這是一個使用 Context Sharing 的小型專案範例。

## 專案背景

**專案名稱：** 個人部落格 API  
**技術棧：** Node.js, Express, SQLite  
**團隊：** 個人開發  
**時程：** 2 週

## 文件演進過程

### Day 1: 初始化專案

#### 執行初始化

```bash
$ python3 scripts/init-project.py \
    --project-name "個人部落格 API" \
    --tech-stack "Node.js, Express, SQLite"

✓ 已創建: CLAUDE.md
✓ 已創建: TASKS.md
✓ 已創建: ARCHITECTURE.md
✓ 已創建: DECISIONS.md
```

#### CLAUDE.md 內容

```markdown
# CLAUDE.md

## 專案資訊
**專案名稱：** 個人部落格 API
**技術棧：** Node.js, Express, SQLite
**開發階段：** MVP

## AI 工具分工
- Claude: 架構設計
- Copilot: 代碼實作
```

### Day 2: 規劃任務

#### 與 Claude 對話

```bash
$ claude
> "根據部落格 API 的需求，在 TASKS.md 列出所有需要完成的任務"
```

#### TASKS.md 更新

```markdown
## 待辦 📋

### #1 設計資料庫 Schema
**優先級：** 🔴 高
**預估：** 4 小時

### #2 實作文章 CRUD API
**優先級：** 🔴 高
**預估：** 1 天

### #3 實作分類功能
**優先級：** 🟡 中
**預估：** 0.5 天
```

### Day 3: 架構設計

#### 與 Claude 對話

```bash
$ claude
> "設計部落格 API 的完整架構，記錄到 ARCHITECTURE.md"
```

#### ARCHITECTURE.md 更新

```markdown
## 資料庫設計

### posts 表
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API 端點

- GET /api/posts - 文章列表
- POST /api/posts - 新增文章
- GET /api/posts/:id - 文章詳情
- PUT /api/posts/:id - 更新文章
- DELETE /api/posts/:id - 刪除文章
```

### Day 4-5: 實作文章 CRUD

#### 使用 Copilot 生成代碼

```bash
$ gh copilot --prompt "根據 ARCHITECTURE.md 的設計，
  實作 Express.js 文章 CRUD API，使用 SQLite"
```

#### 更新進度

```bash
$ claude
> "更新 TASKS.md #2：標記文章 CRUD 已完成"
```

#### TASKS.md 更新

```markdown
## 已完成 ✅

### #2 實作文章 CRUD API
**完成日期：** 2025-01-30
**實際耗時：** 6 小時

**成果：**
- 完成所有 CRUD 端點
- 通過單元測試
- API 文檔已更新
```

### Day 6: 技術決策

#### 遇到問題：如何處理文章標籤？

```bash
$ claude
> "分析文章標籤的實作方式：
   方案 A: 使用 JSON 欄位
   方案 B: 建立獨立的 tags 表
   記錄決策到 DECISIONS.md"
```

#### DECISIONS.md 更新

```markdown
## 決策 #2: 文章標籤實作方式

**日期：** 2025-02-01
**狀態：** ✅ 已採用

### 考慮的方案

#### 方案 A: JSON 欄位
優點：簡單、快速
缺點：查詢效率低、不易統計

#### 方案 B: 多對多關聯表
優點：查詢靈活、易於統計
缺點：複雜度較高

### 決策
選擇方案 B：建立 tags 表和 post_tags 關聯表

### 理由
1. 未來需要標籤統計功能
2. 查詢效率更高
3. 符合正規化原則
```

### Day 10: 專案完成

#### 最終文件狀態

**TASKS.md：**
```markdown
## 統計
- 總任務：8
- 已完成：8 (100%)
```

**ARCHITECTURE.md：**
- 完整的資料庫 Schema
- 所有 API 端點文檔
- 錯誤處理機制

**DECISIONS.md：**
- 5 個技術決策記錄
- 包含理由和後果分析

## 協作流程總結

```
Day 1-2:   規劃階段
           ├─ Claude 分析需求
           └─ 規劃任務 (TASKS.md)

Day 3:     設計階段
           └─ Claude 設計架構 (ARCHITECTURE.md)

Day 4-8:   實作階段
           ├─ Copilot 生成代碼
           ├─ Claude 審查品質
           └─ 更新進度 (TASKS.md)

Day 6:     決策階段
           └─ 記錄技術決策 (DECISIONS.md)

Day 9-10:  收尾階段
           ├─ 最終測試
           └─ 文檔完善
```

## 學到的經驗

### 有效的做法 ✅

1. **每日更新 TASKS.md** - 追蹤進度清晰
2. **設計先行** - ARCHITECTURE.md 指引實作
3. **記錄決策** - DECISIONS.md 避免重複討論
4. **即時審查** - Claude 審查保證品質

### 需要改進 ⚠️

1. **初期規劃不足** - 應該更詳細的任務分解
2. **文檔滯後** - 有時忘記更新文檔
3. **決策記錄不及時** - 應該在決策當下就記錄

## 文件價值體現

### 新功能開發

需要新增評論功能時：

```bash
$ claude
> "查閱 ARCHITECTURE.md 了解現有架構，
   設計評論功能並更新架構文檔"
```

Claude 可以快速了解：
- 現有資料庫結構
- API 命名規範
- 技術棧選擇

### 問題排查

遇到標籤查詢效能問題時：

```bash
$ claude
> "查閱 DECISIONS.md #2，了解當初為何選擇多對多關聯"
```

快速回憶：
- 決策背景
- 選擇理由
- 預期後果

## 總結

小型專案雖然簡單，但通過 Context Sharing：

1. **效率提升**：文檔指引清晰，減少重複思考
2. **品質保證**：Claude 審查 + 文檔規範
3. **知識沉澱**：技術決策記錄便於回顧
4. **擴展容易**：新功能基於現有架構

**時間投資：**
- 文檔維護：每天 15 分鐘
- 總計：3.5 小時（10 天）

**回報：**
- 節省思考時間：5+ 小時
- 避免返工：3+ 小時
- 知識沉澱：無價

---

**結論：** 即使小型專案，Context Sharing 也非常值得！
