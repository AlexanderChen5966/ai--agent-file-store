# AI-Pair: Heterogeneous AI Team Collaboration

# AI-Pair：異構 AI 團隊協作

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)](#status)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills)

Coordinate multiple AI models to work together as a team. One creates, three review — not for redundancy, but because different models naturally focus on different dimensions.

讓不同 AI 模型組成團隊協作。一個創作，三個審查 — 不是為了冗餘，而是因為不同模型天然關注不同維度。

> **v4.1.0：** Phase 1 模型驗證完成 ✅  
> - 驗證 11 個模型（7 Copilot + 4 Gemini）全部可用
> - 新增 Tier 系統（FREE / LOW / STANDARD / COMPLEX）
> - 統一 FREE 層級 Fallback：移除 Haiku 4.5，改用 gpt-5-mini → gpt-4.1
> - 動態模型選擇：Team Lead 可透過 `--model` 參數覆寫固定分配
> - 拆分文檔：SKILL.md (603 行) + agents-prompts.md + cli-invocation-ref.md
> - 補充已知限制、偏誤防護、兼容性驗證

> **v3.0.0：** 開發與內容流程統一升級為 **Copilot CLI（GPT）+ Claude + Gemini** 三審查架構，加入分層 review、壓縮協議、diff-only review 與降級機制。

> **Next Step:** Want to turn Skills from demo to asset? Check out [Agent Skills Resource Library](https://www.axtonliu.ai/agent-skills) (includes slides, PDF, diagnostics)

## Status

> **Status: Experimental | 狀態：實驗性**
>
> - This is a public prototype that works for real workflows, but does not yet cover all edge cases. | 公開原型，可用於實際工作流程，但尚未涵蓋所有邊界情況。
> - Requires Claude Code + Copilot CLI + Gemini CLI
> - My primary focus is demonstrating how tools and systems work together, not maintaining this codebase. | 重點是展示工具和系統如何協作，而非維護這個程式庫。
> - If you encounter issues, please submit a reproducible case (input + output + steps to reproduce). | 如遇問題，請提交可重現的案例。

## Why This Exists | 為什麼做這個

Most people use multiple AI subscriptions by asking the same question to each and comparing answers. That's useful sometimes, but it only uses one dimension of what different models can do — you get multiple answers to the same question, instead of multiple perspectives on the same work.

大部分人使用多個 AI 的方式是：同一個問題分別問一遍，然後對比答案。這有時候有用，但只用到了不同模型能力的一個維度 — 你得到的是同一個問題的多個回答，而不是同一份工作的多個視角。

AI-Pair turns model differences into a structured workflow: assign each model a role that matches its strength, and let them review the same work from different angles. It's a [Claude Code Skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) — a reusable instruction set that extends Claude Code's capabilities.

AI-Pair 把模型差異變成結構化的工作流程：給每個模型分配匹配其特長的角色，讓它們從不同角度審查同一份工作。它是一個 [Claude Code Skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) — 一組可複用的指令，擴展 Claude Code 的能力。

## How It Works | 工作原理

```
User (you) | 使用者（你）
  |
Team Lead (Claude Code session) | 團隊領導（Claude Code 工作階段）
  |-- creator (Claude Code agent) — writes code or content | 創作者 — 寫程式碼或內容
  |-- copilot-reviewer (agent → Copilot CLI) — GPT analytical review | GPT 分析型審查
  |-- claude-reviewer (Claude Code agent) — Claude editorial review | Claude 編輯型審查
  |-- gemini-reviewer (agent → Gemini CLI) — requirements and coverage review | Gemini 需求對齊與覆蓋率審查
```

The workflow is semi-automatic — you stay in control at every step:

工作流程是半自動的 — 每一步你都保持控制權：

1. You assign a task → creator executes | 你下達任務 → 創作者執行
2. Creator reports back → you decide whether to send for review | 創作者回報 → 你決定是否送審
3. Team Lead prepares one shared diff/review file | Team Lead 準備一份共享 diff/review 檔
4. Reviewers analyze in parallel based on review level | 依 review level 並行審查
5. You decide: revise or pass → loop or next task | 你決定：修改還是通過 → 循環或下一個任務

## Prerequisites | 前置條件

These are **command-line tools** that run in your terminal (Terminal, iTerm2, etc.), not desktop apps.

這些都是**命令列工具**，在終端機中執行（Terminal、iTerm2 等），不是桌面應用程式。

| Tool | Purpose | Install |
|------|---------|---------|
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) | Team Lead + agent runtime | `npm install -g @anthropic-ai/claude-code` |
| [Copilot CLI](https://github.com/github/copilot-cli) | GPT-powered developer/reviewer | `npm install -g @github/copilot-cli` |
| Gemini CLI | Requirement-alignment reviewer | Follow Gemini CLI official install instructions |

Copilot CLI and Gemini CLI must have authentication configured before use.

兩個 CLI 使用前都需要完成認證設定。

> **Quick check | 快速確認:** Run `claude --version`, `copilot --version`, and `gemini --version` to verify installation.

## Installation | 安裝

### Option A: Direct Install (Recommended) | 直接安裝（推薦）

```bash
# Clone to your global Claude Code skills directory
# 複製到 Claude Code 全域 skills 目錄
git clone https://github.com/axtonliu/ai-pair.git ~/.claude/skills/ai-pair
```

For project-level installation, clone into `.claude/skills/ai-pair` within your project directory instead.

如需專案層級安裝，請複製到專案目錄下的 `.claude/skills/ai-pair`。

### Option B: Manual | 手動安裝

1. Download `SKILL.md` from this repo | 下載本儲存庫的 `SKILL.md`
2. Place it in `~/.claude/skills/ai-pair/SKILL.md` | 放到 `~/.claude/skills/ai-pair/SKILL.md`
3. Restart Claude Code | 重新啟動 Claude Code

## Usage | 使用方式

### Dev Team — for code, bugs, refactoring | 開發團隊 — 寫程式碼、修 bug、重構

```bash
/ai-pair dev-team MyProject
/ai-pair dev-team MyProject --quick
/ai-pair dev-team MyProject --deep
```

Team Lead creates | 團隊領導建立:
- **developer** — writes code | 寫程式碼
- **copilot-reviewer** — GPT model, checks bugs, security, performance, edge cases | GPT 模型審查 bug、安全性、效能、邊界條件
- **claude-reviewer** — Claude second perspective, checks architecture, design patterns, maintainability | Claude 第二視角，審查架構、設計模式、可維護性
- **gemini-reviewer** — Gemini perspective, checks spec compliance, missing scenarios, requirement alignment | Gemini 視角，審查需求對齊、遺漏情境、覆蓋率

### Content Team — for articles, scripts, newsletters | 內容團隊 — 寫文章、腳本、Newsletter

```bash
/ai-pair content-team AI-Newsletter
```

Team Lead creates | 團隊領導建立:
- **author** — writes content | 寫內容
- **copilot-reviewer** — GPT model, checks logic, accuracy, structure, fact-checking | GPT 模型審查邏輯、準確性、結構、事實查核
- **claude-reviewer** — Claude second perspective, checks readability, engagement, style, audience fit | Claude 第二視角，審查可讀性、吸引力、風格、受眾適配
- **gemini-reviewer** — Gemini perspective, checks completeness, missing points, topic alignment | Gemini 視角，審查完整性、缺漏與主題對齊

### Stop Team | 關閉團隊

```bash
/ai-pair team-stop
```

## Real-World Example | 真實案例

We used `content-team` to review a newsletter article. The three AIs found completely different issues:

我們用 `content-team` 審查了一篇 Newsletter 文章。三個 AI 發現的問題完全不同：

- **Claude** (Team Lead): spotted an overreach in interpreting a cited source | 發現對引用來源的過度解讀
- **GPT** (Codex): dissected the argument chain and challenged a logical leap | 拆解論證鏈，質疑邏輯跳躍
- **Gemini**: suggested the opening was too academic for the target audience | 建議開頭對目標讀者來說太學術化

None of these overlapped. That's the point. See [`examples/`](examples/) for step-by-step walkthrough scenarios.

三者零重疊。這就是意義所在。查看 [`examples/`](examples/) 取得逐步演示情境。

## File Structure | 檔案結構

```
ai-pair/
├── SKILL.md                      # 核心 skill 定義（603 行）| Core skill definition
├── README.md                      # 本文件 | This file
├── 說明文件.md                   # 繁體中文說明 | Traditional Chinese guide
├── LICENSE                        # MIT
├── reference/                     # 技術參考文檔 | Technical reference
│   ├── agents-prompts.md         # 8 個 Agent 初始化提示 | Agent init prompts
│   └── cli-invocation-ref.md     # CLI 協議技術細節 | CLI protocol reference
└── examples/                      # 使用範例 | Usage examples
    ├── dev-team.md
    └── content-team.md
```

**v4.1 新增檔案結構：**
- `reference/` — 可獨立查閱的技術文檔資料夾
  - `agents-prompts.md` — 8 個 Agent 初始化提示（複製貼上即用）
  - `cli-invocation-ref.md` — Copilot / Gemini 協議詳細說明與錯誤處理

## Review Levels | 審查層級

- `--quick` — Gemini only，適合 typo、小 UI 調整、低風險微調
- default — Copilot reviewer + Claude reviewer，適合一般功能與 bug fix
- `--deep` — Copilot reviewer + Claude reviewer + Gemini reviewer，適合高風險模組與架構變更

## Troubleshooting | 常見問題

### Copilot reviewer not actually calling Copilot CLI | 審查者沒有真正呼叫 Copilot CLI

**Symptom:** Reviews complete but Copilot CLI usage stays flat. The sub-agent is role-playing as Copilot instead of actually invoking it.

**症狀：** 審查完成但 Copilot CLI 用量沒有任何變化。子代理人在角色扮演而非真正呼叫外部 CLI。

**How to verify | 如何驗證:** Check the review output for the `**Source: Copilot CLI gpt-4.1**` label and the `### CLI Raw Output` section. If these are missing, the CLI was not called.

**如何驗證：** 檢查審查輸出中是否有 `**Source: Copilot CLI gpt-4.1**` 標籤和 `### CLI Raw Output` 部分。如果缺失，表示 CLI 沒有被呼叫。

**Fix | 解決方式:** Ensure Copilot CLI and Gemini CLI are installed and authenticated (`copilot --version`, `gemini --version`). Update to v3.0.0 if on an older version.

**解決方式：** 確認 Copilot CLI 與 Gemini CLI 已安裝並完成認證（`copilot --version`、`gemini --version`）。如使用舊版請更新至 v3.0.0。

## What's Not Included | 未包含的功能

This open-source version includes the **Agent Teams mode** only. The full private version also has:

開源版僅包含 **Agent Teams 模式**。完整私有版還包括：

- **Manual mode** — two CLI instances communicating via shared file | 手動模式 — 兩個 CLI 透過共享檔案通訊
- **iTerm2 orchestration** — automated Author/Reviewer relay with file watchers | iTerm2 編排 — 自動化的創作/審查中繼

These require specific local setup and are maintained separately.

這些需要特定的本機設定，單獨維護。

## Evolution | 演變

AI-Pair evolved from [AI Roundtable](https://github.com/axtonliu/ai-roundtable), a Chrome extension that lets multiple AI web interfaces discuss and cross-review in the same panel. AI-Pair moves this concept to the command line with structured role assignments, making it more practical for daily workflows.

AI-Pair 從 [AI Roundtable](https://github.com/axtonliu/ai-roundtable) 演變而來。AI Roundtable 是一個 Chrome 擴充功能，讓多個 AI 的網頁版在同一個面板裡討論和互評。AI-Pair 把這個概念搬到了命令列，加入了結構化的角色分工，更適合日常工作流程。

## Contributing | 貢獻

Contributions welcome (low-maintenance project):

歡迎貢獻（低維護專案）：

- Reproducible bug reports (input + output + steps + environment) | 可重現的 bug 報告
- Documentation improvements | 文件改進
- Small PRs (fixes/docs) | 小型 PR（修復/文件）

> **Note:** Feature requests may not be acted on due to limited maintenance capacity. | 功能需求可能因維護資源有限而無法回應。

## License | 授權條款

[MIT](LICENSE) - Axton Liu

---

## Author | 作者

**Axton Liu** — AI Educator & Creator

- Website: [axtonliu.ai](https://www.axtonliu.ai)
- YouTube: [@AxtonLiu](https://youtube.com/@AxtonLiu)
- Twitter/X: [@axtonliu](https://x.com/axtonliu)

### Learn More

- [MAPS™ AI Agent Course](https://www.axtonliu.ai/aiagent) - Systematic AI agent skills training
- [Claude Skills: A Systematic Guide](https://www.axtonliu.ai/newsletters/ai-2/posts/claude-agent-skills-maps-framework) - Complete methodology
- [AI Elite Weekly Newsletter](https://www.axtonliu.ai/newsletters/ai-2) - Weekly AI insights
- [Free AI Course](https://www.axtonliu.ai/axton-free-course) - Get started with AI

---

© AXTONLIU™ & AI 精英學院™ 版權所有
