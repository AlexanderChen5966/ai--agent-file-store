---
name: multi-tool-coordination
description: Coordinate multiple AI coding tools (Claude Code, GitHub Copilot, Codex, Gemini) for complex development tasks. Use when combining different AI tools' strengths for architecture design, rapid coding, algorithm implementation, or research. Helps decide which tool to use and how to hand off context between tools.
metadata:
  version: "2.0.0"
  author: "community"
  license: "Apache-2.0"
  keywords: ["multi-agent", "copilot", "codex", "workflow", "collaboration"]
  platforms: ["claude-code", "codex-cli", "github-copilot"]
  changelog: "v2.0.0 — 將 gh copilot --prompt 替換為 copilot --model gpt-4.1 -p（standalone Copilot CLI）"
---

# Multi-Tool Coordination

## 概述

這個 Skill 幫助你在複雜開發任務中協調多個 AI 工具。每個工具都有其優勢領域，透過適當的工具選擇和上下文傳遞，你可以最大化開發效率。

## 何時使用

### 適用場景
- 複雜功能需要架構設計和快速實作
- 大型專案需要不同專長領域的協助
- 需要研究技術方案並實作
- 想節省單一工具的使用額度
- 團隊協作時需要統一工作流程

### 不適用場景
- 簡單任務（直接用單一工具即可）
- 緊急修復（切換工具會浪費時間）
- 學習階段（先熟悉單一工具）

## 工具選擇指南

### Claude Code 最適合

**優勢領域：**
- 🏗️ 架構和系統設計
- 🔍 多檔案分析和重構
- 📝 代碼審查和品質提升
- 🎯 技術決策和策略規劃
- 🐛 複雜問題除錯

**使用時機：**
```
需求分析階段
系統架構設計
代碼品質審查
技術選型決策
跨檔案重構
```

### GitHub Copilot CLI 最適合

**優勢領域：**
- ⚡ 快速代碼生成
- 📋 樣板和模板代碼
- 💡 語法建議和補全
- 🔧 Shell 命令生成
- 🎨 常見模式實作

**使用時機：**
```
實作標準功能
生成測試案例
Shell 腳本撰寫
常見問題查詢
快速原型開發
```

**執行命令：**
```bash
copilot --model gpt-4.1 -p "你的問題或需求"

# 多行 prompt 或 pipe 內容
echo "你的問題" | copilot --model gpt-4.1
cat context.txt | copilot --model gpt-4.1 -p "根據以上內容實作..."
```

### Codex CLI 最適合

**優勢領域：**
- 🧮 演算法實作
- 📊 資料處理管道
- 🐍 Python/JavaScript 專案
- 🔬 數學和科學計算
- 🤖 機器學習相關代碼

**使用時機：**
```
演算法優化
資料轉換邏輯
科學計算任務
ML 模型實作
數據管道建構
```

### Gemini CLI 最適合

**優勢領域：**
- 🔬 技術研究和比較
- 📚 多角度分析
- 🌐 最新技術調研
- ✅ 方案驗證
- 📖 文檔綜合整理

**使用時機：**
```
技術選型研究
方案比較分析
最新趨勢調查
多方案驗證
知識整合
```

## 協作模式

### 模式 1：設計 → 實作 → 審查

**適用：** 新功能開發

```
Claude Code (設計) → Copilot (實作) → Claude Code (審查)
```

**實戰範例：**
```bash
# 步驟 1: Claude 設計
$ claude
> "設計一個用戶認證 API，包含註冊、登入、JWT refresh"

# 步驟 2: Copilot 實作
$ copilot --model gpt-4.1 -p "根據以下設計實作 Express.js 認證 API：
  - POST /auth/register (email, password)
  - POST /auth/login 返回 JWT
  - POST /auth/refresh (refresh_token)"

# 步驟 3: Claude 審查
$ claude
> "審查這個認證實作，檢查安全性和最佳實踐"
```

### 模式 2：研究 → 規劃 → 實作

**適用：** 技術選型

```
Gemini (研究) → Claude (規劃) → Copilot/Codex (實作)
```

**實戰範例：**
```bash
# 步驟 1: Gemini 研究
$ gemini "比較 Redis vs Memcached 用於 session 儲存"

# 步驟 2: Claude 規劃
$ claude
> "根據分析，規劃在 Express 專案整合 Redis"

# 步驟 3: Copilot 實作
$ copilot --model gpt-4.1 -p "Express.js 整合 Redis session store"
```

### 模式 3：快速查詢 → 深度分析

**適用：** 問題排查

```
Copilot (快速查詢) → Claude (深度分析)
```

**實戰範例：**
```bash
# 步驟 1: Copilot 快速查詢
$ copilot --model gpt-4.1 -p "PostgreSQL 查詢效能優化技巧"

# 步驟 2: Claude 深度分析
$ claude
> "分析這個慢查詢並優化：[貼上查詢]"
```

## 上下文傳遞技巧

### 技巧 1：摘要傳遞

```bash
# ✅ 好的方式
$ copilot --model gpt-4.1 -p "優化 JWT 中間件：
  當前問題：每次請求都查詢資料庫
  期望：實作快取機制"
```

### 技巧 2：使用共享文件

結合 `context-sharing` skill：

```bash
# 維護共享文件
TASKS.md          # 任務列表
ARCHITECTURE.md   # 架構文檔

# Claude 更新
$ claude
> "更新 ARCHITECTURE.md：記錄認證流程"

# Copilot 讀取（透過 pipe 傳入文件內容）
$ cat ARCHITECTURE.md | copilot --model gpt-4.1 -p "根據以上架構文件實作認證"
```

### 技巧 3：分階段驗證

```bash
# 生成 → 檢查 → 改進
$ copilot --model gpt-4.1 -p "生成用戶註冊 API"
$ claude
> "審查註冊 API 安全性"
$ copilot --model gpt-4.1 -p "應用改進建議"
```

## 實戰案例

詳細案例請參考：
- [API 開發案例](examples/api-development.md)
- [資料處理案例](examples/data-pipeline.md)
- [全端開發案例](examples/fullstack-app.md)
- [效能優化案例](examples/performance-optimization.md)

## 常見陷阱

### ❌ 不要做

1. **頻繁切換工具** - 完成邏輯單元再切換
2. **過度複雜** - 簡單任務用簡單工具
3. **不驗證輸出** - 總是審查 AI 生成的代碼
4. **丟失上下文** - 使用共享文件維護狀態

### ✅ 應該做

1. **完整單元** - 完成一個模組再切換
2. **適當工具** - 根據任務選擇工具
3. **驗證測試** - 審查並測試輸出
4. **共享上下文** - 維護 CLAUDE.md 等文件

## 工具配置

### GitHub Copilot CLI（Standalone）

```bash
# 安裝（standalone CLI，非 gh extension）
npm install -g @github/copilot-cli

# 驗證
copilot --version

# 使用
copilot --model gpt-4.1 -p "你的問題"

# 可用模型（--model 參數）
# gpt-4.1（預設建議）
# 其他模型依 Copilot 訂閱方案而異
```

> **注意：** 此版本使用 `copilot`（standalone CLI），而非 `gh copilot`（gh extension）。
> 兩者皆連接 GitHub Copilot 服務，但 standalone CLI 支援 stdin pipe 和 `--model` 參數，
> 更適合腳本化和工具協作場景。

### 專案配置

建議建立 `CLAUDE.md`：

```markdown
# 專案配置

## AI 工具分工
- Claude Code: 架構、審查
- Copilot: 快速編碼（copilot --model gpt-4.1）
- Codex: 演算法
- Gemini: 研究調查

## 工作流程
1. Claude 設計
2. Copilot 實作
3. Claude 審查
```

## 進階技巧

### 自動化工作流程

參考：[scripts/auto-workflow.sh](scripts/auto-workflow.sh)

```bash
#!/bin/bash
# 自動化協作

claude "規劃 $1 功能"
copilot --model gpt-4.1 -p "實作 $1"
claude "審查 $1"
```

## 效能指標

### 成本節省

```
單用 Claude: 2500 tokens/功能
協作模式: 1200 tokens/功能
節省: 52%
```

### 效率提升

```
傳統: 120 分鐘
協作: 40 分鐘
提升: 3x
```

## 疑難排解

詳見：[references/troubleshooting.md](references/troubleshooting.md)

## 相關 Skills

- `context-sharing` - 上下文共享
- `skill-creator` - 創建新 Skills

## 參考資源

- [最佳實踐](references/best-practices.md)
- [決策樹](references/decision-tree.md)
- [完整範例](examples/)

---

**版本：** 2.0.0
**授權：** Apache-2.0
