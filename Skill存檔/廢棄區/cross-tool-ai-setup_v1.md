# 跨工具 AI 協作設定指南

從本專案（B2B Manager）實戰經驗蒸餾，適用於其他專案整合多個 AI 工具時使用。

**適用工具：** Claude Code、Gemini CLI、OpenAI Codex CLI、VS Code Copilot、Cursor、Windsurf、Google Antigravity

---

## 一、設計原則

### 核心目標
- **單一維護點**：共用規則只寫一份，其他工具透過機制同步
- **最小化重複**：避免複製貼上造成長期失同步
- **工具原生支援**：盡量使用各工具原生讀取機制，不強迫統一

### 三個不要
1. **不要讓每份工具文件都自行維護完整規則** → 容易失同步
2. **不要把所有規則塞進同一個檔案** → 難以管理，各工具有 token 限制
3. **不要依賴工具記憶代替文件** → AI 記憶不可靠，規則應在檔案中

---

## 二、各工具讀取的 Context 檔案

| 工具 | 原生讀取檔案 | 支援 @import | 說明 |
|------|------------|------------|------|
| **Claude Code** | `CLAUDE.md`、`.claude/CLAUDE.md` | ✅ `@path/to/file` | + `.claude/rules/*.md` 自動載入 |
| **Gemini CLI** | `GEMINI.md` | ✅ `@path/to/file` | 支援 5 層遞迴 import |
| **OpenAI Codex CLI** | `AGENTS.md` | ❌ | Linux Foundation AAIF 標準 |
| **VS Code Copilot** | `.github/copilot-instructions.md`、`AGENTS.md` | ❌ | + `.github/instructions/*.instructions.md`（路徑專屬） |
| **Cursor** | `.cursorrules`、`.cursor/rules/*.mdc` | ❌ | 有 token 上限（~2000 tokens） |
| **Windsurf** | `.windsurfrules`、`AGENTS.md` | ❌ | 兩者都讀，優先 `.windsurfrules` |
| **Google Antigravity** | `.agent/rules/`、`~/.gemini/rules/` | ❌ | Rules/Workflows/Skills 三層架構 |

> **趨勢：** `AGENTS.md` 正成為跨工具事實標準，Windsurf、Codex、VS Code Copilot 均支援。

---

## 三、@import 機制詳解

### Claude Code / Gemini CLI 支援的 `@path` 語法

```markdown
# CLAUDE.md 範例
@AGENTS.md

## Claude Code 專屬補充
...
```

```markdown
# GEMINI.md 範例
@./AGENTS.md

<!-- 以下為 Gemini 專屬補充（選填） -->
```

### 重要特性

| 特性 | 說明 |
|------|------|
| **路徑基準** | 相對路徑相對於「包含 import 的檔案本身」，不是工作目錄 |
| **遞迴深度** | 最深 5 層（防止循環引用） |
| **Token 用量** | ❌ **不節省 token**：imported 檔案在啟動時展開進入 context |
| **用途** | 避免複製貼上 + 確保同步，不是 lazy load |
| **首次確認** | 首次遇到外部路徑 import 時，Claude Code 會顯示確認對話框 |
| **支援格式** | 僅 `.md` 檔案 |

### 官方建議（Anthropic 文件原文）

> *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them."*

---

## 四、建議架構

### 標準架構（推薦）

```
AGENTS.md               ← 單一維護點：完整共用規則
GEMINI.md               ← @./AGENTS.md（+ Gemini 專屬補充，選填）
CLAUDE.md               ← @AGENTS.md（+ Claude 專屬補充）
.claude/rules/          ← Claude Code 自動載入的分類規則
  ├── project-scope.md
  ├── change-policy.md
  └── ...（依需求增加）
.github/
  └── copilot-instructions.md  ← 精簡版，指向 AGENTS.md 為主
.cursorrules            ← 精簡版（有 token 限制）
```

### Context 流向圖

```
                    ┌─────────────┐
                    │  AGENTS.md  │ ← 單一維護點
                    │  （完整規則） │
                    └──────┬──────┘
                           │ @import
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    CLAUDE.md          GEMINI.md      （其他工具直接讀取）
    + 專屬補充          + 專屬補充      Codex、Copilot、Windsurf
          │
          ▼
    .claude/rules/
    （Claude Code 自動載入）
```

### Context 用量評估

| 層級 | 行數參考 | 說明 |
|------|---------|------|
| `AGENTS.md`（共用規則） | ~80–120 行 | 所有工具看到的核心規則 |
| 工具專屬補充 | ~20–50 行 | Claude 或 Gemini 各自的額外規則 |
| `.claude/rules/`（總計） | ~80–120 行 | 自動載入，與 AGENTS.md 輕度重疊可接受 |
| **Claude Code 總計** | **~200–280 行** | 建議控制在 300 行以內 |

> **官方建議**：每份 CLAUDE.md 控制在 200 行以內，超過會降低遵循率。

---

## 五、建立步驟（新專案）

### Step 1：撰寫 AGENTS.md（單一來源）

內容包含：

```markdown
# [專案名稱] — AI Agent 共用規則

## 專案定位
- 技術棧、平台、部署方式
- 不支援的平台或使用情境

## 嚴格禁止
- 不可觸碰的核心邏輯或架構
- 不可更動的第三方套件或設定

## 高風險變更（需使用者確認）
- 需要特別謹慎的操作列表

## 核心架構規則
- 具體的技術規則（命名、結構、呼叫方式）

## 驗證指令
- 修改後應執行的指令

## 輸出語言
- 指定回覆語言與術語規範
```

### Step 2：建立 GEMINI.md

```markdown
@./AGENTS.md

<!-- Gemini 專屬補充（選填）-->
```

### Step 3：建立 CLAUDE.md

```markdown
@AGENTS.md

## Claude Code 專屬補充

### .claude/rules/ 自動載入
Claude Code 啟動時自動載入 `.claude/rules/` 下所有規則檔。

### [其他 Claude 專屬規則]
...

## 文件索引
| 文件 | 內容 |
|---|---|
| `docs/xxx.md` | ... |

## 驗收自我測試
[列出關鍵問題，用於驗證規則是否完整]
```

### Step 4：建立 .claude/rules/（選填，但推薦）

每份規則檔案專注一個主題，格式：

```markdown
# [主題] 規則

[簡短條列規則，不超過 20 行]

> 詳見 docs/xxx.md
```

**推薦分類：**

| 檔案 | 用途 |
|------|------|
| `project-scope.md` | 專案定位、平台限制 |
| `change-policy.md` | 變更原則、禁止事項 |
| `auth-security.md` | 認證、授權、安全規則 |
| `api-codegen.md` | API 修改後的程式碼生成 |
| `ui-components.md` | UI 元件規則 |
| `external-deps.md` | 外部套件管理規則 |
| `output-style.md` | 回覆語言與格式 |

**路徑專屬規則（`paths` frontmatter）：**

在 rule 檔案最頂端加入 YAML frontmatter，讓該規則只在 Claude 讀取符合路徑的檔案時才載入，減少 context 雜訊。

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "lib/api/**/*.dart"
---

# API 相關規則

[只在處理上述路徑時才載入]
```

**觸發時機：** 當 Claude 讀取符合路徑的檔案時才載入，不是每次 tool call 都觸發。

**Glob 語法參考：**

| Pattern | 匹配對象 |
|---------|---------|
| `src/api/**/*.ts` | `src/api/` 下所有層級的 `.ts` 檔 |
| `external_libs/**` | `external_libs/` 目錄下所有檔案 |
| `src/**/*.{ts,tsx}` | `src/` 下所有 `.ts` 和 `.tsx` 檔（brace expansion） |
| `pubspec.yaml` | 只匹配專案根目錄的 `pubspec.yaml` |
| `**/*.md` | 任意目錄下的所有 `.md` 檔 |

**決策原則：何時加 `paths`？**

| 情況 | 建議 |
|------|------|
| 規則只在特定目錄／副檔名下才有意義 | ✅ 加 `paths` |
| 所有變更都需遵守的原則（禁止事項、輸出語言） | ❌ 不加，無條件載入 |
| 安全敏感規則（認證、核心架構） | ❌ 不加，寧可常駐警戒 |

### Step 5：建立精簡版（其他工具）

**.github/copilot-instructions.md：**

```markdown
# [專案名稱] - Copilot 指引

詳細規則請見 AGENTS.md。以下為核心摘要：

## 絕對禁止
[3–5 條最重要的禁止事項]

## 必做（修改 API 後）
[需要執行的指令]

## 語言
[指定回覆語言]
```

**.cursorrules（有 token 限制）：**

```markdown
# [專案名稱] - Cursor 規則

[同 copilot-instructions.md 精簡版]
```

---

## 六、維護規則

### 日常修改流程

| 修改內容 | 需更新的檔案 |
|---------|------------|
| 新增或修改共用規則 | `AGENTS.md` → Gemini / Codex / Copilot 自動同步；Claude 透過 @import 同步 |
| 新增 Claude 專屬規則 | 只改 `.claude/rules/` 或 `CLAUDE.md` 的專屬補充區塊 |
| 新增 Gemini 專屬規則 | 在 `GEMINI.md` 的 `@./AGENTS.md` 之後加入 |
| 刪除規則 | 改 `AGENTS.md`，確認 `.claude/rules/` 是否有對應的重複內容需一起刪除 |

### 同步檢查清單（每次更新 AGENTS.md 後）

- [ ] `.claude/rules/` 對應規則是否需要更新？
- [ ] `.github/copilot-instructions.md` 精簡版是否需要更新？
- [ ] `.cursorrules` 精簡版是否需要更新？

### 輕度重複是可接受的

`AGENTS.md`（透過 @import）與 `.claude/rules/` 的內容部分重疊。
這是刻意取捨：

- `AGENTS.md` = 其他工具的單一來源
- `.claude/rules/` = Claude Code 的分類結構 + 路徑專屬規則

重疊部分通常不超過 100 行，在可接受範圍內。

---

## 七、Memory 系統

各工具 Memory 系統**互不相通**，共用策略是透過 Context 檔案：

| 工具 | Memory 系統 | 跨 Session |
|------|------------|-----------|
| Claude Code | ✅ `~/.claude/projects/<project>/memory/` | ✅ |
| Windsurf | ✅ `~/.codeium/windsurf/memories/` | ✅ |
| Cursor | ❌ 無 | ❌ |
| VS Code Copilot | ❌ 無（靠 instructions 持久化） | ❌ |
| Gemini CLI | ❌ 無 | ❌ |

**跨工具 Memory 橋接方案：** MCP memory server（目前最可行，但需額外設定）

---

## 八、常見問題

### Q：@import 會節省 token 嗎？
**不會。** Imported 檔案在啟動時展開進入 context，等同複製貼上。
@import 的價值是「避免手動維護多份複本」，不是減少 token 用量。

### Q：.claude/rules/ 和 CLAUDE.md 哪個優先？
兩者都會載入，沒有優先級覆蓋關係。Claude Code 在啟動時：
1. 載入 CLAUDE.md（含其中的 @import）
2. 自動載入 `.claude/rules/` 下所有 `.md`
兩者合計成為 Claude Code 的完整 context。

### Q：AGENTS.md 和 CLAUDE.md 可以讓 Claude Code 同時讀到嗎？
可以，透過 CLAUDE.md 中的 `@AGENTS.md` import 即可。
Claude Code 不直接讀 AGENTS.md，但透過 import 等效於讀取了其內容。

### Q：rules/ 的 `paths` frontmatter 有什麼效果？
- 有 `paths`：只在 Claude Code 操作匹配路徑的檔案時才載入
- 無 `paths`：每次啟動都無條件載入（等同 CLAUDE.md 中的指令）

### Q：GEMINI.md 的 `@./AGENTS.md` 中的 `./` 是必要的嗎？
Gemini CLI 支援相對路徑，`@./AGENTS.md` 和 `@AGENTS.md` 效果相同，
`./` 是明確指定同目錄，建議保留以增加可讀性。

---

## 九、本專案實際驗收數據

以 B2B Manager 為基準：

| 指標 | 改前（v4.0） | 改後（v5.0） |
|------|------------|------------|
| CLAUDE.md 行數 | 215 行 | 84 行（含 @import 後展開 ~184 行） |
| AGENTS.md 行數 | 104 行 | 118 行（補充 Riverpod、路由規則） |
| Claude Code 總 context | ~315 行 | ~250 行 |
| 維護點數量 | 3 份（CLAUDE.md、AGENTS.md、rules/） | 1 份（AGENTS.md）+ 輕度同步 |

---

**資料來源：**
- Anthropic 官方文件：https://code.claude.com/docs/en/memory
- Anthropic 官方文件：https://code.claude.com/docs/en/best-practices
- 本專案實戰紀錄：`docs/ai-collaboration/agents-gemini-restructure.md`
- 工具比較：`docs/ai-collaboration/tool-comparison.md`

**最後更新：** 2026-04-27
**版本：** 1.0（從 B2B Manager 蒸餾）