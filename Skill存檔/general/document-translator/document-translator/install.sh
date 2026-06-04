#!/bin/bash
# Document Translator Skill - 安裝腳本
# Version: 3.2.1

set -e

echo "=================================="
echo "Document Translator Skill 安裝程式"
echo "Version: 3.2.1"
echo "=================================="
echo ""

# 檢查 Python 版本
echo "檢查 Python 版本..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 找不到 Python 3"
    echo "請安裝 Python 3.7 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ 找到 Python $PYTHON_VERSION"
echo ""

# 切換到 scripts 目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/scripts"

# 建立虛擬環境（可選）
read -p "是否建立 Python 虛擬環境？(建議) [Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "建立虛擬環境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ 虛擬環境已建立並啟用"
else
    echo "跳過虛擬環境建立"
fi
echo ""

# 安裝依賴
echo "安裝 Python 依賴套件..."
pip install -r requirements.txt
echo "✓ 依賴套件安裝完成"
echo ""

# 檢查安裝
echo "檢查安裝..."
python3 -c "import nodriver; print('✓ nodriver 已安裝')"
python3 -c "from deep_translator import GoogleTranslator; print('✓ deep-translator 已安裝')"
echo ""

echo "=================================="
echo "✅ 安裝完成！"
echo "=================================="
echo ""
echo "快速開始："
echo "  cd $SCRIPT_DIR"
echo "  python scripts/translate.py --mode chatgpt docs/en/YOUR_FILE.md"
echo ""
echo "查看更多範例："
echo "  cat README.md"
echo "  cat references/examples.md"
echo ""
