#!/bin/bash

# Multi-Tool Coordination Skill 安裝腳本
# 版本: 1.0
# 日期: 2025-01-28

set -e

echo "================================"
echo "Multi-Tool Coordination Skill"
echo "安裝程式 v1.0"
echo "================================"
echo ""

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 檢查作業系統
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    CYGWIN*)    PLATFORM=Cygwin;;
    MINGW*)     PLATFORM=MinGw;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo "偵測到作業系統: ${PLATFORM}"
echo ""

# 決定安裝位置
if [ -z "$1" ]; then
    echo "請選擇安裝位置："
    echo "1) 個人 Skills (~/.claude/skills/)"
    echo "2) 專案 Skills (./.claude/skills/)"
    echo "3) 自訂路徑"
    read -p "選擇 (1-3): " choice
    
    case $choice in
        1)
            INSTALL_DIR="$HOME/.claude/skills/multi-tool-coordination"
            ;;
        2)
            INSTALL_DIR="./.claude/skills/multi-tool-coordination"
            ;;
        3)
            read -p "輸入自訂路徑: " custom_path
            INSTALL_DIR="${custom_path}/multi-tool-coordination"
            ;;
        *)
            echo -e "${RED}無效選擇${NC}"
            exit 1
            ;;
    esac
else
    INSTALL_DIR="$1/multi-tool-coordination"
fi

echo ""
echo "安裝位置: ${INSTALL_DIR}"
echo ""

# 檢查目錄是否已存在
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}警告：目錄已存在${NC}"
    read -p "是否覆蓋？(y/N): " overwrite
    if [ "$overwrite" != "y" ]; then
        echo "安裝取消"
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

# 建立目錄結構
echo "建立目錄結構..."
mkdir -p "$INSTALL_DIR"/{templates,references,scripts,examples}

# 複製檔案（假設當前目錄就是 skill 目錄）
echo "複製檔案..."

# 複製 SKILL.md
if [ -f "SKILL.md" ]; then
    cp SKILL.md "$INSTALL_DIR/"
    echo -e "${GREEN}✓${NC} SKILL.md"
else
    echo -e "${RED}✗${NC} SKILL.md 不存在"
    exit 1
fi

# 複製 templates
if [ -d "templates" ]; then
    cp -r templates/* "$INSTALL_DIR/templates/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} templates/"
fi

# 複製 references
if [ -d "references" ]; then
    cp -r references/* "$INSTALL_DIR/references/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} references/"
fi

# 複製 scripts
if [ -d "scripts" ]; then
    cp -r scripts/* "$INSTALL_DIR/scripts/" 2>/dev/null || true
    chmod +x "$INSTALL_DIR"/scripts/*.sh 2>/dev/null || true
    echo -e "${GREEN}✓${NC} scripts/"
fi

# 複製 examples
if [ -d "examples" ]; then
    cp -r examples/* "$INSTALL_DIR/examples/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} examples/"
fi

# 複製 README（如果存在）
if [ -f "README.md" ]; then
    cp README.md "$INSTALL_DIR/"
    echo -e "${GREEN}✓${NC} README.md"
fi

echo ""
echo -e "${GREEN}安裝完成！${NC}"
echo ""

# 驗證安裝
echo "驗證安裝..."
if [ -f "$INSTALL_DIR/SKILL.md" ]; then
    echo -e "${GREEN}✓${NC} Skill 已正確安裝"
else
    echo -e "${RED}✗${NC} Skill 安裝失敗"
    exit 1
fi

# 檢查 GitHub Copilot CLI
echo ""
echo "檢查依賴工具..."

if command -v gh &> /dev/null; then
    echo -e "${GREEN}✓${NC} GitHub CLI (gh) 已安裝"
    
    if gh extension list | grep -q "gh-copilot"; then
        echo -e "${GREEN}✓${NC} GitHub Copilot CLI 已安裝"
    else
        echo -e "${YELLOW}!${NC} GitHub Copilot CLI 未安裝"
        read -p "是否要安裝 GitHub Copilot CLI？(y/N): " install_copilot
        if [ "$install_copilot" = "y" ]; then
            gh extension install github/gh-copilot
            echo -e "${GREEN}✓${NC} GitHub Copilot CLI 安裝完成"
        fi
    fi
else
    echo -e "${YELLOW}!${NC} GitHub CLI (gh) 未安裝"
    echo "請訪問 https://cli.github.com/ 安裝 GitHub CLI"
fi

echo ""
echo "================================"
echo "安裝資訊"
echo "================================"
echo "Skill 位置: ${INSTALL_DIR}"
echo ""
echo "使用方式："
echo "1. 在 Claude Code 中使用（會自動載入）"
echo "2. 查看文檔: cat ${INSTALL_DIR}/SKILL.md"
echo "3. 查看範例: ls ${INSTALL_DIR}/examples/"
echo ""
echo "設定 GitHub Copilot："
echo "gh extension install github/gh-copilot"
echo "gh auth login"
echo ""
echo "快速開始："
echo "1. 閱讀 SKILL.md"
echo "2. 查看範例：examples/api-development.md"
echo "3. 設定專案：templates/CLAUDE.md.template"
echo ""
echo -e "${GREEN}Happy Coding!${NC}"
echo "================================"
