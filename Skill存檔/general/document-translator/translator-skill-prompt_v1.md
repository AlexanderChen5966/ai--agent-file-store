# Translator Skill 創建提示詞

> 用於透過 skill-creator 創建 translator skill 的完整提示詞文檔

---

## 使用方式

將本文檔的「提示詞內容」部分複製貼給 Claude，Claude 將使用 skill-creator skill 自動創建 translator skill。

---

## 提示詞內容

```
請使用 skill-creator skill 幫我創建一個名為 "document-translator" 的 skill。

以下是詳細需求：

---

## Skill 基本資訊

**Skill 名稱**: document-translator
**目的**: 協助 Claude 理解和操作技術文檔翻譯系統
**位置**: /mnt/skills/user/document-translator/

---

## Skill 功能說明

這個 skill 是為了讓 Claude 能夠：
1. 理解翻譯系統的架構和工作流程
2. 協助用戶執行翻譯操作
3. 解釋不同翻譯模式和校稿後端的差異
4. 提供翻譯系統的故障排除建議
5. 管理術語表和翻譯配置

---

## 翻譯系統架構

### 目錄結構
```
project-root/
├── docs/
│   ├── en/              # 英文原文（權威來源）
│   └── zh-TW/           # 繁體中文譯文（自動生成）
│
├── translation/         # 翻譯系統
│   ├── translate.sh     # Shell 入口點
│   ├── translate.py     # Python 主程式
│   │
│   ├── translator/      # Python 模組
│   │   ├── google_translator.py
│   │   ├── interactive_proofreader.py
│   │   ├── chatgpt_proofreader.py
│   │   ├── claude_desktop_proofreader.py
│   │   ├── claude_cli_proofreader.py
│   │   ├── manual_proofreader.py
│   │   └── validator.py
│   │
│   └── config/
│       ├── glossary.json
│       ├── proofreading_prompt.txt
│       └── translation_config.json
```

### 翻譯流程
```
英文文檔 (docs/en/)
    ↓
【步驟 1】Google Translate 粗翻（快速、免費）
    ↓
【步驟 2】智慧校稿（多種後端可選）
    ↓
繁體中文文檔 (docs/zh-TW/)
```

---

## 翻譯模式

### Mode 1: google
- 僅使用 Google Translate
- 最快速、完全免費
- 適用場景：草稿、內部文檔
- 品質：⭐⭐

### Mode 2: auto（推薦）
- Google Translate + 智慧校稿
- 高品質、省成本
- 適用場景：生產文檔
- 品質：⭐⭐⭐⭐

---

## 校稿後端（auto 模式專用）

### Backend 1: auto（預設）
- 自動偵測可用的校稿器
- 偵測優先順序：chatgpt > cli > desktop > manual
- 零配置、最方便

### Backend 2: chatgpt
- 使用 ChatGPT Translate 網頁服務
- 透過 Selenium 自動化操作
- 優勢：免費、品質好、完全自動化
- 需求：Chrome 瀏覽器
- 適用：一般技術文檔

### Backend 3: desktop
- 使用 Claude Desktop GUI
- 透過檔案交換互動
- 優勢：品質最佳、可視覺化審查
- 需求：Claude Desktop 應用程式
- 適用：重要對外文檔、需要精確審查的內容

### Backend 4: cli
- 使用 Claude CLI 命令列工具
- 完全腳本化
- 優勢：穩定、適合自動化
- 需求：安裝 Claude CLI
- 適用：CI/CD 流程

### Backend 5: manual
- 開啟文字編輯器手動校稿
- 完全控制
- 優勢：無需任何 AI 工具、精確控制
- 需求：文字編輯器（VS Code/Sublime/nano/vi）
- 適用：少量修改、最終審查

---

## 使用方式

### 基本命令
```bash
# 自動模式（推薦）
./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md

# 指定校稿後端
./translation/translate.sh --mode=auto --proofreader=chatgpt docs/en/API.md
./translation/translate.sh --mode=auto --proofreader=desktop docs/en/IMPORTANT.md

# 僅 Google Translate（最快）
./translation/translate.sh --mode=google docs/en/DRAFT.md

# 批量翻譯
./translation/translate.sh --mode=auto docs/en/*.md

# 強制覆蓋已存在的譯文
./translation/translate.sh --mode=auto --force docs/en/*.md

# 詳細日誌
./translation/translate.sh --mode=auto --verbose docs/en/API.md
```

### Claude 應該如何協助用戶

當用戶說：
- "翻譯這個文件"
- "Translate this document"
- "幫我翻譯 API 文檔"

Claude 應該：
1. 確認檔案位置（應在 docs/en/）
2. 選擇適當的翻譯模式
3. 執行翻譯命令
4. 驗證輸出（docs/zh-TW/）
5. 使用 present_files 呈現譯文

---

## 術語表管理

### 術語表位置
`translation/config/glossary.json`

### 術語表結構
```json
{
  "technical_terms": {
    "API": "API",
    "endpoint": "端點",
    "request": "請求",
    "response": "回應"
  },
  
  "taiwan_terms": {
    "account": "帳號",
    "data": "資料",
    "software": "軟體",
    "network": "網路"
  },
  
  "preserve": [
    "Claude",
    "GitHub",
    "Docker"
  ]
}
```

### Claude 協助更新術語表

當用戶說：
- "新增術語到術語表"
- "更新翻譯術語"

Claude 應該：
1. 讀取現有術語表
2. 詢問要新增的術語
3. 更新 JSON 檔案
4. 確認更新成功

---

## 品質驗證

### 自動驗證項目
- [ ] 程式碼區塊數量一致
- [ ] 標題數量一致
- [ ] 連結數量一致
- [ ] 無簡體中文字元（賬、數據、軟件、網絡）
- [ ] Markdown 格式正確

### Claude 檢查清單

當翻譯完成後，Claude 應該：
1. 確認譯文已生成
2. 檢查檔案大小合理（不能為空或過小）
3. 快速掃描是否有明顯錯誤
4. 提醒用戶人工審查重要文檔

---

## 常見問題與故障排除

### 問題 1: 翻譯失敗
**可能原因**:
- Python 環境未正確設定
- 缺少依賴套件
- 檔案路徑錯誤

**解決方式**:
```bash
# 重建虛擬環境
cd translation
rm -rf venv
./translate.sh --mode=auto docs/en/test.md
```

### 問題 2: 校稿器未偵測到
**可能原因**:
- Chrome 未安裝（chatgpt）
- Claude CLI 未安裝（cli）
- Claude Desktop 未安裝（desktop）

**解決方式**:
```bash
# 手動指定校稿器
./translate.sh --mode=auto --proofreader=manual docs/en/API.md
```

### 問題 3: ChatGPT 翻譯失敗
**可能原因**:
- 網頁結構改變
- Chrome 版本問題
- 網路連線問題

**解決方式**:
```bash
# 使用其他校稿器
./translate.sh --mode=auto --proofreader=desktop docs/en/API.md

# 或僅用 Google
./translate.sh --mode=google docs/en/API.md
```

### 問題 4: 翻譯品質不佳
**解決方式**:
1. 更新術語表（glossary.json）
2. 使用品質更好的校稿器（desktop）
3. 手動校稿重要文檔
4. 調整校稿提示詞（proofreading_prompt.txt）

---

## 效能與成本比較

| 模式 | 速度 | 品質 | Token 成本 | 適用場景 |
|------|------|------|-----------|---------|
| google | ⚡⚡⚡ | ⭐⭐ | $0 | 草稿 |
| auto + chatgpt | ⚡⚡ | ⭐⭐⭐⭐ | $0 | 一般文檔 |
| auto + desktop | ⚡ | ⭐⭐⭐⭐⭐ | $0 | 重要文檔 |
| auto + cli | ⚡⚡ | ⭐⭐⭐⭐ | $0 | 自動化 |
| auto + manual | ⚡ | ⭐⭐⭐ | $0 | 少量修改 |

---

## GitLab CI/CD 整合

### 自動翻譯觸發條件
- 當 `docs/en/` 目錄下的 `.md` 檔案有變更
- 推送到 `main` 或 `develop` 分支

### CI/CD 流程
```
推送英文文檔變更
    ↓
偵測變更的檔案
    ↓
自動翻譯（mode=auto, proofreader=manual）
    ↓
驗證翻譯品質
    ↓
自動提交譯文到 docs/zh-TW/
```

---

## 相關檔案路徑

重要檔案位置：
- 翻譯腳本：`./translation/translate.sh`
- Python 主程式：`./translation/translate.py`
- 術語表：`./translation/config/glossary.json`
- 校稿提示詞：`./translation/config/proofreading_prompt.txt`
- 翻譯配置：`./translation/config/translation_config.json`
- 英文原文：`./docs/en/`
- 中文譯文：`./docs/zh-TW/`

---

## Claude 的職責

作為翻譯系統的助手，Claude 應該：

1. **理解用戶意圖**
   - 判斷用戶想翻譯哪些文檔
   - 推薦適合的翻譯模式

2. **執行翻譯**
   - 構建正確的命令
   - 使用 bash_tool 執行
   - 監控執行狀態

3. **驗證結果**
   - 確認譯文已生成
   - 檢查基本品質
   - 使用 present_files 呈現

4. **提供建議**
   - 根據文檔重要性推薦模式
   - 解釋不同後端的差異
   - 協助故障排除

5. **管理配置**
   - 協助更新術語表
   - 調整翻譯配置
   - 維護校稿提示詞

---

## 範例對話

### 範例 1: 基本翻譯
```
用戶: "幫我翻譯 API 文檔"

Claude:
1. 確認檔案：docs/en/API_DOCUMENTATION.md
2. 執行命令：
   bash_tool: ./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md
3. 檢查輸出：docs/zh-TW/API_DOCUMENTATION.md
4. present_files: API_DOCUMENTATION.md
```

### 範例 2: 批量翻譯
```
用戶: "翻譯 docs/en 下所有文檔"

Claude:
1. 列出檔案：ls docs/en/*.md
2. 確認數量
3. 執行批量翻譯：
   bash_tool: ./translation/translate.sh --mode=auto docs/en/*.md
4. 報告結果
```

### 範例 3: 術語管理
```
用戶: "新增 'container' 翻譯為 '容器' 到術語表"

Claude:
1. 讀取術語表：view translation/config/glossary.json
2. 更新 technical_terms 區段
3. 寫入檔案：str_replace
4. 確認更新
```

### 範例 4: 故障排除
```
用戶: "翻譯失敗了"

Claude:
1. 詢問錯誤訊息
2. 檢查常見問題
3. 提供解決方案
4. 協助重新執行
```

---

## 進階功能

### 自訂校稿提示詞
用戶可以修改 `translation/config/proofreading_prompt.txt` 來自訂校稿規則。

Claude 應該協助：
1. 理解現有提示詞結構
2. 根據需求修改
3. 測試修改效果

### 多語言支援
雖然目前只支援英文→繁體中文，但架構允許擴展。

Claude 應該：
1. 解釋如何新增其他語言對
2. 指導修改配置檔案
3. 協助測試新語言

---

## 特別注意事項

### 網路環境
- ChatGPT 後端需要穩定的網路連線
- 可能需要處理防火牆或代理設定

### 檔案權限
- 確保翻譯腳本有執行權限
- 確保輸出目錄可寫入

### 版本控制
- 英文文檔是權威來源
- 中文譯文自動生成，不應手動編輯
- 所有修改應在英文版進行

---

請根據以上資訊創建 translator skill 的 SKILL.md 檔案。

要求：
1. 結構清晰，易於 Claude 理解
2. 包含所有重要資訊
3. 提供足夠的範例
4. 考慮實際使用場景
5. 使用 Markdown 格式
6. 加入適當的章節和目錄
7. 包含 Mermaid 圖表（如果有助於理解）
8. 提供完整的命令參考
9. 包含錯誤處理指南
10. 加入最佳實踐建議

謝謝！
```

---

## 使用步驟

### 步驟 1: 複製提示詞

將上面「提示詞內容」區塊中的所有文字（從「請使用 skill-creator...」到「謝謝！」）複製。

### 步驟 2: 與 Claude 對話

在 Claude Desktop 或 Claude.ai 中：

```
[貼上完整提示詞]
```

### 步驟 3: 等待生成

Claude 會使用 skill-creator skill 生成 translator skill 的 SKILL.md。

### 步驟 4: 下載檔案

Claude 會使用 `present_files` 工具呈現生成的 SKILL.md，點擊下載即可。

### 步驟 5: 放置檔案

將下載的 SKILL.md 放到：

```
/mnt/skills/user/translator/SKILL.md
```

或專案中的：

```
skills/user/translator/SKILL.md
```

---

## 驗證 Skill

創建完成後，測試 skill 是否正確工作：

### 測試 1: 基本理解

```
用戶: "使用 translator skill 解釋翻譯系統的工作流程"

預期: Claude 能清楚解釋 Google Translate + 校稿的兩步驟流程
```

### 測試 2: 執行翻譯

```
用戶: "使用 translator skill 幫我翻譯 docs/en/test.md"

預期: Claude 執行翻譯命令並呈現結果
```

### 測試 3: 後端比較

```
用戶: "使用 translator skill 比較不同校稿後端的差異"

預期: Claude 能解釋 chatgpt, desktop, cli, manual 的區別
```

### 測試 4: 故障排除

```
用戶: "使用 translator skill 幫我解決翻譯失敗的問題"

預期: Claude 能詢問錯誤並提供解決方案
```

---

## 進階調整

如果生成的 SKILL.md 需要調整，可以追加要求：

### 補充內容

```
"請在 translator skill 中補充：
1. 更詳細的 ChatGPT 後端說明
2. Selenium 自動化的技術細節
3. 更多實際使用範例
4. 完整的錯誤碼參考"
```

### 調整格式

```
"請調整 translator skill 的格式：
1. 加入更多 Mermaid 流程圖
2. 使用表格呈現命令參數
3. 增加視覺化的決策樹
4. 加入彩色的狀態標記"
```

### 簡化內容

```
"請簡化 translator skill：
1. 移除過於技術性的細節
2. 聚焦在最常用的功能
3. 簡化範例
4. 使用更簡潔的語言"
```

---

## 預期輸出結構

Claude 生成的 SKILL.md 應該包含以下主要章節：

```markdown
# Translator Skill

## 📋 Table of Contents

## Overview
- Skill purpose
- Key features
- System requirements

## System Architecture
- Directory structure
- Component diagram
- Data flow

## Translation Modes
- Mode comparison
- When to use each mode
- Performance metrics

## Proofreading Backends
- Backend comparison
- Detection priority
- Setup requirements

## Usage Guide
- Basic commands
- Advanced options
- Batch processing

## Glossary Management
- Structure
- Update procedures
- Best practices

## Quality Validation
- Automatic checks
- Manual review
- Error patterns

## Troubleshooting
- Common issues
- Solutions
- Debug tips

## Examples
- Basic translation
- Batch processing
- Glossary updates
- Error handling

## CI/CD Integration
- GitLab setup
- Workflow
- Automation tips

## Best Practices
- File organization
- Naming conventions
- Version control

## Advanced Topics
- Custom prompts
- Multi-language support
- Performance tuning

## Reference
- File paths
- Command reference
- Configuration options
```

---

## 附錄

### A. 相關檔案

- 翻譯系統主程式：`translation/translate.py`
- Shell 入口點：`translation/translate.sh`
- 術語表：`translation/config/glossary.json`

### B. 參考資源

- Anthropic Skills 官方文檔
- skill-creator 使用指南
- Python Selenium 文檔

### C. 版本歷史

- v1.0.0 (2025-01-16): 初始版本
  - 支援 Google Translate
  - 支援 5 種校稿後端
  - 完整的術語表管理

---

## 授權

本提示詞文檔採用 MIT License。

---

**文檔結束**
