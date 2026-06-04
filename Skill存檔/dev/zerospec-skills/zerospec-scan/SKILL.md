---
name: zerospec:scan
metadata:
  version: 0.5.2
description: 掃描目標專案並產出結構化分析報告，不寫入任何檔案。觸發時機：/zerospec:scan、開始使用 ZeroSpec、初始化專案文件、分析專案現狀、INIT-SCAN。
---

# ZeroSpec — INIT-SCAN

分析目前專案狀態，確定以最低成本導入 SDD（規格驅動開發）時應優先建立哪些文件。**此步驟只輸出分析，不寫入任何檔案。**

完成後，使用 `/zerospec:build` 生成 `AGENTS.md` 與 `docs/README.md`。

## 前置狀態確認

執行前先檢查：

- 若 `AGENTS.md` **已存在** → 告知使用者：「AGENTS.md 已存在，通常不需要重新 SCAN。若專案有重大重構，可繼續；否則建議改用 `/zerospec:update`。」並詢問是否繼續。
- 若 `AGENTS.md` **不存在** → 直接執行，無需確認。

---

## Role

Act as a project system analyst.
This task is analysis-only. Do not generate code or write files.

> **Language**: Detect the repository's primary language from README, docs, and code comments. Respond in that language. Default to English if ambiguous.
> To override, prepend `Respond in {locale}` (e.g. `Respond in zh-TW`) before running this skill.

## Goal

Produce a structured status report for this repository. Determine which documents should be created first to adopt SDD (Specification-Driven Development) at minimal cost.

## Definitions

The following are the four document types in SDD lean mode. Use these definitions throughout the analysis:
- **SA** (System Analysis): Milestone-level analysis snapshot recording gaps between specs and actual state
- **ADR** (Architecture Decision Record): Single architecture decision with context, options, and conclusion; append-only — supersede with a new ADR, never edit
- **SPEC** (Interface Specification): Behavioral contract for external interfaces; serves as the primary development reference (Source of Truth), includes Changelog
- **INFRA** (Infrastructure): Infrastructure selection and topology; Library projects may use INTEGRATION instead

## Analysis Framework

### Core Analysis (Required)

1. **Tech stack and runtime type**:
   - Read build.gradle / package.json / .csproj / pyproject.toml / go.mod / requirements.txt / Cargo.toml or equivalent config files
   - Extract language version, framework version (Major.Minor only — omit Patch)
   - Determine project type: library / API service / frontend SPA / monorepo / CLI tool / etc.

2. **External interfaces and integration points**:
   - API endpoints, SDKs, events, scheduled jobs, MQ, external system integrations
   - Which interfaces are most worth specifying first (high complexity, frequent changes, or multiple consumers)

3. **Existing documentation status**:
   - Identify README, design docs, API docs, architecture docs, spec files
   - Which can serve as Source of Truth
   - Which are likely outdated or insufficient

### Supplementary Analysis (Include only when findings exist)

4. **Directory and module structure**: Main directories' responsibilities, whether clear layering exists
5. **Architecture decisions and risk signals**: Important architecture choices inferred from code, places where ADRs may be needed

### Scan Order

Scan in this priority: root config files (package.json / build.gradle / .csproj etc.) → source entry (src/) → docs/ → CI/CD.

## Output Format

Use the structure below. Keep each section to 5–15 lines. Draft B-class content during analysis and mark each section `[needs review]`.

### 1. Project Status Summary
List 5–10 bullet points describing the current state of the project.

### 2. Tech Stack Extraction (A-class)
List all technical information auto-detected from config files.

### 3. Core Modules and Boundaries
List main modules, their responsibilities, and upstream/downstream relationships.

### 4. B-class Draft
Present these 5 items in order, each marked `[needs review]`:
1. **Docs navigation table**: Scan docs/, use intent-driven format (left column: "What you want to do", right column: path)
2. **Domain-to-code map**: Scan core classes, group by naming correlation
3. **Architecture layers**: Infer layering pattern or data flow from existing code
4. **Naming conventions**: Identify existing naming patterns from statistics
5. **Related projects**: Detect cross-project dependencies from build config or relative paths

### 5. Top Priorities for Specification (1–3 items)
List the topics most urgently needing a Source of Truth. Explain why.

### 6. Recommended Minimal SDD Document Set
Give direct recommendations in this format:
- `SA-001`: What to analyze
- `ADR-001`: What decision to record (omit if no clear need)
- `SPEC-001`: What interface or behavior to describe
- `INTEGRATION.md`: What integration flow to document (omit if not needed)

### 7. Open Questions (max 5)
List the most critical questions that cannot be determined from the current state. These will be carried into the next step (INIT-BUILD).

## Rules

- **This skill MUST NOT write any files** — output analysis in the conversation only
- Prioritize understanding the current state and building minimal consensus; DO NOT introduce heavy processes
- Write versions as Major.Minor only — omit Patch
- DO NOT list exact file counts; describe structural patterns (e.g., "multiple Controllers" not "19 Controllers")
- If any field lacks code or config evidence, mark `[unverified]` — DO NOT guess
