# Skill 測試與驗證

## 驗證 Skill 結構

### 1. 檢查必要文件
bash
在專案根目錄執行
ls -la .github/skills/doc-generator/
應該看到：
✅ SKILL.md          - 主要定義檔
✅ README.md         - 說明文件  
✅ CHANGELOG.md      - 版本記錄
✅ INSTALL.md        - 安裝指南
✅ USAGE_EXAMPLES.md - 使用範例
✅ scripts/          - 腳本目錄
✅ fonts/            - 字型目錄


### 2. 驗證 SKILL.md 格式
bash
檢查 YAML frontmatter
head -10 .github/skills/doc-generator/SKILL.md


### 3. 執行測試
bash
在專案根目錄測試
./generate_all.sh
驗證輸出
ls -la delivery_doc/

