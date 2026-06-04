# 跨工具 AI 協作設定指南

從本專案（B2B Manager）實戰經驗蒸餾，適用於其他專案整合多個 AI 工具時使用。

**適用工具：** Claude Code、Gemini CLI / Antigravity CLI (`agy`)、Antigravity Desktop（IDE）、OpenAI Codex CLI、VS Code Copilot、Cursor、Windsurf

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
| **Gemini CLI** ⚠️ | `GEMINI.md` | ✅ `@path/to/file` | 支援 5 層遞迴 import。**2026-06-18 停止服務，請遷移至 `agy`** |
| **Antigravity CLI (`agy`)** | **`AGENTS.md`**（主）、`GEMINI.md`（可省略） | ⚠️ 未確認 | Gemini CLI 直接接替者。實測以 `AGENTS.md` 為主要來源，`GEMINI.md` 無需維護；settings 在 `~/.gemini/antigravity-cli/`；`@import` 遞迴未有官方文件確認 |
| **Antigravity Desktop** | **`AGENTS.md`**（主）、`GEMINI.md`（可省略） | ⚠️ 未確認 | Google I/O 2026 發布的獨立 IDE。多 agent 編排、Browser Subagent、Scheduled Tasks；Skills 放 `.agents/skills/` |
| **OpenAI Codex CLI** | `AGENTS.md` | ❌ | Linux Foundation AAIF 標準 |
| **VS Code Copilot** | `.github/copilot-instructions.md`、`AGENTS.md` | ❌ | + `.github/instructions/*.instructions.md`（路徑專屬） |
| **Cursor** | `.cursorrules`、`.cursor/rules/*.mdc` | ❌ | 有 token 上限（~2000 tokens） |
| **Windsurf** | `.windsurfrules`、`AGENTS.md` | ❌ | 兩者都讀，優先 `.windsurfrules` |

> **趨勢：** `AGENTS.md` 正成為跨工具事實標準，Windsurf、Codex、VS Code Copilot 均支援。Gemini CLI 自 2026-06-18 起停止服務，官方接替為 **Antigravity 2.0 平台**（CLI `agy` + Desktop IDE + SDK，2026-05-19 Google I/O 發布）。實測確認 `agy` 以 `AGENTS.md` 為主要來源，**只需維護 `AGENTS.md`** 即可覆蓋 Antigravity 系列工具，`GEMINI.md` 可省略。

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

> **⚠️ Antigravity 2.0（CLI `agy` 與 Desktop IDE）注意：** 兩者皆原生同時讀取 `GEMINI.md` 和 `AGENTS.md`，`GEMINI.md` 中的 `@./AGENTS.md` 不一定必要（`AGENTS.md` 已被原生讀取），但保留無害。`@import` 的 5 層遞迴支援狀態**尚未有官方文件確認**；如需確保規則完整同步，建議保留 `@./AGENTS.md` 以防萬一。

### 實測紀錄：agy 1.0.3 讀取行為驗證（2026-06-01）

本專案以 CLAUDE.md 驗收自我測試 10 題在 `agy 1.0.3` 實測，結果如下：

| 項目 | 結果 |
|------|------|
| **讀取檔案** | 只讀取 `AGENTS.md`（1 次 Read call），未讀取 `GEMINI.md` |
| **10 題全對率** | ✅ 10/10 正確，所有來源皆引用 `AGENTS.md` 對應行號 |
| **@import 是否生效** | `GEMINI.md` 中的 `@./AGENTS.md` **未被觸發**，`agy` 直接原生讀取 `AGENTS.md` |
| **不完整答案** | 第 9 題（Riverpod build phase）只說「禁止」，漏了正確做法 `Future(() {})` |

**結論：**
- `agy` **不依賴 `@import`** 即可取得 `AGENTS.md` 規則，`GEMINI.md` 中的 `@./AGENTS.md` 對 `agy` 而言為冗餘（但無害）
- `AGENTS.md` 寫完整是確保 `agy` 正確運作的關鍵；`GEMINI.md` 對 `agy` 只是備援
- `@import` 對 `agy` 的支援狀態：**實測未觸發，效果存疑**

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

## 驗收自我測試

讀完本文件後，以下問題應全部能答對：

1. [平台限制題]
2. [嚴格禁止題]
3. [高風險操作題]
4. [核心架構題]
5. [構建指令題]
6. [輸出語言題]
...
```

> **驗收自我測試必須在建立 AGENTS.md 時一併產生。**
> 因為所有工具（Claude、Gemini、Codex、Copilot）都讀取 AGENTS.md，
> 題目只需維護一份，各工具透過直接讀取或 @import 自動獲得相同題目。
> 產生題目的提示詞模板參見「十、驗收自我測試」。

### Step 2：建立 GEMINI.md

```markdown
@./AGENTS.md

<!-- Gemini 專屬補充（選填）-->
```

> GEMINI.md 透過 `@./AGENTS.md` import，驗收自我測試會自動包含，無需重複撰寫。

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
```

> CLAUDE.md 透過 `@AGENTS.md` import，驗收自我測試會自動包含，無需重複撰寫。
> 若 Claude Code 有額外的 `.claude/rules/` 專屬規則未涵蓋在 AGENTS.md 的題目中，
> 可在 CLAUDE.md 末尾追加少量補充題（但核心題目仍以 AGENTS.md 為準）。

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
- [ ] 驗收自我測試題目是否仍涵蓋新增／修改的規則？

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
| Gemini CLI ⚠️ | ❌ 無 | ❌ |
| Antigravity CLI (`agy`) | ⚠️ 對話記錄存於 `~/.gemini/antigravity-cli/brain/`，可用 `agy -c <id>` 續接，但無跨專案語意記憶 | ⚠️ 有限 |
| Antigravity Desktop | ⚠️ 同上（共用 `~/.gemini/antigravity-cli/brain/`） | ⚠️ 有限 |

**跨工具 Memory 橋接方案：** MCP memory server（目前最可行，但需額外設定）；Antigravity 系列可透過 Mem0 MCP 整合提供語意記憶，非原生功能。

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

## 十、驗收自我測試（Self-Verification Test）

### 為什麼需要？

Agent 設定檔讀完後，AI 工具應能立即回答與專案安全邊界直接相關的問題。
若回答不出來，代表規則覆蓋不足，需補充文件。

**價值：**
- 強迫撰寫者確認「規則是否真的寫清楚了」
- 作為新成員或新工具 onboard 時的快速校驗
- 防止 context 太長時 AI 遺漏關鍵規則

---

### 核心原則：題目只維護一份

驗收自我測試**放在 AGENTS.md**，所有工具共用同一份題目：

| 檔案 | 驗收題來源 |
|------|----------|
| `AGENTS.md` | ✅ 直接撰寫（唯一維護點） |
| `CLAUDE.md` | 透過 `@AGENTS.md` import 自動包含 |
| `GEMINI.md` | 透過 `@./AGENTS.md` import 自動包含 |
| Codex / Copilot / Windsurf | 直接讀取 AGENTS.md |

> 這與本指南的「單一維護點」原則一致：共用內容只寫一份，其他工具透過機制同步。

---

### 產生驗收題目的提示詞模板

建立 AGENTS.md 時，使用以下提示詞讓 AI 工具一併產生驗收題目：

````
你是一位技術文件審查員。

我的專案使用以下 AI 設定規則：

---
[在此貼上 AGENTS.md 全文（不含驗收自我測試區塊）]
---

請根據以上規則，在文件最末尾生成一個「驗收自我測試」區塊。

要求：
1. 題目數量：8–12 題
2. 必須涵蓋以下類別（有對應規則才出題）：
   - 平台限制（支援哪些平台？哪些不支援？）
   - 嚴格禁止事項（哪些操作絕對不可做？）
   - 高風險操作（哪些操作需要使用者確認？）
   - 架構核心元件（核心元件如何使用？有哪些禁止用法？）
   - 構建 / 驗證指令（修改特定路徑後需執行什麼？）
   - 輸出語言與格式
3. 題目設計原則：
   - 用「可以／不可以」「要注意什麼」「要執行什麼」等句型
   - 答案必須在設定文件中明確可查到（不出推論題）
   - 優先針對「容易踩雷」的細節出題（例如反直覺的規則）
4. 輸出格式：

## 驗收自我測試

讀完本文件後，以下問題應全部能答對：

1. ...
2. ...
````

---

### 驗收題目類別參考

| 類別 | 範例題型 |
|------|---------|
| **平台限制** | 本專案支援哪些平台？iOS / Android 可以嗎？ |
| **禁止事項** | [核心元件] 套件可以用套件管理工具更新嗎？ |
| **高風險操作** | 修改 [路由檔案] 要注意什麼？ |
| **架構元件** | [單例元件] 的授權流程必須透過什麼處理？ |
| **反直覺規則** | [數值參數] 傳入時要加 +1 嗎？表格高度可以用相對單位嗎？ |
| **構建指令** | 修改 [API 路徑] 後要執行什麼指令？ |
| **UI 互動規則** | [UI 元件] 的三種游標分別對應什麼設定？ |
| **狀態管理** | 在 build phase 可以直接修改 provider 狀態嗎？ |
| **輸出語言** | 回覆要使用什麼語言？技術術語要翻譯嗎？ |

---

### AGENTS.md 驗收區塊模板

```markdown
---

## 驗收自我測試

讀完本文件後，以下問題應全部能答對：

1. 本專案支援哪些平台？（涵蓋「不支援」的部分）
2. 哪些操作屬於嚴格禁止，不需使用者確認即應拒絕？
3. [核心單例元件] 的職責是什麼？哪些操作不可繞過它？
4. 修改 [API 端點 / DTO 路徑] 後必須執行什麼指令？
5. [UI 元件] 的互動狀態分別對應什麼設定？
6. [某數值參數] 在傳入 [元件] 時要加修正值嗎？
7. [外部套件目錄] 可以用套件管理工具升級嗎？
8. 回覆必須使用什麼語言？技術術語如何處理？
9. 在 build phase 可以直接修改 provider 狀態嗎？正確做法？
10. 修改 [路由設定檔] 要注意什麼？屬於哪種風險等級？
```

> 將 `[ ]` 佔位符替換為你的專案實際名稱與路徑。


---

## 十一、本專案實際驗收數據

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
- Antigravity CLI 遷移參考：`ai-pair-main-v4.2/reference/重構建議-v4.3-agy遷移.md`
- Antigravity 2.0 官方部落格：https://antigravity.google/blog/google-io-2026
- Google I/O 2026 開發者亮點：https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/

**最後更新：** 2026-06-01
**版本：** 1.3（新增 Antigravity 2.0 Desktop IDE、更新 Memory 表格與 agy config 路徑）