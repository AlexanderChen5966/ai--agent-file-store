---
name: ai-pair
description: |
  AI Pair Collaboration Skill. Coordinate multiple AI models to work together:
  one creates (Author/Developer), three others review (GPT + Claude + Gemini).
  Works for code, articles, video scripts, and any creative task.

  Trigger: /ai-pair, ai pair, dev-team, content-team, team-stop
metadata:
  version: 4.1.0
---

# AI Pair Collaboration

Coordinate heterogeneous AI teams: one creates, three review from different angles.
Uses Claude Code's native Agent Teams with GitHub Copilot CLI (GPT), Claude subagent, and Gemini CLI as reviewers.

## Why Multiple AI Reviewers?

Different AI models have fundamentally different review tendencies. Using reviewers from different model families maximizes coverage across three orthogonal dimensions:

| Reviewer | Model | Focus |
|---|---|---|
| copilot-reviewer | GPT-4.1 | bugs, security, concurrency, performance, edge cases |
| claude-reviewer | Claude | architecture, design patterns, maintainability, alternatives |
| gemini-reviewer | gemini-2.5-flash | spec compliance, missing scenarios, requirement alignment |

## Commands

```bash
/ai-pair dev-team [project]        # Start dev team (default: Level 2 review)
/ai-pair dev-team [project] --quick  # Level 1: fast scan (gemini only)
/ai-pair dev-team [project] --deep   # Level 3: all 3 reviewers in parallel
/ai-pair content-team [topic]      # Start content team
/ai-pair team-stop                 # Shut down the team
```

Examples:
```bash
/ai-pair dev-team HighlightCut
/ai-pair dev-team SSGS-11275 --deep
/ai-pair content-team AI-Newsletter
/ai-pair team-stop
```

## Tier System (Phase 1 Verified ✅)

Model selection is guided by **Tier** (cost + capability):

| Tier | Cost | Models | Use Case |
|---|---|---|---|
| **FREE** | 0x | `gpt-5-mini`, `gpt-4.1` | Fallback, quota exhaust, cost-sensitive tasks |
| **LOW** | 0.33x | `gpt-5.4-mini`, `gemini-3.1-flash-lite-preview` | Level 1 quick scans |
| **STANDARD** | 1x | `claude-sonnet-4.6`, `gpt-5.2/5.3/5.4`, `gemini-2.5-flash`, `gemini-3-flash-preview` | Default for Level 2/3 reviews |
| **COMPLEX** | 1x+ | Reserved for large-scale, multi-turn reasoning (future) | Enterprise tasks |

**Team Lead Model Selector:** Assign models by task complexity, not hard-coded roles.

## Prerequisites

- **Claude Code** — Team Lead + agent runtime
- **Copilot CLI** (`copilot`) — for copilot-reviewer and copilot-developer
- **Gemini CLI** (`gemini`) — for gemini-reviewer

Verify installation:
```bash
copilot --version
gemini --version
```

### Permissions Setup (Required)

Add to `.claude/settings.local.json`:

```json
"Write(//tmp/**)",
"Bash(mktemp:*)",
"Bash(copilot --model gpt-5-mini:*)",
"Bash(copilot --model gpt-4.1:*)",
"Bash(copilot --model gpt-5.4-mini:*)",
"Bash(copilot --model gpt-5.2-codex:*)",
"Bash(copilot --model gpt-5.3-codex:*)",
"Bash(copilot --model gpt-5.2:*)",
"Bash(copilot --model gpt-5.4:*)",
"Bash(copilot --model claude-sonnet-4.6:*)",
"Bash(cat * | copilot:*)",
"Bash(gemini --model gemini-2.5-flash:*)",
"Bash(gemini --model gemini-2.5-flash-lite:*)",
"Bash(gemini --model gemini-3-flash-preview:*)",
"Bash(gemini --model gemini-3.1-flash-lite-preview:*)",
"Bash(cat * | gemini:*)"
```

## Tested Models (Phase 1 Verified ✅ 2026-05-14)

### Copilot CLI

| Model | ID | Tier | Role | Cost |
|---|---|---|---|---|
| GPT-5 Mini | `gpt-5-mini` | FREE | L1 fallback | 0x (FREE) |
| GPT-4.1 | `gpt-4.1` | FREE | L2 fallback | 0x (FREE) |
| Claude Sonnet 4.6 | `claude-sonnet-4.6` | STANDARD | copilot-developer | 1x |
| GPT-5.4 Mini | `gpt-5.4-mini` | LOW | - | 0.33x |
| GPT-5.2 Codex | `gpt-5.2-codex` | STANDARD | copilot-reviewer alt | 1x |
| GPT-5.3 Codex | `gpt-5.3-codex` | STANDARD | copilot-reviewer alt | 1x |
| GPT-5.2 | `gpt-5.2` | STANDARD | copilot-reviewer alt | 1x |
| GPT-5.4 | `gpt-5.4` | STANDARD | copilot-reviewer alt | 1x |

### Gemini CLI

| Model | ID | Tier | Role | Status |
|---|---|---|---|---|
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | STANDARD | gemini-reviewer alt | ✅ verified |
| Gemini 3.1 Flash Lite Preview | `gemini-3.1-flash-lite-preview` | LOW | Level 1 quick scan alt | ✅ verified |
| Gemini 2.5 Flash | `gemini-2.5-flash` | STANDARD | gemini-reviewer (primary) | ✅ verified |
| Gemini 2.5 Flash Lite | `gemini-2.5-flash-lite` | LOW | gemini fallback / Level 1 | ✅ verified |

## Team Architecture

### Dev Team (`/ai-pair dev-team [project]`)

```
User (Commander)
  │
Team Lead (current Claude session)
  │  Role: planner — reads codebase, writes task context file, coordinates
  │
  ├── copilot-developer (Claude Code agent)
  │     Invokes: copilot --model claude-sonnet-4.6 --allow-all-tools --autopilot
  │     Role: executes implementation based on Team Lead's task context file
  │
  ├── copilot-reviewer (Claude Code agent)     [Level 2 / Level 3]
  │     Invokes: copilot --model gpt-4.1 -p "..."
  │     Focus: bugs, security, concurrency, performance, edge cases
  │
  ├── claude-reviewer (Claude Code agent)      [Level 2 / Level 3]
  │     Role: Claude second perspective
  │     Focus: architecture, design patterns, maintainability
  │
  └── gemini-reviewer (Claude Code agent)      [Level 1 / Level 3]
        Invokes: gemini --model gemini-2.5-flash -p "..."
        Focus: spec compliance, missing scenarios, requirement alignment
```

### Review Levels

```
Level 1 — Quick scan (--quick)
  Reviewers: gemini-reviewer only (gemini-2.5-flash-lite for speed)
  When: typo fix, i18n key, small UI tweaks
  Est. time: ~30s

Level 2 — Standard review (default)
  Reviewers: copilot-reviewer + claude-reviewer (parallel)
  When: general feature, bug fix
  Est. time: ~2 min

Level 3 — Deep review (--deep)
  Reviewers: all 3 in parallel
  When: architecture changes, high-risk modules, core logic
  Est. time: ~3 min
```

**Auto-escalation:** Level 1 finds CRITICAL → auto-escalate to Level 2 (notify user). Level 2 finds CRITICAL in core module → suggest Level 3 (ask user).

## Inter-Agent Protocol v1

> Agent-to-agent messages use compressed format only.
> Only the final output presented to the user is human-readable.

### Review Report (Compressed)

```
SRC:{model_id}
{severity}|{file:line_or_NA}|{issue}|{fix}
VERDICT:{PASS|WARN|BLOCK}
```

Severity codes:
- `C` = critical (blocks merge)
- `W` = warning (should fix)
- `S` = suggestion

Example:
```
SRC:gpt-4.1
C|car_edit_page.dart:142|vehicleData null→crash|add null check before access
W|car_response.dart:58|fromJson empty array unhandled|add isEmpty guard
S|NA|extract validation to mixin
VERDICT:BLOCK
```

### Error Report

```
SRC:{model_id}
ERR:{code}|{raw_message}
```

Error codes: `QUOTA` | `AUTH` | `MODEL` | `TIMEOUT` | `CLI_MISSING`

### Task Dispatch / Acknowledge

```
TASK:{file_path}          # Team Lead → developer
ACK                       # developer → Team Lead (started)
DONE:{file1,file2,...}    # developer → Team Lead (finished)
FAIL:{reason}             # developer → Team Lead (failed)
```

## Quota Fallback (Decision B: Unified FREE Tier ✅)

When any reviewer reports `ERR:QUOTA`, `ERR:AUTH`, `ERR:MODEL`, or `ERR:TIMEOUT`:

**Fallback chains (Phase 1 verified):**
```
Gemini:  gemini-2.5-flash → gemini-2.5-flash-lite → SKIP
GPT:     gpt-5-mini (FREE) → gpt-4.1 (FREE) → SKIP
Claude:  native subagent (no external dependency, almost never fails)
```

**Decision rationale:**
- Both `gpt-5-mini` and `gpt-4.1` are verified as FREE (0x cost)
- Removes Claude Haiku 4.5 (cost contradiction: fallback 0.33x > primary 0x)
- Ensures unified free-tier retry logic, no cost volatility

**Minimum viable threshold:**
- 2+ reviewers available → continue with note
- 1 reviewer available → continue with warning
- 0 reviewers → abort, ask user to fix

**Team Lead decision table:**

| ERR code | Action |
|---|---|
| QUOTA | Mark SKIPPED, continue with remaining |
| AUTH | Prompt user to re-login, continue |
| MODEL | Try fallback chain; if all fail → SKIP |
| TIMEOUT | Retry once; if still fails → SKIP |
| CLI_MISSING | Mark SKIPPED, show install command |

## Workflow (Semi-Automatic)

1. **User assigns task** → Team Lead reads codebase, writes task context file
2. **Team Lead dispatches** `TASK:{path}` → copilot-developer
3. **copilot-developer implements** → reports `DONE:{files}` + summary
4. **Team Lead shows result** to user, asks for review approval
5. **User approves** → Team Lead builds one shared diff/review file, then dispatches to reviewers (parallel per level)
6. **Reviewers report** compressed format → Team Lead collects all, handles any ERR
7. **Team Lead translates** to human-readable and presents:

```markdown
## Review 結果

### GPT-4.1 Review（bugs / security / performance）
❌ CRITICAL `file.dart:142` — issue description
⚠️ WARNING `file.dart:58` — issue description

### Claude Review（architecture / maintainability）
✅ 架構合理，無 blocking issue

### Gemini Review（spec compliance / missing scenarios）
⚠️ WARNING — missing edge case: batch size = 0 unhandled

**綜合判定：BLOCK** — 需修復 1 個 critical issue
```

If a reviewer was skipped:
```markdown
### Gemini Review
⏭️ 已跳過 — gemini-2.5-flash 額度耗盡（ERR:QUOTA）
建議額度恢復後用 `--deep` 重新 review
```

8. **User decides** → "Revise" (back to step 1 with feedback) or "Pass" (next task or end)
9. **Team Lead handles local review cache** (see Review Context Protocol Step 0 / Step 6):
   - PASS → delete `CACHE_FILE`
   - WARN / BLOCK → write findings to `CACHE_FILE`; next re-review will prepend as `Previous findings`

**Auto PASS/BLOCK logic:**
```
All VERDICT=PASS  → auto PASS, notify user
Any VERDICT=BLOCK → BLOCK, user decides
All WARN, no BLOCK → WARN, list warnings for user
```

## Team Lead Execution Steps

### Step 1: Create Team

```
TeamCreate: team_name = "{project}-dev" or "{topic}-content"
```

### Step 2: Pre-flight CLI Check

```bash
copilot --version || echo "COPILOT_MISSING"
gemini --version || echo "GEMINI_MISSING"
```

Warn user of any missing CLI and ask to proceed with degraded mode or abort.

**Dynamic model selection (Decision C: Team Lead flexibility ✅):**

Default model assignment (backward compatible):
- copilot-developer → `claude-sonnet-4.6` (STANDARD tier)
- copilot-reviewer  → `gpt-4.1` or `gpt-5-mini` (FREE tier, auto-fallback)
- claude-reviewer   → Claude subagent (always available)
- gemini-reviewer   → `gemini-2.5-flash` (STANDARD tier, fallback to `gemini-2.5-flash-lite`)

**Team Lead override (advanced usage):**
Directly invoke Bash with `--model` parameter:
```bash
copilot --model gpt-5.3-codex -c @TASK_FILE --allow-all-tools --autopilot
```
Useful for testing specific tier models or avoiding quota exhaustion.

### Step 3: Launch Agents

Launch 4 agents using the Agent tool with `subagent_type: "general-purpose"`.

### Step 4: Confirm to User

```
Team ready.

Team: {team_name}
Members:
  - copilot-developer: ready (claude-sonnet-4.6)
  - copilot-reviewer:  ready (gpt-4.1)
  - claude-reviewer:   ready (Claude)
  - gemini-reviewer:   ready (gemini-2.5-flash)

Review level: Level 2 (default) — use --quick or --deep to change

Awaiting your first task.
```

## Team Lead Planning Protocol (Dev Team)

### Bias Mitigation: High-Confidence Trap Prevention ✅

Team Lead should NOT assume confidence in:
- **Self-review:** Always send code to at least 2 reviewers, never skip review
- **"Small" changes:** Even typos get 1-reviewer pass (Level 1 --quick); never auto-accept without review
- **Code familiarity:** High-risk modules (auth, payment, core logic) demand Level 3 --deep
- **Decision overrides:** If all 3 reviewers report BLOCK, accept it; do NOT dismiss consensus

**Auto-escalation trigger:**
- If Team Lead overrides 2+ BLOCK verdicts in 5 tasks → halt and audit for bias

Before dispatching to copilot-developer:

1. Read codebase — Read/Glob/Grep relevant files
2. Clarify if ambiguous — ask ONE question max
3. Split work into a single task only. Do NOT batch multiple tasks into one dispatch.
4. Write task context file:

```bash
TASK_FILE=$(mktemp /tmp/task-context-XXXXXX.md)
```

**Task context file format:**

```markdown
# Task: {task name}

## Project Context
- Project path: {project_path}
- Tech stack: {e.g. Flutter + Riverpod}
- Relevant files:
  - {file1}: {role}
  - {file2}: {role}

## Requirement
{Clear description}

## Implementation Guide
{Specific instructions, before/after snippets, edge cases}

## Files to Modify
- {filepath}: {what to change}

## Constraints
- {constraint}
- {project-specific rules from CLAUDE.md}

## Verification
- {how to verify}
```

5. Dispatch: `TASK:{path}` via SendMessage to copilot-developer
6. After `DONE:{files}`, delete the task file and create a new one for the next task only

### Review Context Protocol

Before dispatching to reviewers:

**Step 0 — Cache check**

```bash
CACHE_DIR=.ai-pair-cache/review-findings
CACHE_FILE="$CACHE_DIR/{task_id}.md"
```

- If `CACHE_FILE` exists and all reuse conditions are met (same task id, same workspace, same reviewer set, same review level, age ≤ 48h, small iterative fix) → read it; set `HAS_CACHE=true`
- Otherwise → `HAS_CACHE=false`

**Step 1 — Generate REVIEW_FILE**

```bash
mkdir -p "$CACHE_DIR"
REVIEW_FILE=$(mktemp /tmp/review-XXXXXX.txt)
git diff --no-color HEAD~1 > "$REVIEW_FILE"
```

2. If a changed file is newly added or the diff omits essential context, append the minimum required file content.
3. If `HAS_CACHE=true`, prepend the cached findings as a `Previous findings` section so reviewers verify fixes first, then look for new issues.
4. Reuse the same `REVIEW_FILE` path for all reviewers in the same round. Do NOT let each reviewer rebuild its own full-source package.
5. Send `REVIEW:{path}` to each reviewer via SendMessage. Reviewers must NOT read source files on their own — REVIEW_FILE is their only input.

**Step 6 — Post-review cache write/clear** (after all reviewers return VERDICT)

- If综合判定 is **PASS** → delete `CACHE_FILE` (task done, cache no longer needed)
- If WARN or BLOCK → write normalized findings to `CACHE_FILE`:

```bash
# CACHE_FILE format
task_id: {task_id}
review_level: {--quick | default | --deep}
reviewer_set: {copilot,claude,gemini}
changed_files: {file1,file2,...}
timestamp: {ISO8601}
findings:
{SRC/findings lines from all reviewers, excluding VERDICT}
```

### Review Cache Mechanism

Use local cache only for the same user, same machine, same workspace. Never commit review cache to git.

**Cache contents**
- task id
- review level (`--quick` / default / `--deep`)
- reviewer set
- changed file list
- normalized findings summary for `Previous findings`
- review timestamp

**When to write cache**
- After a review round completes and at least one reviewer returns `VERDICT`
- Save normalized findings only; do not store raw CLI logs

**When cache may be reused**
- Same task id
- Same workspace
- Same review level or narrower scope
- Same reviewer set
- Cache age <= 48 hours
- Current changes are a small iterative fix on the same file set

**When cache must be cleared**
- User confirms PASS / task done
- Task id changes
- Requirement pivots
- Changed-file set grows materially
- Review level changes
- Reviewer set changes
- Cache unused for more than 48 hours
- Team-lead is unsure whether reuse is safe

**Reuse procedure**
1. Read `CACHE_FILE`
2. Prepend `Previous findings` to `REVIEW_FILE`
3. Tell reviewers to verify whether old issues are fixed first
4. Then review the current diff for new issues
5. Overwrite `CACHE_FILE` with the latest normalized findings after the round

---

## CLI Invocation Protocols

See `reference/cli-invocation-ref.md` for detailed technical specifications:

- **[Copilot Developer](reference/cli-invocation-ref.md#cli-invocation-protocol-copilot-developer)** — Task execution with `--allow-all-tools --autopilot`
- **[Copilot Reviewer](reference/cli-invocation-ref.md#cli-invocation-protocol-copilot-reviewer)** — Code review for bugs/security/performance
- **[Gemini Reviewer](reference/cli-invocation-ref.md#cli-invocation-protocol-gemini-reviewer)** — Spec compliance review with error handling

**Quick reference:**
- All use stdin piping (`cat $FILE | cli-name --model MODEL -p "..."`)
- All output compressed format (SRC / findings / VERDICT)
- All have error handling + fallback logic
- Phase 1 verified: `--allow-all-tools --autopilot` compatible with all Copilot models ✅

---

## Agent Prompt Templates

See `reference/agents-prompts.md` for copy-paste agent initialization prompts:

**Dev Team:**
- [Copilot Developer](reference/agents-prompts.md#copilot-developer-agent-dev-team) — Implements tasks via Copilot CLI
- [Copilot Reviewer](reference/agents-prompts.md#copilot-reviewer-agent-dev-team) — Reviews for bugs/security/performance
- [Claude Reviewer](reference/agents-prompts.md#claude-reviewer-agent-dev-team) — Reviews for architecture/maintainability
- [Gemini Reviewer](reference/agents-prompts.md#gemini-reviewer-agent-dev-team) — Reviews for spec compliance

**Content Team:**
- [Author Agent](reference/agents-prompts.md#author-agent-content-team) — Writes content per task
- [Copilot Reviewer](reference/agents-prompts.md#copilot-reviewer-agent-content-team) — Reviews for logic/accuracy
- [Claude Reviewer](reference/agents-prompts.md#claude-reviewer-agent-content-team) — Reviews for readability/engagement
- [Gemini Reviewer](reference/agents-prompts.md#gemini-reviewer-agent-content-team) — Reviews for completeness/gaps

All 8 agents dispatch to external CLI or subagents; copy prompt text as-is into SendMessage.

## Team Lead Translation Layer

When presenting review results to the user, translate compressed format to human-readable:

```
C → ❌ CRITICAL
W → ⚠️ WARNING
S → 💡 SUGGESTION
VERDICT:PASS  → ✅
VERDICT:WARN  → ⚠️
VERDICT:BLOCK → ❌ BLOCK
ERR:QUOTA     → ⏭️ 已跳過 — {model} 免費額度耗盡，建議額度恢復後用 --deep 重新 review
ERR:AUTH      → ⏭️ 已跳過 — {model} 認證失敗，請重新登入後重試
ERR:MODEL     → ⏭️ 已跳過 — {model} 無法使用，已嘗試 fallback 或建議稍後重試
ERR:TIMEOUT   → ⏭️ 已跳過 — {model} 執行逾時，已重試一次仍失敗
ERR:CLI_MISSING → ⏭️ 已跳過 — Gemini CLI 未安裝（brew install gemini-cli 或對應安裝方式）
```

---

## Known Limitations & Resolutions (Phase 1 ✅)

### 1. Gemini CLI Chinese Path Encoding

**Issue:** Gemini CLI context supplementation fails when paths contain Chinese characters  
**Signature:** `Failed to read file: "ai-pair-main/\\351\\207\\265..."`  
**Resolution:** Keep TASK_FILE and REVIEW_FILE paths ASCII-only (/tmp/...) — already implemented ✅  
**Impact:** None (by design)

### 2. Gemini Quota Exhaustion

**Issue:** Gemini models occasionally return `exhausted capacity` error  
**Signature:** Exit code 1 + "quota exhausted" in stderr  
**Resolution:** Auto-retry with 1-7 second delay — implemented via fallback chain ✅  
**Impact:** Automatic recovery, no manual intervention needed

### 3. Model Unavailability (Rare)

**Issue:** o1, o3-mini not available (not released or no permission)  
**Resolution:** Do not attempt these models; use Tier STANDARD alternatives ✅  
**Impact:** None (Phase 1 verified 11 models all available)

### 4. Claude Haiku 4.5 Removal

**Issue:** Cost contradiction (fallback 0.33x > primary FREE tier)  
**Resolution:** Removed from model roster; replaced with gpt-4.1 FREE fallback ✅  
**Impact:** Simplified Tier logic, unified free-tier retry strategy

---

## team-stop Flow

When user calls `/ai-pair team-stop`:

1. Send `shutdown_request` to all agents
2. Wait for confirmation
3. Call `TeamDelete`
4. Output:
   ```
   Team shut down.
   Closed: copilot-developer, copilot-reviewer, claude-reviewer, gemini-reviewer
   Resources cleaned up.
   ```

---

## Phase 1 Validation Closure ✅

**Document Version:** 4.1.0 (Phase 1 Verified)  
**Validation Date:** 2026-05-14  
**Validation Status:** ✅ COMPLETE — All 11 models verified, 3 decisions confirmed, ready for production

**Changes from v3.1.0:**
- ✅ Added 7 new Copilot models (gpt-5.4-mini, gpt-5.2/5.3/5.4, gpt-5.2/5.3-codex)
- ✅ Added 2 new Gemini models (gemini-3-flash-preview, gemini-3.1-flash-lite-preview)
- ✅ Removed Claude Haiku 4.5 (cost contradiction)
- ✅ Updated Fallback chain: unified FREE tier (gpt-5-mini → gpt-4.1)
- ✅ Added Tier System (FREE, LOW, STANDARD, COMPLEX)
- ✅ Added dynamic model selection via --model parameter
- ✅ Added High-confidence bias mitigation for Team Lead
- ✅ Documented Gemini CLI limitations & resolutions
- ✅ Verified --allow-all-tools --autopilot compatibility

**Reference:** See `/Users/alexander/GitLab/b2b-manager/ai-pair-main/PHASE1-驗證報告.md` for full test results and decision rationale.

---

*Last updated: 2026-05-15 — Phase 1 implementation complete, ready for v4.1 deployment*
