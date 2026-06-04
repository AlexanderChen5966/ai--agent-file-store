---
name: zerospec:spec
metadata:
  version: 0.5.2
description: 當 API 新增或行為變更時，生成或更新 SPEC 文件草稿並存入 docs/spec/。觸發時機：/zerospec:spec、新增 API endpoint、修改 Request/Response 結構、變更 API 權限規則、行為變更的 bug fix。
---

# ZeroSpec — SPEC

當 **API 新增或行為變更**時，生成或更新 SPEC 文件。

**觸發條件**：
- 新增外部 API endpoint
- 修改既有 API 的 Request / Response 結構
- 變更 API 的權限要求或業務規則
- 行為變更的 bug fix（記錄前後差異，而非重寫整份 SPEC）

## 前置狀態確認

執行前依序檢查以下檔案：

| 檔案 | 必要條件 |
|---|---|
| `AGENTS.md` | 必須存在 |
| `CLAUDE.md` | 必須存在，且包含 `@AGENTS.md` |
| `GEMINI.md` | 必須存在，且包含 `@./AGENTS.md` 或 `@AGENTS.md` |
| `docs/README.md` | 必須存在 |

若任何一項缺少或不符合 → 列出所有缺少的項目，告知：「請先執行 `/zerospec:build` 補齊後再繼續。」並停止執行。
若全部符合 → 直接執行。

---

Generate or update a SPEC document for this API change.

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Prerequisites

- `AGENTS.md` exists (if not, run `/zerospec:scan` + `/zerospec:build` first)
- `docs/README.md` exists (if not, run `/zerospec:build` first)

## Bugfix Variant

If this change is a bug fix rather than a new feature, record it as a delta update instead of rewriting the full interface definition:

- **Current Behavior**: Actual behavior before the fix (infer from the prior SPEC or Git log)
- **Expected Behavior**: Correct behavior after the fix
- **Unchanged Behavior**: Behavior not affected by this fix (to prevent regression misunderstandings)
- **Impact Scope**: Affected consumers / downstream systems

Write the above as a new entry in `## Changelog`. Example: `- YYYY-MM-DD Bugfix: {summary} (Before: … → After: …)`.

## Steps

1. **Read AGENTS.md**: Understand the project's tech stack, architecture layers, API path conventions, and permission format
2. **Read docs/README.md**: Confirm naming regex, SPEC numbering sequence, and candidate document list
3. **Scan related source code**: Read the Controller, Service, and DTO classes involved in this change
4. **Read existing document (if updating)**: If this updates an existing SPEC, MUST read the original `docs/spec/SPEC-xxx.md` content first to avoid overwriting existing API definitions
5. **Produce SPEC draft** in the following format:

```markdown
# SPEC-xxx: {Business Domain Name}

| Field   | Value                                         |
| ------- | --------------------------------------------- |
| Version | v0.1                                          |
| Status  | Draft                                         |
| Scope   | (Controllers / Services covered by this SPEC) |
| Related | SA-xxx, ADR-xxx (if any)                      |

## Overview
(Infer the domain's business goal and API endpoint scope from code)

## Interface Definitions
### `METHOD /api/v1/resource`
| Item       | Description |
| ---------- | ----------- |
| Function   | ...         |
| Permission | ...         |
| Request    | ...         |
| Response   | ...         |

## DTO Definitions
(List key DTO classes and fields)

## Business Rules
(Infer from validation logic and comments in code)

## Changelog
| Version | Date           | Changes       |
| ------- | -------------- | ------------- |
| v0.1    | {today's date} | Initial draft |
```

## Rules

- Naming format: `SPEC-{3-digit}_{lowercase-hyphenated-desc}.md`
- If updating an existing SPEC: modify only the changed sections + append one row to Changelog
- Write versions as Major.Minor only — omit Patch
- Extract DTO fields from actual code — DO NOT guess
- If any field lacks code or config evidence, mark `[unverified]` — DO NOT guess
- Mark business rules and permission definitions with `[needs review]` (requires human confirmation of boundary conditions and RBAC consistency)

## Post-Output Verification

1. Verify that every class / method / API path referenced in the document actually exists in code
2. Confirm `docs/README.md` document index includes the newly created SPEC
3. If a matching entry exists in the candidate documents table, move it to the document index
4. If `docs/spec/README.md` exists, add or update the corresponding row in its Document Index table (match by SPEC filename, e.g. `SPEC-003_…`). Do NOT create `docs/spec/README.md` — that is handled by the UPDATE skill when the threshold is reached. Do NOT modify the "How to Choose" section — that is maintained during periodic UPDATE reviews.
5. For `docs/spec/README.md` row updates, preserve the index file's existing locale for human-facing text. Keep file paths, code identifiers, SPEC filenames, commands, and links literal.
6. If `docs/spec/README.md` does **not** exist and `docs/spec/` now contains ≥ 8 SPEC files, append a note in your output: "Sub-index threshold reached (>= 8 SPECs). Run `/zerospec:update` to create `docs/spec/README.md`." Do NOT create it yourself.
