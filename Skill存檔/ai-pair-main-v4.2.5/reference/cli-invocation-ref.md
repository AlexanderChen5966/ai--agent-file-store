---
title: CLI Invocation Protocols Reference
description: Detailed CLI command specifications for Copilot and Gemini invocations
version: 4.1.0
last_updated: 2026-05-15
---

# CLI Invocation Protocols (v4.1)

Technical reference for Team Lead and agent developers. These are **not** copy-paste prompts — they define the exact CLI command structure and error handling logic.

---

## CLI Invocation Protocol (Copilot Developer)

**Used by:** copilot-developer agent dispatching implementations to Copilot CLI

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

[Compatibility ✅ Phase 1 Verified]
  --allow-all-tools flag: Works with all Copilot models (GPT-5.x, GPT-4.1, Claude Sonnet)
  --autopilot flag: Confirmed compatible with claude-sonnet-4.6 in Phase 1 testing
  Tested command chain: cat $TASK_FILE | copilot --model MODEL --allow-all-tools --autopilot -p "..."
  Result: All tested models execute autonomously without interactive prompts
```

### Details

- **Model:** `claude-sonnet-4.6` (STANDARD tier, fixed)
- **Flags:**
  - `--allow-all-tools` — Enable all tools in the agent (Read, Write, Edit, Bash, etc.)
  - `--autopilot` — Run without waiting for user confirmation between steps
- **stdin:** Task context file piped via `cat $TASK_FILE |`
- **Output:** Must include DONE message with changed file list
- **Retry logic:** One retry with simplified prompt; no endless loops

---

## CLI Invocation Protocol (Copilot Reviewer)

**Used by:** copilot-reviewer agent dispatching code reviews to Copilot CLI

```
[Timeout] Bash timeout: 300000 (5 min)
[Model] gpt-5.4-mini (or gpt-5-mini fallback)

[Command]
cat $REVIEW_FILE | copilot --model gpt-5.4-mini \
  -p "Review for bugs, security, concurrency, performance, edge cases.
      Output ONLY in this compressed format (no markdown prose):
      SRC:gpt-5.4-mini
      {C|W|S}|{file:line_or_NA}|{issue}|{fix}
      VERDICT:{PASS|WARN|BLOCK}" 2>&1

[On failure]
  - Parse stderr for error type → report ERR:{code}|{message} to team-lead
  - Retry once on TIMEOUT. Do NOT substitute own review if CLI fails.
[Cleanup] Team-lead cleans REVIEW_FILE after all reviewers finish
```

### Details

- **Primary model:** `gpt-5.4-mini` (LOW tier)
- **Fallback model:** `gpt-5-mini` (FREE tier) if quota exhausted
- **Output format:** Compressed, no prose (see Inter-Agent Protocol v1)
- **stdin:** Review file (diff + optional cached findings) piped via `cat $REVIEW_FILE |`
- **Error handling:**
  - `QUOTA` → try fallback
  - `AUTH` → ask user to re-login
  - `TIMEOUT` → retry once, then SKIP
  - `MODEL` → try fallback

---

## CLI Invocation Protocol (Gemini Reviewer)

**Used by:** gemini-reviewer agent dispatching spec reviews to Gemini CLI

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

[Note — Compression format ✅ Verified Phase 1]
  All Gemini models (2.5-flash, 3-flash-preview, 3.1-flash-lite-preview) use `|` separator in Inter-Agent Protocol.
  Example: `C|file.dart:142|issue|fix` (NOT forward slash)
  gemini-2.5-flash-lite may output findings on one line with "|" separators.
  Team Lead should accept both newline and single-line "|" separated formats when parsing.

[Error handling]
  - Exit code 1 + "ModelNotFoundError" in stderr → ERR:MODEL, try gemini-2.5-flash-lite
  - Exit code 1 + "quota" / "429" in stderr → ERR:QUOTA
  - Exit code 1 + "401" / "Unauthorized" in stderr → ERR:AUTH
  - Timeout (no output) → ERR:TIMEOUT, retry once
  - "command not found" → ERR:CLI_MISSING
  Do NOT substitute own review.

[Known Limitation — Chinese filenames in paths]
  Gemini CLI may fail to parse Chinese character paths in context supplementation.
  Workaround: Keep REVIEW_FILE and TASK_FILE paths ASCII-only (use /tmp/review-XXXXXX, /tmp/task-XXXXXX)
  Already satisfied: Review files are generated in /tmp and stdin piped directly.

[Cleanup] Team-lead cleans REVIEW_FILE after all reviewers finish
```

### Details

- **Primary model:** `gemini-2.5-flash` (STANDARD tier)
- **Fallback model:** `gemini-2.5-flash-lite` (LOW tier) for Level 1 quick scans
- **Additional models:** `gemini-3-flash-preview`, `gemini-3.1-flash-lite-preview` (Phase 1 verified alternatives)
- **Output format:** Pipe-separated (`|`), not forward-slash (`/`)
- **stdin:** Review file piped via `cat $REVIEW_FILE |`
- **Error handling:**
  - `QUOTA` → fallback or SKIP
  - `AUTH` → ask user to re-login
  - `TIMEOUT` → retry once
  - `MODEL` → try lite variant or SKIP
  - `CLI_MISSING` → show install command

### Known Limitations

1. **Chinese character paths:** Gemini CLI context supplementation fails with non-ASCII paths
   - **Mitigation:** Keep `/tmp/review-*` paths ASCII-only (already implemented)
   - **Impact:** None for current workflow

2. **Quota exhaustion:** Gemini models occasionally return "exhausted capacity"
   - **Mitigation:** Auto-retry with 1-7 second delay via fallback chain
   - **Impact:** Transparent to user

---

## Reference

- See `../SKILL.md` → Team Lead Planning Protocol for task context file format
- See `agents-prompts.md` for agent initialization prompts
- See `../SKILL.md` → Inter-Agent Protocol v1 for compression format details
