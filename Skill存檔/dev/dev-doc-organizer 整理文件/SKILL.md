---
name: dev-doc-organizer
version: "1.0.0"
description: Structures and validates software development documents for Agent consumption and human review. Use when the user wants to organize, format, or validate requirement docs, API docs, architecture docs, or Agent task files. Triggers: "整理需求文件", "整理API文件", "整理架構文件", "幫我把這個寫成規格", "整理成Agent可以讀的格式", "幫我整理這份文件".
---

# Dev Doc Organizer

Converts raw development content into structured documents that Agents can execute without ambiguity and humans can audit clearly.

**Two readers, two needs:**
- Agent: needs precision — no room for "I think this means..."
- Human reviewer: needs auditability — must be able to spot gaps and contradictions fast

## Document type detection

Identify type first — determines which template and validation rules apply:

| Type | Signals | Template |
|------|---------|----------|
| 需求文件 (PRD) | 功能描述、使用者故事、驗收條件 | See templates.md → PRD |
| API 文件 | endpoint、參數、回傳格式、HTTP method | See templates.md → API |
| 架構文件 | 系統元件、資料流、技術選型、設計決策 | See templates.md → ARCH |
| Agent 任務文件 | 任務目標、輸入輸出、執行步驟、完成條件 | See templates.md → TASK |

If type is unclear, ask: "這份文件主要是給 Agent 執行任務、理解需求、還是了解系統架構？"

## Three-layer processing

Apply to every document in order. Read sop-complete.md for detailed rules per document type.

### Layer 1: Completeness check

Verify all required fields are present (see templates.md for required vs optional per type).

```
Missing required field → ⚠️ 缺少必填欄位: [field name]
  Rule: do NOT guess or fill in — flag only

Missing optional field → 💡 建議補充: [field name]
  Include reason: why an Agent would need this field
```

### Layer 2: Ambiguity elimination

Scan every field for language that forces an Agent to make assumptions:

```
模糊數量   「一些」「多個」「若干」          → ⚠️ 需明確數量
模糊條件   「通常」「一般來說」「大部分情況」  → ⚠️ 需明確條件
模糊時間   「盡快」「稍後」「適當時機」       → ⚠️ 需明確時間或觸發條件
模糊範圍   「相關的」「必要的」「適當的」      → ⚠️ 需明確範圍
邏輯衝突   同一欄位前後矛盾                → ❌ 邏輯衝突，需人工解決
隱含前提   依賴某條件但未說明               → ⚠️ 需補充前提條件
```

Rule: Never resolve ambiguity by guessing. Flag with exact location + what needs clarification.

### Layer 3: Agent-readability formatting

Apply to all content that passed Layer 1 and 2:

```
自然語言描述   → 條件句或編號步驟清單
「應該要」     → 明確選擇「必須 (MUST)」或「可選 (OPTIONAL)」
巢狀敘述段落   → 拆成獨立條目，每條只表達一個要求
隱含執行順序   → 明確標示步驟編號或依賴關係 (depends on: X)
```

## Workflow

```
1. Detect document type
2. Load corresponding template from templates.md
3. Layer 1: Completeness check — mark all gaps
4. Layer 2: Ambiguity scan — mark all flags
5. Layer 3: Reformat clean sections
6. Self-check (below)
7. Output structured document + validation report
```

## Self-check before output

```
Structure
- [ ] Correct template applied for document type
- [ ] All required fields present or explicitly flagged ⚠️
- [ ] All optional gaps noted with 💡 and reason

Ambiguity
- [ ] No unflagged vague quantifiers (一些/多個/若干)
- [ ] No unflagged vague conditions (通常/一般來說)
- [ ] No unflagged implicit assumptions
- [ ] Conflicts marked ❌, not silently resolved

Formatting
- [ ] Each requirement is one atomic statement
- [ ] All MUST / OPTIONAL distinctions are explicit
- [ ] Step sequences are numbered with dependencies noted

Output
- [ ] Validation report appended (see format below)
```

## Validation report format

Append after every output:

```
📋 驗收報告
文件類型：[PRD / API / ARCH / TASK]
必填欄位：[N 個完整 / M 個缺少 ⚠️]
歧義標記：[N 處 ⚠️ / M 處 ❌ 衝突]
建議補充：[N 個 💡]
人工必看：[列出所有 ❌ 衝突項目，一行一條]
```

## Edge cases

| Situation | Action |
|-----------|--------|
| 文件已有完整格式 | 仍執行三層處理，只輸出 delta（差異），不重複輸出已完整的部分 |
| 多種類型混合 | 拆成獨立文件分開處理，說明拆分理由 |
| 內容明顯過時 | 標記 `🕐 可能過時: [具體欄位]`，不刪除 |
| 純程式碼無文字說明 | 請求補充說明後再處理，不自行推斷意圖 |

For detailed per-type SOPs see sop-complete.md. For all templates see templates.md.