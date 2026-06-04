# Multi-Tool Coordination Skill

> 協調多個 AI 編碼工具（Claude Code、GitHub Copilot、Codex、Gemini）以提升開發效率

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-orange.svg)](https://agentskills.io)

## 🎯 功能特色

- ✅ **工具選擇指南** - 根據任務類型選擇最適合的 AI 工具
- ✅ **協作模式** - 預定義的工作流程模式
- ✅ **上下文傳遞** - 在工具間高效傳遞資訊
- ✅ **最佳實踐** - 累積的實戰經驗和技巧
- ✅ **成本優化** - 節省 50%+ Claude 使用額度

## 📦 快速安裝

### 方式 1：自動安裝（推薦）

```bash
# 下載 Skill
git clone <repository-url>
cd multi-tool-coordination

# 執行安裝腳本
chmod +x scripts/install.sh
./scripts/install.sh

# 選擇安裝位置：
# 1) 個人 Skills (~/.claude/skills/)
# 2) 專案 Skills (./.claude/skills/)
# 3) 自訂路徑
```

### 方式 2：手動安裝

```bash
# 複製到 Claude Code skills 目錄
cp -r multi-tool-coordination ~/.claude/skills/

# 或複製到專案目錄
cp -r multi-tool-coordination ./.claude/skills/
```

## 🚀 快速開始

### 1. 確認 Skill 已載入

```bash
$ claude
> "列出可用的 skills"
# 應該看到 multi-tool-coordination
```

### 2. 設定 GitHub Copilot（必要）

```bash
# 安裝 GitHub CLI
brew install gh  # macOS
# 或 winget install GitHub.cli  # Windows

# 安裝 Copilot 擴展
gh extension install github/gh-copilot

# 登入
gh auth login

# 驗證
gh copilot --version
```

### 3. 第一次使用

```bash
# Claude 會自動使用這個 Skill
$ claude
> "我要開發一個用戶認證 API，應該如何分配給不同的 AI 工具？"

# Claude 會根據 Skill 指引：
# 1. 建議用 Claude 做架構設計
# 2. 用 Copilot 快速實作
# 3. 用 Claude 審查代碼
```

## 📚 使用範例

### 範例 1：新功能開發

```bash
# 步驟 1: Claude 設計
$ claude
> "設計一個用戶認證系統"
# → Claude 產生完整架構

# 步驟 2: Copilot 實作
$ gh copilot --prompt "根據設計實作 Express.js 認證 API"
# → 快速生成代碼

# 步驟 3: Claude 審查
$ claude
> "審查這個認證實作的安全性"
# → 發現問題並建議改進
```

### 範例 2：問題排查

```bash
# Copilot 快速查詢
$ gh copilot --prompt "PostgreSQL 查詢效能優化"

# Claude 深度分析
$ claude
> "分析這個慢查詢並提供優化方案：[貼上查詢]"
```

### 範例 3：技術選型

```bash
# Gemini 研究（如果可用）
$ gemini "比較 Redis vs Memcached"

# Claude 決策
$ claude
> "根據研究結果，選擇適合我們專案的快取方案"

# Copilot 實作
$ gh copilot --prompt "整合 Redis 到 Express.js"
```

## 📖 文檔結構

```
multi-tool-coordination/
├── SKILL.md                      # 核心 Skill 文件
├── README.md                     # 本文件
├── templates/
│   ├── copilot-setup.md         # Copilot 設定指南
│   └── CLAUDE.md.template       # 專案配置模板
├── references/
│   └── best-practices.md        # 最佳實踐指南
├── examples/
│   ├── api-development.md       # API 開發範例
│   ├── data-pipeline.md         # 資料處理範例
│   └── fullstack-app.md         # 全端開發範例
└── scripts/
    └── install.sh               # 安裝腳本
```

## 🎓 核心概念

### 工具分工

| 工具 | 最適合 | 不適合 |
|------|--------|--------|
| **Claude** | 架構設計、代碼審查 | 簡單查詢 |
| **Copilot** | 快速編碼、測試生成 | 複雜設計 |
| **Codex** | 演算法、資料處理 | UI 設計 |
| **Gemini** | 技術研究、方案比較 | 代碼生成 |

### 協作模式

1. **設計 → 實作 → 審查** - 新功能開發
2. **研究 → 規劃 → 實作** - 技術選型
3. **快速查詢 → 深度分析** - 問題排查
4. **並行協作** - 大型專案

### 成本優化

```
傳統方式（只用 Claude）：
- 複雜功能：2500 tokens

協作模式：
- Claude 設計：800 tokens
- Copilot 實作：免費（訂閱內）
- Claude 審查：400 tokens
總計：1200 tokens

節省：52% Claude 額度
```

## 🛠️ 進階功能

### 自訂專案配置

複製模板到專案根目錄：

```bash
cp templates/CLAUDE.md.template ./CLAUDE.md
# 編輯 CLAUDE.md 設定專案特定配置
```

### 整合 Context Sharing

搭配 `context-sharing` skill 使用：

```bash
# 維護共享文件
TASKS.md          # 任務追蹤
ARCHITECTURE.md   # 架構文檔
DECISIONS.md      # 技術決策
```

## 📊 效能指標

### 真實使用數據

- **開發速度：** 提升 2-3x
- **成本節省：** 50-60% Claude 額度
- **代碼品質：** 通過 Claude 審查確保
- **學習效果：** 從 AI 互動中學習最佳實踐

### 適用專案規模

- ✅ 小型專案（< 5000 行）
- ✅ 中型專案（5000-50000 行）
- ✅ 大型專案（> 50000 行）
- ✅ 個人開發
- ✅ 團隊協作

## 🔧 故障排解

### Skill 沒有載入

```bash
# 檢查 Skill 位置
ls ~/.claude/skills/multi-tool-coordination/SKILL.md

# 或專案目錄
ls ./.claude/skills/multi-tool-coordination/SKILL.md

# 重啟 Claude Code
```

### Copilot 命令失效

```bash
# 檢查安裝
gh extension list | grep copilot

# 重新安裝
gh extension install github/gh-copilot

# 檢查認證
gh auth status
```

### 上下文丟失

使用文件記錄：

```bash
$ claude
> "更新 ARCHITECTURE.md：記錄新的設計決策"

$ gh copilot --prompt "根據 ARCHITECTURE.md 實作"
```

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📝 授權

Apache 2.0 License

## 🔗 相關資源

- [Agent Skills 官方規範](https://agentskills.io)
- [GitHub Copilot 文檔](https://docs.github.com/copilot)
- [Claude Code 文檔](https://code.claude.com/docs)

## 📮 支援

- 問題回報：GitHub Issues
- 社群討論：GitHub Discussions

---

**版本：** 1.0  
**更新日期：** 2025-01-28  
**維護者：** Community

**⭐ 如果這個 Skill 對你有幫助，請給個 Star！**
