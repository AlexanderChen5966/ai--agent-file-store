---
name: document-translator
version: 3.2.2
description: 技術文檔翻譯系統助手，使用智慧降級翻譯策略 + nodriver 反偵測自動化。優先使用 ChatGPT Translate（CAPTCHA 觸發率 <5%），失敗時自動降級到 Google Translate + 校稿。支援 Markdown 及純文字檔案。已修復 macOS 瀏覽器連接問題。使用時機：(1) 翻譯技術文檔 (2) 管理術語表 (3) 選擇翻譯模式或校稿後端 (4) 故障排除。觸發關鍵字：「翻譯」「translate」「術語表」「glossary」「校稿」「proofread」「document-translator」。
---

# Document Translator Skill

> **Version**: 3.2.2 | **Last Updated**: 2026-02-06

技術文檔翻譯系統助手，使用**智慧降級翻譯策略 + nodriver 反偵測自動化**提供高品質翻譯。

## v3.2.0 重大更新

### 新功能
- **`--doc-type` 參數**：指定文件類型，讓校稿更精準
- **強化校稿提示詞**：程式碼區塊保護規則（最高優先級）
- **ChatGPT 校稿器**：使用 chatgpt.com 對話頁面進行校稿
- **`google+proofread` 模式**：直接 Google 粗翻 + 校稿

### nodriver 技術（v3.0.0 引入）
| 特性 | Selenium | Playwright | nodriver |
|------|----------|------------|----------|
| CAPTCHA 觸發率 | 50-70% | ~10% | **<5%** |
| 安裝複雜度 | 複雜 | 中等 | **極簡單** |
| 瀏覽器管理 | 手動 | 需安裝 | **自動下載** |
| 反偵測能力 | 需大量配置 | 需 stealth | **內建** |

## 智慧降級翻譯策略

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

## 快速開始

```bash
# ChatGPT Translate（推薦）
python scripts/translate.py --mode chatgpt docs/en/FILE.md

# 智慧降級模式（高可靠性）
python scripts/translate.py --mode auto docs/en/FILE.md

# Google Translate + ChatGPT 校稿 ⭐ 新增
python scripts/translate.py --mode google+proofread --proofreader chatgpt docs/en/FILE.md

# 指定文件類型（校稿更精準）⭐ 新增
python scripts/translate.py --mode google+proofread --doc-type api docs/en/API.md
python scripts/translate.py --mode google+proofread --doc-type tutorial docs/en/GUIDE.md

# 顯示瀏覽器視窗（調試/手動 CAPTCHA）
python scripts/translate.py --mode chatgpt --no-headless docs/en/FILE.md

# 批量翻譯
python scripts/translate.py --mode chatgpt docs/en/*.md

# 強制覆蓋 + 詳細日誌
python scripts/translate.py --mode chatgpt --force --verbose docs/en/FILE.md
```

## 支援的檔案格式

### ✅ 主要支援：Markdown 檔案

此 skill **主要設計用於翻譯 Markdown (.md) 技術文檔**：
- API 文檔
- README 專案說明
- 技術教學
- 變更日誌
- 軟體需求規格書

### ✅ 也可處理：純文字檔案

由於使用 UTF-8 文字讀取，**理論上也支援**：
- `.txt` - 純文字檔案
- `.rst` - reStructuredText
- `.html` - HTML 檔案
- 其他 UTF-8 純文字格式

```bash
# 翻譯純文字檔案
python scripts/translate.py --mode chatgpt docs/en/README.txt
```

### ❌ 不支援：二進位檔案

目前**無法直接處理**以下格式：
- `.docx` - Word 文件
- `.pdf` - PDF 文件
- `.xlsx` - Excel 檔案

### 💡 處理 Word/PDF 檔案的解決方案

如需翻譯 Word 或 PDF 檔案，可以結合其他 skills：

```bash
# 方案 1: 使用 docx skill 處理 Word 檔案
# 1. 讀取 .docx 內容
# 2. 提取純文字並儲存為 .md
# 3. 使用 document-translator 翻譯
# 4. 再寫回 .docx

# 方案 2: 使用 pdf skill 處理 PDF 檔案
# 1. 使用 pdf skill 提取文字
# 2. 儲存為 .md 格式
# 3. 使用 document-translator 翻譯
```

**建議工作流程**：
1. 將 Word/PDF 轉換為 Markdown
2. 使用本 skill 翻譯 Markdown
3. 如需要，再轉回原格式

## 命令參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--mode` | 翻譯模式 (chatgpt/auto/google+proofread/google) | chatgpt |
| `--proofreader` | 校稿後端 (auto/chatgpt/desktop/cli/manual) | auto |
| `--doc-type` | 文件類型，用於校稿時提供上下文 | general |
| `--no-headless` | 顯示瀏覽器視窗 | False |
| `--no-fallback` | 禁用降級機制 | False |
| `--force` | 強制覆蓋已存在的譯文 | False |
| `--verbose` | 顯示詳細日誌 | False |

### --doc-type 文件類型選項

| 選項 | 說明 |
|------|------|
| `api` | API 技術文檔 |
| `srs` | 軟體需求規格書 (SRS) |
| `design` | 軟體設計文檔 |
| `user-guide` | 使用者手冊 |
| `tutorial` | 教學文件 |
| `readme` | README 專案說明 |
| `changelog` | 變更日誌 |
| `general` | 一般技術文檔（預設）|

## 翻譯模式

| 模式 | 說明 | 品質 | 成功率 | CAPTCHA |
|------|------|------|--------|---------|
| `chatgpt` | ChatGPT Translate (nodriver) | ⭐⭐⭐⭐⭐ | 95%+ | <5% |
| `auto` | ChatGPT + 智慧降級 | ⭐⭐⭐⭐⭐ | 98%+ | <5% |
| `google+proofread` | Google + 校稿 | ⭐⭐⭐⭐ | ~95% | <5% |
| `google` | 僅 Google Translate | ⭐⭐ | ~95% | 0% |

## 校稿後端

| 後端 | 說明 | 優先順序 |
|------|------|----------|
| `auto` | 自動偵測可用後端 | - |
| `chatgpt` | ChatGPT 對話頁面 (nodriver) | 1（最高）|
| `desktop` | Claude Desktop GUI | 2 |
| `cli` | Claude CLI 命令列 | 3 |
| `manual` | 文字編輯器手動校稿 | 4 |

### ChatGPT 校稿器特點
- 使用 chatgpt.com 對話頁面
- 與翻譯器共用 Chrome Profile
- **內容穩定偵測**：連續 3 次（約 9 秒）長度不變 → 完成

## 校稿提示詞

### 程式碼區塊保護（最高優先級）

技術文檔校稿時，程式碼區塊必須 100% 保持原樣：

1. **程式碼區塊**：` ```語言 ` 和 ` ``` ` 之間的內容不可修改
2. **行內程式碼**：反引號 `` ` `` 包圍的內容保持原樣
3. **英文字串**：`'networkidle'`、`'POST'` 等保持原文

### 臺灣慣用詞彙

| 正確（臺灣） | 錯誤（中國） |
|--------------|--------------|
| 帳號 | 賬號 |
| 資料 | 數據 |
| 軟體 | 軟件 |
| 網路 | 網絡 |
| 伺服器 | 服務器 |
| 記憶體 | 內存 |
| 預設 | 默認 |

## Skill 目錄結構

```
document-translator/
├── SKILL.md                 # 本文件
├── scripts/
│   ├── translate.py         # Python 主程式
│   ├── requirements.txt     # Python 依賴
│   ├── translator/          # 翻譯器模組
│   │   ├── chatgpt_translator.py    # ChatGPT 翻譯 (nodriver)
│   │   ├── chatgpt_proofreader.py   # ChatGPT 校稿 (nodriver) ⭐
│   │   ├── google_translator.py     # Google 翻譯
│   │   └── proofreader_factory.py   # 校稿器工廠
│   └── config/
│       ├── glossary.json            # 術語表
│       └── proofreading_prompt.txt  # 校稿提示詞
└── references/              # 參考文件
```

## 環境設定

### 安裝依賴

```bash
cd scripts
pip install -r requirements.txt
# 主要依賴：nodriver>=0.38, deep-translator>=1.11.0
```

### nodriver 優勢
- **自動下載 Chrome**：不依賴系統版本
- **內建反偵測**：無需額外 stealth 設定
- **瀏覽器資料持久化**：登入狀態保存

### 瀏覽器資料目錄

位置：`~/.chatgpt-translator/chrome-profile/`

清除資料（如遇問題）：
```bash
rm -rf ~/.chatgpt-translator/chrome-profile/
```

## Claude 職責

### 執行翻譯

1. **確認檔案** - 檢查來源檔案在 `docs/en/`
2. **選擇模式** - 預設使用 `--mode chatgpt`
3. **指定文件類型** - 使用 `--doc-type` 讓校稿更精準
4. **執行命令** - 使用 Bash 執行
5. **監控狀態** - 觀察翻譯進度和 CAPTCHA 情況
6. **驗證結果** - 確認 `docs/zh-TW/` 已生成

### 翻譯策略建議

```bash
# API 文檔
python scripts/translate.py --mode chatgpt --doc-type api docs/en/API.md

# 教學文件
python scripts/translate.py --mode google+proofread --doc-type tutorial docs/en/GUIDE.md

# 快速草稿
python scripts/translate.py --mode google docs/en/DRAFT.md
```

## 常見問題

### CAPTCHA 驗證

```bash
# 使用有頭模式手動完成驗證
python scripts/translate.py --mode chatgpt --no-headless docs/en/API.md
# 驗證後狀態會保存，下次不用再驗
```

### nodriver 安裝問題

```bash
pip install nodriver
# nodriver 會自動下載 Chrome
```

### 翻譯品質不佳

```bash
# 使用 ChatGPT 校稿
python scripts/translate.py --mode google+proofread --proofreader chatgpt docs/en/FILE.md

# 指定文件類型
python scripts/translate.py --mode google+proofread --doc-type api docs/en/API.md
```

### 如何翻譯 Word 或 PDF 檔案？

目前 skill 無法直接處理二進位檔案。建議工作流程：

```bash
# 方案 1: 手動轉換
# 1. 將 Word/PDF 內容複製到 .md 檔案
# 2. 使用本 skill 翻譯
# 3. 再複製回原檔案

# 方案 2: 使用其他 skills 配合
# - 使用 docx skill 讀取 Word 內容
# - 使用 pdf skill 提取 PDF 文字
# - 轉換為 .md 後使用本 skill 翻譯
```

**提示**：純文字檔案 (.txt) 可以直接翻譯，不需要轉換。

## 術語表

位置：`scripts/config/glossary.json`

```json
{
  "technical_terms": {
    "API": "API",
    "endpoint": "端點"
  },
  "taiwan_terms": {
    "account": "帳號",
    "data": "資料"
  },
  "preserve": ["Claude", "GitHub"]
}
```

## 重要注意

- **英文是權威來源** - 所有修改應在英文版進行
- **中文自動生成** - 不應手動編輯 `docs/zh-TW/`
- **程式碼區塊** - 校稿時絕對不可修改程式碼

---

## 版本歷史

### v3.2.2 (2026-02-06) - Bug 修復版
- 🐛 修復 macOS 瀏覽器連接問題（sandbox 設定）
- 🐛 修復 asyncio 事件循環錯誤（__del__ 方法）
- 🔧 更新 Chrome Profile 資料夾名稱（chrome-profile-v3）
- 📝 改進錯誤訊息和除錯資訊
- ✅ 測試確認 Google + ChatGPT 校稿模式正常運作

### v3.2.1 (2026-02-06) - 文件改進
- 新增「支援的檔案格式」章節，明確說明支援範圍
- 說明可處理 Markdown、純文字檔案
- 提供 Word/PDF 檔案的處理建議
- 更新 description 加入檔案格式資訊

### v3.2.0 (2025-01-20) - --doc-type 參數 + 校稿強化
- 新增 `--doc-type` 參數（api/srs/design/user-guide/tutorial/readme/changelog/general）
- 校稿提示詞自動加入文件類型背景資訊
- 強化程式碼區塊保護規則（最高優先級）
- ChatGPT 校稿器使用內容穩定偵測機制

### v3.1.0 (2025-01-20) - ChatGPT 校稿器 + google+proofread 模式
- 新增 ChatGPT 校稿器（使用 chatgpt.com 對話頁面）
- 新增 `google+proofread` 翻譯模式
- 校稿器與翻譯器共用 Chrome Profile

### v3.0.0 (2025-01-20) - nodriver 升級版
- 從 Playwright 遷移到 nodriver
- CAPTCHA 觸發率降至 <5%
- 自動下載 Chrome，安裝更簡單
- 瀏覽器資料持久化

### v2.0.0 (2025-01-18) - Playwright 升級版
- 從 Selenium 遷移到 Playwright + Stealth
- CAPTCHA 觸發率降至 ~10%

### v1.0.0 (2025-01-16) - 初始版本
- 智慧降級翻譯策略
- ChatGPT Translate 優先（Selenium）
