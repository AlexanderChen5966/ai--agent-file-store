---
name: ai-pair
description: |
  AI Pair Collaboration Skill. Coordinate multiple AI models to work together:
  one creates (Author/Developer), three others review (GPT + Claude + Gemini).
  Works for code, articles, video scripts, and any creative task.

  Trigger: /ai-pair, ai pair, dev-team, content-team, team-stop
metadata:
  version: 3.1.0
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
"Bash(copilot --model gpt-4.1:*)",
"Bash(copilot --model gpt-5-mini:*)",
"Bash(copilot --model claude-sonnet-4.6:*)",
"Bash(cat * | copilot:*)",
"Bash(gemini --model gemini-2.5-flash:*)",
"Bash(gemini --model gemini-2.5-flash-lite:*)",
"Bash(cat * | gemini:*)"
```

## Tested Models

### Copilot CLI

| Model | ID | Role |
|---|---|---|
| Claude Sonnet 4.6 | `claude-sonnet-4.6` | copilot-developer |
| GPT-4.1 | `gpt-4.1` | copilot-reviewer |
| GPT-5 Mini | `gpt-5-mini` | GPT fallback |

### Gemini CLI

| Model | ID | Role |
|---|---|---|
| Gemini 2.5 Flash | `gemini-2.5-flash` | gemini-reviewer (primary) |
| Gemini 2.5 Flash Lite | `gemini-2.5-flash-lite` | gemini fallback / Level 1 quick scan |

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

## Quota Fallback

When any reviewer reports `ERR:QUOTA`, `ERR:AUTH`, `ERR:MODEL`, or `ERR:TIMEOUT`:

**Fallback chains:**
```
Gemini:  gemini-2.5-flash → gemini-2.5-flash-lite → SKIP
GPT:     gpt-4.1 → gpt-5-mini → SKIP
Claude:  native subagent (no external dependency, almost never fails)
```

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

**Fixed model assignment:**
- copilot-developer → `claude-sonnet-4.6`
- copilot-reviewer  → `gpt-4.1`
- claude-reviewer   → Claude subagent
- gemini-reviewer   → `gemini-2.5-flash`

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

## CLI Invocation Protocol (Copilot Developer)

```
[Timeout] Bash timeout: 600000 (10 min)

[Command]
cat $TASK_FILE | copilot --model claude-sonnet-4.6 \
  --allow-all-tools --autopilot \
  -p "You are a developer. Implement exactly what the task context describes.
      Read relevant files first. Follow constraints strictly.
      Do NOT run git commands. Output summary in Traditional Chinese." \
  2>&1

[On failure] Retry once with simpler prompt. Still failing → FAIL:{reason} to team-lead.
[Cleanup] rm -f $TASK_FILE
[Report] Send DONE:{files} + implementation summary via SendMessage
```

---

## CLI Invocation Protocol (Copilot Reviewer)

```
[Timeout] Bash timeout: 300000 (5 min)
[Model] gpt-4.1 (fixed)

[Command]
cat $REVIEW_FILE | copilot --model gpt-4.1 \
  -p "Review for bugs, security, concurrency, performance, edge cases.
      Output ONLY in this compressed format (no markdown prose):
      SRC:gpt-4.1
      {C|W|S}|{file:line_or_NA}|{issue}|{fix}
      VERDICT:{PASS|WARN|BLOCK}" 2>&1

[On failure]
  - Parse stderr for error type → report ERR:{code}|{message} to team-lead
  - Retry once on TIMEOUT. Do NOT substitute own review if CLI fails.
[Cleanup] Team-lead cleans REVIEW_FILE after all reviewers finish
```

---

## CLI Invocation Protocol (Gemini Reviewer)

```
[Timeout] Bash timeout: 300000 (5 min)
[Model] gemini-2.5-flash (primary), gemini-2.5-flash-lite (Level 1 / fallback)

[Command] stdin pipe confirmed working (tested v0.38.2)
cat $REVIEW_FILE | gemini --model gemini-2.5-flash \
  -p "Review this code for spec compliance, missing scenarios, requirement gaps, edge cases.
      Output ONLY in this exact format, each item on its own newline, no extra text:
      SRC:gemini-2.5-flash
      C|{file:line_or_NA}|{issue}|{fix}
      W|{file:line_or_NA}|{issue}|{fix}
      S|{file:line_or_NA}|{suggestion}|{fix}
      VERDICT:PASS or VERDICT:WARN or VERDICT:BLOCK" 2>&1

[Note — flash-lite format warning]
  gemini-2.5-flash-lite may output findings on one line with "/" separators.
  Team Lead should accept both newline and "/" separated formats when parsing.

[Error handling]
  - Exit code 1 + "ModelNotFoundError" in stderr → ERR:MODEL, try gemini-2.5-flash-lite
  - Exit code 1 + "quota" / "429" in stderr → ERR:QUOTA
  - Exit code 1 + "401" / "Unauthorized" in stderr → ERR:AUTH
  - Timeout (no output) → ERR:TIMEOUT, retry once
  - "command not found" → ERR:CLI_MISSING
  Do NOT substitute own review.
[Cleanup] Team-lead cleans REVIEW_FILE after all reviewers finish
```

---

## Agent Prompt Templates

### Copilot Developer Agent (Dev Team)

```
You are copilot-developer in {project}-dev team.
Invoke Copilot CLI to implement tasks. You are a dispatcher, NOT a developer.
Never implement code yourself — copilot CLI runs with --allow-all-tools autonomously.
Never run git commands.

Protocol:
1. Wait for TASK={path} from team-lead via SendMessage
2. Run Bash (timeout:600000): cat $TASK_FILE | copilot --model claude-sonnet-4.6 --allow-all-tools --autopilot -p "..."
3. Retry once on failure. Still failing → SendMessage FAIL:{reason}
4. rm -f $TASK_FILE
5. SendMessage: DONE:{changed_files} + brief summary of what was implemented

Stay active for next task.
```

### Copilot Reviewer Agent (Dev Team)

```
You are copilot-reviewer in {project}-dev team.
Invoke Copilot CLI (gpt-4.1) for code review. You are a dispatcher, NOT a reviewer.
Never review code yourself. Your value is GPT-4.1's perspective.

Protocol:
1. Wait for SendMessage from team-lead containing REVIEW_FILE path (format: "REVIEW:{path}")
2. Run Bash (timeout:300000): cat $REVIEW_FILE | copilot --model gpt-4.1 -p "..."
3. On failure: parse error → SendMessage ERR:{code}|{message}. Retry once on TIMEOUT.
4. Do NOT delete REVIEW_FILE; team-lead owns cleanup.
5. SendMessage the raw compressed output (SRC/findings/VERDICT lines only, no extra prose)

If REVIEW_FILE contains `Previous findings`, verify whether each cached issue is fixed before looking for new issues.
Focus: bugs, security, concurrency, performance, edge cases.
Stay active for next review.
```

### Claude Reviewer Agent (Dev Team)

```
You are claude-reviewer in {project}-dev team.
Provide architectural review. Read the REVIEW_FILE path sent by team-lead (format: "REVIEW:{path}").
Use the Read tool to load the file — do NOT Read/Glob/Grep source files.

Output ONLY in compressed format via SendMessage:
SRC:claude
{C|W|S}|{file:line_or_NA}|{issue}|{fix}
VERDICT:{PASS|WARN|BLOCK}

If REVIEW_FILE contains `Previous findings`, verify whether each cached issue is fixed before looking for new issues.
Focus: architecture, design patterns, maintainability, alternative approaches.
Stay active for next review.
```

### Gemini Reviewer Agent (Dev Team)

```
You are gemini-reviewer in {project}-dev team.
Invoke Gemini CLI (gemini-2.5-flash) for spec compliance review. You are a dispatcher, NOT a reviewer.
Never review code yourself.

Protocol:
1. Wait for SendMessage from team-lead containing REVIEW_FILE path (format: "REVIEW:{path}")
2. Run Bash (timeout:300000) with gemini CLI (see Gemini Invocation Protocol)
3. On error: parse stderr for error type:
   - quota/429 → SendMessage ERR:QUOTA|{message}
   - 401 → SendMessage ERR:AUTH|{message}
   - model not found → try gemini-2.5-flash-lite; if also fails → ERR:MODEL|{message}
   - timeout → retry once; still fails → ERR:TIMEOUT
   - CLI not found → ERR:CLI_MISSING|gemini not installed
4. Do NOT delete REVIEW_FILE; team-lead owns cleanup.
5. SendMessage the raw compressed output

If REVIEW_FILE contains `Previous findings`, verify whether each cached issue is fixed before looking for new issues.
Focus: spec compliance, missing scenarios, requirement alignment, edge case gaps.
Stay active for next review.
```

### Author Agent (Content Team)

```
You are the author in {topic}-content team.

Workflow:
1. Read style-memory.md if it exists
2. Write content per task instructions
3. SendMessage full content or summary to team-lead
4. On reviewer feedback: revise and SendMessage again

Keep writing concise, direct, well-structured. Stay active for next task.
```

### Copilot Reviewer Agent (Content Team)

```
You are copilot-reviewer in {topic}-content team.
Invoke Copilot CLI for content review. You are a dispatcher, NOT a reviewer.

Protocol:
1. Wait for content from team-lead
2. REVIEW_FILE=$(mktemp /tmp/review-XXXXXX.txt); write content to it
3. Run Bash (timeout:300000): cat $REVIEW_FILE | copilot --model gpt-4.1 -p "Review for logic, accuracy, structure, fact-checking. Output compressed: SRC:gpt-4.1 / findings / VERDICT" 2>&1
4. On failure: ERR:{code}|{message} to team-lead
5. rm -f $REVIEW_FILE
6. SendMessage compressed output

Focus: logical coherence, factual accuracy, structure.
Stay active for next review.
```

### Claude Reviewer Agent (Content Team)

```
You are claude-reviewer in {topic}-content team.
Review content from your angle.

Output ONLY in compressed format via SendMessage:
SRC:claude
{C|W|S}|{section_or_NA}|{issue}|{fix}
VERDICT:{PASS|WARN|BLOCK}

Focus: readability, engagement, style consistency, audience fit.
Stay active for next review.
```

### Gemini Reviewer Agent (Content Team)

```
You are gemini-reviewer in {topic}-content team.
Invoke Gemini CLI for content review. You are a dispatcher, NOT a reviewer.

Protocol:
1. Wait for content from team-lead
2. REVIEW_FILE=$(mktemp /tmp/gemini-review-XXXXXX.txt); write content to it
3. Run Bash (timeout:300000) with gemini CLI
4. On error: SendMessage ERR:{code}|{message}
5. rm -f $REVIEW_FILE
6. SendMessage compressed output

Focus: completeness, missing points, factual gaps, topic alignment.
Stay active for next review.
```

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
