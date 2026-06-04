# API 文件生成工具 Agent Skill

## 概述

這是一個 GitHub Copilot Agent Skill，專為自動化 API 文件生成設計。

## 目錄結構

```
.github/skills/doc-generator/
├── SKILL.md              # Skill 主要定義檔（給 Agent 讀取）
├── README.md             # 本文件（給人類閱讀）
├── scripts/              # 所有生成腳本（從專案根目錄複製）
│   ├── generate_all.sh
│   ├── api_to_postman.py
│   ├── convert_api_pdf.py
│   ├── convert_api_to_uml_flow.py
│   ├── dbml_to_png.py
│   ├── draw_schema.py
│   └── template.html
└── fonts/                # 字型文件（從專案根目錄複製）
```

## 使用方式

### 在專案中使用

1. 確保你在包含此 Skill 的專案根目錄
2. 對 GitHub Copilot 說出觸發關鍵字：
   - "產生 API 文件"
   - "建立所有文件"
   - "生成 Postman Collection"
   - "產生流程圖"

3. Copilot 會自動：
   - 檢測專案環境
   - 執行對應的生成腳本
   - 驗證輸出結果

### 安裝為全域 Skill（可選）

如果想在所有專案中使用此 Skill：

```bash
# 複製到個人 skills 目錄
cp -r .github/skills/doc-generator ~/.copilot/skills/

# 重啟 GitHub Copilot CLI
```

## 功能列表

1. ✅ **Postman Collection 生成** - 從 Markdown 產生可匯入的 API 測試集合
2. ✅ **PDF 文件生成** - 轉換為格式化的 PDF 文件
3. ✅ **UML 流程圖生成** - PlantUML 時序圖
4. ✅ **資料庫架構圖生成** - ER Diagram

## 系統需求

- Python 3.7+
- macOS 或 Linux
- Homebrew (macOS) 或 apt-get (Linux)

## 腳本說明

所有腳本都是從專案根目錄複製而來，**不會修改原始檔案**。

### 為什麼複製？

1. **隔離性** - Skill 獨立運作，不影響原專案
2. **可攜性** - 可以輕鬆分享或移植到其他專案
3. **版本控制** - Skill 有自己的版本管理

### 執行位置

腳本執行時會：
1. 從專案**根目錄**讀取輸入檔案（`API_DOCUMENT.md`）
2. 輸出到專案根目錄的 `delivery_doc/` 資料夾

**注意**：不要直接在 `.github/skills/doc-generator/scripts/` 中執行腳本！

## 版本資訊

- **Skill 版本**: 1.0.0
- **相容專案**: washcar API 文件生成專案
- **最後更新**: 2026-01-28

## 授權

本 Skill 供內部使用。

## 疑難排解

如遇到問題，請參考：
1. `SKILL.md` 中的「錯誤處理」章節
2. 專案根目錄的 `docs/TROUBLESHOOTING.md`

## 貢獻

如需修改此 Skill：
1. 修改專案根目錄的原始腳本
2. 重新複製到 `.github/skills/doc-generator/scripts/`
3. 更新 `SKILL.md` 的版本號和說明
