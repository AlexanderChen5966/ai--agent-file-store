#!/bin/bash
# Document Translator - Shell 入口點
# Version: 3.2.0
#
# 使用 nodriver 反偵測自動化 + 智慧降級翻譯策略

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/translate.py"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# 顯示使用說明
show_help() {
    echo "Document Translator - 技術文檔翻譯系統 (v3.2.0)"
    echo ""
    echo -e "${MAGENTA}使用 nodriver 反偵測自動化 + 智慧降級翻譯策略${NC}"
    echo ""
    echo "使用方式："
    echo "  $0 [選項] <檔案路徑...>"
    echo ""
    echo "翻譯模式 (--mode)："
    echo "  chatgpt          ChatGPT Translate 專用頁面（預設，品質最佳）"
    echo "  auto             ChatGPT + 智慧降級（高可靠性）"
    echo "  google+proofread Google Translate + 智慧校稿"
    echo "  google           僅 Google Translate（最快，無校稿）"
    echo ""
    echo "校稿後端 (--proofreader)："
    echo "  auto             自動偵測可用後端（預設）"
    echo "  chatgpt          ChatGPT 對話頁面校稿（推薦）"
    echo "  desktop          Claude Desktop GUI"
    echo "  cli              Claude CLI 命令列"
    echo "  manual           文字編輯器手動校稿"
    echo ""
    echo "文件類型 (--doc-type)："
    echo "  api              API 技術文檔"
    echo "  srs              軟體需求規格書"
    echo "  design           軟體設計文檔"
    echo "  user-guide       使用者手冊"
    echo "  tutorial         教學文件"
    echo "  readme           README 專案說明"
    echo "  changelog        變更日誌"
    echo "  general          一般技術文檔（預設）"
    echo ""
    echo "其他選項："
    echo "  --no-headless    顯示瀏覽器視窗（調試/手動 CAPTCHA）"
    echo "  --no-fallback    禁用降級機制"
    echo "  --force          強制覆蓋已存在的譯文"
    echo "  --verbose        顯示詳細日誌"
    echo "  --dry-run        僅顯示將執行的操作，不實際執行"
    echo "  --help           顯示此說明"
    echo ""
    echo "範例："
    echo "  # ChatGPT Translate（推薦）"
    echo "  $0 --mode chatgpt docs/en/API.md"
    echo ""
    echo "  # Google Translate + ChatGPT 校稿"
    echo "  $0 --mode google+proofread --proofreader chatgpt docs/en/API.md"
    echo ""
    echo "  # 指定文件類型（校稿更精準）"
    echo "  $0 --mode google+proofread --doc-type api docs/en/API.md"
    echo ""
    echo "  # 顯示瀏覽器視窗（手動 CAPTCHA）"
    echo "  $0 --mode chatgpt --no-headless docs/en/API.md"
    echo ""
    echo "  # 批量翻譯"
    echo "  $0 --mode chatgpt docs/en/*.md"
}

# 檢查並建立虛擬環境
setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${BLUE}[INFO]${NC} 建立 Python 虛擬環境..."
        python3 -m venv "$VENV_DIR"
        echo -e "${GREEN}[OK]${NC} 虛擬環境建立完成"
    fi

    # 啟動虛擬環境
    source "$VENV_DIR/bin/activate"

    # 檢查是否需要安裝依賴
    if [ -f "$REQUIREMENTS_FILE" ]; then
        # 檢查 nodriver 是否已安裝
        if ! python3 -c "import nodriver" 2>/dev/null; then
            echo -e "${BLUE}[INFO]${NC} 安裝依賴套件..."
            pip install --upgrade pip > /dev/null 2>&1
            pip install -r "$REQUIREMENTS_FILE" > /dev/null 2>&1
            echo -e "${GREEN}[OK]${NC} 依賴套件安裝完成"
        fi
    else
        # 如果沒有 requirements.txt，安裝基本依賴
        if ! python3 -c "import nodriver" 2>/dev/null; then
            echo -e "${BLUE}[INFO]${NC} 安裝基本依賴套件..."
            pip install --upgrade pip > /dev/null 2>&1
            pip install nodriver deep-translator > /dev/null 2>&1
            echo -e "${GREEN}[OK]${NC} 依賴套件安裝完成"
        fi
    fi
}

# 執行 Python 腳本
run_python() {
    python3 "$PYTHON_SCRIPT" "$@"
    local exit_code=$?
    deactivate
    return $exit_code
}

# 主程式
main() {
    # 檢查是否有參數
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi

    # 檢查是否請求幫助
    for arg in "$@"; do
        if [ "$arg" == "--help" ] || [ "$arg" == "-h" ]; then
            show_help
            exit 0
        fi
    done

    # 設定虛擬環境
    setup_venv

    # 執行翻譯
    run_python "$@"
}

main "$@"
