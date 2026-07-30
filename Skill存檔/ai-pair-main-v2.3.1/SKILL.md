---
name: ai-pair
description: |
  AI Pair Collaboration Skill. Coordinate multiple AI models to work together:
  one creates (Author/Developer), two others review (Copilot + Claude).
  Works for code, articles, video scripts, and any creative task.

  Trigger: /ai-pair, ai pair, dev-team, content-team, team-stop
metadata:
  version: 2.3.1
---

# AI Pair Collaboration

Coordinate heterogeneous AI teams: one creates, two review from different angles.
Uses Claude Code's native Agent Teams capability with GitHub Copilot CLI (GPT) and Claude as reviewers.

## Why Multiple AI Reviewers?

Different AI models have fundamentally different review tendencies. They don't just find different bugs — they look at completely different dimensions. Using reviewers from different model families maximizes coverage.

## Commands

```bash
/ai-pair dev-team [project]       # Start dev team (developer + copilot-reviewer + claude-reviewer)
/ai-pair content-team [topic]     # Start content team (author + copilot-reviewer + claude-reviewer)
/ai-pair team-stop                # Shut down the team, clean up resources
```

Examples:
```bash
/ai-pair dev-team HighlightCut        # Dev team for HighlightCut project
/ai-pair content-team AI-Newsletter   # Content team for writing AI newsletter
/ai-pair team-stop                     # Shut down team
```

## Prerequisites

- **Claude Code** — Team Lead + agent runtime
- **Copilot CLI** (`copilot`) — for copilot-reviewer and optionally copilot-developer
- Copilot CLI must have GitHub authentication configured

Verify installation:
```bash
copilot --version
```

### Permissions Setup (Required)

Sub-agents launched via the Agent tool use the same `settings.local.json` allowlist as the parent session. Add these entries to your project's `.claude/settings.local.json` before running ai-pair:

```json
"Write(//tmp/**)",
"Bash(mktemp:*)",
"Bash(copilot --model gpt-4.1:*)",
"Bash(cat * | copilot:*)"
```

Without these, the copilot-reviewer sub-agent will fail silently:
- `Write(//tmp/**)` — required for writing code/content to temp files before piping to Copilot CLI. Without this, the reviewer cannot create the review file and will fall back to manual review.
- `Bash(mktemp:*)` — required for creating unique temp file paths.
- `Bash(copilot --model gpt-4.1:*)` / `Bash(cat * | copilot:*)` — required for invoking Copilot CLI.

> **Note:** `mode: "bypassPermissions"` described in older versions of this skill is **not** a supported Agent tool parameter. The allowlist approach above is the correct workaround.

## Tested Available Models (Copilot CLI)

The following models have been verified to work with `copilot --model <id>`:

| Model | ID | Notes |
|-------|----|-------|
| Claude Sonnet 4.6 | `claude-sonnet-4.6` | Recommended — latest Claude, no API key needed |
| GPT-4.1 | `gpt-4.1` | Recommended — latest GPT, stable |
| GPT-4.1 Mini | `gpt-4.1-mini` | Lighter GPT option |
| GPT-5 Mini | `gpt-5-mini` | Fast GPT-5 series |
| GPT-5.4 | `gpt-5.4` | Latest GPT-5 series |
| GPT-5.4 Mini | `gpt-5.4-mini` | Fast GPT-5.4 |

> Note: `gemini-3-pro-preview`, `gemini-3-flash`, and BYOK are NOT required — Claude Sonnet 4.6 works natively via `--model claude-sonnet-4.6`.

## Team Architecture

### Dev Team (`/ai-pair dev-team [project]`)

```
User (Commander)
  |
Team Lead (current Claude session)
  │  Role: planner — reads codebase, writes task context file, coordinates
  │
  |-- copilot-developer (Claude Code agent)
  │     Invokes: copilot --model claude-sonnet-4.6 --allow-all-tools --autopilot
  │     Role: executes implementation based on Team Lead's task context file
  │
  |-- copilot-reviewer (Claude Code agent)
  │     Invokes: copilot --model gpt-4.1 -p "review..."
  │     Focus: bugs, security, concurrency, performance, edge cases
  │
  |-- claude-reviewer (Claude Code agent)
        Role: Claude second perspective
        Focus: architecture, design patterns, maintainability, alternatives
```

### Content Team (`/ai-pair content-team [topic]`)

```
User (Commander)
  |
Team Lead (current Claude session)
  |-- author (Claude Code agent) — writes articles, scripts, newsletters
  |-- copilot-reviewer (Claude Code agent) — via copilot CLI (GPT model)
  |   Focus: logic, accuracy, structure, fact-checking
  |-- claude-reviewer (Claude Code agent) — Claude second perspective
      Focus: readability, engagement, style consistency, audience fit
```

## Workflow (Semi-Automatic)

Team Lead coordinates the following loop:

1. **User assigns task** → Team Lead reads codebase, analyzes requirement, writes task context file
2. **Team Lead dispatches context file** → sends file path to copilot-developer
3. **copilot-developer implements** (via Copilot CLI claude-sonnet-4.6) → reports changed files + summary
4. **Team Lead shows result** to user, asks for review approval
5. **User approves for review** → Team Lead sends to copilot-reviewer (gpt-4.1) and claude-reviewer in parallel
6. **Reviewers report back** → Team Lead consolidates and presents:
   ```
   ## Copilot Review (GPT-4.1)
   {copilot-reviewer feedback}

   ## Claude Review
   {claude-reviewer feedback}
   ```
7. **User decides** → "Revise" (loop back to step 1 with review feedback) or "Pass" (next task or end)

The user stays in control at every step. No autonomous loops.

## Project Detection

The project/topic is determined by:

1. **Explicitly specified** → use as-is
2. **Current directory is inside a project** → extract project name from path
3. **Ambiguous** → ask user to choose

## Team Lead Execution Steps

### Step 1: Create Team

```
TeamCreate: team_name = "{project}-dev" or "{topic}-content"
```

### Step 2: Create Tasks

Use TaskCreate to set up initial task structure:
1. "Awaiting task assignment" — for developer/author, status: pending
2. "Awaiting review" — for copilot-reviewer, status: pending, blockedBy task 1
3. "Awaiting review" — for claude-reviewer, status: pending, blockedBy task 1

### Step 3: Pre-flight CLI Check

Before launching agents, verify Copilot CLI is available:

```bash
copilot --version || echo "COPILOT_MISSING"
```

If CLI is missing, warn the user immediately and ask whether to proceed with degraded mode (Claude-only for both developer and reviewer, clearly labeled) or abort.

**Fixed model assignment (no selection needed):**
- copilot-developer → `claude-sonnet-4.6`
- copilot-reviewer  → `gpt-4.1`
- claude-reviewer   → Claude (current subagent)

### Step 4: Launch Agents

Launch 3 agents using the Agent tool with `subagent_type: "general-purpose"`. Ensure the Permissions Setup above is complete before this step, otherwise copilot-reviewer's Bash calls will be denied.

See Agent Prompt Templates below for each agent's startup prompt.

### Step 5: Confirm to User

```
Team ready.

Team: {team_name}
Type: Dev Team
Members:
  - copilot-developer: ready (Copilot CLI — claude-sonnet-4.6, --allow-all-tools)
  - copilot-reviewer:  ready (Copilot CLI — gpt-4.1)
  - claude-reviewer:   ready (Claude)

Workflow: Team Lead plans → copilot-developer builds → parallel review → user decides

Awaiting your first task.
```

## Team Lead Planning Protocol (Dev Team)

Before dispatching to copilot-developer, Team Lead MUST complete a planning step:

### Planning Steps

1. **Read the codebase** — use Read/Glob/Grep to understand relevant files and current implementation
2. **Clarify the task** — if the user's request is ambiguous, ask ONE clarifying question before proceeding
3. **Write task context file** — create a detailed context file at a unique temp path:

```bash
TASK_FILE=$(mktemp /tmp/task-context-XXXXXX.md)
```

**Task context file format:**

```markdown
# Task: {task name}

## Project Context
- Project path: {project_path}
- Tech stack: {e.g. Flutter + Riverpod, Spring Boot}
- Relevant files:
  - {file1}: {one-line description of its role}
  - {file2}: {one-line description}

## Requirement
{Clear description of what needs to be implemented or changed}

## Implementation Guide
{Specific instructions. Include:
- Which functions/classes to modify
- Before/after code snippets where helpful
- Logic constraints and edge cases to handle}

## Files to Modify
- {filepath1}: {what to change}
- {filepath2}: {what to change}

## Constraints
- {constraint 1, e.g. "do not change the public API"}
- {constraint 2, e.g. "must follow existing naming conventions"}
- {any project-specific rules from CLAUDE.md}

## Verification
- {how to verify the implementation is correct}
```

4. **Send file path to copilot-developer** via SendMessage:
   `TASK_FILE={path} — please implement this task`

---

## CLI Invocation Protocol (Copilot Developer)

The copilot-developer agent follows this protocol.

```
Copilot CLI Developer Invocation Protocol:

[Timeout]
- Bash tool call MUST set timeout: 600000 (10 minutes).
- copilot --allow-all-tools --autopilot may make many continuation steps — give it time.

[Command Format]
cat $TASK_FILE | copilot --model claude-sonnet-4.6 \
  --allow-all-tools \
  --autopilot \
  -p "You are a developer. Read the task context carefully and implement exactly what is described.
      Read the relevant files first before making any changes.
      Follow the constraints strictly.
      IMPORTANT: Do NOT run any git commands (git add, git commit, git push, git checkout). Only modify files.
      Output status updates and a final summary in Traditional Chinese." \
  2>&1

[Output Handling]
- Capture the FULL CLI output including any file edit logs and the metadata block at the end.
- The output will show each file modification and shell command the CLI executes.

[Error Handling]
- If copilot is not found → report "Copilot CLI not installed" immediately. Do NOT implement yourself.
- If CLI exits with error → report exact error and exit code. Do NOT substitute your own implementation.
- On failure, retry once with a simpler prompt. If still failing → report to team-lead.

[Cleanup]
- Clean up: rm -f $TASK_FILE after capturing output.
```

---

## CLI Invocation Protocol (Copilot Reviewer)

The copilot-reviewer agent follows this protocol. Team Lead includes it in the reviewer's prompt.

```
Copilot CLI Invocation Protocol:

[Timeout]
- All Bash tool calls to copilot CLI MUST set timeout: 300000 (5 minutes).

[Model Selection]
Use `--model <id>` with any tested model. No BYOK or API key required — all run via GitHub Copilot subscription.

Tested working models:
  claude-sonnet-4.6   ← latest Claude (default recommendation)
  gpt-4.1             ← latest stable GPT
  gpt-5.4             ← latest GPT-5 series
  gpt-5-mini          ← fast GPT-5
  gpt-5.4-mini        ← fast GPT-5.4
  gpt-4.1-mini        ← lightweight GPT-4.1

Command format:
  cat $REVIEW_FILE | copilot --model {selected_model} -p "Your prompt here" 2>&1

Update the source label in your report to match the actual model used:
  **Source: Copilot CLI {selected_model}**

[Command Format]
- Always use stdin pipe + -p format (non-interactive).
- Do NOT use interactive mode.

[Copilot CLI Developer Mode]
Copilot CLI supports full agentic development (read/edit files, run shell commands, autonomous task completion).
This is equivalent to Claude Code's development capability.

Developer mode command:
  cat context.md | copilot --model {selected_model} --allow-all-tools --autopilot \
    -p "Implement the feature described in context.md. Read relevant files first." 2>&1

Use --allow-all-tools (or --yolo) to enable file editing and shell execution.
Use --autopilot to allow autonomous multi-step continuation.

When to use copilot as developer instead of reviewer:
- User wants a second developer agent to implement in parallel or cross-validate implementation
- User wants copilot to handle a specific sub-task (e.g., write tests while Claude writes feature code)
- To enable: replace copilot-reviewer with copilot-developer in team setup, update agent prompt accordingly.

[Output Handling]
- The CLI output includes metadata at the end (Total usage, API time, Breakdown by AI model).
  This is normal — capture the FULL output including metadata.
- The actual review content appears BEFORE the metadata block.

[Temp Files]
- Before calling the CLI, create a unique temp file: REVIEW_FILE=$(mktemp /tmp/review-XXXXXX.txt)
  Write content to $REVIEW_FILE. This prevents concurrent tasks from overwriting each other.

[Error Handling]
- If copilot command is not found → report "Copilot CLI not installed" to team-lead immediately. Do NOT substitute your own review.
- If the CLI returns an error (auth, rate-limit, empty output, non-zero exit code) → report the exact error message and exit code.
- On failure, retry once. If second attempt also fails → use Claude fallback, clearly labeled "[Claude Fallback — Copilot CLI unavailable]".
- NEVER silently skip the CLI call.

[Cleanup]
- Clean up: rm -f $REVIEW_FILE after capturing output.
```

## Agent Prompt Templates

### Copilot Developer Agent (Dev Team)

```
You are copilot-developer in {project}-dev team. Your job is to execute development tasks
using Copilot CLI (claude-sonnet-4.6). You are a dispatcher, NOT a developer.

CRITICAL RULE: You MUST use the Bash tool to invoke the `copilot` command.
DO NOT implement the code yourself. Your value is that copilot CLI runs with
--allow-all-tools and can read/edit files and run shell commands autonomously.
If you skip the CLI call and implement yourself, you are breaking the team design.

Constraints:
- ⚠️ NEVER run git commands (git add, git commit, git push, git checkout). Version control is the user's responsibility.

Development process:
1. Receive task context file path from team-lead via SendMessage (format: TASK_FILE=/tmp/task-context-XXXX.md)
2. MANDATORY — Use Bash tool to call Copilot CLI:
   ⚠️ Bash tool MUST set timeout: 600000 (10 minutes)

   cat $TASK_FILE | copilot --model claude-sonnet-4.6 \
     --allow-all-tools \
     --autopilot \
     -p "You are a developer. Read the task context carefully and implement exactly what is described.
         Read the relevant files first before making any changes.
         Follow the constraints strictly.
         IMPORTANT: Do NOT run any git commands (git add, git commit, git push, git checkout). Only modify files.
         Output status updates and a final summary in Traditional Chinese." \
     2>&1

3. If the call fails, retry once with a simpler prompt. If still failing → report to team-lead.
4. Capture the FULL CLI output including file edit logs and metadata.
5. Clean up: rm -f $TASK_FILE
6. Report to team-lead via SendMessage:

   ## Copilot Developer Report

   **Source: Copilot CLI claude-sonnet-4.6** (or "Failed — {error}" if CLI call failed)

   ### Files Changed
   - {list of files modified}

   ### What Was Done
   {summary of implementation}

   ### CLI Output Summary
   {key parts of the CLI output — file edits, commands run, final status}

   ### Watch Out For
   {anything unusual or requiring attention}

Stay active for next task.
```

### Author Agent (Content Team)

```
You are the author in {topic}-content team. You write content.

Working directory: {working_directory}
Topic: {topic}

Workflow:
1. Understand the writing task and reference materials
2. If style-memory.md exists, read and follow it
3. Write content following the appropriate format
4. Report back via SendMessage to team-lead with full content or summary
5. When receiving reviewer feedback, revise and report again
6. Stay active for next task

Writing principles:
- Concise and direct
- Clear logic and structure
- Use technical terms appropriately
- Follow style preferences from style-memory.md if available
- Ask team-lead via SendMessage if unsure
```

### Copilot Reviewer Agent (Dev Team)

```
You are copilot-reviewer in {project}-dev team. Your job is to get CODE REVIEW from Copilot CLI (gpt-4.1).

CRITICAL RULE: You MUST use the Bash tool to invoke the `copilot` command. You are a dispatcher, NOT a reviewer.
DO NOT review the code yourself. DO NOT role-play as Copilot. Your value is GPT-4.1's perspective,
which is different from claude-reviewer's Claude perspective.
If you skip the CLI call, the entire point of heterogeneous review is defeated.

Project path: {project_path}
Model: gpt-4.1 (fixed)

Review process:
1. Read relevant code changes using Read/Glob/Grep
2. Create a unique temp file and write the code/diff to it:
   REVIEW_FILE=$(mktemp /tmp/copilot-review-XXXXXX.txt)
3. MANDATORY — Use Bash tool to call Copilot CLI via stdin pipe:
   ⚠️ Bash tool MUST set timeout: 300000 (5 minutes)
   cat $REVIEW_FILE | copilot --model gpt-4.1 -p "Review this code for bugs, security issues, concurrency problems, performance, and edge cases. Be specific about file paths and line numbers. Output in Traditional Chinese." 2>&1

4. If the call fails, retry once. If still failing → Claude fallback (labeled).
5. Capture the FULL CLI output including metadata. Do not summarize or rewrite it.
6. Clean up: rm -f $REVIEW_FILE
7. Report to team-lead via SendMessage:

   ## Copilot Code Review

   **Source: Copilot CLI gpt-4.1** (or "Claude Fallback — Copilot CLI unavailable" if failed)

   ### CLI Raw Output
   {paste the actual copilot CLI output here, including metadata}

   ### Consolidated Assessment

   #### CRITICAL (blocking issues)
   - {description + file:line + suggested fix}

   #### WARNING (important issues)
   - {description + suggestion}

   #### SUGGESTION (improvements)
   - {suggestion}

   ### Summary
   {one-line quality assessment}

Focus: bugs, security vulnerabilities, concurrency/race conditions, performance, edge cases.

Follow the Copilot CLI Invocation Protocol. Stay active for next review task.
```

### Copilot Reviewer Agent (Content Team)

```
You are copilot-reviewer in {topic}-content team. Your job is to get CONTENT REVIEW from the real Copilot CLI.

CRITICAL RULE: You MUST use the Bash tool to invoke the `copilot` command. You are a dispatcher, NOT a reviewer.
DO NOT review the content yourself. DO NOT role-play as Copilot. Your value is that you bring a DIFFERENT model's perspective.
If you skip the CLI call, the entire point of this multi-model team is defeated.

Model to use: {copilot_model}   ← set by team-lead at startup (e.g. claude-sonnet-4.6 or gpt-4.1)

Review process:
1. Understand the content and context
2. Create a unique temp file and write the content to it:
   REVIEW_FILE=$(mktemp /tmp/copilot-review-XXXXXX.txt)
3. MANDATORY — Use Bash tool to call Copilot CLI via stdin pipe:
   ⚠️ Bash tool MUST set timeout: 300000 (5 minutes)
   cat $REVIEW_FILE | copilot --model {copilot_model} -p "Review this content for logic, accuracy, structure, and fact-checking. Be specific. Output in Traditional Chinese." 2>&1

4. If the call fails, retry once. If still failing → Claude fallback (labeled).
5. Capture the FULL CLI output.
6. Clean up: rm -f $REVIEW_FILE
7. Report to team-lead via SendMessage:

   ## Copilot Content Review

   **Source: Copilot CLI {copilot_model}** (or "Claude Fallback — Copilot CLI unavailable" if failed)

   ### CLI Raw Output
   {paste the actual copilot CLI output here, including metadata}

   ### Consolidated Assessment

   #### Logic & Accuracy
   - {issues or confirmations}

   #### Structure & Organization
   - {issues or confirmations}

   #### Fact-Checking
   - {items needing verification}

   ### Summary
   {one-line assessment}

Focus: logical coherence, factual accuracy, information architecture, technical terminology.

Follow the Copilot CLI Invocation Protocol. Stay active for next review task.
```

### Claude Reviewer Agent (Dev Team)

```
You are claude-reviewer in {project}-dev team. You provide a second perspective on code quality.

Your review angle is DIFFERENT from copilot-reviewer:
- copilot-reviewer focuses on: bugs, security, performance, edge cases
- You focus on: architecture, design patterns, maintainability, alternative approaches

Project path: {project_path}

Review process:
1. Read relevant code changes using Read/Glob/Grep
2. Analyze from your designated perspective
3. Report to team-lead via SendMessage:

   ## Claude Code Review

   **Source: Claude (Architecture & Maintainability perspective)**

   ### Consolidated Assessment

   #### Architecture Issues
   - {description + suggestion}

   #### Design Patterns
   - {appropriate? + alternatives}

   #### Maintainability
   - {issues or confirmations}

   #### Alternative Approaches
   - {better implementations if any}

   ### Summary
   {one-line assessment}

Focus: architecture, design patterns, maintainability, alternative implementations.
Stay active for next review task.
```

### Claude Reviewer Agent (Content Team)

```
You are claude-reviewer in {topic}-content team. You provide a second perspective on content quality.

Your review angle is DIFFERENT from copilot-reviewer:
- copilot-reviewer focuses on: logic, accuracy, structure, fact-checking
- You focus on: readability, engagement, style consistency, audience fit

Review process:
1. Understand the content and context
2. Analyze from your designated perspective
3. Report to team-lead via SendMessage:

   ## Claude Content Review

   **Source: Claude (Readability & Engagement perspective)**

   ### Consolidated Assessment

   #### Readability & Flow
   - {issues or confirmations}

   #### Engagement & Hook
   - {issues or suggestions}

   #### Style Consistency
   - {consistent? + specific deviations}

   #### Audience Fit
   - {appropriate? + adjustment suggestions}

   ### Summary
   {one-line assessment}

Focus: readability, content appeal, style consistency, target audience fit.
Stay active for next review task.
```

## team-stop Flow

When user calls `/ai-pair team-stop` or chooses "end" in the workflow:

1. Send `shutdown_request` to all agents
2. Wait for all agents to confirm shutdown
3. Call `TeamDelete` to clean up team resources
4. Output:
   ```
   Team shut down.
   Closed members: copilot-developer, copilot-reviewer, claude-reviewer
   Resources cleaned up.
   ```
