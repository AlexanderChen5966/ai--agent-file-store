---
name: zerospec:drift
metadata:
  version: 0.5.2
description: 驗證既有 SPEC 文件是否仍與目前程式碼一致，產出結構化落差報告，不寫入任何檔案。觸發時機：/zerospec:drift、發布前確認 SPEC 正確性、大規模重構後、每月/每季定期檢查、懷疑 SPEC 與程式碼已不同步。
---

# ZeroSpec — DRIFT

驗證既有 SPEC 文件是否仍與目前程式碼一致。**此步驟只輸出報告，不寫入任何檔案。**

**觸發條件**：
- 發布或里程碑前，確認 SPEC 反映當前行為
- 大規模重構觸及多個模組後
- 每月/每季定期審查（搭配 `/zerospec:update`）
- PR review 或專案筆記指出「文件描述的是舊行為」
- 任何懷疑 SPEC 已靜默落差的時候

若報告結果為 DRIFTED，建議後續執行 `/zerospec:spec` 更新對應 SPEC。

## 前置狀態確認

執行前依序檢查以下檔案：

| 檔案 | 必要條件 |
|---|---|
| `AGENTS.md` | 必須存在 |
| `CLAUDE.md` | 必須存在，且包含 `@AGENTS.md` |
| `GEMINI.md` | 必須存在，且包含 `@./AGENTS.md` 或 `@AGENTS.md` |
| `docs/spec/SPEC-*.md` | 至少一份存在（若無，告知先用 `/zerospec:spec` 建立第一份） |

若 `AGENTS.md` 不存在 → 停止，告知請先執行 `/zerospec:build`。
若無任何 SPEC → 停止，告知沒有可檢查的 SPEC 文件。

---

Check whether the specified SPEC documents are still consistent with the current codebase. **This task is read-only — DO NOT write any files.**

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Steps

### Step 1: Identify Scope

1. Read `AGENTS.md` to understand the tech stack, permission format, and Domain-to-Code Map
2. Determine which SPEC files to check:
   - If the user specified paths → use those
   - Otherwise → list all `docs/spec/SPEC-*.md` files. If there are 5 or fewer, proceed; if there are more than 5, ask the user to narrow the scope.
3. For each SPEC, read its `Scope` field to identify the corresponding Controller / Service / DTO files. If the Scope field is absent or too vague, infer from the Domain-to-Code Map in `AGENTS.md`; continue when there is one clear mapping, and ask the user only when multiple plausible mappings exist.

### Step 2: Check Each SPEC Across Six Dimensions

For each SPEC file, scan the corresponding code and evaluate the following. Only check dimensions that apply — if a SPEC has no Business Rules section, skip Dimension 4.

**Dimension 1 — Endpoint Alignment**

Read `## Interface Definitions` in the SPEC. For each listed `METHOD /path`:
- Does this endpoint still exist in the Controller with the same method and path?
- If removed or renamed: severity `BREAKING`
- If path changed but logic preserved: severity `DRIFT`

**Dimension 2 — Request / Response Schema**

For each endpoint, compare SPEC DTO definitions against current code:
- Missing or renamed required fields: severity `BREAKING`
- Type change (e.g. `string` → `number`): severity `BREAKING`
- New optional fields not documented: severity `DRIFT`
- Enum values added/removed: severity `BREAKING` if removed, `DRIFT` if added

**Dimension 3 — Permission Alignment**

Read the `Permission` column in `## Interface Definitions`. Compare against code annotations (e.g. `@RequirePermission`, `[Authorize]`, `@authorize`):
- Permission key mismatch or missing: severity `BREAKING`
- Permission key renamed: severity `DRIFT`

**Dimension 4 — Business Rules**

Read `## Business Rules` in the SPEC. For each rule:
- If code branches, validation logic, or state machine transitions clearly contradict the SPEC: severity `BREAKING`
- If the rule is partially outdated or ambiguous relative to code: severity `DRIFT`

**Dimension 5 — Changelog Completeness** *(Optional — requires terminal access)*

If terminal access is available, run:
```
git log --oneline --since="90 days ago" -- <paths covered by this SPEC>
```
Check whether commits that appear to change external behavior (keyword scan: `feat`, `fix`, `refactor`, `breaking`) have a corresponding entry in the SPEC `## Changelog`.

- Missing Changelog entry for a behavioral change: severity `STALE`
- If terminal access is unavailable, skip this dimension and mark it as `SKIPPED: no terminal access` in the report.

**Dimension 6 — Bugfix Variant Drift**

Check whether the SPEC's current description matches code behavior post-fix:
- If a recent bugfix changed external behavior but the SPEC still describes pre-fix behavior: severity `BREAKING`
- If behavior was corrected but the SPEC has no Bugfix Variant entry: severity `STALE`

### Step 3: Produce Drift Report

```markdown
# SPEC Drift Report — {project name}

Scan date: {YYYY-MM-DD}
Checked by: {AI model / tool}
SPEC files checked: {list}

## Summary

| SPEC File    | Status          | Finding Count | Highest Severity |
| ------------ | --------------- | ------------- | ---------------- |
| SPEC-001_... | CLEAN / DRIFTED | 0             | —                |
| SPEC-002_... | DRIFTED         | 3             | BREAKING         |

Overall status: CLEAN / DRIFTED (any BREAKING, DRIFT, or STALE finding → DRIFTED; SKIPPED alone does not make the SPEC drifted)

## Findings

### SPEC-001_...

| #   | Dimension | Location            | Severity | Description                                    |
| --- | --------- | ------------------- | -------- | ---------------------------------------------- |
| 1   | Endpoint  | `GET /api/v1/users` | BREAKING | Endpoint removed from UserController           |
| 2   | Schema    | `UserResponse.role` | BREAKING | Field type changed from `string` to `RoleEnum` |

### SPEC-002_...

(no findings — CLEAN)

## Recommended Actions

For each DRIFTED SPEC, choose one:

1. **Update SPEC** (recommended): Use `/zerospec:spec` Bugfix Variant or standard update flow to bring the SPEC current
2. **Revert code**: If the drift was unintentional, fix the code and keep the SPEC as-is
3. **Deprecate SPEC**: If the module was removed or superseded, update SPEC Status to `Deprecated` and note the date

## Skipped Dimensions

List any dimensions skipped and the reason (e.g. `Dimension 5: SKIPPED: no terminal access`).
```

## Severity Reference

| Severity   | Meaning                                                                      | Typical Action                                 |
| ---------- | ---------------------------------------------------------------------------- | ---------------------------------------------- |
| `BREAKING` | SPEC describes behavior that no longer exists or is actively wrong           | Must update SPEC or revert code before release |
| `DRIFT`    | SPEC is partially outdated; code has evolved but SPEC not yet updated        | Update SPEC in next PR                         |
| `STALE`    | SPEC is missing documentation (Changelog, Bugfix Variant) for a known change | Add Changelog entry                            |
| `SKIPPED`  | Dimension could not be checked (e.g. no terminal access)                     | Note in report; check manually if needed       |
