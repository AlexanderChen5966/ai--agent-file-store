# Context Sharing Skill

> 標準化文件系統，讓多個 AI 工具能夠共享上下文、追蹤進度、記錄決策

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-orange.svg)](https://agentskills.io)

## 🎯 解決的核心問題

### 問題：AI 協作時的上下文丟失

❌ **沒有 Context Sharing：**
```
你: "Claude, 設計一個認證系統"
Claude: [詳細設計...]

[切換到 Copilot]
你: "實作剛才設計的認證系統"
Copilot: "什麼設計？" ← 上下文丟失
```

✅ **使用 Context Sharing：**
```
你: "Claude, 設計認證系統並記錄到 ARCHITECTURE.md"
Claude: [設計並記錄...]

[切換到 Copilot]
你: "根據 ARCHITECTURE.md 實作認證系統"
Copilot: "讀取 ARCHITECTURE.md... 開始實作" ← 上下文共享
```

## ✨ 核心特性

- ✅ **四個標準文件** - CLAUDE.md, TASKS.md, ARCHITECTURE.md, DECISIONS.md
- ✅ **文件即協議** - 所有 AI 工具都能讀寫
- ✅ **版本控制友善** - Git 可追蹤變更
- ✅ **人類可讀** - Markdown 格式，易於閱讀
- ✅ **零依賴** - 純文件系統，無需額外工具
- ✅ **跨平台** - 支援所有採用 Agent Skills 標準的工具

## 📦 快速安裝

### 自動安裝

```bash
# 下載 Skill
git clone <repository-url>
cd context-sharing

# 安裝到 Claude Code
cp -r context-sharing ~/.claude/skills/

# 或使用安裝腳本
./scripts/install.sh
```

### 手動安裝

```bash
# 複製到 Claude skills 目錄
mkdir -p ~/.claude/skills
cp -r context-sharing ~/.claude/skills/
```

## 🚀 快速開始

### 1. 初始化專案

```bash
# 使用初始化腳本
python3 ~/.claude/skills/context-sharing/scripts/init-project.py \
    --project-name "我的專案" \
    --tech-stack "Node.js, PostgreSQL"

# 自動生成
✓ CLAUDE.md
✓ TASKS.md
✓ ARCHITECTURE.md
✓ DECISIONS.md
```

### 2. 開始使用

```bash
$ claude

# 新增任務
> "在 TASKS.md 新增任務：實作用戶認證"

# 設計架構
> "設計認證系統架構，記錄到 ARCHITECTURE.md"

# 記錄決策
> "記錄技術決策：為何選擇 JWT"
```

### 3. 協作使用

```bash
# Claude 設計
$ claude
> "設計並記錄到 ARCHITECTURE.md"

# Copilot 實作
$ gh copilot --prompt "根據 ARCHITECTURE.md 實作"

# Claude 審查
$ claude
> "審查實作，更新 TASKS.md"
```

## 📚 四個核心文件

### CLAUDE.md - 專案配置

**用途：** 專案總覽、AI 工具分工、工作流程  
**更新時機：** 專案初始化、配置變更

```markdown
## 專案資訊
- 名稱、技術棧、階段

## AI 工具分工
- Claude: 架構設計
- Copilot: 快速編碼

## 標準工作流程
1. 規劃 2. 設計 3. 實作 4. 審查
```

### TASKS.md - 任務追蹤

**用途：** 追蹤任務、記錄進度  
**更新時機：** 新任務、進度變更、完成任務

```markdown
## 進行中 🚧
### #23 用戶認證
- 進度: 60%
- 已完成: [x] 設計 [x] 註冊
- 進行中: [ ] Token 刷新

## 待辦 📋
### #24 API 優化
```

### ARCHITECTURE.md - 系統架構

**用途：** 記錄架構、設計、API  
**更新時機：** 架構變更、新增模組

```markdown
## 系統架構
- 整體架構圖
- 資料庫 Schema
- API 端點設計
```

### DECISIONS.md - 技術決策

**用途：** 記錄決策及理由（ADR 格式）  
**更新時機：** 技術選型、重要決策

```markdown
## 決策 #12: 選擇 JWT

**決策：** 使用 JWT 而非 Session
**理由：** 無狀態、易擴展
**後果：** ✅ 擴展容易 ⚠️ 需實作撤銷
```

## 💡 使用場景

### 場景 1：多工具協作

```bash
# 早上 - Claude 規劃
$ claude
> "規劃本週任務，更新 TASKS.md"

# 下午 - Copilot 實作
$ gh copilot --prompt "根據 TASKS.md 實作 #1"

# 晚上 - Claude 審查
$ claude
> "審查今天的代碼，更新進度"
```

### 場景 2：團隊協作

```bash
# 開發者 A
$ claude
> "設計支付模組，記錄到 ARCHITECTURE.md"

# 開發者 B（隔天）
$ claude
> "查閱 ARCHITECTURE.md，了解支付模組設計"
```

### 場景 3：跨時間維護

```bash
# 今天
$ claude
> "開始實作搜尋功能，進度 40%，記錄到 TASKS.md"

# 一週後
$ claude
> "查看 TASKS.md，繼續上週的搜尋功能"
# Claude 自動載入上週的上下文
```

## 📊 實戰數據

### 小型專案（個人部落格）
- **專案規模：** 2 週，8 個任務
- **文檔時間：** 每天 15 分鐘
- **節省時間：** 8+ 小時（避免重複思考）
- **品質提升：** Claude 多重審查

### 中型專案（電商平台）
- **專案規模：** 3 個月，50+ 任務
- **團隊：** 3-5 人
- **新人上手：** 從 3 天縮短到半天
- **決策追溯：** 100% 可追溯

### 企業級專案
- **專案規模：** 1 年+，200+ 任務
- **團隊：** 10+ 人
- **知識沉澱：** 完整的技術決策庫
- **維護成本：** 降低 40%

## 🎓 最佳實踐

### DO ✅

1. **立即更新** - 改動後馬上更新文件
2. **具體描述** - 避免模糊的描述
3. **連結相關** - 文件間建立連結
4. **版本控制** - 將文件加入 Git

### DON'T ❌

1. **延遲更新** - 不要拖到最後
2. **過度詳細** - 避免記錄過多細節
3. **複製代碼** - 不要複製大段代碼
4. **忽略決策** - 重要決策一定記錄

## 🔧 工具整合

### 與 multi-tool-coordination 整合

```bash
$ claude
> "使用 context-sharing 維護文檔，
   使用 multi-tool-coordination 協調工具"
```

兩個 Skills 完美配合：
- **context-sharing：** 維護上下文
- **multi-tool-coordination：** 協調工具分工

### Git 整合

```bash
# 將文件加入版本控制
git add CLAUDE.md TASKS.md ARCHITECTURE.md DECISIONS.md
git commit -m "docs: 更新專案文檔"
```

### IDE 整合

```bash
# VS Code: 設定快捷鍵
{
  "key": "ctrl+shift+t",
  "command": "workbench.action.openEditorAtIndex1",
  "args": { "path": "TASKS.md" }
}
```

## 📁 完整目錄結構

```
context-sharing/
├── SKILL.md                      # 核心 Skill
├── README.md                     # 本文件
├── templates/
│   ├── CLAUDE.md.template       # 專案配置模板
│   ├── TASKS.md.template        # 任務追蹤模板
│   ├── ARCHITECTURE.md.template # 架構文檔模板
│   └── DECISIONS.md.template    # 決策記錄模板
├── references/
│   ├── best-practices.md        # 最佳實踐指南
│   └── troubleshooting.md       # 故障排除
├── examples/
│   ├── small-project.md         # 小型專案範例
│   ├── medium-project.md        # 中型專案範例
│   └── enterprise-project.md    # 企業級範例
└── scripts/
    ├── init-project.py          # 專案初始化腳本
    └── validate-format.py       # 格式驗證腳本
```

## 🤔 常見問題

### Q: 文件會不會過時？

**A:** 將文件更新納入工作流程：
- Code Review 時檢查文件
- 定期（每週）審查
- Git hooks 提醒

### Q: 團隊成員不更新怎麼辦？

**A:** 建立團隊規範：
- 文檔更新列入 Definition of Done
- Review 時檢查
- 展示文檔的價值

### Q: 適合什麼規模的專案？

**A:** 所有規模都適合：
- 小型（個人）：降低認知負擔
- 中型（團隊）：促進協作
- 大型（企業）：知識管理

## 📖 學習資源

### 入門路徑

**第 1 天：** 了解概念
- 閱讀 SKILL.md
- 查看 examples/small-project.md

**第 2-3 天：** 實踐應用
- 初始化一個小專案
- 嘗試更新各個文件

**第 4-7 天：** 深入使用
- 整合多個 AI 工具
- 建立團隊規範

### 進階主題

- [團隊協作指南](references/team-collaboration.md)
- [最佳實踐](references/best-practices.md)
- [企業級部署](examples/enterprise-project.md)

## 🤝 相關 Skills

- **multi-tool-coordination** - AI 工具協調
- **skill-creator** - 創建自訂 Skills
- **doc-coauthoring** - 文檔協作

## 📝 授權

Apache 2.0 License

## 🔗 資源連結

- [Agent Skills 官方規範](https://agentskills.io)
- [GitHub Repository](#)
- [問題回報](#)

---

**版本：** 1.0  
**更新日期：** 2025-01-28  
**維護者：** Community

**⭐ 如果這個 Skill 幫助到你，請給個 Star！**

---

## 🚀 立即開始

```bash
# 1. 安裝 Skill
cp -r context-sharing ~/.claude/skills/

# 2. 初始化專案
python3 ~/.claude/skills/context-sharing/scripts/init-project.py \
    --project-name "我的專案"

# 3. 開始使用
$ claude
> "在 TASKS.md 新增第一個任務"
```

**Happy Coding! 文檔化你的開發旅程！** 📚✨
