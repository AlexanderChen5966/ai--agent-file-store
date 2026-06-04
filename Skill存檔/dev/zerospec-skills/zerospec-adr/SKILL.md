---
name: zerospec:adr
metadata:
  version: 0.5.2
description: 當做出跨模組的非此即彼技術決策時，生成 ADR 文件草稿並存入 docs/adr/。觸發時機：/zerospec:adr、架構分層策略選擇、技術方案決策（Kafka vs Event Hubs、JWT vs Session）、跨模組共用元件設計決策、基礎設施選型。
---

# ZeroSpec — ADR

當做出**跨模組的非此即彼技術決策**時，生成 ADR 文件。

**觸發條件**：
- 架構分層策略選擇（如 Clean Architecture vs Hexagonal）
- 非此即彼的技術決策（如 Kafka vs Event Hubs、JWT vs Session）
- 跨模組共用元件的設計決策
- 基礎設施選型（如 PostgreSQL vs MySQL、Redis vs Memcached）

**不觸發**（以下情況不需要 ADR）：
- 新增 CRUD API
- 修改 Redis TTL 預設值
- 簡單 bug fix

## 前置狀態確認

執行前依序檢查以下檔案：

| 檔案 | 必要條件 |
|---|---|
| `AGENTS.md` | 必須存在 |
| `CLAUDE.md` | 必須存在，且包含 `@AGENTS.md` |
| `GEMINI.md` | 必須存在，且包含 `@./AGENTS.md` 或 `@AGENTS.md` |
| `docs/README.md` | 必須存在 |

若任何一項缺少或不符合 → 列出所有缺少的項目，告知：「請先執行 `/zerospec:build` 補齊後再繼續。」並停止執行。
若全部符合 → 確認觸發條件符合後直接執行。

---

Generate an ADR document for this technical decision.

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Prerequisites

- `AGENTS.md` exists (if not, run `/zerospec:scan` + `/zerospec:build` first)
- `docs/README.md` exists (if not, run `/zerospec:build` first)

## Steps

1. **Read AGENTS.md**: Understand the project's tech stack and architecture constraints
2. **Read docs/README.md**: Confirm naming regex and ADR numbering sequence
3. **Read existing ADRs**: Scan docs/adr/ to confirm numbering and existing decision context
4. **Confirm with me**:
   - What is the decision context? (Cite verifiable evidence first; if insufficient, mark `[unverified]` and ask)
   - What are the options? (List at least 2)
   - Which was chosen and why?
5. **Produce ADR draft** in the following format:

```markdown
# ADR-xxx: {Decision Title}

| Field         | Value                              |
| ------------- | ---------------------------------- |
| Decision Date | {today's date}                     |
| Status        | Accepted                           |
| Related       | SA-xxx, ADR-yyy, SPEC-xxx (if any) |
| Impact Scope  | (Affected modules or domains)      |

## Context
(Infer from conversation context and code, mark [needs review])

## Options Considered

### Option A — {Name}
- Pros: ...
- Cons: ...

### Option B — {Name}
- Pros: ...
- Cons: ...

## Decision
Chose Option X because...

## Consequences
- Positive impact: ...
- Negative impact / risks: ...
- Follow-up actions: ...
```

## Rules

- Naming format: `ADR-{3-digit}_{lowercase-hyphenated-desc}.md`
- ADRs are append-only or supersede-only (new ADR marks old one as `Superseded by ADR-yyy`) — MUST NOT edit accepted content
- Numbering starts from max existing ADR number + 1
- If no verifiable evidence exists, DO NOT fill in context details — mark `[unverified]` instead

## Post-Output Verification

1. Verify that modules and component names referenced in the document actually exist in code
2. Confirm `docs/README.md` document index includes the newly created ADR
3. If a matching entry exists in the candidate documents table, move it to the document index
