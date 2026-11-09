# AI 工具協作規劃文件

本目錄記錄跨 AI 工具（Claude Code、Antigravity `agy`、Codex、GitHub Copilot 等）的協作方案與設定規劃。

## 文件索引

| 文件 | 說明 |
|------|------|
| [**cross-tool-ai-setup.md**](./cross-tool-ai-setup.md) | **跨工具 AI 協作設定指南（通用版，供其他專案整合使用）：AGENTS.md 單一來源 + CLAUDE.md import 兩層架構、各工具讀取行為、驗收自我測試** |
| [**backend-doc-sync-hook.md**](./backend-doc-sync-hook.md) | **跨 repo 文件同步（b2b-backend ↔ b2b-manager）：兩個 `SessionStart` hook、為什麼「產出文件」不自動化、設計沿革（上游推送已退役）、換機器重建清單** |
| [**claude-subagent-delegation-generic.md**](./claude-subagent-delegation-generic.md) | **Claude Code 分工設定指南（通用版，供其他專案整合使用）：該不該分工的決策框架、三種設定層級、分工需要哪些文件、禁區清單建立方法、導入步驟** |
| [**claude-subagent-delegation.md**](./claude-subagent-delegation.md) | **本專案分工結論：派工判準、prompt 模板、跨 repo 循序變更（後端先行 → 契約落地 → 前端跟進）、為什麼 b2b-manager 預設不分工** |

## 快速導覽

```
通用設定指南     → cross-tool-ai-setup.md（其他專案首選參考）
跨 repo 文件同步 → backend-doc-sync-hook.md（hook 觸發方式 + 換機器重建）
Claude 分工      → claude-subagent-delegation-generic.md（通用框架，其他專案首選）
                   claude-subagent-delegation.md（本專案結論 + 派工模板）
```

> ⚠️ **`backend-doc-sync-hook.md` 兼任重建指引**：它描述的機制（`.claude/scripts/` 腳本
> 與 hook config）**不進 git**，換機器就沒了。該文件末尾的「🔧 重建清單」是唯一的復原依據。

---

> 📁 本份為 `~/GitLab/b2b-manager/docs/ai-collaboration/` 的精簡複本（2026-10-19）：已移除封存歷程（`_archive/`）與暫緩中的 `mcp-setup.md`，以專案內版本為準。

最後更新：2026-10-19
