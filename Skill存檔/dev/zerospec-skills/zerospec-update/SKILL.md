---
name: zerospec:update
metadata:
  version: 0.5.2
description: 當專案演進導致 AGENTS.md 或 docs/README.md 與程式碼產生落差時，比對現狀並更新文件。觸發時機：/zerospec:update、專案新增或移除業務模組、技術棧版本升級、架構層異動、Domain-to-Code Map 明顯過時、每月/每季定期維護。
---

# ZeroSpec — UPDATE

當**專案演進導致 AGENTS.md 或 docs/README.md 與程式碼落差**時，比對並更新文件。

**觸發條件**：
- 專案新增或移除業務模組
- 技術棧版本升級（框架 Major/Minor 版本跳升）
- 架構層異動（新增層級、模組合併）
- Domain-to-Code Map 明顯過時
- 相關專案新增或移除
- docs/ 有新檔案未列入 docs/README.md
- 每月快速檢查 / 每季完整檢查

## 前置狀態確認

執行前依序檢查以下檔案：

| 檔案 | 必要條件 |
|---|---|
| `AGENTS.md` | 必須存在（若無，UPDATE 無法執行，請先用 `/zerospec:build`） |
| `CLAUDE.md` | 必須存在，且包含 `@AGENTS.md` |
| `GEMINI.md` | 必須存在，且包含 `@./AGENTS.md` 或 `@AGENTS.md` |
| `docs/README.md` | 必須存在（若無，在 Step 3 補建） |

若 `AGENTS.md` 不存在 → 停止，告知請先執行 `/zerospec:build`。
若 `CLAUDE.md` 或 `GEMINI.md` 缺少或缺少 import → 列出問題項目，詢問是否補齊後繼續；確認後在 Step 5 一併寫入修正。
若 `docs/README.md` 不存在 → 在 Step 3 補建，不停止執行。

---

Check and update this project's AGENTS.md and docs/README.md to keep them in sync with the codebase.

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Steps

### Step 1: Re-scan A-class Information

Scan the project and extract the latest:
1. **Tech stack**: Read config files, extract language and framework versions (Major.Minor)
2. **Base Namespace / Package / Alias**: Infer from src/ structure
3. **Version source of truth**: Confirm whether config files have changed
4. **Common commands**: Scan Makefile / package.json scripts / gradlew etc.
5. **Directory structure**: List newly added or removed key directories

### Step 2: Diff Against Current AGENTS.md

Compare section by section and flag differences:

1. **Project Summary**: Does the tech stack version need updating?
2. **Quick Constraints**: Still consistent with Code Generation Rules? Still reflects the top 5–8 hard rules?
3. **Domain-to-Code Map**: Any Controllers / Services / Components added, removed, or renamed?
4. **Code Generation Rules**: Any new naming conventions or architecture changes?
5. **Docs Navigation**: Any new docs/ files not yet in the navigation table?
6. **Common Commands**: Any scripts added or removed?
7. **Related Projects**: Any new cross-project dependencies?
8. **Docs Maintenance Reminders**: Do trigger conditions need adjustment?
9. **驗收自我測試**：
   - 是否存在 `## 驗收自我測試` 區塊？若不存在，列為必補項目
   - 新增或修改的規則是否需要對應新增題目？
   - 已刪除的規則是否有對應題目需要移除？

### Step 3: Diff Against docs/README.md

1. **Document Index**: Scan docs/ directory — confirm all .md files are listed
2. **Candidate Documents**: Move established candidates from the candidate table to the document index
3. **Classification**: Confirm whether new document types need to be added

### Step 3.5: Sub-Index Check

Count files matching `docs/spec/SPEC-*.md`.

- If count **≥ 8** AND `docs/spec/README.md` does **not** exist → propose creating it using the ZeroSpec SPEC index template structure, populated with current SPEC metadata. Localize human-facing README content (headings, prose, table labels, scenarios, maintenance rule descriptions, and status meanings) to the detected repository language or explicit `Respond in {locale}` override. Keep file paths, code identifiers, SPEC filenames, commands, and links literal. Add a link row in `docs/README.md` pointing to the new sub-index.
- If `docs/spec/README.md` already exists → verify its Document Index table lists all and only current SPEC files. Report missing, stale, renamed, or duplicate entries. Review "How to Choose" and "Maintenance Rules" for missing, stale, or duplicate scenario/maintenance mappings.

This check applies to SPEC only. Other document categories do not have sub-index rules unless explicitly added later.

### Step 3.7: Code-to-Docs Map Check

Check whether `AGENTS.md` contains a **Code-to-Docs Map** section (or equivalent) that maps source path patterns to owning documentation.

- If the section **exists** → verify it covers the project's main code areas (service layer, host config, DB models/migrations, public API, external integrations, deployment config). Report any gaps as "Update" items.
- If the section **does not exist** → propose adding one. Use the template below as a starting point. Do not write without user confirmation.

Minimum Code-to-Docs Map template:

| Changed path pattern | Docs to check | Notes |
| --- | --- | --- |
| `{service layer}` — new file or responsibility change | SA (domain-and-service-map) | Add relevant SPEC if external integration |
| `{host config}` — Program.cs / DI / middleware | SA (runtime-architecture) | |
| `{config files}` — structure change | SA (runtime-architecture), INFRA | |
| `{DB model / migration}` | SA (domain-and-service-map), relevant SPEC | |
| New public-facing interface / endpoint | Relevant SPEC + Changelog | |
| External integration behavior change | Relevant SPEC | |
| Deployment / CI/CD / infra topology change | INFRA | |
| Cross-module either/or architectural decision | New or updated ADR | |

After confirming the map exists or is proposed, remind the user that AI agents should use the Code-to-Docs Map as a **mandatory post-edit checklist**: list changed files → cross-reference the map → state "needs update / no update (reason)" for each candidate doc — before declaring the coding task complete.

### Step 3.8: Post-Edit Self-Check Audit

Check whether `AGENTS.md` contains a **Post-Edit Self-Check** section.

- If the section **exists** → verify it includes: (a) instructions to list changed files, (b) cross-reference with Code-to-Docs Map, (c) a **Forcing Function** requiring AI to output a `### Docs Impact` block after any response containing code changes. Report any missing elements as "Update" items.
- If the section **does not exist** → propose adding one. Use the template below as a starting point. Do not write without user confirmation.

Minimum Post-Edit Self-Check template:

```
## Post-Edit Self-Check
Before declaring work complete:
1. List changed files from the current diff.
2. Cross-reference every changed file with the Code-to-Docs Map (if present).
3. For each candidate doc, state `Update needed` or `No update needed` with a reason.
4. If interface, schema, permission, or business rules changed, update the relevant SPEC.
5. Run any applicable build/test command to confirm no regressions.

**Forcing Function**: AI agents MUST append a `### Docs Impact` block at the end of any
response containing code changes, listing: (a) affected `docs/spec/` files and their update
status; (b) reason if no update is needed.
```

### Step 4: Output Diff Report

Present differences as tables in the conversation (DO NOT write to files directly). Produce the following reports as applicable:

- **AGENTS.md diff**: Section-by-section (Project Summary, Quick Constraints, Domain-to-Code Map, Code Generation Rules, Docs Navigation, Common Commands, Related Projects, Docs Maintenance Reminders). Mark each as "Update / Add / No change" + explanation
- **docs/README.md diff**: List document index and candidate document changes
- **Sub-Index proposal** (only if Step 3.5 triggered): Present the proposed `docs/spec/README.md` creation or update content for user review
- **Code-to-Docs Map check**: State whether the map exists, whether its path patterns cover the changed areas, and any proposed additions
- **Post-Edit Self-Check check**: State whether the section exists and whether it includes changed-file listing, Code-to-Docs Map cross-reference, and the `### Docs Impact` Forcing Function

### Step 5: Write After Confirmation

After receiving user confirmation, apply the following changes:
- Modify only sections with differences; preserve user-edited C-class content (hard rules, project summary, etc.)
- Mark new B-class content with `[needs review]`
- If Quick Constraints exist, re-extract from Code Generation Rules to keep both sections consistent
- Treat Quick Constraints as a pinned projection of C3 decisions: preserve original decision intent during sync, and write only after user confirmation
- **驗收自我測試**：若 Step 2-9 發現缺少區塊，補齊 8–12 題；若規則有異動，同步更新對應題目；若 AGENTS.md 不存在此區塊，此次 UPDATE 必須一併補齊
- Update docs/README.md document index

## Rules

- MUST NOT delete or modify C-class human decisions (hard rules, project summary, deployment strategy, permission format, etc.) — propose changes only and wait for user confirmation
- A-class information: update directly (tech stack versions, command lists, etc.)
- B-class information: mark `[needs review]` after update
- Follow drift prevention rules: Major.Minor versions only, no exact counts, DO NOT guess
