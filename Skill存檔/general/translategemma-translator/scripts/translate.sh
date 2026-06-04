#!/bin/bash

# 設定腳本所在的目錄變數，確保在任何地方執行都能找到資源
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/translate.py"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

# 顏色定義，讓輸出更易讀
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 輔助函式：日誌輸出
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查系統是否有 Python 3
if ! command -v python3 &> /dev/null; then
    log_error "錯誤：找不到 Python 3。請先安裝 Python 3。"
    exit 1
fi

# 1. 檢查並建立 Python 虛擬環境 (venv)
if [ ! -d "$VENV_DIR" ]; then
    log_info "正在建立 Python 虛擬環境 ($VENV_DIR)..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        log_error "虛擬環境建立失敗。"
        exit 1
    fi
    
    # 啟用虛擬環境並安裝依賴
    source "$VENV_DIR/bin/activate"
    
    log_info "正在升級 pip..."
    pip install --upgrade pip > /dev/null 2>&1
    
    if [ -f "$REQUIREMENTS" ]; then
        log_info "正在安裝依賴套件 (這可能需要幾分鐘)..."
        pip install -r "$REQUIREMENTS"
        if [ $? -ne 0 ]; then
             log_error "依賴套件安裝失敗。"
             deactivate
             exit 1
        fi
    else
        log_warn "找不到 requirements.txt，跳過依賴安裝。"
    fi
else
    # 若虛擬環境已存在，直接啟用
    source "$VENV_DIR/bin/activate"
fi

# 2. 檢查參數
if [ $# -eq 0 ]; then
    echo "用法: ./translate.sh --input <檔案路徑> [選項]"
    echo ""
    echo "選項:"
    echo "  --input FILE       輸入的英文 Markdown 檔案路徑 (必填)"
    echo "  --output FILE      輸出的繁體中文檔案路徑 (選填)"
    echo "  --model_name NAME  Hugging Face 模型名稱 (預設: google/translategemma-4b-it)"
    echo "  --device DEVICE    指定運算裝置: cuda, cpu, mps (MacOS) (自動偵測)"
    echo "  --token TOKEN      Hugging Face Access Token (Gemma 模型必填)"
    echo ""
    echo "範例:"
    echo "  ./translate.sh --input docs/readme.md --token hf_AbCdEf123456"
    deactivate
    exit 1
fi

# 3. 執行 Python 翻譯腳本
log_info "開始執行翻譯任務..."
python3 "$PYTHON_SCRIPT" "$@"
EXIT_CODE=$?

# 4. 結束處理
if [ $EXIT_CODE -eq 0 ]; then
    log_info "任務完成！"
else
    log_error "翻譯過程中發生錯誤。"
fi

deactivate
exit $EXIT_CODE
