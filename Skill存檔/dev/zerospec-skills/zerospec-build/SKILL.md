---
name: zerospec:build
metadata:
  version: 0.5.2
description: 根據 INIT-SCAN 分析結果，生成 AGENTS.md、CLAUDE.md、GEMINI.md 與 docs/README.md 四個專案 AI 導覽檔案。觸發時機：/zerospec:build、完成 INIT-SCAN 後、建立專案文件、INIT-BUILD。需先執行 /zerospec:scan。
---

# ZeroSpec — INIT-BUILD

根據先前的掃描分析結果，建立四個檔案：`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`docs/README.md`。

## 前置狀態確認

執行前先檢查：

- 若當前對話**有** SCAN 分析結果 → 直接進入 Step 2（Ask C-class Questions），沿用掃描結果。
- 若當前對話**沒有** SCAN 分析結果，但 `AGENTS.md` **不存在** → 先執行一次 SCAN 再繼續，告知使用者：「找不到先前的掃描結果，先重新掃描專案。」
- 若 `AGENTS.md` **已存在** → 告知使用者：「AGENTS.md 已存在。若要更新，請改用 `/zerospec:update`；若確定要重建，請告知。」並停止等待確認。
- 若 `AGENTS.md` 存在但 `CLAUDE.md` 或 `GEMINI.md` 缺少 → 告知使用者缺少哪個檔案，詢問是否只補建缺少的部分，確認後執行 Step 3.5。

---

Based on the prior project analysis, create two files: `AGENTS.md` and `docs/README.md`.
Follow these four steps in strict order:

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Step 1: Import SCAN Results

Read the following from the confirmed INIT-SCAN output (if in a new conversation, re-scan the project for equivalent information):

- **A-class (auto-extracted)**: Tech stack, version source of truth, common commands, directory structure, Base Namespace/Package/Alias
- **B-class (reviewed drafts)**: Docs navigation table, domain-to-code map, architecture layers, naming conventions, related projects

## Step 2: Ask C-class Questions (Team decisions only humans can answer)

Ask each question below. Provide a suggested default (prefixed with `Suggested:`) inferred from the SCAN phase, so the user can confirm or adjust:

1. **Project summary**: Describe this project's business purpose in one sentence
   > Suggested: "{inferred from SCAN}"
2. **Deployment method**: How is this project deployed?
   > Suggested: {inferred from CI/CD config or Dockerfile}
3. **Hard rules**: What architecture hard rules (Do / Don't) MUST the team follow?
   > Suggested: {inferred from layering patterns, e.g., "Controllers MUST NOT contain business logic"}
4. **Routing conventions**: Are there conventions for API routes or page paths?
   > Suggested: {inferred from existing routes}
5. **Auth / state management**: Is there a specific pattern for access control or state management?
   > Suggested: {inferred from code — mark `[unverified]` if no clear pattern}
6. **Data access rules**: Are there rules for data access or database migrations? (Skip if no database)
   > Suggested: {inferred from ORM/migration config}
7. **Docs sync triggers**: Which PR changes require docs updates?
   > Suggested: Update SPEC on any API addition or behavior change
8. **Other hard rules**: Any other team-specific hard rules? (May skip)

## Step 3: Assemble Output

Combine all content into two files:

### File 1: AGENTS.md

```markdown
# AGENTS.md — {project name} AI Navigation Guide

> This file is the primary entry point for GenAI Agents to understand the {project name} project. Read this file completely before performing any code task.

## Project Summary
{C1 answer + A-class tech stack, architecture pattern, deployment method}
{A-class Base Namespace/Package/Alias}
{A-class version source of truth declaration}

## Quick Constraints
The **first item MUST always be copied verbatim** (or localized per `Respond in {locale}` if the user requested a specific locale):
1. **At task start**: if the task spans 3+ Controllers/handlers or affects 2+ SPEC documents, suggest using the IMPL Prompt (`/zerospec:impl`) before proceeding. **At task end**: assess whether `docs/spec/` needs updating (triggers: new endpoint, request/response schema change, permission change, business rule change, behavioral bugfix). If yes → update SPEC + Changelog in the same changeset. If no → state the reason explicitly.
<!-- zh-TW localization hint: 「任務開始時先評估範圍：若涉及 3+ Controller/handler 檔案或影響 2+ SPEC，建議先啟用 /zerospec:impl 再動工。任務結束前：必須評估 docs/spec/ 是否需要更新（觸發情境：新端點、Request/Response schema 改動、Permission 改動、Business Rule 改動、行為性 bugfix）。是 → 同一變更集更新 SPEC + Changelog；否 → 明確說明理由。」 -->
Then add 4–7 more rules extracted from "Code Generation Rules" below (violations cause PR rejection or system errors):
{Additional rules from C3, one per line}

## Domain-to-Code Map
{B-class domain-to-code map}

## Code Generation Rules
{C3 hard rules + C4 routing conventions + C5 auth/state + C6 data access + B-class naming conventions}
(Items already in Quick Constraints may have expanded details and examples here)

## GenAI Docs Navigation
{B-class docs navigation table (intent-driven format)}

## Common Commands
{A-class auto-extracted commands — MUST include build, test, lint, and type-check categories so the Agent can self-verify after task completion. If any category does not exist, explicitly mark "Not configured" to prompt the team to set it up.}

## Related Projects
{B-class related projects (omit this section if none)}

## Docs Maintenance Reminders
{C7 docs sync trigger conditions}
- Docs governance rules: see `docs/README.md`

## Post-Edit Self-Check
Before declaring work complete:
1. List changed files from the current diff.
2. Cross-reference every changed file with the Code-to-Docs Map (if present).
3. For each candidate doc, state `Update needed` or `No update needed` with a reason.
4. If interface, schema, permission, or business rules changed, update the relevant SPEC.
5. Run any applicable build/test command to confirm no regressions.

**Forcing Function**: AI agents MUST append a `### Docs Impact` block at the end of any response containing code changes. Evaluate document impact per `docs/README.md > AI Auto-Trigger Heuristics`:

### Docs Impact
- **SPEC**: [Updated SPEC-001 § ... / No update — reason]
- **ADR**: [Proposing ADR-00x for ... / No decision point]
- **SA**: [No structural change / Proposing SA scope: ...]
- **INFRA**: [Updated INFRA-001 / No infra change]

<!-- zh-TW localization hint: 在回覆中包含程式碼異動時，必須以「### Docs Impact」區塊結尾，依 docs/README.md > AI Auto-Trigger Heuristics 逐項評估 SPEC / ADR / SA / INFRA 四類文件的影響狀態。 -->

---

## 驗收自我測試

讀完本文件後，以下問題應全部能答對：

{自動產生 8–12 題，涵蓋以下類別（有對應規則才出題）：
- 平台限制（支援哪些平台？哪些不支援？）
- 嚴格禁止事項（哪些操作絕對不可做？）
- 高風險操作（哪些操作需要使用者確認？）
- 架構核心元件（核心元件如何使用？有哪些禁止用法？）
- 構建 / 驗證指令（修改特定路徑後需執行什麼？）
- 輸出語言與格式
}
```

> **Length guideline**: Keep AGENTS.md within 150–300 lines. If it exceeds 300 lines, move low-frequency sections to docs/ sub-documents and reference them in the navigation table.

> **驗收自我測試必須在 AGENTS.md 建立時一併產生**（不可省略）。
> CLAUDE.md 與 GEMINI.md 透過 @import 自動取得相同題目，無需重複撰寫。
> 題目必須答案可在文件中明確查到，禁止出推論題或超出文件範圍的題目。

### File 2: docs/README.md

```markdown
# {project name} — Docs Governance Hub

> This file defines the layering rules, naming conventions, and maintenance triggers for project documentation.
> GenAI Agents MUST read this file before performing any documentation task.

## SDD Document Classification

| Category                    | Directory        | Naming Format               | Trigger                                         |
| --------------------------- | ---------------- | --------------------------- | ----------------------------------------------- |
| SA (System Analysis)        | `docs/analysis/` | `SA-{3-digit}_{desc}.md`    | Milestone or major architecture change          |
| ADR (Architecture Decision) | `docs/adr/`      | `ADR-{3-digit}_{desc}.md`   | Cross-module either/or tech decision            |
| SPEC (Interface Contract)   | `docs/spec/`     | `SPEC-{3-digit}_{desc}.md`  | API addition or behavior change (**mandatory**) |
| INFRA (Infrastructure)      | `docs/infra/`    | `INFRA-{3-digit}_{desc}.md` | Deployment topology or CI change                |

- Naming regex: `^(SA|ADR|SPEC|INFRA)-\d{3}_[a-z0-9-]+\.md$`

## Source of Truth

SPEC is the primary reference for development and GenAI. Update SPEC directly on every interface addition or change, and track changes in the Changelog.

**Minimum maintenance rule**: Every PR involving interface or behavior changes MUST update the SPEC content and Changelog.

## ADR Trigger Conditions

- ✅ Needs ADR: architecture layering strategy, auth scheme design (e.g., JWT dual-token), either/or tech decision (e.g., Kafka vs Event Hubs), design decisions for cross-module shared components
- ❌ No ADR needed: adding a CRUD API, changing cache TTL defaults, simple bug fix

## SA Trigger Conditions

> SA is a system-level snapshot. Unlike SPEC (mandatory on every interface change), SA is created on-demand when global understanding is lacking.

- ✅ Suggest SA: entering a Brownfield codebase with no current architecture overview, cross-module boundaries shifting (3+ modules restructured), team members repeatedly asking "how does this system work?", or recent architecture-level changes not reflected in existing docs
- ❌ No SA needed: routine feature work within a single module, adding endpoints, bug fixes
- ⚠️ AI action: **Propose** the SA topic and scope — do NOT silently generate. Wait for human confirmation before using `/zerospec:sa`.

## AI Auto-Trigger Heuristics (Zero-Dependency)

> GenAI Agents MUST autonomously assess document needs during every coding task.
> This table is the **single decision matrix** — no external tooling required.

| Signal Detected in Task | Document to Create/Update | AI Action Mode |
| :--- | :--- | :--- |
| New/modified endpoint, handler, or public API; Request/Response schema change; permission or business rule change; behavioral bugfix | **SPEC** | **Mandatory**: update in the same changeset. |
| Cross-module either/or tech decision; new third-party integration choice; shared pattern introduction | **ADR** | **Propose**: explain alternatives, draft ADR after human approval. |
| Brownfield codebase with no current architecture overview; large-scale module restructure (3+ modules); team onboarding gaps | **SA** | **Propose**: suggest scope, wait for human confirmation. |
| Deployment topology, runtime configuration, IaC, or CI/CD release behavior changes | **INFRA** | **Mandatory** when deployment behavior changes. |
| None of the above signals detected | — | State "No doc update needed" with reason in `### Docs Impact`. |

## Candidate Documents (Lazy Evaluation)

| Candidate | Trigger |
| --------- | ------- |
{From SCAN's "Recommended Minimal SDD Document Set"}

## Document Index

| Document                              | Path | Status |
| ------------------------------------- | ---- | ------ |
| (Update this table as docs are added) |      |        |
```

## Step 3.5: Generate Cross-Tool Import Files

在 `AGENTS.md` 寫入完成後，生成以下兩個工具專屬橋接檔：

### File 3: CLAUDE.md

```markdown
@AGENTS.md

## Claude Code Supplements

<!-- Add Claude Code-specific rules below if needed. -->
<!-- Rules here are IN ADDITION to AGENTS.md, not replacements. -->
```

> - 若 `CLAUDE.md` 已存在且包含 `@AGENTS.md` → 跳過，不覆蓋。
> - 若 `CLAUDE.md` 已存在但**不包含** `@AGENTS.md` → 在檔案最前面插入 `@AGENTS.md`，並告知使用者已補齊 import。
> - 若 `CLAUDE.md` 不存在 → 建立新檔。

### File 4: GEMINI.md

```markdown
@./AGENTS.md

<!-- Add Gemini CLI-specific supplements below if needed. -->
```

> - 若 `GEMINI.md` 已存在且包含 `@./AGENTS.md` 或 `@AGENTS.md` → 跳過，不覆蓋。
> - 若 `GEMINI.md` 已存在但**不包含** import → 在檔案最前面插入 `@./AGENTS.md`，並告知使用者已補齊 import。
> - 若 `GEMINI.md` 不存在 → 建立新檔。

## Step 4: Assessment and Next Steps

After assembling both files, output the following assessment in the conversation (DO NOT write to file):

1. **Scan summary**: List detected tech stack, module count scale (few/moderate/many), existing docs/ file count
2. **Project type**: Based on detected Controller/endpoint count, mark **Greenfield** (< 10 endpoints or brand new) or **Brownfield** (existing moderate/large API surface)
3. **Recommended first SPEC**: Adjust recommendation by project type:
   - Greenfield: Create the first SPEC as soon as the first real API endpoint is complete (follow the development track)
   - Brownfield: Pick one API from a domain with code changes in the last 30 days and create the first SPEC
4. **Recommended minimal document set**: Based on project scale, suggest initial SDD documents (e.g., "Start with 1 SPEC + 1 SA; create ADR only when a decision arises")
5. **Next steps**: Output recommendations based on detected project type:

   **Greenfield path**:
   - Enter event-driven mode directly
   - Recommendation: Run SPEC Prompt as soon as the first real API endpoint is complete
   - Priority: `SPEC → ADR (when decisions arise) → SA (at milestones)`

   **Brownfield path**:
   - Run **SA Prompt** first (produce a system architecture snapshot for AI to gain global understanding)
   - Then pick an API with changes in the last 30 days as the priority for the first **SPEC**
   - Reminder: Write SPEC as As-Is (describe current code behavior — DO NOT mix in To-Be improvements)
   - Priority: `SA → High-priority SPEC (backfill) → Normal SPEC triggered by development`

## Drift Prevention Rules (Apply to all output)

- Write versions as Major.Minor only — omit Patch
- DO NOT list exact file counts; describe structural patterns
- Each version number MUST appear only once; second references MUST use "see X declaration"
- Declare "version source of truth" pointing to config files
- If any field lacks code or config evidence, mark `[unverified]` — DO NOT guess
- This skill produces `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `docs/README.md`; DO NOT create other docs/ sub-documents
- If existing docs/ files are found, reference them in the "GenAI Docs Navigation" table — DO NOT create or modify them
- AGENTS.md MUST NOT embed docs governance rules (classification table, naming regex); those belong in docs/README.md
