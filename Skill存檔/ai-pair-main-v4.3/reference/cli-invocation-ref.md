---
title: CLI Invocation Protocols Reference
description: Detailed CLI command specifications for Copilot and Antigravity (agy) invocations
version: 4.3.0
last_updated: 2026-06-22
---

# CLI Invocation Protocols (v4.3)

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

## CLI Invocation Protocol (Gemini Reviewer → Antigravity CLI `agy`)

**Used by:** gemini-reviewer agent dispatching spec reviews to Antigravity CLI (`agy`)

> **遷移備註（v4.3）：** Gemini CLI（`gemini`）自 2026-06-18 起停止為 Google One / 免費帳號提供服務，已遷移至 Antigravity CLI（`agy`）。**角色名稱 `gemini-reviewer` 保留不變**（避免 `reviewer_set` 快取鍵失效），只有底層 CLI 由 `gemini` 換成 `agy`。

```
[Timeout] Bash timeout: 300000 (5 min)
[Model] "Gemini 3.1 Pro (High)" (Level 3 primary) / "Gemini 3.5 Flash (Low)" (Level 1)

[Command] stdin pipe + --model confirmed working (tested agy v1.0.10, 2026-06-22)
cat $REVIEW_FILE | agy --model "Gemini 3.1 Pro (High)" \
  -p "Review this code for spec compliance, missing scenarios, requirement gaps, edge cases.
      Output ONLY in this exact format, each item on its own newline, no extra text:
      SRC:agy/gemini-3.1-pro-high
      C|{file:line_or_NA}|{issue}|{fix}
      W|{file:line_or_NA}|{issue}|{fix}
      S|{file:line_or_NA}|{suggestion}|{fix}
      VERDICT:PASS or VERDICT:WARN or VERDICT:BLOCK" 2>&1

[Note — Compression format ✅ Verified Phase 1 (2026-06-22)]
  agy 各模型均使用 `|` 分隔符，符合 Inter-Agent Protocol v1。
  Example: `C|file.dart:142|issue|fix` (NOT forward slash)
  Team Lead should accept both newline and single-line "|" separated formats when parsing.
  SRC 欄位格式改為 `SRC:agy/{model-slug}`，方便識別實際使用模型。

[Model-level fallback chain]
  agy L3: "Gemini 3.1 Pro (High)" → "Gemini 3.5 Flash (Medium)" → "Gemini 3.5 Flash (Low)" → SKIP
  agy L1: "Gemini 3.5 Flash (Low)" → "Gemini 3.5 Flash (Medium)" → SKIP

[Error handling]
  - Exit code 1 + "model not found" / "unknown model" in stderr → ERR:MODEL, try next tier
  - Exit code 1 + "quota" / "429" in stderr → ERR:QUOTA
  - Exit code 1 + "401" / "Unauthorized" in stderr → ERR:AUTH
  - Timeout (no output) → ERR:TIMEOUT, retry once
  - "command not found: agy" → ERR:CLI_MISSING
  Do NOT substitute own review.

[⚠️ 已知行為 — 無效模型名稱不報錯（agy v1.0.10 實測 2026-06-22）]
  傳入不存在的模型名稱時，agy 不會回傳 exit 1，而是**靜默改用預設模型**回應。
  因此 ERR:MODEL 較難由 stderr 偵測；fallback chain 主要在 QUOTA/AUTH/TIMEOUT 時觸發。
  影響：使用未驗證的模型名稱可能拿到非預期模型的審查結果，請確認 --model 字串完全符合「agy 可用模型清單」。

[Known Limitation — Chinese filenames in paths]
  agy 中文路徑行為尚未完整驗證；沿用既有防護：
  Workaround: Keep REVIEW_FILE and TASK_FILE paths ASCII-only (use /tmp/review-XXXXXX, /tmp/task-XXXXXX)
  Already satisfied: Review files are generated in /tmp and stdin piped directly.

[Cleanup] Team-lead cleans REVIEW_FILE after all reviewers finish
```

### Details

- **Primary model:** `"Gemini 3.1 Pro (High)"` (PREVIEW tier，Level 3 主力)
- **Additional models:** `"Gemini 3.5 Flash (Medium)"`（STANDARD fallback）、`"Gemini 3.5 Flash (Low)"`（LITE，Level 1 快速掃描）— Phase 1 已驗證
- **`--model` 語法：** 帶引號的完整名稱（含括號），如 `agy --model "Gemini 3.1 Pro (High)"`
- **Output format:** Pipe-separated (`|`), not forward-slash (`/`)；SRC 為 `SRC:agy/{model-slug}`
- **stdin:** Review file piped via `cat $REVIEW_FILE |`
- **Error handling:**
  - `QUOTA` → 依 fallback chain 降級或 SKIP
  - `AUTH` → ask user to re-login
  - `TIMEOUT` → retry once
  - `MODEL` → 換下一層 tier（注意：agy 對無效模型多半靜默改用預設，不一定觸發）
  - `CLI_MISSING` → show install command

### agy 可用模型清單（實測確認）

| 模型名稱 | tier 對應 | 備註 |
|---|---|---|
| `Gemini 3.5 Flash (Low)` | LITE | 速度最快，Level 1 |
| `Gemini 3.5 Flash (Medium)` | STANDARD | 預設模型，fallback 層 |
| `Gemini 3.5 Flash (High)` | — | 高算力 Flash |
| `Gemini 3.1 Pro (Low)` | — | Pro 低算力 |
| `Gemini 3.1 Pro (High)` | PREVIEW | 最強，Level 3 主力 |
| `Claude Sonnet 4.6 (Thinking)` | — | Anthropic |
| `Claude Opus 4.6 (Thinking)` | — | Anthropic 最強 |
| `GPT-OSS 120B (Medium)` | — | OpenAI |

### Known Limitations

1. **無效模型靜默 fallback：** agy 傳入不存在模型名稱時不報錯，改用預設模型
   - **Mitigation:** 確認 `--model` 字串與上方清單完全一致
   - **Impact:** ERR:MODEL 偵測不可靠，fallback 主要靠 QUOTA/AUTH/TIMEOUT

2. **Chinese character paths:** agy 中文路徑行為待驗證
   - **Mitigation:** Keep `/tmp/review-*` paths ASCII-only (already implemented)
   - **Impact:** None for current workflow

3. **Quota exhaustion:** 額度耗盡時依 fallback chain 降級
   - **Mitigation:** model-level fallback（Pro High → Flash Medium → Flash Low → SKIP）
   - **Impact:** Transparent to user

---

## Reference

- See `../SKILL.md` → Team Lead Planning Protocol for task context file format
- See `agents-prompts.md` for agent initialization prompts
- See `../SKILL.md` → Inter-Agent Protocol v1 for compression format details
