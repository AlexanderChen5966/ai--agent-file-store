---
name: zerospec:audit
metadata:
  version: 0.5.2
description: 量化評估 AGENTS.md 的品質，產出結構化自我檢查報告，不寫入任何檔案。觸發時機：/zerospec:audit、每月/每季定期審查、AI 重複違反同一條規則、AGENTS.md 越來越長需評估是否精簡、新成員加入需驗證文件可讀性。
---

# ZeroSpec — AUDIT

量化評估 `AGENTS.md` 的品質，產出結構化自我檢查報告。**此步驟只輸出報告，不寫入任何檔案。**

**觸發條件**：
- 每月 / 每季定期審查
- AI 重複違反同一條規則
- AGENTS.md 主線越來越長，評估是否需要精簡
- 新成員想驗證文件是否易於理解

若報告結果為 WARN 或 FAIL，建議後續執行 `/zerospec:update` 將審查結果作為輸入，套用到實際的 AGENTS.md。

## 前置狀態確認

執行前依序檢查以下檔案：

| 檔案 | 必要條件 | 缺少時 |
|---|---|---|
| `AGENTS.md` | 必須存在 | 停止執行，告知請先執行 `/zerospec:build` |
| `CLAUDE.md` | 需包含 `@AGENTS.md` | 在報告中列為警告項目 |
| `GEMINI.md` | 需包含 `@./AGENTS.md` 或 `@AGENTS.md` | 在報告中列為警告項目 |

> AUDIT 主要稽核 `AGENTS.md` 本身品質；`CLAUDE.md`／`GEMINI.md` 的 import 缺失會額外列在報告的「跨工具同步問題」區段，並建議執行 `/zerospec:build` 補齊。

---

Audit this project's `AGENTS.md` and produce a structured report across the dimensions below. **This task is read-only — DO NOT write any files.**

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Prerequisites

- `AGENTS.md` exists (if not, prompt the user to run `/zerospec:scan` + `/zerospec:build` first)
- This analysis targets the repo root's AGENTS.md; if nested AGENTS.md files exist, audit each separately and label them in the report

## Analysis Dimensions

### 1. Length & Structure

- Actual line count
- Character count (rough token estimate)
- Section distribution (list line-count share per `##` / `###` heading)
- Whether it exceeds ZeroSpec's recommended mainline length and upper limit

### 2. Rule Specificity

For each rule in `## Code Generation Rules` and `## Quick Constraints`, assess:

- **Verifiable** (e.g., "Controllers MUST NOT directly access DbContext")
- **Partially verifiable** (e.g., "Follow REST conventions")
- **Not verifiable** (e.g., "Keep code clean", "Write clear commit messages")

List all "Not verifiable" rules and suggest rewrite directions.

### 3. Rule Duplication & Conflicts

- Whether the same rule appears multiple times with inconsistent wording
- Whether two rules contradict each other
- Consistency between Quick Constraints and Code Generation Rules sections

### 4. Content AI Can Infer (Wasted context signals)

List content that **could be removed**, including:

- Language-built-in conventions (e.g., "Python uses snake_case", "TypeScript uses camelCase")
- Version numbers derivable from `.csproj` / `package.json` / `build.gradle`
- Generic code quality advice ("write clean code", "add appropriate comments")
- Build/test process already covered by Common Commands
- **Domain-to-code map necessity in small projects**: If the project is small AND the Agent supports semantic search (`#codebase` / Cursor indexing / Claude Code), the domain-to-code map's value is lower than the Agent's on-the-fly scanning — consider removing or heavily trimming

Apply this principle: **"Would removing this line cause the AI to make an error on its next task?" If not, it's a removal candidate.**

### 5. Missing ZeroSpec Required Fields

Check coverage of required sections:

- Project Summary
- Anchor Information (Base Package / Alias / Version Source of Truth)
- Quick Constraints
- Domain-to-Code Map
- Code Generation Rules
- Docs Sync Triggers
- **驗收自我測試**（Self-Verification Test）：
  - 是否存在 `## 驗收自我測試` 區塊？
  - 題目數量是否達到 8–12 題？
  - 是否涵蓋：平台限制、禁止事項、高風險操作、核心元件、構建指令、輸出語言？
  - 每道題的答案是否在文件中可明確查到（不應有推論題）？
  - 若缺少此區塊 → 列為 **WARN**；若存在但題目數 < 5 → 列為 **WARN**

### 6. Attention Weight Diagnosis

Assess whether the top section of AGENTS.md contains the most important information:

- Does the top section include "Project Summary + Anchor Information + Quick Constraints"?
- If the top section is occupied by onboarding narratives or lengthy background stories, flag as a high-priority trim target

### 7. Token Usage Observation (Optional)

AGENTS.md is injected into every Agent conversation's system context; longer content dilutes attention for other files. This dimension does not require precise calculation — provide a semantic judgment:

- **Low**: Minimal impact on other file attention
- **Moderate**: Noticeable but acceptable — review removal candidates from Dimension 4
- **High**: Clearly impacting context — prioritize trimming and deduplication

### 8. Domain-to-Code Map Health

Spot-check that entries in the Domain-to-Code Map still exist in the codebase or documentation tree:

- Pick 3–5 representative entries (Controller, Service, package, primary file, or directory) from the map
- Verify each still exists by direct path lookup, file search, glob expansion, or package/class declaration search
- Report: `✅ found`, `⚠️ not verified (no direct file access)`, or `❌ not found` for each spot-checked entry
- If ≥ 2 entries cannot be confirmed, flag as WARN; if ≥ 1 entry is confirmed absent, flag as FAIL

> Note: This dimension has limited accuracy without direct file-system access. If Agent cannot browse files freely, mark spot-checked entries as `⚠️ not verified` and note in the report.

### 9. Path Link Health

Check whether paths referenced in AGENTS.md resolve correctly:

- **Internal doc links** (`docs/`, `templates/`, relative markdown links): Do the target files exist?
- **Cross-repo relative paths** (`../other-repo/`, `../../shared/`): Are they resolvable from the current workspace root? If not, note and flag as WARN.
- **Broken links**: Any path reference that clearly does not exist → flag as FAIL

> Note: For cross-repo paths, use workspace context to determine whether the sibling repo is present. If it cannot be confirmed, mark as `⚠️ not verified` rather than FAIL.

## Output Format

Produce the report in Markdown:

```markdown
# AGENTS.md Audit Report — {project name}

Scan date: {YYYY-MM-DD}
File path: {AGENTS.md actual path}
Total lines: {n}

## Summary

- Health score: {PASS / WARN / FAIL} (any single FAIL condition triggers overall FAIL)
- Key findings:
  - …
  - …
  - …

## Detailed Analysis

### 1. Length & Structure
... (bullet points)

### 2. Rule Specificity
| Rule | Grade | Suggested Rewrite |
| ---- | ----- | ----------------- |
| ...  | ...   | ...               |

### 3. Rule Duplication & Conflicts
...

### 4. Removal Candidates
...

### 5. Missing Required Fields
...

### 6. Attention Weight Diagnosis
...

### 7. Token Usage Observation (Optional)
- Assessment: {Low / Moderate / High}
- Notes: {brief explanation}

### 8. Domain-to-Code Map Health
| Entry (file / class / package) | Status                                 |
| ------------------------------ | -------------------------------------- |
| `XxxController`                | ✅ found / ⚠️ not verified / ❌ not found |

### 9. Path Link Health
| Path Referenced | Target Exists?                |
| --------------- | ----------------------------- |
| `docs/spec/...` | ✅ / ⚠️ not verified / ❌ broken |

## Suggested Trim List (by priority)

1. **Must fix** (FAIL-level): ...
2. **Should fix** (WARN-level): ...
3. **Optional** (INFO): ...

## Actionable Fix List

For each finding, indicate the recommended follow-up action:

| #   | Finding                                            | Severity | Recommended Action                              |
| --- | -------------------------------------------------- | -------- | ----------------------------------------------- |
| 1   | Domain-to-code map entry `XxxController` not found | FAIL     | Update map manually or run `/zerospec:update`   |
| 2   | Broken link `docs/spec/SPEC-003.md`                | FAIL     | Create the missing SPEC or remove the reference |
| 3   | Unverifiable rule "write clean code"               | WARN     | Rewrite to a specific, testable constraint      |
| 4   | SPEC content may be stale after map/path changes   | INFO     | Run `/zerospec:drift` on related SPECs          |

Action codes:
- **UPDATE**: Run `/zerospec:update` to sync AGENTS.md
- **SPEC**: Run `/zerospec:spec` to create or update a SPEC
- **DRIFT**: Run `/zerospec:drift` to verify SPEC content matches code
- **Manual**: Requires human judgment — cannot be automated

## Not Recommended to Change

Explicitly list items that "look like they should change but actually shouldn't" to prevent over-trimming.
```

## Health Score Criteria

- **PASS**: Mainline length within recommended range; few unverifiable rules and no obvious conflicts; top section dominated by core information; no confirmed broken Domain-to-Code Map entries or internal links
- **WARN**: Mainline slightly long, unverifiable rules / duplicates starting to accumulate, top section has some non-core content, or multiple map/path entries cannot be verified
- **FAIL**: Content clearly too long, many unverifiable rules / mutual conflicts, top section dominated by non-core content, or confirmed stale map entries / broken internal links already impact task comprehension
