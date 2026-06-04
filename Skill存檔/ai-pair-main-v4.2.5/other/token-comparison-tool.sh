#!/bin/bash

# AI-Pair v4.1 Token Comparison Tool
# 用途：蒐集和對比不同對話中的 Token 消耗數據

set -e

# 配置
COMPARISON_FILE="CROSS-CONVERSATION-TOKEN-COMPARISON.md"
DATA_DIR=".token-history"
REQUIREMENT="batch_edit_car_undo"

# 確保數據目錄存在
mkdir -p "$DATA_DIR"

# ============================================================================
# 函數：記錄新 Session
# ============================================================================
record_session() {
    local session_id=$1
    local team_lead=$2
    local dev_tier=$3
    local review_level=$4
    local total_token=$5
    local issues=$6
    local notes=$7

    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")

    cat > "$DATA_DIR/${session_id}.json" << EOF
{
  "session_id": "$session_id",
  "timestamp": "$timestamp",
  "requirement": "$REQUIREMENT",
  "models": {
    "team_lead": "$team_lead",
    "dev_tier": "$dev_tier",
    "review_level": "$review_level"
  },
  "tokens": {
    "total": $total_token
  },
  "quality": {
    "issues_found": $issues
  },
  "notes": "$notes"
}
EOF

    echo "✅ Session $session_id 記錄完成"
    echo "   檔案：$DATA_DIR/${session_id}.json"
}

# ============================================================================
# 函數：生成對比報告
# ============================================================================
generate_comparison() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "📊 Token 消耗對比分析"
    echo "════════════════════════════════════════════════════════════"
    echo ""

    # 掃描所有 session 檔案
    local sessions=()
    for file in "$DATA_DIR"/*.json; do
        if [ -f "$file" ]; then
            sessions+=("$file")
        fi
    done

    if [ ${#sessions[@]} -eq 0 ]; then
        echo "❌ 未找到任何 session 記錄"
        echo "   請先執行: record_session 記錄數據"
        return 1
    fi

    # 顯示所有記錄
    echo "| Session ID | Team Lead | Tier | Level | Token | Issues | 成本倍率 |"
    echo "|-----------|-----------|------|-------|-------|--------|---------|"

    local total_tokens=0
    local session_count=0

    for file in "${sessions[@]}"; do
        local data=$(cat "$file")

        local session_id=$(echo "$data" | jq -r '.session_id')
        local team_lead=$(echo "$data" | jq -r '.models.team_lead')
        local dev_tier=$(echo "$data" | jq -r '.models.dev_tier')
        local review_level=$(echo "$data" | jq -r '.models.review_level')
        local total_token=$(echo "$data" | jq -r '.tokens.total')
        local issues=$(echo "$data" | jq -r '.quality.issues_found')

        # 計算成本倍率（相對 STANDARD Sonnet = 1x）
        local cost_ratio=1.0
        case "$dev_tier" in
            "FREE")      cost_ratio="0.3x" ;;
            "LOW")       cost_ratio="0.5x" ;;
            "STANDARD")  cost_ratio="1.0x" ;;
            "COMPLEX")   cost_ratio="1.5x" ;;
        esac

        echo "| $session_id | $team_lead | $dev_tier | $review_level | $total_token | $issues | $cost_ratio |"

        total_tokens=$((total_tokens + total_token))
        session_count=$((session_count + 1))
    done

    # 統計摘要
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "📈 統計摘要"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "Session 總數：$session_count"
    echo "總 Token 消耗：$total_tokens"

    if [ $session_count -gt 0 ]; then
        local avg_token=$((total_tokens / session_count))
        echo "平均 Token/Session：$avg_token"
    fi

    echo ""
    echo "💡 建議下一步："
    echo "   1. 執行 FREE tier 的 session：record_session 'session-2' 'Haiku' 'FREE' '1' '50000' '8' 'quick review'"
    echo "   2. 執行 COMPLEX tier 的 session：record_session 'session-3' 'Sonnet' 'COMPLEX' '3' '190000' '15' 'deep review'"
    echo "   3. 執行本命令查看最新對比"
}

# ============================================================================
# 函數：快速輸入助手
# ============================================================================
interactive_input() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "📝 Session 數據輸入向導"
    echo "════════════════════════════════════════════════════════════"
    echo ""

    read -p "Session ID (如: session-2): " session_id
    read -p "Team Lead 模型 (Haiku/Sonnet/Opus): " team_lead
    read -p "Developer Tier (FREE/LOW/STANDARD/COMPLEX): " dev_tier
    read -p "Review Level (1/2/3): " review_level
    read -p "總 Token 消耗: " total_token
    read -p "發現的問題數: " issues
    read -p "備註 (可選): " notes

    record_session "$session_id" "$team_lead" "$dev_tier" "$review_level" "$total_token" "$issues" "$notes"

    echo ""
    read -p "是否立即查看對比報告？(y/n): " show_report
    if [ "$show_report" = "y" ]; then
        generate_comparison
    fi
}

# ============================================================================
# 函數：預設樣本
# ============================================================================
load_sample_data() {
    echo "📥 加載樣本數據..."

    # Session 1：本次實測
    record_session "2026-05-15-session-1" "Haiku" "STANDARD" "3" "120000" "12" "Phase 1 validation"

    # Session A：v3.1 參考（全 Sonnet）
    record_session "2026-05-15-reference-v3.1" "Sonnet" "STANDARD" "3" "180000" "10" "v3.1 reference baseline"

    # Session B：假設的 FREE tier
    record_session "2026-05-15-estimate-free" "Haiku" "FREE" "1" "50000" "8" "estimated from Tier model"

    echo ""
    echo "✅ 樣本數據加載完成"
    echo "   包含 3 個 session：本次實測 + v3.1 參考 + 估算的 FREE tier"
}

# ============================================================================
# 主程序
# ============================================================================
show_help() {
    cat << EOF
AI-Pair v4.1 Token Comparison Tool

用法：
  ./token-comparison-tool.sh [命令]

命令：
  record [session_id] [team_lead] [tier] [level] [token] [issues] [notes]
    記錄一個新的執行 session
    例：./token-comparison-tool.sh record session-2 Haiku FREE 1 50000 8 "quick review"

  interactive
    交互式輸入向導，一步步記錄 session

  compare
    生成所有已記錄 session 的對比報告

  sample
    加載樣本數據（包含本次實測 + 參考值）

  help
    顯示此幫助信息

範例：
  1. 加載樣本數據並查看對比：
     ./token-comparison-tool.sh sample
     ./token-comparison-tool.sh compare

  2. 交互式記錄新 session：
     ./token-comparison-tool.sh interactive
     ./token-comparison-tool.sh compare

  3. 直接記錄（單行命令）：
     ./token-comparison-tool.sh record session-2 Haiku FREE 1 50000 8 "--quick review"
     ./token-comparison-tool.sh compare

EOF
}

# ============================================================================
# 命令解析
# ============================================================================
case "${1:-help}" in
    record)
        if [ $# -lt 7 ]; then
            echo "❌ 缺少參數"
            echo "用法：record [session_id] [team_lead] [tier] [level] [token] [issues] [notes]"
            exit 1
        fi
        record_session "$2" "$3" "$4" "$5" "$6" "$7" "${8:-}"
        ;;

    interactive)
        interactive_input
        ;;

    compare)
        generate_comparison
        ;;

    sample)
        load_sample_data
        generate_comparison
        ;;

    help|--help|-h)
        show_help
        ;;

    *)
        echo "❌ 未知命令：$1"
        echo ""
        show_help
        exit 1
        ;;
esac
