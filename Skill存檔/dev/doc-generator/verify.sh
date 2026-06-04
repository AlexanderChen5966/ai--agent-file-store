#!/bin/bash
# Skill 驗證腳本

echo "🔍 驗證 doc-generator Agent Skill"
echo "=================================="
echo ""

SKILL_DIR=".github/skills/doc-generator"
PASS=0
FAIL=0

check() {
    if [ "$2" = "true" ]; then
        echo "✅ $1"
        ((PASS++))
    else
        echo "❌ $1"
        ((FAIL++))
    fi
}

# 檢查目錄
check "Skill 目錄存在" "$(test -d $SKILL_DIR && echo true || echo false)"

# 檢查必要文件
check "SKILL.md 存在" "$(test -f $SKILL_DIR/SKILL.md && echo true || echo false)"
check "README.md 存在" "$(test -f $SKILL_DIR/README.md && echo true || echo false)"
check "CHANGELOG.md 存在" "$(test -f $SKILL_DIR/CHANGELOG.md && echo true || echo false)"

# 檢查 YAML frontmatter
if [ -f $SKILL_DIR/SKILL.md ]; then
    check "包含 'name:' 欄位" "$(grep -q '^name:' $SKILL_DIR/SKILL.md && echo true || echo false)"
    check "包含 'version:' 欄位" "$(grep -q '^version:' $SKILL_DIR/SKILL.md && echo true || echo false)"
    check "包含 'description:' 欄位" "$(grep -q '^description:' $SKILL_DIR/SKILL.md && echo true || echo false)"
fi

# 檢查腳本
check "scripts/ 目錄存在" "$(test -d $SKILL_DIR/scripts && echo true || echo false)"
check "generate_all.sh 存在" "$(test -f $SKILL_DIR/scripts/generate_all.sh && echo true || echo false)"
check "api_to_postman.py 存在" "$(test -f $SKILL_DIR/scripts/api_to_postman.py && echo true || echo false)"

# 檢查字型
check "fonts/ 目錄存在" "$(test -d $SKILL_DIR/fonts && echo true || echo false)"

echo ""
echo "=================================="
echo "結果: $PASS 通過, $FAIL 失敗"

if [ $FAIL -eq 0 ]; then
    echo "✅ 所有檢查通過！Skill 已正確安裝。"
    exit 0
else
    echo "❌ 有 $FAIL 項檢查失敗，請修復後重試。"
    exit 1
fi
