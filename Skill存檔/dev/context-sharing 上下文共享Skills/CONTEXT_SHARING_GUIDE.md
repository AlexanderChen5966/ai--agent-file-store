# Context Sharing Skill - 完整安裝使用指南

## 📦 你收到的檔案

1. **context-sharing/** - 完整 Skill 目錄
2. **context-sharing.tar.gz** - 壓縮打包版本（22KB）
3. **CONTEXT_SHARING_GUIDE.md** - 本檔案

## 🎯 這個 Skill 解決什麼問題？

### 核心問題：AI 協作時的上下文丟失

想像這個場景：

```
你: "Claude, 設計一個用戶認證系統"
Claude: [給你完整的架構設計...]

[5 分鐘後，切換到 GitHub Copilot]
你: "實作剛才設計的認證系統"
Copilot: "什麼設計？我沒看到..." ← 💥 上下文丟失
```

### 解決方案：文件即協議

```
你: "Claude, 設計認證系統並記錄到 ARCHITECTURE.md"
Claude: [設計並保存到檔案...]

[切換到 Copilot]
你: "根據 ARCHITECTURE.md 的設計實作認證系統"
Copilot: "讀取 ARCHITECTURE.md... 了解設計，開始實作" ← ✅ 完美
```

## 🚀 快速安裝（5 分鐘）

### 步驟 1：解壓縮（可選）

如果使用壓縮檔：

```bash
tar -xzf context-sharing.tar.gz
cd context-sharing
```

如果直接使用目錄，跳過這步。

### 步驟 2：安裝到 Claude Code

**方法 A：複製到個人目錄（推薦）**

```bash
# 所有專案都能用
mkdir -p ~/.claude/skills
cp -r context-sharing ~/.claude/skills/

# 驗證
ls ~/.claude/skills/context-sharing/SKILL.md
```

**方法 B：複製到專案目錄**

```bash
# 只在特定專案用
mkdir -p ./.claude/skills
cp -r context-sharing ./.claude/skills/

# 驗證
ls ./.claude/skills/context-sharing/SKILL.md
```

### 步驟 3：驗證安裝

```bash
$ claude

# 測試 Skill
> "檢查 context-sharing skill 是否已載入"

# 或
> "列出可用的 skills"
# 應該看到 context-sharing
```

## ✅ 安裝確認清單

- [ ] Skill 目錄存在於 `~/.claude/skills/context-sharing/`
- [ ] `SKILL.md` 檔案存在
- [ ] Claude Code 能識別這個 Skill
- [ ] 可以看到 templates/ 目錄

## 📖 第一次使用（實戰教學）

### 情境：開始一個新的 Node.js 專案

#### 1. 初始化專案文件

**使用初始化腳本（推薦）：**

```bash
# 進入你的專案目錄
cd ~/projects/my-awesome-app

# 執行初始化
python3 ~/.claude/skills/context-sharing/scripts/init-project.py \
    --project-name "我的超棒應用" \
    --tech-stack "Node.js, Express, PostgreSQL, React"

# 輸出
✓ 已創建: CLAUDE.md
✓ 已創建: TASKS.md
✓ 已創建: ARCHITECTURE.md
✓ 已創建: DECISIONS.md

✅ 初始化完成！
```

**手動創建（替代方案）：**

```bash
# 複製模板
cp ~/.claude/skills/context-sharing/templates/CLAUDE.md.template ./CLAUDE.md
cp ~/.claude/skills/context-sharing/templates/TASKS.md.template ./TASKS.md
cp ~/.claude/skills/context-sharing/templates/ARCHITECTURE.md.template ./ARCHITECTURE.md
cp ~/.claude/skills/context-sharing/templates/DECISIONS.md.template ./DECISIONS.md

# 編輯檔案
vim CLAUDE.md
```

#### 2. 第一次使用 - 規劃任務

```bash
$ claude

> "我要開發一個簡單的 Todo API，幫我規劃任務並記錄到 TASKS.md"
```

**Claude 會自動：**
1. 分析需求
2. 拆分任務
3. 更新 TASKS.md

**TASKS.md 更新內容範例：**
```markdown
## 待辦 📋

### #1 設計資料庫 Schema
**優先級：** 🔴 高
**預估：** 2 小時
**檢查清單：**
- [ ] 設計 todos 表
- [ ] 設計索引

### #2 實作 CRUD API
**優先級：** 🔴 高
**預估：** 1 天
```

#### 3. 設計階段 - 記錄架構

```bash
$ claude

> "設計 Todo API 的完整架構，包含資料庫 schema 和 API 端點，
   記錄到 ARCHITECTURE.md"
```

**ARCHITECTURE.md 更新內容範例：**
```markdown
## 資料庫設計

### todos 表
```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API 端點

- GET /api/todos - 列表
- POST /api/todos - 新增
- PUT /api/todos/:id - 更新
- DELETE /api/todos/:id - 刪除
```

#### 4. 實作階段 - 切換到 Copilot

```bash
$ gh copilot --prompt "根據 ARCHITECTURE.md 的設計，
  實作 Express.js Todo API，使用 PostgreSQL"
```

**Copilot 會：**
1. 讀取 ARCHITECTURE.md
2. 了解設計
3. 生成代碼

#### 5. 審查階段 - 回到 Claude

```bash
$ claude

> "審查 Copilot 生成的 Todo API 代碼，
   檢查安全性和最佳實踐，
   更新 TASKS.md 標記進度"
```

#### 6. 決策記錄 - 記住為什麼

假設你在「分頁」實作上做了選擇：

```bash
$ claude

> "記錄技術決策：為何選擇 Cursor-based 分頁而非 Offset-based，
   記錄到 DECISIONS.md"
```

**DECISIONS.md 更新範例：**
```markdown
## 決策 #1: 選擇 Cursor-based 分頁

**日期：** 2025-01-28
**狀態：** ✅ 已採用

### 背景
Todo 列表需要分頁功能

### 考慮方案
- 方案 A: Offset-based (LIMIT/OFFSET)
- 方案 B: Cursor-based (WHERE id > last_id)

### 決策
選擇 Cursor-based

### 理由
1. 效能更好（大數據集）
2. 避免重複/遺漏
3. 適合無限滾動

### 後果
✅ 效能優異
⚠️ 實作稍複雜（可接受）
```

## 🎯 完整工作流程範例

### 場景：開發用戶認證功能（完整流程）

```bash
# Day 1 早上：規劃
$ claude
> "規劃用戶認證功能的開發任務，記錄到 TASKS.md"

# Day 1 下午：設計
$ claude
> "設計用戶認證系統的架構：
   - 資料庫 schema (users, refresh_tokens)
   - API 端點 (register, login, refresh)
   - 安全機制 (JWT, bcrypt)
   記錄到 ARCHITECTURE.md"

# Day 2：實作（Copilot）
$ gh copilot --prompt "根據 ARCHITECTURE.md 實作註冊端點，
  使用 bcrypt 加密密碼"

# Day 2：審查（Claude）
$ claude
> "審查註冊端點的安全性，更新 TASKS.md 進度"

# Day 3：決策記錄
$ claude
> "記錄為何選擇 JWT 而非 Session-based 認證，
   記錄到 DECISIONS.md"

# Day 4：繼續實作
$ gh copilot --prompt "根據 ARCHITECTURE.md 實作登入端點"

# Day 5：完成
$ claude
> "標記 TASKS.md 用戶認證功能為已完成，
   記錄完成時間和成果"
```

## 📊 四個核心文件詳解

### CLAUDE.md - 專案配置中心

**用途：**
- 專案基本資訊
- AI 工具分工策略
- 標準工作流程
- 代碼規範

**何時更新：**
- 專案初始化
- 技術棧變更
- 工作流程調整

**實際用法：**
```bash
$ claude
> "更新 CLAUDE.md：加入 Redis 到技術棧"
```

### TASKS.md - 任務追蹤板

**用途：**
- 追蹤所有任務
- 記錄進度
- 發現的問題
- Bug 追蹤

**何時更新：**
- 新增任務
- 開始工作
- 進度變更
- 完成任務

**實際用法：**
```bash
# 新增任務
$ claude
> "在 TASKS.md 新增任務：實作搜尋功能"

# 更新進度
$ claude
> "更新 TASKS.md #5：標記資料庫設計完成"

# 記錄問題
$ claude
> "在 TASKS.md #5 記錄發現的問題：缺少索引"
```

### ARCHITECTURE.md - 架構藍圖

**用途：**
- 系統整體架構
- 資料庫設計
- API 規格
- 模組職責

**何時更新：**
- 架構設計
- 新增模組
- API 變更
- 重構

**實際用法：**
```bash
$ claude
> "設計支付模組的架構，更新 ARCHITECTURE.md"
```

### DECISIONS.md - 決策歷史

**用途：**
- 技術選型
- 設計決策
- 權衡分析
- 決策理由

**何時更新：**
- 技術選擇
- 重大決策
- 方案變更

**實際用法：**
```bash
$ claude
> "記錄為何選擇 PostgreSQL 而非 MongoDB"
```

## 💡 進階使用技巧

### 技巧 1：團隊協作

```bash
# 開發者 A (早上)
$ claude
> "設計支付模組，記錄到 ARCHITECTURE.md"
> "新增任務到 TASKS.md：實作支付模組"

# 開發者 B (下午)
$ claude
> "查閱 ARCHITECTURE.md 了解支付模組設計"
> "根據設計實作支付模組"
> "更新 TASKS.md 進度"

# 開發者 C (Code Review)
$ claude
> "根據 ARCHITECTURE.md 審查支付模組實作"
```

### 技巧 2：跨時間維護

```bash
# 今天 (18:00)
$ claude
> "我要下班了，記錄當前進度到 TASKS.md：
   搜尋功能完成 60%，明天繼續 Elasticsearch 整合"

# 明天 (09:00)
$ claude
> "查看 TASKS.md，繼續昨天的搜尋功能"
# Claude 自動載入昨天的上下文
```

### 技巧 3：新人快速上手

```bash
# 新人第一天
$ claude
> "我是新加入的開發者，幫我了解這個專案：
   1. 閱讀 CLAUDE.md
   2. 查看 ARCHITECTURE.md
   3. 瀏覽 DECISIONS.md 了解技術選擇
   4. 給我一個總結"

# Claude 會整理所有資訊並給出清晰的專案概覽
```

### 技巧 4：定期回顧

```bash
# 每週五
$ claude
> "回顧本週 TASKS.md 的進度，
   生成週報：完成了什麼、遇到什麼問題、下週計劃"

# 每月底
$ claude
> "回顧 DECISIONS.md 的所有決策，
   評估哪些決策是正確的，哪些需要調整"
```

## 🔧 與其他工具整合

### 與 multi-tool-coordination Skill 整合

```bash
$ claude
> "使用 context-sharing 維護專案文檔，
   使用 multi-tool-coordination 協調 AI 工具分工"
```

**完美組合：**
- **context-sharing：** 解決「上下文共享」問題
- **multi-tool-coordination：** 解決「工具選擇」問題

### Git 整合

```bash
# .gitignore 設定
# 如果不想追蹤個人任務
echo "TASKS.md" >> .gitignore

# 提交文檔
git add CLAUDE.md ARCHITECTURE.md DECISIONS.md
git commit -m "docs: 更新專案架構和決策記錄"
```

### VS Code 整合

```json
// .vscode/settings.json
{
  "files.associations": {
    "CLAUDE.md": "markdown",
    "TASKS.md": "markdown",
    "ARCHITECTURE.md": "markdown",
    "DECISIONS.md": "markdown"
  },
  "markdown.preview.breaks": true
}
```

## 🎓 學習路徑

### 第 1 天：理解概念

**閱讀：**
- [ ] README.md - 了解 Skill 概述
- [ ] SKILL.md - 理解使用方式
- [ ] examples/small-project.md - 看實際案例

**練習：**
```bash
# 初始化一個測試專案
python3 scripts/init-project.py \
    --project-name "測試專案"
```

### 第 2-3 天：實際應用

**實作：**
- [ ] 在實際專案中初始化文件
- [ ] 嘗試新增任務
- [ ] 記錄一個架構設計
- [ ] 記錄一個技術決策

**檢查點：**
```bash
# 確認檔案都有內容
ls -lh CLAUDE.md TASKS.md ARCHITECTURE.md DECISIONS.md
```

### 第 4-7 天：深入使用

**進階練習：**
- [ ] 整合多個 AI 工具協作
- [ ] 團隊協作（如果有團隊）
- [ ] 定期更新和回顧
- [ ] 建立個人/團隊規範

### 第 2 週：優化工作流程

**優化：**
- [ ] 找出最適合的更新頻率
- [ ] 自訂文檔模板
- [ ] 建立快捷方式
- [ ] 分享經驗給團隊

## ❓ 常見問題

### Q1: Skill 沒有被使用？

**檢查：**
```bash
# 1. 確認安裝位置
ls ~/.claude/skills/context-sharing/SKILL.md

# 2. 重啟 Claude Code

# 3. 明確提及
$ claude
> "使用 context-sharing skill 初始化專案"
```

### Q2: 文件太多，記不住？

**解決方案：**

1. **從基礎開始**
   - 先用 TASKS.md（最常用）
   - 再加入 ARCHITECTURE.md
   - 最後用 DECISIONS.md

2. **設定提醒**
   ```bash
   # Git pre-commit hook
   #!/bin/bash
   echo "記得更新 TASKS.md！"
   ```

3. **使用 Claude 幫忙**
   ```bash
   $ claude
   > "提醒我：哪些情況需要更新哪個檔案"
   ```

### Q3: 團隊成員不更新文檔？

**解決方案：**

1. **展示價值**
   - 演示如何利用文檔快速上手
   - 展示決策追溯的便利性

2. **納入流程**
   - Code Review 檢查文檔
   - Definition of Done 包含文檔更新

3. **簡化更新**
   - 使用 Claude 自動更新
   - 提供模板和範例

### Q4: 適合什麼規模的專案？

**答案：所有規模！**

**小型專案（個人）：**
- 降低認知負擔
- 跨時間維護上下文
- 時間投資：每天 10-15 分鐘

**中型專案（3-10人）：**
- 促進團隊協作
- 新人快速上手
- 時間投資：每天 20-30 分鐘

**大型專案（10+人）：**
- 知識管理和沉澱
- 決策追溯和審計
- 時間投資：專人維護

## 📚 參考資源

### Skill 內建文檔

```bash
# 查看模板
cat ~/.claude/skills/context-sharing/templates/CLAUDE.md.template

# 查看範例
cat ~/.claude/skills/context-sharing/examples/small-project.md

# 查看最佳實踐
cat ~/.claude/skills/context-sharing/references/best-practices.md
```

### 外部資源

- [Agent Skills 官方規範](https://agentskills.io)
- [ADR 格式說明](https://adr.github.io/)
- [Markdown 語法](https://www.markdownguide.org/)

## 🎉 下一步行動

安裝完成後，建議立即：

1. ✅ **測試初始化**
   ```bash
   python3 scripts/init-project.py --project-name "測試"
   ```

2. ✅ **閱讀範例**
   ```bash
   cat examples/small-project.md
   ```

3. ✅ **開始實際專案**
   ```bash
   $ claude
   > "使用 context-sharing 初始化我的專案"
   ```

4. ✅ **建立習慣**
   - 每天更新 TASKS.md
   - 架構變更時更新 ARCHITECTURE.md
   - 重要決策時更新 DECISIONS.md

---

**Happy Documenting! 讓 AI 協作更順暢！** 📚🤖✨

**版本：** 1.0  
**日期：** 2025-01-28

有任何問題，查閱文檔或尋求社群協助！
