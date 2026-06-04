# GitHub Copilot CLI 設定指南

## 安裝步驟

### macOS

```bash
# 1. 安裝 GitHub CLI
brew install gh

# 2. 安裝 Copilot 擴展
gh extension install github/gh-copilot

# 3. 登入 GitHub
gh auth login
# 選擇：GitHub.com → HTTPS → Login with web browser

# 4. 驗證安裝
gh copilot --version
```

### Windows

```powershell
# 1. 安裝 GitHub CLI
winget install GitHub.cli

# 2. 安裝 Copilot 擴展
gh extension install github/gh-copilot

# 3. 登入
gh auth login

# 4. 驗證
gh copilot --version
```

### Linux

```bash
# 1. 安裝 GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
  sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

# 2. 安裝 Copilot 擴展
gh extension install github/gh-copilot

# 3. 登入
gh auth login

# 4. 驗證
gh copilot --version
```

## 基本使用

### 一般問題查詢

```bash
gh copilot --prompt "如何在 TypeScript 使用 async/await"
gh copilot --prompt "Python 讀取 CSV 檔案"
gh copilot --prompt "React Hooks 最佳實踐"
```

### Shell 命令建議

```bash
gh copilot --prompt "批次重命名檔案"
gh copilot --prompt "Git 撤銷最後一次 commit"
gh copilot --prompt "Docker 清理未使用的映像"
```

### 代碼片段生成

```bash
gh copilot --prompt "Express.js 中間件範例"
gh copilot --prompt "PostgreSQL 連線設定"
gh copilot --prompt "JWT 認證實作"
```

### 代碼解釋

```bash
gh copilot --prompt "解釋這段代碼：$(cat src/auth.ts)"
```

## 進階使用

### 結合專案上下文

```bash
# 讀取專案文件後查詢
gh copilot --prompt "根據 package.json 的依賴，
  建議 Express.js 專案結構"
```

### 多步驟任務

```bash
# 步驟 1: 獲取建議
gh copilot --prompt "設計 REST API 端點"

# 步驟 2: 實作建議
gh copilot --prompt "實作剛才建議的 GET /users 端點"

# 步驟 3: 測試
gh copilot --prompt "為上述端點寫測試"
```

## 訂閱資訊

### 個人版
- 費用：$10/月
- 包含：CLI + IDE 擴展
- 免費試用：30 天

### 學生/教師
- 費用：免費
- 需要：GitHub Student/Teacher 認證
- 申請：https://education.github.com/

### 企業版
- 費用：$19/用戶/月
- 額外功能：企業級支援

## 故障排解

### 問題 1: 指令不存在

```bash
# 錯誤
gh: unknown command "copilot"

# 解決
gh extension install github/gh-copilot
```

### 問題 2: 認證失敗

```bash
# 錯誤
Error: not logged in

# 解決
gh auth login
gh auth refresh
```

### 問題 3: 沒有訂閱

```bash
# 錯誤
GitHub Copilot subscription required

# 解決
# 訪問 https://github.com/settings/copilot
# 開始試用或訂閱
```

### 問題 4: 網路問題

```bash
# 檢查網路
ping github.com

# 重新認證
gh auth refresh

# 更新擴展
gh extension upgrade gh-copilot
```

## 最佳實踐

### DO ✅

- 提供清晰的問題描述
- 包含技術棧資訊
- 說明預期結果
- 指定語言或框架

### DON'T ❌

- 提問過於模糊
- 期待完美輸出（總是需要審查）
- 複製完整專案代碼
- 忽略安全性檢查

## 範例腳本

### 一鍵測試

```bash
#!/bin/bash
# test-copilot.sh

echo "測試 GitHub Copilot CLI"

# 檢查安裝
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI 未安裝"
    exit 1
fi

# 檢查 Copilot
if ! gh extension list | grep -q "gh-copilot"; then
    echo "❌ Copilot 擴展未安裝"
    exit 1
fi

# 測試查詢
echo "✅ 執行測試查詢..."
gh copilot --prompt "Hello World in Python"

echo "✅ 測試完成"
```

## 相關資源

- 官方文檔：https://docs.github.com/copilot/github-copilot-in-the-cli
- 社群支援：https://github.community/
- 問題回報：https://github.com/github/gh-copilot/issues
