---
name: zerospec:impl
metadata:
  version: 0.5.2
description: 複雜多模組實作任務的護欄，確保程式碼變更時同步更新 SPEC。觸發時機：/zerospec:impl、任務預計觸及 3+ Controller/handler、影響 2+ SPEC 文件、跨模組功能開發、大規模重構改變外部行為。
---

# ZeroSpec — IMPL

複雜編碼任務的護欄：**預計觸及多個模組或影響多份 SPEC 時使用**，確保實作與文件同步。

**觸發條件**：
- 任務預計觸及 **3 個以上 Controller**（或等效 handler 檔案）
- 任務預計影響 **2 份以上 SPEC 文件**
- 跨模組功能開發（同時涉及 API 變更和業務規則變更）
- 大規模重構改變多個端點的外部行為

> 較簡單的任務（單一 controller、單一 SPEC），使用 AGENTS.md 的 Post-Edit Self-Check 區段即可，不需要此 skill。

## 快速自我評估

開始前先回答以下問題，若**任一**為「是」，就應使用此 skill：

1. 此任務會觸及 **3 個以上 Controller**（或等效 handler）？
2. 此任務會改動 **2 份以上 SPEC** 描述的介面？
3. 此任務跨越**模組邊界**（例如 API host + service layer + DB schema 同時變更）？
4. 預期變更範圍大到**無法同時記住所有受影響的文件**？

若全部為「否」，使用 AGENTS.md 的 Post-Edit Self-Check 即可。

## 前置狀態確認

執行前依序檢查以下檔案：

| 檔案 | 必要條件 |
|---|---|
| `AGENTS.md` | 必須存在 |
| `CLAUDE.md` | 必須存在，且包含 `@AGENTS.md` |
| `GEMINI.md` | 必須存在，且包含 `@./AGENTS.md` 或 `@AGENTS.md` |

若任何一項缺少 → 列出缺少項目，告知：「請先執行 `/zerospec:build` 補齊後再繼續。」並停止執行。

---

Implement the described coding task with explicit SPEC synchronization.

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Prerequisites

- `AGENTS.md` exists (if not, run `/zerospec:scan` + `/zerospec:build` first)
- The task description is provided above or below this skill invocation

## Steps

### Step 1: Understand Scope

1. Read `AGENTS.md` fully — note Quick Constraints, Code-to-Docs Map, and Post-Edit Self-Check sections.
2. List the Controllers / Services / DB models expected to change.
3. For each changed area, identify the corresponding SPEC file(s):
   - Prefer the Code-to-Docs Map in `AGENTS.md`.
   - If no map exists, read `docs/spec/README.md` (if present), then review relevant `docs/spec/SPEC-*.md` overview or scope sections before mapping.
   - If the mapping is still uncertain, state the ambiguity explicitly and ask before coding — do not guess from filename alone.
4. Before coding, output a brief plan: changed code areas → affected SPEC files.

### Step 2: Implement

Apply code changes according to the task description and Quick Constraints in `AGENTS.md`.

- Follow all rules in `## Quick Constraints` without exception. The first constraint (SPEC assessment) applies at the end of this task.
- If you encounter an ambiguity that could affect SPEC accuracy, pause and ask — do not silently choose.

### Step 3: SPEC Synchronization

For every SPEC identified in Step 1:

1. **New endpoint** → Add a row to `## Interface Definitions` with Method, Path, Description, Request, Response, Permission, and Error codes.
2. **Modified request/response schema** → Update the relevant DTO or parameter description; add a Changelog entry: `YYYY-MM-DD Change: {summary}`.
3. **Permission change** → Update the `Permission` column and add a Changelog entry.
4. **Business rule change** → Update `## Business Rules`; add Changelog entry.
5. **Behavioral bug fix** → Use the Bugfix Variant format in Changelog: `YYYY-MM-DD Bugfix: {summary} (Before: … → After: …)`.
6. If no SPEC update is needed for a file, state the reason explicitly.

### Step 4: Post-Edit Self-Check

After all code and SPEC changes are complete:

1. List every changed file.
2. Cross-reference the Code-to-Docs Map (or your Step 1 mapping) for each changed file.
3. State `Update needed` or `No update needed (reason)` for every candidate document.
4. Confirm all SPEC files identified in Step 1 have been updated or explicitly dismissed.
5. Run any applicable build/test command and confirm no regressions.

## Output Requirements

**Forcing Function**: Every response that contains code changes MUST end with a `### Docs Impact` block:

```markdown
### Docs Impact
| Changed path | Affected SPEC | Status | Notes |
| --- | --- | --- | --- |
| {path} | {SPEC file or "none"} | Updated / No update needed | {reason if no update} |
```
