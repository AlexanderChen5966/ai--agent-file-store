# Document Translator Skill 創建提示詞

> 用於透過 skill-creator 創建 document-translator skill 的完整提示詞文檔

---

## 使用方式

將本文檔的「提示詞內容」部分複製貼給 Claude，Claude 將使用 skill-creator skill 自動創建 document-translator skill。

---

## 提示詞內容

```
請使用 skill-creator skill 幫我創建一個名為 "document-translator" 的 skill。

以下是詳細需求：

---

## Skill 基本資訊

**Skill 名稱**: document-translator
**目的**: 協助 Claude 理解和操作技術文檔翻譯系統（使用智慧降級翻譯策略）
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

### 翻譯流程（智慧降級策略）
```
英文文檔 (docs/en/)
    ↓
【策略 1】ChatGPT Translate（優先）
    ↓
  成功?
    ↓ 是
  完成 ✅
    ↓ 否
【策略 2】降級：Google Translate 粗翻
    ↓
【策略 3】智慧校稿（多種後端可選）
    ↓
繁體中文文檔 (docs/zh-TW/) ✅
```

**核心策略**：
1. **優先使用 ChatGPT Translate**（品質最佳、免費）
2. **失敗時自動降級**到 Google Translate + 校稿
3. **雙重保障**確保翻譯總是能完成

---

## 翻譯模式

### Mode 1: chatgpt
- 僅使用 ChatGPT Translate
- 品質最佳、免費
- 適用場景：重要文檔、對外發布
- 品質：⭐⭐⭐⭐
- 備註：失敗時不會降級，直接報錯

### Mode 2: auto（推薦）⭐
- ChatGPT Translate（優先）+ 智慧降級
- **優先使用 ChatGPT，失敗自動降級到 Google + 校稿**
- 高品質、高可靠性、零成本
- 適用場景：所有生產文檔（推薦）
- 品質：⭐⭐⭐⭐⭐
- 成功率：95%+

### Mode 3: google
- 僅使用 Google Translate（無校稿）
- 最快速、完全免費
- 適用場景：快速草稿、內部文檔
- 品質：⭐⭐

---

## 翻譯與校稿機制

### 主要翻譯器

#### Translator 1: ChatGPT Translate（優先）⭐
- 使用 ChatGPT Translate 網頁服務
- 透過 Selenium 自動化操作
- 優勢：品質最佳、免費、完全自動化
- 需求：Chrome 瀏覽器
- 適用：所有技術文檔（優先使用）
- 成功率：~85%

#### Translator 2: Google Translate（備案）
- 快速、免費的機器翻譯
- 作為降級備案使用
- 需要配合校稿器提升品質

### 校稿後端（降級時使用）

當 ChatGPT Translate 失敗，系統會降級到 Google Translate，此時需要校稿提升品質：

#### Backend 1: auto（預設）
- 自動偵測可用的校稿器
- 偵測優先順序：desktop > cli > manual
- 零配置、最方便

#### Backend 2: desktop
- 使用 Claude Desktop GUI
- 透過檔案交換互動
- 優勢：品質最佳、可視覺化審查
- 需求：Claude Desktop 應用程式
- 適用：重要對外文檔

#### Backend 3: cli
- 使用 Claude CLI 命令列工具
- 完全腳本化
- 優勢：穩定、適合自動化
- 需求：安裝 Claude CLI
- 適用：CI/CD 流程

#### Backend 4: manual
- 開啟文字編輯器手動校稿
- 完全控制
- 優勢：無需任何 AI 工具
- 需求：文字編輯器（VS Code/Sublime/nano/vi）
- 適用：少量修改、最終審查

---

## 使用方式

### 基本命令
```bash
# 智慧降級模式（推薦）⭐
./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md
# → 優先 ChatGPT，失敗自動降級到 Google + 校稿

# 僅 ChatGPT Translate（不降級）
./translation/translate.sh --mode=chatgpt docs/en/IMPORTANT.md

# 僅 Google Translate（最快，無校稿）
./translation/translate.sh --mode=google docs/en/DRAFT.md

# 批量翻譯（智慧降級）
./translation/translate.sh --mode=auto docs/en/*.md

# 禁用降級機制（ChatGPT 失敗就報錯）
./translation/translate.sh --mode=auto --no-fallback docs/en/*.md

# 指定降級時的校稿器
./translation/translate.sh --mode=auto --proofreader=desktop docs/en/API.md

# 顯示瀏覽器視窗（調試用）
./translation/translate.sh --mode=auto --no-headless docs/en/API.md

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
2. **選擇智慧降級模式（--mode=auto）** 作為預設
3. 執行翻譯命令
4. 監控翻譯狀態（ChatGPT 成功 or 降級到 Google）
5. 驗證輸出（docs/zh-TW/）
6. 使用 present_files 呈現譯文
7. **報告使用的翻譯方法**（ChatGPT or Google+校稿）

### Claude 翻譯策略建議

根據文檔類型推薦模式：

**一般文檔**（推薦）:
```bash
./translation/translate.sh --mode=auto docs/en/API.md
```

**重要對外文檔**:
```bash
# 先用 ChatGPT
./translation/translate.sh --mode=chatgpt docs/en/IMPORTANT.md
# 如果失敗，再用 auto 模式
./translation/translate.sh --mode=auto docs/en/IMPORTANT.md
```

**快速草稿**:
```bash
./translation/translate.sh --mode=google docs/en/DRAFT.md
```

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

### 問題 1: ChatGPT Translate 失敗（最常見）
**可能原因**:
- 網頁結構改變
- Chrome 版本問題
- 網路連線不穩定
- Selenium WebDriver 問題

**解決方式**:
```bash
# 自動降級（推薦）
./translate.sh --mode=auto docs/en/API.md
# → 會自動降級到 Google + 校稿

# 或直接使用 Google
./translate.sh --mode=google docs/en/API.md
```

**預期行為**:
使用 auto 模式時，ChatGPT 失敗會自動降級，用戶會看到：
```
⚠️  ChatGPT Translate 失敗，降級到 Google + 校稿
步驟 1/2: Google Translate 粗翻...
步驟 2/2: 智慧校稿...
✅ Google + 校稿完成
```

### 問題 2: 翻譯完全失敗
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

### 問題 3: Chrome 或 ChromeDriver 問題
**可能原因**:
- Chrome 瀏覽器未安裝
- ChromeDriver 版本不匹配

**解決方式**:
```bash
# 方案 1: 安裝 Chrome（macOS）
brew install --cask google-chrome

# 方案 2: 使用無需 Chrome 的模式
./translate.sh --mode=google docs/en/API.md
```

### 問題 4: 降級機制未啟動
**可能原因**:
- 使用了 --no-fallback 參數
- 使用 chatgpt 模式而非 auto 模式

**解決方式**:
```bash
# 確保使用 auto 模式且未禁用降級
./translate.sh --mode=auto docs/en/API.md
# 不要使用 --no-fallback
```

### 問題 5: 翻譯品質不佳
**診斷**:
1. 檢查使用的翻譯方法（查看日誌）
2. ChatGPT 成功 → 品質應該不錯
3. 降級到 Google → 可能需要更好的校稿器

**解決方式**:
```bash
# 使用更好的校稿器（降級時）
./translate.sh --mode=auto --proofreader=desktop docs/en/API.md

# 或手動校稿
./translate.sh --mode=auto --proofreader=manual docs/en/API.md
```

---

## 效能與成本比較

| 模式 | 速度 | 品質 | 成功率 | Token 成本 | 適用場景 |
|------|------|------|--------|-----------|---------|
| chatgpt | ⚡⚡ | ⭐⭐⭐⭐ | ~85% | $0 | 重要文檔 |
| auto（推薦）⭐ | ⚡⚡ | ⭐⭐⭐⭐⭐ | 95%+ | $0 | 所有文檔 |
| google | ⚡⚡⚡ | ⭐⭐ | ~90% | $0 | 快速草稿 |

### 智慧降級統計範例

執行 10 個文檔翻譯後的統計：
```
============================================================
翻譯完成
============================================================
總計: 10 個檔案
✅ 成功: 10
❌ 失敗: 0

============================================================
翻譯統計
============================================================
ChatGPT 成功: 8 (80%)
ChatGPT 失敗: 2 (20%)
降級到 Google: 2
ChatGPT 成功率: 80.0%
============================================================
```

### 品質對比

| 翻譯來源 | 術語準確度 | 語句流暢度 | 格式保留 |
|---------|----------|----------|---------|
| ChatGPT | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Google + Desktop校稿 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Google + Manual校稿 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Google（無校稿） | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## GitLab CI/CD 整合

### 自動翻譯觸發條件
- 當 `docs/en/` 目錄下的 `.md` 檔案有變更
- 推送到 `main` 或 `develop` 分支

### CI/CD 流程（智慧降級）
```
推送英文文檔變更
    ↓
偵測變更的檔案
    ↓
自動翻譯（mode=auto）
  ├─ 嘗試 ChatGPT Translate
  └─ 失敗時降級到 Google + manual 校稿
    ↓
驗證翻譯品質
    ↓
自動提交譯文到 docs/zh-TW/
```

### CI/CD 配置建議

```yaml
# .gitlab-ci.yml
variables:
  TRANSLATION_MODE: "auto"          # 使用智慧降級
  PROOFREADER: "manual"             # 降級時用手動校稿（穩定）
  CHATGPT_HEADLESS: "true"          # 無頭模式
  ENABLE_FALLBACK: "true"           # 啟用降級
```

**為什麼 CI/CD 用 manual 校稿器？**
- CI/CD 環境無法互動
- manual 模式在 CI 中會跳過校稿（回退到純 Google）
- 仍比完全失敗好

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

### 範例 1: 基本翻譯（智慧降級）
```
用戶: "幫我翻譯 API 文檔"

Claude:
1. 確認檔案：docs/en/API_DOCUMENTATION.md
2. 選擇智慧降級模式（預設）
3. 執行命令：
   bash_tool: ./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md
4. 監控過程：
   - 嘗試 ChatGPT Translate...
   - [成功] 或 [失敗，降級到 Google + 校稿]
5. 檢查輸出：docs/zh-TW/API_DOCUMENTATION.md
6. 報告：「翻譯完成，使用了 ChatGPT Translate」
   或：「ChatGPT 失敗，已降級到 Google + 校稿完成翻譯」
7. present_files: API_DOCUMENTATION.md
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

### 範例 4: 故障排除（降級機制）
```
用戶: "翻譯失敗了"

Claude:
1. 詢問錯誤訊息
2. 檢查使用的模式
3. 診斷：
   - 如果是 chatgpt 模式 → 建議改用 auto（有降級）
   - 如果是 auto 模式 → 檢查是否有降級發生
   - 如果完全失敗 → 檢查 Python 環境
4. 提供解決方案：
   - "請嘗試智慧降級模式："
     ./translate.sh --mode=auto docs/en/API.md
5. 協助重新執行
```

### 範例 5: 查看翻譯統計
```
用戶: "最近的翻譯使用 ChatGPT 的成功率如何？"

Claude:
1. 說明：auto 模式會在翻譯後顯示統計
2. 範例統計：
   ChatGPT 成功: 8 (80%)
   降級到 Google: 2 (20%)
3. 建議：如果成功率低，可能需要檢查網路或 Chrome
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

請根據以上資訊創建 document-translator skill 的 SKILL.md 檔案。

要求：
1. 結構清晰，易於 Claude 理解
2. 包含所有重要資訊
3. **重點強調智慧降級翻譯策略**（ChatGPT 優先，Google 備案）⭐
4. **清楚說明三種翻譯模式的差異和使用場景**（chatgpt, auto, google）⭐
5. **詳細解釋降級機制的運作方式**⭐
6. 提供足夠的範例，特別是降級場景的範例
7. 考慮實際使用場景
8. 使用 Markdown 格式
9. 加入適當的章節和目錄
10. 包含 Mermaid 圖表來解釋智慧降級流程
11. 提供完整的命令參考（包含降級相關參數）
12. 包含錯誤處理指南（特別是 ChatGPT 失敗的處理）
13. 加入最佳實踐建議（何時用哪種模式）
14. 包含翻譯統計的解讀說明

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

Claude 會使用 skill-creator skill 生成 document-translator skill 的 SKILL.md。

### 步驟 4: 下載檔案

Claude 會使用 `present_files` 工具呈現生成的 SKILL.md，點擊下載即可。

### 步驟 5: 放置檔案

將下載的 SKILL.md 放到：

```
/mnt/skills/user/document-translator/SKILL.md
```

或專案中的：

```
skills/user/document-translator/SKILL.md
```

---

## 驗證 Skill

創建完成後，測試 skill 是否正確工作：

### 測試 1: 基本理解

```
用戶: "使用 document-translator skill 解釋智慧降級翻譯流程"

預期: Claude 能清楚解釋 ChatGPT 優先、失敗降級到 Google + 校稿的策略
```

### 測試 2: 執行翻譯

```
用戶: "使用 document-translator skill 幫我翻譯 docs/en/test.md"

預期: Claude 執行 auto 模式翻譯命令並報告使用的方法
```

### 測試 3: 模式比較

```
用戶: "使用 document-translator skill 比較不同翻譯模式的差異"

預期: Claude 能解釋 chatgpt, auto, google 三種模式的區別和使用場景
```

### 測試 4: 故障排除

```
用戶: "使用 document-translator skill 幫我解決 ChatGPT 翻譯失敗的問題"

預期: Claude 能說明降級機制並建議使用 auto 模式
```

### 測試 5: 統計理解

```
用戶: "使用 document-translator skill 解釋翻譯統計資訊"

預期: Claude 能解釋 ChatGPT 成功率、降級次數等統計指標
```

---

## 進階調整

如果生成的 SKILL.md 需要調整，可以追加要求：

### 補充內容

```
"請在 document-translator skill 中補充：
1. 更詳細的智慧降級機制說明
2. ChatGPT Translate 失敗的常見原因
3. 降級統計的解讀方法
4. Selenium 自動化的技術細節
5. 更多實際使用範例"
```

### 調整格式

```
"請調整 document-translator skill 的格式：
1. 加入智慧降級的 Mermaid 流程圖
2. 使用表格呈現翻譯模式對比
3. 增加降級決策樹圖表
4. 加入翻譯統計的視覺化說明"
```

### 簡化內容

```
"請簡化 document-translator skill：
1. 聚焦在智慧降級策略
2. 移除過於技術性的細節
3. 簡化範例
4. 使用更簡潔的語言"
```

---

## 預期輸出結構

Claude 生成的 SKILL.md 應該包含以下主要章節：

```markdown
# Document Translator Skill

## 📋 Table of Contents

## Overview
- Skill purpose
- Key features (智慧降級策略)
- System requirements

## System Architecture
- Directory structure
- Component diagram
- Data flow

## Translation Strategy (重點)⭐
- 智慧降級機制
- ChatGPT 優先策略
- Google 備案機制
- 成功率統計

## Translation Modes
- chatgpt mode
- auto mode (推薦)
- google mode
- Mode comparison

## Translators & Proofreaders
- ChatGPT Translate (主要)
- Google Translate (備案)
- Proofreading backends (降級時使用)
- Backend selection logic

## Usage Guide
- Basic commands
- Mode selection guide
- Fallback behavior
- Advanced options

## Glossary Management
- Structure
- Update procedures
- Best practices

## Quality Validation
- Automatic checks
- Translation validation
- Manual review

## Troubleshooting
- ChatGPT failures (最常見)
- Fallback not triggered
- Chrome/ChromeDriver issues
- Quality problems
- Debug tips

## Examples
- Basic translation with fallback
- Batch processing
- Glossary updates
- Fallback statistics

## CI/CD Integration
- GitLab setup
- Fallback in CI
- Automation tips

## Performance Metrics
- Success rates
- Quality comparison
- Speed comparison

## Best Practices
- When to use which mode
- Fallback configuration
- Monitoring statistics

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
  - **智慧降級翻譯策略**
  - ChatGPT Translate 優先
  - Google Translate 備案機制
  - 支援 3 種翻譯模式（chatgpt, auto, google）
  - 支援 4 種校稿後端（desktop, cli, manual, auto）
  - 完整的術語表管理
  - 翻譯統計與成功率追蹤

---

## 授權

本提示詞文檔採用 MIT License。

---

**文檔結束**
