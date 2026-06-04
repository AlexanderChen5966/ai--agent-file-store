# Document Translator Skill

> **Version**: 3.2.2 | 技術文檔翻譯系統

使用智慧降級翻譯策略 + nodriver 反偵測自動化，提供高品質的英文→繁體中文技術文檔翻譯。

## ✨ 特色功能

- 🎯 **智慧降級策略**：ChatGPT 優先，失敗自動降級到 Google + 校稿
- 🔒 **反偵測技術**：使用 nodriver，CAPTCHA 觸發率 <5%
- 🤖 **多種校稿後端**：ChatGPT、Claude Desktop、Claude CLI、手動校稿
- 📝 **程式碼保護**：翻譯時自動保護程式碼區塊不被修改
- 🌏 **臺灣用語**：使用臺灣慣用詞彙（帳號、資料、軟體等）
- 📊 **術語表管理**：自訂技術術語翻譯規則

## 🚀 快速開始

### 1. 安裝依賴

```bash
cd scripts
pip install -r requirements.txt
```

主要依賴：
- `nodriver>=0.38` - 反偵測自動化
- `deep-translator>=1.11.0` - Google Translate

### 2. 基本使用

```bash
# ChatGPT Translate（推薦）
python scripts/translate.py --mode chatgpt docs/en/FILE.md

# 智慧降級模式（高可靠性）
python scripts/translate.py --mode auto docs/en/FILE.md

# Google Translate + ChatGPT 校稿
python scripts/translate.py --mode google+proofread --proofreader chatgpt docs/en/FILE.md
```

### 3. 支援的檔案格式

✅ **主要支援**：
- `.md` - Markdown（推薦）
- `.txt` - 純文字
- `.rst` - reStructuredText
- `.html` - HTML 檔案

❌ **不支援**：
- `.docx`、`.pdf`、`.xlsx` 等二進位格式
- 請參考 [SKILL.md](./SKILL.md#支援的檔案格式) 了解處理方法

## 📖 文件結構

```
document-translator/
├── SKILL.md                      # Skill 主文件（給 Claude 閱讀）
├── README.md                     # 快速開始指南（本文件）
├── scripts/
│   ├── translate.py              # 主程式
│   ├── translate.sh              # Shell 腳本入口
│   ├── requirements.txt          # Python 依賴
│   ├── config/
│   │   ├── glossary.json         # 術語表
│   │   └── proofreading_prompt.txt  # 校稿提示詞
│   └── translator/               # 翻譯器模組
│       ├── chatgpt_translator.py
│       ├── chatgpt_proofreader.py
│       ├── google_translator.py
│       └── ...
└── references/                   # 參考文件
    ├── examples.md               # 使用範例
    ├── troubleshooting.md        # 故障排除
    ├── backends.md               # 翻譯器與校稿後端說明
    ├── advanced.md               # 進階功能
    └── cicd.md                   # CI/CD 整合
```

## 🎨 使用場景

### 場景 1: 翻譯 API 文檔

```bash
python scripts/translate.py --mode chatgpt --doc-type api docs/en/API.md
```

### 場景 2: 批量翻譯

```bash
python scripts/translate.py --mode chatgpt docs/en/*.md
```

### 場景 3: 處理 CAPTCHA

```bash
# 使用有頭模式手動驗證
python scripts/translate.py --mode chatgpt --no-headless docs/en/API.md
```

### 場景 4: Google + 校稿（品質與速度平衡）

```bash
python scripts/translate.py --mode google+proofread --proofreader chatgpt docs/en/FILE.md
```

### 🛡️ CAPTCHA 處理

首次使用 ChatGPT Translate 可能遇到 CAPTCHA 驗證：

**方式 1：手動驗證一次（推薦給經常使用者）**
```bash
# 使用有頭模式手動完成驗證
python scripts/translate.py --mode chatgpt --no-headless docs/en/FILE.md

# 驗證完成後，狀態會保存在 ~/.chatgpt-translator/chrome-profile-v3/
# 之後使用 headless 模式就不會再遇到 CAPTCHA
```

**方式 2：使用 Google + ChatGPT 校稿（無需驗證）**
```bash
# 這個模式完全不會遇到 CAPTCHA，品質也很好
python scripts/translate.py --mode google+proofread --proofreader chatgpt docs/en/FILE.md
```

## 🔧 命令參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--mode` | 翻譯模式 (chatgpt/auto/google+proofread/google) | chatgpt |
| `--proofreader` | 校稿後端 (auto/chatgpt/desktop/cli/manual) | auto |
| `--doc-type` | 文件類型 (api/srs/design/tutorial/etc) | general |
| `--no-headless` | 顯示瀏覽器視窗 | False |
| `--force` | 強制覆蓋已存在的譯文 | False |
| `--verbose` | 顯示詳細日誌 | False |

## 📚 詳細文件

- **[SKILL.md](./SKILL.md)** - 完整的 Skill 說明文件
- **[使用範例](./references/examples.md)** - 9 個實用範例
- **[故障排除](./references/troubleshooting.md)** - 常見問題解決方案
- **[翻譯器說明](./references/backends.md)** - 翻譯器與校稿後端詳解
- **[進階功能](./references/advanced.md)** - 自訂提示詞、術語表管理
- **[CI/CD 整合](./references/cicd.md)** - GitLab CI/CD、GitHub Actions

## 🌟 翻譯品質

| 模式 | 品質 | 成功率 | CAPTCHA | 速度 |
|------|------|--------|---------|------|
| `chatgpt` | ⭐⭐⭐⭐⭐ | 95%+ | <5% | 中等 |
| `auto` | ⭐⭐⭐⭐⭐ | 98%+ | <5% | 中等 |
| `google+proofread` | ⭐⭐⭐⭐ | ~95% | 0% | 快速 |
| `google` | ⭐⭐ | ~95% | 0% | 最快 |

## 🤝 在 Claude Code 中使用

### 觸發關鍵字

- 「翻譯」、「translate」
- 「術語表」、「glossary」
- 「校稿」、「proofread」
- 「document-translator」

### 使用範例

```
用戶: 幫我翻譯 docs/en/API.md

Claude: 我來幫您翻譯 API 文檔。
[執行 document-translator skill]
```

## ⚠️ 重要注意事項

1. **檔案格式限制**：目前僅支援純文字格式（Markdown、TXT 等），不支援 Word、PDF
2. **英文為權威來源**：所有修改應在英文版進行，中文自動生成
3. **程式碼保護**：翻譯和校稿時絕對不可修改程式碼區塊
4. **瀏覽器資料**：驗證狀態保存在 `~/.chatgpt-translator/chrome-profile/`

## 🔄 版本歷史

### v3.2.2 (2026-02-06) - Bug 修復版
- 🐛 修復 macOS 瀏覽器連接問題（sandbox 設定）
- 🐛 修復 asyncio 事件循環錯誤
- 🔧 更新 Chrome Profile 資料夾（chrome-profile-v3）
- 📝 新增 CAPTCHA 處理說明
- ✅ 測試確認所有翻譯模式正常運作

### v3.2.1 (2026-02-06)
- 新增「支援的檔案格式」說明
- 更新 troubleshooting.md 加入檔案格式問題
- 新增純文字檔案翻譯範例

### v3.2.0 (2025-01-20)
- 新增 `--doc-type` 參數
- 強化校稿提示詞
- 新增 ChatGPT 校稿器

### v3.0.0 (2025-01-20)
- 從 Playwright 遷移到 nodriver
- CAPTCHA 觸發率降至 <5%

## 📧 問題回報

如有問題或建議，請參考 [故障排除指南](./references/troubleshooting.md)。

---

**License**: MIT
**Author**: Document Translator Team
**Powered by**: nodriver, ChatGPT, Google Translate
