---
name: context-sharing
description: Maintain shared context across multiple AI tools using standardized markdown files (TASKS.md, ARCHITECTURE.md, DECISIONS.md). Use when coordinating between Claude, Copilot, Codex, Gemini, or when team members need to track AI-assisted development progress. Essential for multi-agent workflows and knowledge preservation.
metadata:
  version: "1.0.0"
  author: "community"
  license: "Apache-2.0"
  keywords: ["multi-agent", "documentation", "context", "collaboration", "workflow", "knowledge-management"]
  platforms: ["claude-code", "codex-cli", "github-copilot", "universal"]
---

# Context Sharing Skill

## 概述

這個 Skill 提供標準化的文件系統，讓多個 AI 工具能夠共享上下文、追蹤進度、記錄決策。解決 AI 協作中最大的痛點：**上下文丟失**。

### 核心理念

```
文件即協議 (Documents as Protocol)

所有 AI Agent 透過讀寫標準化文件來交換資訊
→ 人類可讀
→ 版本可控
→ 工具無關
→ 零依賴
```

## 何時使用

### 適用場景

- ✅ 使用多個 AI 工具協作（Claude + Copilot + Codex）
- ✅ 團隊協作的 AI 輔助專案
- ✅ 需要追蹤技術決策和進度
- ✅ 長期專案需要知識沉澱
- ✅ 新成員需要快速了解專案
- ✅ 跨時間維護上下文（今天做到一半，明天繼續）

### 解決的問題

❌ **沒有 Context Sharing 時：**
```
Claude: "我設計了一個認證系統..."
[切換到 Copilot]
Copilot: "認證系統？什麼設計？" ← 上下文丟失
```

✅ **使用 Context Sharing 後：**
```
Claude: "設計完成，已記錄到 ARCHITECTURE.md"
[切換到 Copilot]
Copilot: "讀取 ARCHITECTURE.md... 了解設計，開始實作"
```

## 核心文件系統

### 四個標準文件

```
project/
├── CLAUDE.md          # 專案配置和 AI 工具設定
├── TASKS.md           # 任務追蹤和進度管理
├── ARCHITECTURE.md    # 系統架構和設計文檔
└── DECISIONS.md       # 技術決策記錄（ADR）
```

每個文件都有特定用途，互相配合形成完整的上下文系統。

### CLAUDE.md - 專案配置

**用途：** 專案總覽、AI 工具分工、工作流程

**何時更新：** 專案初始化、工具策略調整

**誰來讀取：** 所有 AI 工具、新加入的團隊成員

**核心內容：**
```markdown
- 專案基本資訊（技術棧、目標）
- AI 工具分工策略
- 標準工作流程
- 代碼規範和風格
- 常見問題 FAQ
```

詳細模板：[templates/CLAUDE.md.template](templates/CLAUDE.md.template)

### TASKS.md - 任務追蹤

**用途：** 追蹤當前任務、記錄進度、分配責任

**何時更新：** 新任務、進度變更、完成任務

**誰來讀取：** 所有 AI 工具、團隊成員

**核心內容：**
```markdown
## 進行中 🚧
### #23 用戶認證重構
- **負責：** Claude (設計) + Copilot (實作)
- **進度：** 60%
- **已完成：** [x] 架構設計 [x] 註冊端點
- **進行中：** [ ] Refresh token
- **發現問題：** ⚠️ 缺少 CSRF 防護

## 待辦 📋
### #24 API 效能優化

## 已完成 ✅
### #22 資料庫遷移
```

詳細模板：[templates/TASKS.md.template](templates/TASKS.md.template)

### ARCHITECTURE.md - 系統架構

**用途：** 記錄系統設計、架構決策、技術堆疊

**何時更新：** 架構變更、新增模組、重構設計

**誰來讀取：** Claude（設計時）、Copilot（實作時）、新成員

**核心內容：**
```markdown
- 系統整體架構
- 資料庫 Schema
- API 設計
- 模組職責
- 資料流向
- 技術棧說明
```

詳細模板：[templates/ARCHITECTURE.md.template](templates/ARCHITECTURE.md.template)

### DECISIONS.md - 技術決策

**用途：** 記錄重要技術決策及其原因（ADR 格式）

**何時更新：** 做出技術選擇時（工具、框架、模式）

**誰來讀取：** 未來的自己、團隊成員、審查代碼時

**核心內容：**
```markdown
## 決策 #12: 選擇 JWT 而非 Session

**日期：** 2025-01-28
**狀態：** ✅ 已採用
**決策者：** Claude (分析) + 團隊討論

### 背景
需要實作用戶認證機制

### 考慮方案
- 方案 A: Session-based (傳統)
- 方案 B: JWT (無狀態)

### 分析
[優缺點比較]

### 決策
選擇 JWT

### 原因
1. 無狀態，易於橫向擴展
2. 適合微服務架構
3. 支援跨域認證
```

詳細模板：[templates/DECISIONS.md.template](templates/DECISIONS.md.template)

## 快速開始

### 初始化專案

**方法 1：使用腳本（推薦）**

```bash
# 執行初始化腳本
python3 scripts/init-project.py --project-name "我的專案" \
                                 --tech-stack "Node.js, PostgreSQL"

# 自動生成所有必要文件
✓ CLAUDE.md
✓ TASKS.md
✓ ARCHITECTURE.md
✓ DECISIONS.md
```

**方法 2：手動創建**

```bash
# 複製模板
cp templates/CLAUDE.md.template ./CLAUDE.md
cp templates/TASKS.md.template ./TASKS.md
cp templates/ARCHITECTURE.md.template ./ARCHITECTURE.md
cp templates/DECISIONS.md.template ./DECISIONS.md

# 編輯內容
vim CLAUDE.md
```

### 基本工作流程

#### 1. 新任務開始

```bash
$ claude
> "在 TASKS.md 新增任務：實作用戶認證 API"
```

**Claude 更新 TASKS.md：**
```markdown
## 待辦 📋

### #25 實作用戶認證 API
- **優先級：** 高
- **預估：** 3 天
- **依賴：** 資料庫 schema 設計
```

#### 2. 架構設計

```bash
$ claude
> "設計用戶認證系統的架構，記錄到 ARCHITECTURE.md"
```

**Claude 更新 ARCHITECTURE.md：**
```markdown
## 認證系統

### API 端點
- POST /auth/register
- POST /auth/login
- POST /auth/refresh

### 資料表
- users (id, email, password_hash)
- refresh_tokens (id, user_id, token, expires_at)
```

#### 3. 實作（切換到 Copilot）

```bash
$ gh copilot --prompt "根據 ARCHITECTURE.md 的認證系統設計，
  實作 POST /auth/register 端點"
```

**Copilot 讀取 ARCHITECTURE.md 並生成代碼**

#### 4. 更新進度

```bash
$ claude
> "更新 TASKS.md：標記 #25 的註冊端點為完成"
```

#### 5. 記錄決策

```bash
$ claude
> "記錄技術決策：為何選擇 bcrypt 而非 argon2"
```

**Claude 更新 DECISIONS.md：**
```markdown
## 決策 #13: 使用 bcrypt 加密密碼

**日期：** 2025-01-28
**狀態：** ✅ 已採用

### 決策
選擇 bcrypt (cost factor 10)

### 原因
1. Node.js 生態系成熟
2. 社群廣泛使用
3. 效能足夠（每秒 30 次驗證）
```

## 協作模式

### 模式 1：Claude → Copilot 協作

```
步驟 1: Claude 規劃
$ claude
> "規劃用戶管理功能，更新 TASKS.md 和 ARCHITECTURE.md"

步驟 2: Copilot 實作
$ gh copilot --prompt "根據 ARCHITECTURE.md 實作用戶 CRUD API"

步驟 3: Claude 審查
$ claude
> "審查新增的代碼，檢查是否符合 ARCHITECTURE.md 的設計"

步驟 4: 更新進度
$ claude
> "更新 TASKS.md：標記用戶管理功能完成"
```

### 模式 2：團隊協作

```
開發者 A (早上):
$ claude
> "設計支付模組，記錄到 ARCHITECTURE.md"

開發者 B (下午):
$ claude
> "讀取 ARCHITECTURE.md，了解支付模組設計"
> "實作支付模組，更新 TASKS.md"

開發者 C (Code Review):
$ claude
> "根據 ARCHITECTURE.md 審查支付模組實作"
```

### 模式 3：跨時間維護

```
今天:
$ claude
> "開始實作搜尋功能，進度 40%，記錄到 TASKS.md"

明天:
$ claude
> "查看 TASKS.md，繼續昨天的搜尋功能"
# Claude 自動載入昨天的上下文
```

## 實戰案例

詳細案例請參考：
- [小型專案範例](examples/small-project.md)
- [中型專案範例](examples/medium-project.md)
- [企業級專案範例](examples/enterprise-project.md)

## 文件更新時機

### CLAUDE.md 更新時機

- 🔄 專案初始化
- 🔄 技術棧變更
- 🔄 工作流程調整
- 🔄 團隊規範更新

### TASKS.md 更新時機

- ✏️ 新增任務
- ✏️ 開始任務
- ✏️ 更新進度
- ✏️ 完成任務
- ✏️ 發現問題

### ARCHITECTURE.md 更新時機

- 📐 設計新模組
- 📐 修改架構
- 📐 新增 API
- 📐 資料庫變更

### DECISIONS.md 更新時機

- 💡 技術選型
- 💡 設計決策
- 💡 重大重構
- 💡 方案變更

## 最佳實踐

### DO ✅

1. **立即更新** - 改動後馬上更新文件
2. **具體描述** - 避免模糊的描述
3. **連結相關** - 在文件間建立連結
4. **保持同步** - 代碼和文件一致
5. **版本控制** - 將文件加入 Git

### DON'T ❌

1. **延遲更新** - 不要等到最後才更新
2. **過度詳細** - 避免記錄過多細節
3. **複製代碼** - 不要複製大段代碼到文件
4. **忽略決策** - 重要決策一定要記錄
5. **孤立文件** - 文件之間要有關聯

## 文件維護

### 定期檢查

**每週：**
```bash
$ claude
> "檢查 TASKS.md，清理已完成的任務"
```

**每月：**
```bash
$ claude
> "審查 ARCHITECTURE.md，確保與實際代碼同步"
```

**每季：**
```bash
$ claude
> "回顧 DECISIONS.md，評估過去的技術決策"
```

### 清理策略

```markdown
## TASKS.md 清理

已完成 > 2 週的任務：
- 移動到 COMPLETED.md
- 或直接刪除

## DECISIONS.md 歸檔

過時的決策：
- 標記為「已廢棄」
- 說明原因
- 連結到新決策
```

## 工具整合

### 與 multi-tool-coordination 整合

```bash
# 結合兩個 skills 使用
$ claude
> "使用 context-sharing 維護專案文件，
   使用 multi-tool-coordination 協調工具分工"
```

### Git 整合

```bash
# 將文件加入版本控制
git add CLAUDE.md TASKS.md ARCHITECTURE.md DECISIONS.md
git commit -m "docs: 更新專案文檔"

# 設定 .gitignore（如果不想追蹤）
echo "TASKS.md" >> .gitignore  # 個人任務
```

### IDE 整合

```bash
# VS Code: 快速開啟文件
code TASKS.md

# Vim: 設定快捷鍵
# .vimrc
nnoremap <leader>t :e TASKS.md<CR>
nnoremap <leader>a :e ARCHITECTURE.md<CR>
```

## 進階功能

### 自動驗證

使用驗證腳本：

```bash
# 檢查文件格式
python3 scripts/validate-format.py

# 輸出
✓ CLAUDE.md: 格式正確
✓ TASKS.md: 格式正確
⚠ ARCHITECTURE.md: 缺少資料庫 schema 章節
✗ DECISIONS.md: 決策 #5 缺少日期
```

### 自動生成

```bash
# 從代碼生成架構文檔
python3 scripts/generate-architecture.py

# 從 Git 歷史生成決策記錄
python3 scripts/extract-decisions.py
```

### 統計報告

```bash
# 生成專案統計
python3 scripts/generate-stats.py

# 輸出
專案統計報告
==============
總任務：45
已完成：32 (71%)
進行中：8 (18%)
待辦：5 (11%)

技術決策：12 個
最近決策：3 天前
```

## 團隊協作建議

### 建立團隊規範

```markdown
# TEAM_GUIDELINES.md

## 文件更新規範

1. **任務更新：** 每天結束前更新 TASKS.md
2. **架構變更：** PR 前更新 ARCHITECTURE.md
3. **技術決策：** 重要決策當天記錄到 DECISIONS.md
4. **Code Review：** 檢查文件是否同步更新
```

### Code Review 檢查清單

```markdown
## PR Review Checklist

文檔檢查：
- [ ] TASKS.md 已更新進度
- [ ] ARCHITECTURE.md 反映代碼變更
- [ ] 新的技術決策已記錄
- [ ] CLAUDE.md 配置仍然正確
```

## 疑難排解

詳細故障排除：[references/troubleshooting.md](references/troubleshooting.md)

### 常見問題快速解答

**Q: 文件太多，記不住何時更新？**
```
A: 使用 Git hooks 自動提醒
   或參考「文件更新時機」章節
```

**Q: 團隊成員不更新文件？**
```
A: 1. 在 Code Review 檢查
   2. 建立團隊規範
   3. 展示文件的價值
```

**Q: 文件和代碼不同步？**
```
A: 1. 設定 CI 檢查
   2. 定期審查
   3. 將文件更新納入 Definition of Done
```

## 參考資源

- [檔案格式規範](references/format-specification.md)
- [最佳實踐指南](references/best-practices.md)
- [團隊協作指南](references/team-collaboration.md)
- [範例專案集](examples/)

## 相關 Skills

- `multi-tool-coordination` - 多工具協調
- `skill-creator` - 創建新 Skills
- `doc-coauthoring` - 文檔協作撰寫

---

**版本：** 1.0  
**授權：** Apache-2.0  
**更新日期：** 2025-01-28
