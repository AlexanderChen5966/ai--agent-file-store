# Document Translator Skill - 安裝指南

> **Version**: 3.2.2 | Bug 修復版

## 📦 套件內容

本套件包含：
- `document-translator-skill-v3.2.2.tar.gz` - Linux/macOS 壓縮檔（52KB）
- `document-translator-skill-v3.2.2.zip` - Windows/通用壓縮檔（67KB）
- `INSTALL.md` - 本安裝指南

## ✨ v3.2.2 修復內容

- ✅ 修復 macOS 瀏覽器連接問題
- ✅ 修復 asyncio 事件循環錯誤
- ✅ 更新 Chrome Profile 資料夾名稱
- ✅ 新增 CAPTCHA 處理說明
- ✅ 測試確認所有翻譯模式正常運作

## 🚀 快速安裝

### 方式 1: 使用安裝腳本（推薦）

#### Linux / macOS

```bash
# 解壓縮
tar -xzf document-translator-skill-v3.2.2.tar.gz
cd document-translator

# 執行安裝腳本
./install.sh
```

#### Windows

```cmd
# 解壓縮 zip 檔案
# 然後開啟 PowerShell 或 CMD

cd document-translator

# 手動安裝（參考下方「方式 2」）
```

### 方式 2: 手動安裝

```bash
# 1. 解壓縮檔案
tar -xzf document-translator-skill-v3.2.2.tar.gz  # Linux/macOS
# 或
unzip document-translator-skill-v3.2.2.zip         # Windows

# 2. 進入目錄
cd document-translator

# 3. 安裝 Python 依賴
cd scripts
pip install -r requirements.txt

# 4. 測試安裝
python translate.py --help
```

## 📁 安裝到 Claude Code

### Claude Desktop (GUI) 使用者

將 `document-translator` 資料夾複製到 Claude skills 目錄：

```bash
# macOS
cp -r document-translator ~/.claude/skills/

# Linux
cp -r document-translator ~/.claude/skills/

# Windows
# 複製到 %USERPROFILE%\.claude\skills\
```

### Claude CLI 使用者

```bash
# 將 skill 加入 Claude CLI
claude skill add document-translator

# 或手動複製到 skills 目錄
cp -r document-translator ~/.claude/skills/
```

## ✅ 驗證安裝

### 1. 測試 Python 程式

```bash
cd document-translator/scripts

# 測試基本功能
python translate.py --help

# 測試 Google Translate（不需登入）
python translate.py --mode google test.md
```

### 2. 測試 Skill（在 Claude Code 中）

```
用戶: 檢查 document-translator skill 是否已安裝

Claude 應該能夠識別並載入這個 skill
```

## 📋 目錄結構

安裝後的目錄結構：

```
document-translator/
├── README.md                      # 快速開始指南
├── SKILL.md                       # Skill 主文件
├── install.sh                     # 自動安裝腳本
├── .gitignore                     # Git 忽略檔案
├── MANIFEST.txt                   # 檔案清單
├── scripts/
│   ├── translate.py               # 主程式
│   ├── translate.sh               # Shell 入口
│   ├── requirements.txt           # Python 依賴
│   ├── config/
│   │   ├── glossary.json          # 術語表
│   │   └── proofreading_prompt.txt
│   └── translator/                # 翻譯器模組
└── references/                    # 參考文件
    ├── examples.md
    ├── troubleshooting.md
    ├── backends.md
    ├── advanced.md
    └── cicd.md
```

## 🔧 系統需求

### 必要條件

- **Python**: 3.7 或更高版本
- **pip**: Python 套件管理工具
- **網路連線**: 用於下載依賴和執行翻譯

### 建議配置

- **記憶體**: 至少 2GB RAM
- **磁碟空間**: 500MB（包含 Python 套件和瀏覽器）
- **作業系統**:
  - macOS 10.14+
  - Ubuntu 18.04+
  - Windows 10+

## 🎯 開始使用

### 基本翻譯

```bash
cd document-translator

# 準備測試檔案
mkdir -p docs/en
echo "# Hello World" > docs/en/test.md

# 執行翻譯
python scripts/translate.py --mode chatgpt docs/en/test.md

# 查看結果
cat docs/zh-TW/test.md
```

### 查看文件

```bash
# 快速開始
cat README.md

# 使用範例
cat references/examples.md

# 故障排除
cat references/troubleshooting.md
```

## 🐛 故障排除

### 問題 1: 找不到 Python

```bash
# 安裝 Python 3
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3 python3-pip

# Windows
# 從 python.org 下載並安裝
```

### 問題 2: pip 安裝失敗

```bash
# 升級 pip
pip install --upgrade pip

# 使用虛擬環境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

pip install -r scripts/requirements.txt
```

### 問題 3: nodriver 無法安裝

```bash
# 確認 Python 版本
python3 --version  # 需要 3.7+

# 手動安裝
pip install nodriver>=0.38
```

### 問題 4: 權限錯誤

```bash
# Linux/macOS
chmod +x install.sh
chmod +x scripts/translate.sh

# 或使用 sudo（不建議）
sudo pip install -r scripts/requirements.txt
```

## 📚 進階安裝

### 使用虛擬環境（推薦）

```bash
cd document-translator/scripts

# 建立虛擬環境
python3 -m venv venv

# 啟用虛擬環境
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 安裝依賴
pip install -r requirements.txt

# 後續使用時記得啟用虛擬環境
```

### 開發模式安裝

```bash
cd document-translator/scripts

# 安裝開發依賴
pip install -e .

# 執行測試
python -m pytest tests/
```

### Docker 容器化（選用）

```bash
cd document-translator

# 建立 Docker 映像
docker build -t document-translator:3.2.1 .

# 執行翻譯
docker run -v $(pwd)/docs:/app/docs document-translator:3.2.1 \
  python scripts/translate.py --mode google docs/en/test.md
```

## 🔄 升級

### 從舊版本升級

```bash
# 備份自訂配置
cp scripts/config/glossary.json ~/glossary.json.bak
cp scripts/config/proofreading_prompt.txt ~/proofreading_prompt.txt.bak

# 刪除舊版本
rm -rf document-translator

# 安裝新版本（重複上述安裝步驟）

# 恢復自訂配置
cp ~/glossary.json.bak document-translator/scripts/config/glossary.json
cp ~/proofreading_prompt.txt.bak document-translator/scripts/config/proofreading_prompt.txt
```

## 🗑️ 解除安裝

```bash
# 刪除 skill 目錄
rm -rf document-translator

# 清除瀏覽器快取（可選）
rm -rf ~/.chatgpt-translator/

# 從 Claude skills 移除
rm -rf ~/.claude/skills/document-translator
```

## 📞 取得協助

- **文件**: 查看 [README.md](document-translator/README.md)
- **範例**: 參考 [references/examples.md](document-translator/references/examples.md)
- **故障排除**: 查閱 [references/troubleshooting.md](document-translator/references/troubleshooting.md)

## 📄 授權

MIT License

---

**安裝完成後，請閱讀 `README.md` 了解使用方法！** 🎉
