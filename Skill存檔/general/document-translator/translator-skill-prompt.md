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
6. **理解 nodriver 的反機器人偵測機制** ⭐
7. **處理 CAPTCHA 相關問題** ⭐

---

## 核心技術

### 自動化技術
- **nodriver**: undetected-chromedriver 作者的新一代反偵測瀏覽器自動化工具 ⭐
- **自動下載 Chrome**: 不依賴系統 Chrome 版本
- **內建反偵測**: 無需額外 stealth 設定
- **Async/Await**: 非同步程式設計（效能優化）

### 反偵測策略（nodriver 內建）
1. 自動隱藏 `navigator.webdriver` 標記
2. 內建瀏覽器指紋偽裝
3. 原生 Chrome 行為（不是控制模式）
4. 人類化的打字速度
5. 隨機延遲
6. **持久化瀏覽器會話**（保存登入狀態）⭐

### 為什麼選擇 nodriver？

> **注意**: 曾評估使用本機端 AI 模型（如 TranslateGemma）進行翻譯，但因執行效率太慢（即使使用 GPU 加速，長文檔翻譯也需要數分鐘至數十分鐘），不實際而放棄。

| 技術 | CAPTCHA 觸發率 | 安裝複雜度 | 維護需求 | 適用場景 |
|------|---------------|-----------|---------|---------|
| nodriver ⭐ | <5% | 極簡單 | 極低 | **推薦** |
| Playwright + Stealth | ~10% | 中等 | 中等 | 備選 |
| Selenium | 50%+ | 複雜 | 高 | 不推薦 |
| 本機 AI (TranslateGemma) | 0% | 複雜 | 低 | ❌ 效率太慢 |

---

## 翻譯系統架構

### 目錄結構
```
project-root/
├── docs/
│   ├── en/              # 英文原文（權威來源）
│   └── zh-TW/           # 繁體中文譯文（自動生成）
│
├── scripts/             # 翻譯系統
│   ├── translate.py     # Python 主程式
│   │
│   ├── translator/      # Python 模組
│   │   ├── google_translator.py
│   │   ├── chatgpt_translator.py       # 使用 nodriver ⭐
│   │   └── __init__.py
│   │
│   └── config/
│       ├── glossary.json
│       └── translation_config.json
```

### 翻譯流程（智慧降級策略）
```
英文文檔 (docs/en/)
    ↓
┌─────────────────────────────────────────────┐
│ --mode chatgpt（預設）                        │
│   → ChatGPT Translate 專用頁面               │
│   → 品質最佳 ⭐⭐⭐⭐⭐                          │
├─────────────────────────────────────────────┤
│ --mode auto（高可靠性）                       │
│   → 先 ChatGPT，失敗降級到 Google + 校稿      │
│   → 成功率 98%+                              │
├─────────────────────────────────────────────┤
│ --mode google+proofread ⭐ 新增              │
│   → Google Translate + 智慧校稿              │
│   → 品質 ⭐⭐⭐⭐（校稿後）                      │
├─────────────────────────────────────────────┤
│ --mode google（快速）                         │
│   → 僅 Google Translate（無校稿）            │
│   → 品質 ⭐⭐                                  │
└─────────────────────────────────────────────┘
    ↓
繁體中文文檔 (docs/zh-TW/) ✅
```

**核心策略**：
1. **優先使用 ChatGPT Translate**（品質最佳、免費）
2. **失敗時自動降級**到 Google Translate + 校稿
3. **支援直接使用 Google + 校稿模式**（`google+proofread`）⭐
4. **雙重保障**確保翻譯總是能完成

---

## 翻譯模式

### Mode 1: chatgpt（推薦）⭐
- 使用 ChatGPT Translate 專用翻譯頁面
- **使用 nodriver 自動化（極低 CAPTCHA 觸發率）** ⭐
- 品質最佳、免費
- 適用場景：所有文檔（推薦預設）
- 品質：⭐⭐⭐⭐⭐
- 成功率：95%+

### Mode 2: auto
- ChatGPT Translate（優先）+ 智慧降級
- **優先使用 ChatGPT，失敗自動降級到 Google + 校稿**
- 高品質、高可靠性、零成本
- 適用場景：需要高可靠性的翻譯任務
- 品質：⭐⭐⭐⭐⭐
- 成功率：98%+

### Mode 3: google+proofread ⭐ 新增
- Google Translate 粗翻 + 智慧校稿
- **直接使用 Google 翻譯後進行校稿**（跳過 ChatGPT Translate）
- 適用場景：測試校稿流程、ChatGPT Translate 暫時不可用時
- 品質：⭐⭐⭐⭐（校稿後）
- 成功率：~95%

### Mode 4: google
- 僅使用 Google Translate（無校稿）
- 最快速、完全免費
- 適用場景：快速草稿、內部文檔
- 品質：⭐⭐

---

## 校稿後端（google+proofread 或降級時使用）

當使用 `google+proofread` 模式，或 ChatGPT Translate 失敗降級到 Google Translate 時，需要校稿提升品質：

### Backend 1: auto（預設）
- 自動偵測可用的校稿器
- 偵測優先順序：**chatgpt > desktop > cli > manual** ⭐
- 零配置、最方便

### Backend 2: chatgpt ⭐ 新增（最高優先）
- **使用 ChatGPT 對話頁面（chatgpt.com）進行校稿**
- 使用 nodriver 自動化操作
- 優勢：品質最佳、免費、自動化
- 需求：nodriver 套件
- 適用：所有文檔（推薦）
- **與翻譯器共用 Chrome Profile**（登入狀態共享）
- **內容穩定偵測機制**：連續 3 次（約 9 秒）回應長度不變 → 校稿完成 ⭐

### Backend 3: desktop
- 使用 Claude Desktop GUI
- 透過檔案交換互動
- 優勢：品質佳、可視覺化審查
- 需求：Claude Desktop 應用程式
- 適用：重要對外文檔

### Backend 4: cli
- 使用 Claude CLI 命令列工具
- 完全腳本化
- 優勢：穩定、適合自動化
- 需求：安裝 Claude CLI
- 適用：CI/CD 流程

### Backend 5: manual
- 開啟文字編輯器手動校稿
- 完全控制
- 優勢：無需任何 AI 工具
- 需求：文字編輯器（VS Code/Sublime/nano/vi）
- 適用：少量修改、最終審查

---

## 校稿提示詞說明 ⭐ 新增

### 校稿提示詞結構

校稿提示詞由兩部分組成：

1. **文件背景資訊**（根據 `--doc-type` 自動產生）
2. **基礎校稿規則**（從 `proofreading_prompt.txt` 載入）

### 最重要規則：程式碼區塊保護 ⚠️

技術文檔校稿時，**程式碼區塊必須 100% 保持原樣**，這是最高優先級規則：

```
## ⚠️ 最重要規則：程式碼區塊絕對不可修改

1. **程式碼區塊必須 100% 保持原樣**
   - ` ```語言標記 ` 開頭和 ` ``` ` 結尾必須保留
   - 區塊內的所有程式碼、註解、字串都不可翻譯或修改
   - 包含 typescript、javascript、python、bash、json 等所有語言

2. **行內程式碼不可修改**
   - 反引號包圍的 `code` 內容保持原樣
   - 例如：`page.waitForLoadState('networkidle')` 不可變成 `page.waitForLoadState('網路idle')`

3. **程式碼中的英文字串不可翻譯**
   - API 參數值如 `'networkidle'`、`'POST'`、`'button'` 保持原文
   - 選擇器如 `'[data-testid="send-button"]'` 保持原文
```

### 臺灣慣用詞彙規則

| 正確用法（臺灣） | 錯誤用法（中國） |
|------------------|------------------|
| 帳號 | 賬號 |
| 資料 | 數據 |
| 軟體 | 軟件 |
| 網路 | 網絡 |
| 伺服器 | 服務器 |
| 記憶體 | 內存 |
| 視窗 | 窗口 |
| 預設 | 默認 |

### 校稿提示詞檔案位置

`scripts/config/proofreading_prompt.txt`

---

## ChatGPT Translator 技術細節

### nodriver 特點 ⭐
- **undetected-chromedriver 作者的新一代工具**
- 自動下載並管理 Chrome（不依賴系統版本）
- 內建反偵測，無需額外 stealth 設定
- Async/Await 非同步設計
- CAPTCHA 觸發率極低（<5%）
- **持久化瀏覽器資料目錄**（保存登入狀態）

### 翻譯頁面流程
1. 導航到 ChatGPT 翻譯專用頁面 `https://chatgpt.com/zh-Hant/translate/`
2. **使用 JavaScript 設定目標語言為「中文 (繁體，臺灣)」**
   - 透過 `<select>` 元素設定 `value='zh-TW'`
   - 觸發 `change` 事件通知頁面
3. 在左側輸入框貼上英文內容
4. **等待翻譯完成（智慧偵測）**
   - 監控輸出 textarea 的內容長度
   - 連續 3 次（約 9 秒）長度不變 → 翻譯完成
5. 從右側輸出框取得翻譯結果

### 智慧等待機制
```python
# 等待翻譯完成的策略：檢測輸出內容是否穩定
while time.time() - start_time < max_wait_time:
    current_length = len(output_textarea.value)

    if current_length == last_length:
        stable_count += 1
        if stable_count >= 3:  # 連續穩定 3 次
            break  # 翻譯完成
    else:
        stable_count = 0  # 重置

    last_length = current_length
    await asyncio.sleep(3)
```

---

## 使用方式

### 基本命令
```bash
# ChatGPT Translate（推薦）⭐
python scripts/translate.py --mode chatgpt docs/en/API.md

# 智慧降級模式（高可靠性）
python scripts/translate.py --mode auto docs/en/API.md
# → 優先 ChatGPT，失敗自動降級到 Google + 校稿

# Google Translate + 校稿（直接跳過 ChatGPT Translate）⭐ 新增
python scripts/translate.py --mode google+proofread docs/en/API.md
# → 可搭配 --proofreader chatgpt 使用 ChatGPT 對話頁面校稿

# Google Translate + ChatGPT 校稿（完整指定）
python scripts/translate.py --mode google+proofread --proofreader chatgpt --no-headless docs/en/API.md

# 顯示瀏覽器視窗（調試/手動 CAPTCHA）
python scripts/translate.py --mode chatgpt --no-headless docs/en/API.md

# Google Translate（快速、無校稿）
python scripts/translate.py --mode google docs/en/DRAFT.md

# 強制覆蓋已存在的譯文
python scripts/translate.py --mode chatgpt --force docs/en/*.md

# 指定降級時的校稿器
python scripts/translate.py --mode auto --proofreader chatgpt docs/en/API.md

# 禁用降級機制（ChatGPT 失敗就報錯）
python scripts/translate.py --mode auto --no-fallback docs/en/*.md

# 詳細日誌
python scripts/translate.py --mode chatgpt --verbose docs/en/API.md

# 批量翻譯
python scripts/translate.py --mode chatgpt docs/en/*.md
```

### 命令參數
| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--mode` | 翻譯模式 (chatgpt/auto/google+proofread/google) | chatgpt |
| `--proofreader` | 校稿後端 (auto/chatgpt/desktop/cli/manual) | auto |
| `--doc-type` | 文件類型，用於校稿時提供上下文 ⭐ 新增 | general |
| `--no-headless` | 顯示瀏覽器視窗 | False |
| `--no-fallback` | 禁用降級機制 | False |
| `--force` | 強制覆蓋已存在的譯文 | False |
| `--verbose` | 顯示詳細日誌 | False |

### --doc-type 文件類型選項 ⭐ 新增

指定文件類型可讓校稿器更精準地進行校對。校稿提示詞會自動加入文件背景資訊。

| 選項 | 說明 |
|------|------|
| `api` | API 技術文檔 |
| `srs` | 軟體需求規格書 (Software Requirements Specification) |
| `design` | 軟體設計文檔 |
| `user-guide` | 使用者手冊 |
| `tutorial` | 教學文件 |
| `readme` | README 專案說明 |
| `changelog` | 變更日誌 |
| `general` | 一般技術文檔（預設） |

**範例**:
```bash
# 翻譯 API 文檔
python scripts/translate.py --mode google+proofread --doc-type api docs/en/API.md

# 翻譯軟體需求規格書
python scripts/translate.py --mode google+proofread --doc-type srs docs/en/SRS.md
```

### Claude 應該如何協助用戶

當用戶說：
- "翻譯這個文件"
- "Translate this document"
- "幫我翻譯 API 文檔"

Claude 應該：
1. 確認檔案位置
2. **選擇 chatgpt 模式**（預設推薦）
3. 執行翻譯命令
4. 監控翻譯狀態
5. 驗證輸出
6. 報告翻譯結果

---

## 術語表管理

### 術語表位置
`scripts/config/glossary.json`

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

---

## 常見問題與故障排除

### 問題 1: CAPTCHA 驗證（罕見）
**現象**:
- 網頁出現「我不是機器人」驗證
- Cloudflare 攔截

**解決方式**:
```bash
# 使用有頭模式手動完成驗證
python scripts/translate.py --mode chatgpt --no-headless docs/en/API.md
# → 系統會等待 120 秒供手動完成驗證
# → 驗證完成後自動繼續翻譯
# → 驗證狀態會保存到瀏覽器資料目錄，下次不用再驗
```

**nodriver 的優勢**:
- CAPTCHA 觸發率 <5%（比 Selenium 的 50%+ 大幅改善）
- 瀏覽器資料持久化，驗證後的狀態會保存
- 下次使用同一個 Chrome Profile 時不需要再驗證

### 問題 2: 翻譯不完整就結束
**現象**:
- 翻譯結果被截斷
- 輸出字數明顯少於輸入

**原因**:
- 等待時間不足（長文檔需要更多時間）

**解決方式**:
- 系統已實作智慧等待機制（偵測輸出穩定）
- 最大等待時間會根據文字長度動態調整（60-180 秒）
- 如果仍有問題，可分段翻譯較長的文檔

### 問題 3: 語言選擇錯誤
**現象**:
- 翻譯結果不是繁體中文
- 輸出是其他語言

**原因**:
- 語言選擇器設定失敗

**解決方式**:
- 系統使用 JavaScript 直接設定 `<select>` 元素的值為 `zh-TW`
- 並觸發 `change` 事件通知頁面
- 如果仍有問題，使用 `--no-headless` 模式觀察

### 問題 4: nodriver 安裝問題
**現象**:
- `ModuleNotFoundError: No module named 'nodriver'`

**解決方式**:
```bash
pip install nodriver
```

### 問題 5: 瀏覽器無法啟動
**現象**:
- 錯誤訊息包含 Chrome 相關字樣

**解決方式**:
```bash
# nodriver 會自動下載 Chrome，但如果失敗：
# 1. 確保網路連線正常
# 2. 確保有足夠磁碟空間
# 3. 嘗試手動清除快取
rm -rf ~/.chatgpt-translator/chrome-profile/
```

---

## 效能與成本比較

| 模式 | 速度 | 品質 | 成功率 | CAPTCHA率 | 成本 |
|------|------|------|--------|----------|------|
| chatgpt (nodriver) ⭐ | ⚡⚡ | ⭐⭐⭐⭐⭐ | 95%+ | <5% | $0 |
| google+proofread ⭐ | ⚡ | ⭐⭐⭐⭐ | ~95% | <5% | $0 |
| google | ⚡⚡⚡ | ⭐⭐ | ~95% | 0% | $0 |

### nodriver vs 其他方案

| 面向 | nodriver ⭐ | Playwright | Selenium |
|------|------------|------------|----------|
| CAPTCHA 觸發率 | <5% | ~10% | 50-70% |
| 安裝複雜度 | 極簡單 | 中等 | 複雜 |
| 瀏覽器管理 | 自動下載 | 需安裝 | 需手動管理 |
| 反偵測能力 | 內建 | 需 stealth | 需大量配置 |
| Async 支援 | ✅ 原生 | ✅ | ❌ |
| 維護需求 | 極低 | 中等 | 高 |

---

## 瀏覽器資料持久化

### 資料目錄位置
`~/.chatgpt-translator/chrome-profile/`

### 持久化內容
- 登入狀態
- Cookie
- CAPTCHA 驗證狀態
- 瀏覽歷史

### 好處
- 首次驗證後，後續使用不需要再驗證
- 如果有 ChatGPT 帳號登入，狀態會保存
- 減少 CAPTCHA 觸發機率

### 清除資料
```bash
# 如果遇到奇怪問題，可以清除重來
rm -rf ~/.chatgpt-translator/chrome-profile/
```

---

## 相關檔案路徑

重要檔案位置：
- Python 主程式：`./scripts/translate.py`
- **ChatGPT 翻譯器（nodriver）**：`./scripts/translator/chatgpt_translator.py` ⭐
- Google 翻譯器：`./scripts/translator/google_translator.py`
- 術語表：`./scripts/config/glossary.json`
- 英文原文：`./docs/en/`
- 中文譯文：`./docs/zh-TW/`

### Python 依賴檔案
- 依賴清單：`./scripts/requirements.txt`
  - `nodriver>=0.38` ⭐
  - `requests>=2.31.0`
  - `deep-translator>=1.11.0`

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

4. **提供建議**
   - 解釋 nodriver 的優勢
   - 協助故障排除

---

## 範例對話

### 範例 1: 基本翻譯
```
用戶: "幫我翻譯 API 文檔"

Claude:
1. 確認檔案位置
2. 執行命令：
   python scripts/translate.py --mode chatgpt --verbose docs/en/API.md
3. 報告：「翻譯完成，使用了 ChatGPT Translate」
```

### 範例 2: CAPTCHA 處理
```
用戶: "翻譯時出現驗證"

Claude:
1. 說明：這是 CAPTCHA，nodriver 極少觸發
2. 解決方案：
   python scripts/translate.py --mode chatgpt --no-headless docs/en/API.md
3. 說明：手動完成驗證後，狀態會保存
```

### 範例 3: 批量翻譯
```
用戶: "翻譯所有文檔"

Claude:
1. 執行：
   python scripts/translate.py --mode chatgpt docs/en/*.md
2. 建議：如果檔案很多，可以分批執行
```

---

## 特別注意事項

### nodriver 環境
- **自動下載 Chrome**，不需要手動安裝
- 需要 Python 3.7+ 以支援 async/await
- 瀏覽器資料存放在 `~/.chatgpt-translator/chrome-profile/`

### CAPTCHA 處理
- nodriver 大幅降低 CAPTCHA 觸發率（<5%）
- 如果遇到 CAPTCHA，使用 `--no-headless` 模式
- 驗證後的狀態會保存，下次不用再驗

### 版本控制
- 英文文檔是權威來源
- 中文譯文自動生成，不應手動編輯
- 所有修改應在英文版進行

---

請根據以上資訊創建 document-translator skill 的 SKILL.md 檔案。

要求：
1. 結構清晰，易於 Claude 理解
2. 包含所有重要資訊
3. **重點強調 nodriver 的優勢**（相對於 Selenium/Playwright）⭐
4. **說明為什麼不使用本機 AI（TranslateGemma）**：效率太慢不實際 ⭐
5. **清楚說明翻譯模式的差異和使用場景**（chatgpt, google）⭐
6. **詳細解釋智慧等待機制**（偵測輸出穩定）⭐
7. **包含瀏覽器資料持久化說明**⭐
8. 提供足夠的範例，特別是 CAPTCHA 處理
9. 考慮實際使用場景
10. 使用 Markdown 格式
11. 加入適當的章節和目錄
12. 提供完整的命令參考
13. **包含完整的故障排除指南**⭐
14. 加入最佳實踐建議
15. **對比 nodriver vs Playwright vs Selenium 的差異**⭐

謝謝！
```

---

## 使用步驟

### 步驟 1: 複製提示詞

將上面「提示詞內容」區塊中的所有文字（從「請使用 skill-creator...」到「謝謝！」）複製。

### 步驟 2: 與 Claude 對話

在 Claude Desktop 或 Claude.ai 中貼上完整提示詞。

### 步驟 3: 等待生成

Claude 會使用 skill-creator skill 生成 document-translator skill 的 SKILL.md。

### 步驟 4: 放置檔案

將生成的 SKILL.md 放到：

```
/mnt/skills/user/document-translator/SKILL.md
```

---

## 版本歷史

- **v3.2.0 (2025-01-20): --doc-type 參數 + 校稿提示詞強化** ⭐
  - **新增 `--doc-type` 參數**（api/srs/design/user-guide/tutorial/readme/changelog/general）
  - 校稿提示詞自動加入文件類型背景資訊
  - **強化程式碼區塊保護規則**（最高優先級）
  - 更新校稿提示詞格式，防止程式碼內容被翻譯
  - ChatGPT 校稿器使用**內容穩定偵測機制**（連續 3 次長度不變 → 完成）

- **v3.1.0 (2025-01-20): ChatGPT 校稿器 + google+proofread 模式**
  - **新增 ChatGPT 校稿器**（使用 chatgpt.com 對話頁面）
  - **新增 `google+proofread` 翻譯模式**（直接 Google 粗翻 + 校稿）
  - ChatGPT 校稿器優先順序最高（priority=5）
  - 校稿器與翻譯器共用 Chrome Profile
  - 校稿後端新增 `--proofreader chatgpt` 選項

- **v3.0.0 (2025-01-20): nodriver 升級版**
  - **從 Playwright 遷移到 nodriver**
  - **移除 TranslateGemma**（本機端執行效率太慢不實際）
  - nodriver 內建反偵測，CAPTCHA 觸發率 <5%
  - 自動下載 Chrome，安裝更簡單
  - 瀏覽器資料持久化（保存驗證狀態）
  - 智慧等待機制（偵測輸出穩定）
  - 支援 ChatGPT 翻譯專用頁面的 `<select>` 語言選擇器

- v2.0.0 (2025-01-18): Playwright 升級版
  - 從 Selenium 遷移到 Playwright + Stealth
  - CAPTCHA 觸發率降低（50%+ → ~10%）
  - 新增 Async/Await 支援

- v1.0.0 (2025-01-16): 初始版本
  - 智慧降級翻譯策略
  - ChatGPT Translate 優先（Selenium）
  - Google Translate 備案機制

---

## 授權

本提示詞文檔採用 MIT License。

---

**文檔結束**
