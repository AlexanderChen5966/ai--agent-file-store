# doc-generator Agent Skill 安裝指南

## 📦 Skill 資訊

- **名稱**: doc-generator
- **版本**: 1.0.0
- **類型**: 專案級 Agent Skill
- **用途**: API 文件自動化生成

---

## 🎯 已完成事項

✅ **Skill 結構已建立**

```
.github/skills/doc-generator/
├── SKILL.md              # ⭐ 主要定義檔（Agent 讀取）
├── README.md             # 📖 說明文件
├── CHANGELOG.md          # 📝 版本記錄
├── USAGE_EXAMPLES.md     # 💡 使用範例
├── TESTING.md            # 🧪 測試指南
├── .skillignore          # 🚫 忽略文件
├── scripts/              # 📂 所有生成腳本（已複製）
│   ├── generate_all.sh
│   ├── api_to_postman.py
│   ├── convert_api_pdf.py
│   ├── convert_api_to_uml_flow.py
│   ├── dbml_to_png.py
│   ├── draw_schema.py
│   └── template.html
└── fonts/                # 🔤 字型文件（已複製）
    └── static/
        └── NotoSansTC-*.ttf
```

✅ **符合 GitHub Copilot Skills 規範**
- YAML frontmatter 格式正確
- name 使用小寫和連字號
- 包含 version 欄位
- description 包含觸發關鍵字
- Markdown 內容完整

✅ **不修改原始程式碼**
- 所有腳本從根目錄**複製**
- 原始檔案保持不變
- Skill 獨立運作

---

## 🚀 如何使用

### 方式 1: 專案內使用（預設）

Skill 已安裝在專案中，無需額外操作！

**直接對 GitHub Copilot 說**：

```
"產生 API 文件"
"建立所有文件"  
"生成 Postman Collection"
```

Copilot 會自動：
1. 識別 doc-generator skill
2. 檢查專案環境
3. 執行對應的生成腳本
4. 報告結果

### 方式 2: 安裝為全域 Skill（可選）

如果想在所有專案中使用此 Skill：

```bash
# 複製到個人 skills 目錄
mkdir -p ~/.copilot/skills
cp -r .github/skills/doc-generator ~/.copilot/skills/

# 重啟 GitHub Copilot CLI
```

---

## 🧪 驗證安裝

### 1. 檢查 Skill 文件

```bash
# 確認主文件存在
cat .github/skills/doc-generator/SKILL.md | head -10

# 應該看到 YAML frontmatter
```

### 2. 驗證腳本完整性

```bash
ls -1 .github/skills/doc-generator/scripts/

# 應該看到 7 個文件：
# ✅ generate_all.sh
# ✅ api_to_postman.py
# ✅ convert_api_pdf.py
# ✅ convert_api_to_uml_flow.py
# ✅ dbml_to_png.py
# ✅ draw_schema.py
# ✅ template.html
```

### 3. 測試功能（可選）

```bash
# 手動執行測試
./generate_all.sh

# 驗證輸出
ls -la delivery_doc/
```

---

## 📚 文件說明

### 核心文件

1. **SKILL.md** ⭐
   - GitHub Copilot Agent 讀取的主要定義文件
   - 包含完整的使用指南、範例和錯誤處理
   - **不要刪除或重命名此文件**

2. **README.md**
   - 給人類閱讀的說明文件
   - 包含目錄結構和快速開始指南

3. **CHANGELOG.md**
   - 版本變更記錄
   - 每次更新都應該記錄

4. **USAGE_EXAMPLES.md**
   - 實際使用範例
   - 包含各種情境的提示詞

5. **TESTING.md**
   - 測試和驗證指南
   - 用於確保 Skill 正常運作

---

## 🎨 功能清單

### 支援的文件生成

| 功能 | 腳本 | 輸出 |
|------|------|------|
| Postman Collection | `api_to_postman.py` | `washcar_api.json` |
| PDF 文件 | `convert_api_pdf.py` | `washcar_api.pdf` |
| UML 流程圖 | `convert_api_to_uml_flow.py` | `Wash_Car_API_Flow.png` |
| DB 架構圖 | `dbml_to_png.py` | `Table_scheme.png` |
| 全部生成 | `generate_all.sh` | 以上全部 |

### 觸發關鍵字

- "產生文件"
- "建立 API 文件"
- "生成 Postman"
- "產生流程圖"
- "建立資料庫架構圖"

---

## 🔧 維護指南

### 更新 Skill

當專案根目錄的腳本更新時：

```bash
# 1. 重新複製腳本
cp -r generate_all.sh api_to_postman.py convert_api_pdf.py \
      convert_api_to_uml_flow.py dbml_to_png.py draw_schema.py \
      template.html \
      .github/skills/doc-generator/scripts/

# 2. 更新版本號
# 編輯 .github/skills/doc-generator/SKILL.md
# version: 1.0.0 -> 1.1.0

# 3. 記錄變更
# 編輯 .github/skills/doc-generator/CHANGELOG.md

# 4. 提交
git add .github/skills/doc-generator/
git commit -m "chore: Update doc-generator skill to v1.1.0"
```

### 版本規則

遵循 [Semantic Versioning](https://semver.org/)：

- **MAJOR** (1.x.x): 不相容的 API 變更
- **MINOR** (x.1.x): 新增功能（向下相容）
- **PATCH** (x.x.1): Bug 修復（向下相容）

---

## 🐛 疑難排解

### Skill 沒有被偵測到

**解決方案**：
1. 確認 `.github/skills/doc-generator/SKILL.md` 存在
2. 重啟 GitHub Copilot CLI
3. 檢查 YAML frontmatter 格式

### 執行時找不到文件

**原因**：腳本設計為從專案根目錄執行

**解決方案**：
```bash
# 確保在專案根目錄
cd /Users/alexander/Desktop/washcar

# 然後執行
./generate_all.sh
```

### 更多問題

參考 `TESTING.md` 中的詳細測試指南。

---

## 📖 延伸閱讀

- [USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md) - 使用範例
- [TESTING.md](./TESTING.md) - 測試指南
- [CHANGELOG.md](./CHANGELOG.md) - 版本歷史
- [專案文件](../../../docs/) - 原專案文件

---

## 📄 授權

本 Skill 供內部使用。

---

## ✅ 安裝完成！

你現在可以：
1. ✨ 直接對 GitHub Copilot 說「產生 API 文件」
2. 🚀 Skill 會自動處理所有技術細節
3. 📦 所有輸出文件會生成在 `delivery_doc/` 目錄

**享受自動化文件生成的便利！** 🎉
