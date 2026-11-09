# Claude Code 分工（Subagent Delegation）指南

**用途：** 說明如何讓 Claude Code 把工作分派給 subagent、可以指定哪些 model、
以及**分工要成立需要準備哪些文件**。

**適用專案：** b2b-manager（Flutter Web）
**最後更新：** 2026-10-19（契約複本路徑改為 `docs/api/` 最新版、後端規則行數更新）

> 📘 **要在其他專案導入分工**，請看
> [`claude-subagent-delegation-generic.md`](./claude-subagent-delegation-generic.md)（通用版）——
> 內含決策框架、禁區清單建立方法與導入步驟。本文件是該框架套用到 b2b-manager 的結果。

---

## 0. 先講結論（本專案的預設立場）

> **本專案預設「不分工」——主 session 直接實作。**
> 只有三種情境值得派工，見 [§4 派工判準](#4-派工判準)。

原因不是分工做不到，而是**本專案的規則密度高、規模不夠大**，派工的固定開銷
（subagent 冷讀規則文件、回報後主 session 再驗證）多數情況大於收益。詳見
[§8 為什麼預設不分工](#8-為什麼預設不分工)。

本文件仍完整說明分工機制，供以下情況參考：
- 遇到符合判準的任務時，照 [§5 派工模板](#5-派工模板必備四段) 執行
- **前後端同時要改**時，照 [§6 跨 repo 循序變更](#6-跨-repo-循序變更b2b-backend--b2b-manager)
  ——這是本專案少數值得派工的實作型任務
- 未來專案長大、或要移植到其他專案時，有完整依據

---

## 1. 分工的三種層級

### 層級 A：單次呼叫時指定

最輕量，不需要任何設定檔。主 session 跑 Opus，呼叫時降級：

```
Agent(subagent_type: "Explore", model: "haiku", prompt: "...")
Agent(subagent_type: "general-purpose", model: "sonnet", prompt: "...")
```

可用 model：`opus` / `sonnet` / `haiku` / `fable`。

⚠️ **例外**：`subagent_type: "fork"` 的 `model` 參數**會被忽略**——fork 要複製
主 session 的完整 context，一律繼承主 session 的 model。要換 model 就別用 fork。

### 層級 B：在 agent 定義檔固定

建立 `.claude/agents/<name>.md`（本專案**目前尚未建立此目錄**）：

```markdown
---
name: flutter-implementer
description: 依 docs/shared/ 任務文件實作既有 pattern 的 Flutter 頁面。
             適用於樣板重複、需求明確的任務；不適用 DataTable / 權限 gating 變更。
model: sonnet
tools: Read, Edit, Write, Bash, Grep, Glob
---

（此處寫 system prompt：要求先讀哪些規則檔、產出格式、禁止事項）
```

**關鍵：`description` 決定它會不會被自動選用。**
Claude Code 是靠 description 判斷「這個任務該不該叫它」，所以 description 要寫
**什麼情況該用**，不是寫**這個 agent 會做什麼**。

呼叫時仍可用 `model` 參數覆寫定義檔的設定。

### 層級 C：Workflow 腳本編排

需要多階段、有明確前後依賴時使用（ai-pair 流程屬於此型）：

```js
await pipeline(tasks,
  t => agent(t.prompt, { model: 'sonnet', effort: 'low' }),      // 實作
  r => agent(`review: ${r}`, { model: 'opus', effort: 'high' })  // 審查
)
```

⚠️ Workflow 會一次展開多個 agent、消耗大量 token，**必須使用者明確要求才可啟動**。

---

## 2. Claude 會自己主動分工嗎？

**預設不會主動。** 主 session 大部分工作自己做，只在以下情況才會考慮派工：

- 需要大範圍搜尋但只想要結論（→ Explore）
- 有多個**互相獨立**的子任務可平行
- agent 定義的 description 明確寫了「應主動使用」

**本專案另有一條 session 層限制：**

```
Do not call the AgentTool unless the user requested it
```

等同於**完全關閉自動派工**。要開啟自動分工必須先移除此條，並在 `CLAUDE.md`
補上明確的委派規則（見 §3）。

---

## 3. 分工需要哪些文件

這是本文件的核心。分工失敗**幾乎都不是 model 能力問題，而是文件沒到位**。

subagent 是**全新的 context**——它看得到的只有下列三類，看不到你和主 session
的對話、也讀不到 memory。

### 3.1 自動載入的（不用特別給，但要確認內容夠用）

| 文件 | 內容 | 對 subagent 的意義 |
|---|---|---|
| `CLAUDE.md` | Claude Code 專屬規則 + `@AGENTS.md` import | 基礎規則 |
| `AGENTS.md` | 跨工具共用規則（screenutil、DataTable2、權限 gating、build_runner） | 主要約束來源 |
| `.claude/rules/*.md` | P0 硬規則集（9 個檔） | 細分類禁令 |

⚠️ 這三類每個 subagent 都會**重新讀一次**，不共用主 session 的 prompt cache——
這是派工的主要固定成本。

### 3.2 必須在 prompt 裡明確指名的（最容易漏）

| 文件 | 何時必須指名 | 漏了會怎樣 |
|---|---|---|
| `DESIGN.md` | **任何 UI 變更** | 寫出 `.w/.h/.sp`、硬編色碼、不用 `SLColor`/`SLText`/`SpacerWidget` |
| `docs/shared/<任務文件>.md` | 有需求文件的實作任務 | 自行揣測需求，做出規格外的東西 |
| `docs/claude/claude-datatable-rules.md` | 動到 DataTable2 / VirtualDataTable | 踩 `sortColumnIndex +1`、欄寬計算、邊框位置的雷 |
| `.claude/rules/permission-gating.md` | 動到權限判斷 | 改用 disable，破壞全站 18:0 慣例 |
| `.claude/rules/list-page-header.md` | 新增列表頁篩選列 | 用 Wrap 換行，或漏掉 1270 最小寬度 |
| `docs/api/api_documentation_vN.md`（取版本號最大者） | 動到 API 契約 / DTO | 欄位名稱對不上後端 |

`DESIGN.md` 特別重要：`CLAUDE.md` 只是「引用」它而非 `@import`，
**不會自動載入**，subagent 不指名就讀不到。

### 3.3 主 session 要自己補進 prompt 的（沒有文件承載）

這類是**對話中累積、或存在 memory 裡**的判斷，subagent 完全接觸不到：

- 這次任務為什麼這樣做的取捨脈絡
- 之前試過但失敗的方向（例：曾把權限 gating 改成 disable，盤點後改回隱藏）
- 使用者當下的偏好與優先順序
- 相鄰模組尚未提交的改動

**沒有寫進 prompt 的，等於不存在。**

---

## 4. 派工判準

### ✅ 值得派工

| 情境 | 建議 agent / model | 為什麼賺 |
|---|---|---|
| 跨檔案盤點、找全站慣例（「全站哪裡用了 X」） | `Explore` + `haiku` | 只回報結論，不把幾十個檔案倒進主 session context |
| 跨 repo 調查／後端實作（b2b-backend） | `general-purpose` + `sonnet` | 隔離掉另一個 repo 的 context——詳見 [§6 跨 repo 循序變更](#6-跨-repo-循序變更b2b-backend--b2b-manager) |
| **3 個以上**獨立的重複樣板頁面 | `sonnet`，平行 | 省的是時間不是 token；1~2 個直接做更快 |

### ❌ 不要派工

- DataTable2 / VirtualDataTable 的欄寬、排序、游標、邊框
- 權限 gating 的呈現方式
- **前端**的 API endpoint / DTO / Retrofit（含 `build_runner` 判斷）
  ⚠️ **後端**的實作是例外，見 [§6](#6-跨-repo-循序變更b2b-backend--b2b-manager)——
  但契約定案與前端跟進一律留在主 session
- `lib/page/page_route.dart`
- OAuth2 / TaskManager 相關
- `external_libs/` 內任何檔案

理由一致：這些是**負面約束密集區**，失敗成本遠高於節省的 token。
subagent 的失敗模式是「不知道自己不知道」——它讀了規則但沒有踩雷記憶。

---

## 5. 派工模板（必備四段）

任何一次派工的 prompt 都應包含這四段，缺一段就容易出事：

```
【任務】
（一句話講清楚要做什麼，含範圍邊界：改哪些檔、不要動哪些檔）

【必讀文件】
1. DESIGN.md（UI token：SLColor / SLText / SpacerWidget / kAppRadius）
2. docs/shared/SSGS-XXXXX-xxx.md（需求規格）
3. .claude/rules/list-page-header.md（若涉及列表頁 header）

【禁止事項】
- 禁止使用 .w / .h / .sp，一律固定 px
- 禁止修改 DataTable2 的 fixedWidth / ColumnSize / sortColumnIndex
- 禁止修改 external_libs/
- 超出上述範圍的檔案不要動，遇到就回報而非自行決定

【回報格式】
只回報：改了哪些檔、每檔做了什麼（各一行）、遇到的疑問。
不要把檔案內容貼回來。
```

最後一段是成本控制的關鍵——**subagent 回報檔案內容會直接吃掉分工省下的開銷**。

---

## 6. 跨 repo 循序變更（b2b-backend → b2b-manager）

前後端同時要改時的專屬做法。這是本專案**少數值得派工**的實作型任務。

### 6.1 為什麼不平行派兩邊

前後端同時改的**唯一耦合點就是契約**（enum / DTO / endpoint）。
兩個 subagent 各自在自己的 repo 裡對契約做微調，誰都不知道對方改了什麼——
這是 drift 的製造機。

實證：`AccountBalanceAdjustmentType` 曾缺 5 個後端已有的值
（`CREDIT_ADJUSTMENT` / `MANUAL_DEPOSIT` / `MANUAL_PAYMENT` / `PAYMENT` /
`SALES_ALLOWANCE`），因 response DTO 非 nullable 解析，收到未知值會
**整批失敗、整頁空白**。契約漂移是本專案真實發生過的痛點。

### 6.2 建議流程（後端先行）

**先後端再前端優於平行**——契約由後端實作**產生**而非事前約定，
前端只是照著已存在的事實走，drift 在結構上不可能發生。

| 步驟 | 誰做 | 說明 |
|---|---|---|
| 1. 後端實作 | **派工**（`sonnet`，cwd = `b2b-backend`） | 見 6.3 |
| 2. 契約落地成文件 | **主 session** | 更新任務文件 / `docs/api/api_documentation_vN.md`（取版本號最大者） |
| 3. 驗證契約 | **主 session** | 見 6.5——不要只信回報 |
| 4. 前端實作 | **主 session，不派工** | 負面約束密集區（screenutil / DataTable / 權限 gating） |

⚠️ **第 2 步不可省。** subagent 的回報只存在於那一輪對話，不落成文件的話，
後續接手者（或下個 session）看不到。

### 6.3 為什麼後端那半值得派

| 理由 | 說明 |
|---|---|
| **context 隔離**（主要價值） | Spring Boot 程式碼完全不需要進主 session 的 context——輸入大、輸出小的典型安全區 |
| **冷讀成本極低** | `b2b-backend` 只有 `CLAUDE.md`(55 行) + `AGENTS.md`(94 行)、**沒有** `.claude/rules/`，共 149 行（2026-10-19 實測）；對照前端整套規則，固定開銷小得多 |
| 規則載入正確性 | 從 `b2b-manager` 為 cwd 去改後端檔案時，**後端的 `CLAUDE.md` 不會自動載入**（Claude Code 只從 cwd 往上找，`b2b-backend` 是平行目錄）——等於用 Flutter 規則改 Spring Boot 程式碼 |

> 第三點有便宜替代方案（149 行直接讀進主 session 即可），所以它比第一點弱。
> **派工的主要價值是 context 隔離。**

### 6.4 回報格式（後端先行時要加嚴）

契約事前定案時，回報只是「做完了」；**後端先行時，回報本身就是契約**。
這裡多了一種失敗模式——它寫了 A、回報成 B，文字描述漂移沒有任何機制會擋。

```
【必讀】
1. b2b-backend/AGENTS.md（cwd 在後端時會自動載入，仍建議明列）
2. docs/shared/<任務文件>.md 的「後端」章節

【回報格式】
1. 改了哪些檔（各一行）
2. 契約明細 —— 這段會被前端直接採用，必須與程式碼逐字一致：
   - enum：完整值列表（照原始碼順序，不要省略既有值）
   - DTO：欄位名稱、型別、**是否 nullable**
   - endpoint：method + 完整路徑 + 權限標註（@PreAuthorize）
3. 不確定或有疑慮的地方
```

**nullable 必須問出來。** 本專案契約失誤的主要爆炸形式就是
「response DTO 非 nullable 解析 → 整頁空白」，回報沒寫清楚等於沒回報。

若契約已事前定案（例如需求文件已寫死），則改用鎖定式指令：

```
【契約鎖定】
enum 值、DTO 欄位名稱、endpoint 路徑一律照任務文件，不得自行增減或改名；
覺得契約有問題就回報，不要自己改。
```

### 6.5 驗證：不要只信回報

拿到回報後**別直接開始寫前端**，先用機器驗一次：

- 既有的 `SessionStart` hook 跨 repo enum 差集比對
  （見 [`backend-doc-sync-hook.md`](./backend-doc-sync-hook.md)）
- 或直接 grep 後端該 enum / DTO 檔案，對照回報內容

這步很便宜，但擋掉的是整條鏈路上最貴的錯誤。

### 6.6 不需要派工的情況

**後端已經做完、前端跟上** → 不用碰後端 repo，
讀 `docs/api/api_documentation_vN.md`（取版本號最大者）（前端的契約複本）即可。
那份複本存在的用意就是這個。

### 6.7 收尾檢查

- [ ] 前端若動到 `lib/api/request/` `response/` `restclient/` → 執行
      `flutter pub run build_runner build --delete-conflicting-outputs`
      （**此判斷留在主 session**，subagent 不知道 `.g.dart` 慣例）
- [ ] 新增權限資源 → 同步 `authorities_enum.dart` 與 `rule_enum.dart`
- [ ] 契約已寫回 `docs/shared/`，不只存在對話裡

---

## 7. 成本模型（為什麼「便宜 model」不等於省錢）

派工的實際成本 =

```
subagent 冷讀規則文件（CLAUDE.md + AGENTS.md + .claude/rules/，無 cache）
+ subagent 讀 prompt 指名的文件
+ subagent 實際工作
+ 主 session 讀回報
+ 主 session 驗證產出
+ （做錯時）重派一輪
```

而主 session 直接做的成本 =

```
規則文件已在 context 且 cache 命中
+ 實際工作
```

**只有當「省下的 context 佔用」大於「上述固定開銷」時才划算。**
這解釋了為什麼 §4 的三個情境會賺——它們共同特徵是
**輸入大、輸出小**（讀很多、只回報一點）或**可平行**。

反過來「改一個報表頁面」這種輸入小、需要精確判斷的任務，派工必虧。

---

## 8. 為什麼預設不分工

本專案的兩個特性讓分工的期望值偏低：

**（一）規則大量是負面約束。** 攤開 `AGENTS.md` 與 `.claude/rules/`，
主體是「不可以做什麼」而非「要做什麼」：

- `sortColumnIndex` 不可加 `+1`
- 權限 gating 不可用 disable（已盤點全站 18:0）
- VirtualDataTable 最後一列邊框不可畫在容器底部
- `external_libs/` 不可 `pub upgrade`
- 新程式碼不可用 `.w/.h/.sp`

正面指示漏了會產出不完整（看得出來）；**負面約束漏了會產出「看起來對但錯」**
（看不出來）。後者正是 subagent 的典型失敗模式。

**（二）規模不足以攤平開銷。** 單一 Flutter Web 專案，多數任務是既有 pattern
的重複套用，主 session 的 context 裝得下。

這個結論與既有的實測紀錄一致，見
[`dev-workflow-handoff-token-strategy.md`](./dev-workflow-handoff-token-strategy.md)
與 ai-pair 的使用經驗：**同 pattern 重複任務直接實作更快、更精確。**

---

## 9. 若要改成自動分工，需要做的事

（目前不建議，但保留路徑）

1. 移除 session 層的 `Do not call the AgentTool unless the user requested it`
2. 建立 `.claude/agents/`，每個 agent 的 `description` 寫清楚**觸發條件**
3. 在 `CLAUDE.md` 補「任務委派規則」區塊，明列該派/不該派的清單
4. 每個 agent 的 system prompt 內建「必讀文件」清單，減少 prompt 遺漏
5. **先手動派工累積數據**，確認哪類任務 subagent 做得乾淨，再自動化該類

第 5 點是前提。跳過它直接開自動，等於讓 Claude 憑「這看起來只是個樣板頁面」
的判斷去派工——而誤判的代價就是有人動到 DataTable 欄寬。

---

## 10. 驗證方法

要判斷某類任務是否適合派工，用對照實驗而非推論：

同一個中型任務，主 session 直接做一次、派 subagent 做一次，比對：

- [ ] 產出正確性（是否踩到負面約束）
- [ ] 實際 token 消耗
- [ ] 往返輪數（有沒有需要補充說明、重做）
- [ ] 主 session context 佔用差異

累積 3~5 次同類任務的數據，再決定是否寫進委派規則。

---

## 相關文件

| 文件 | 關聯 |
|---|---|
| [`dev-workflow-handoff-token-strategy.md`](./dev-workflow-handoff-token-strategy.md) | ai-pair 的 token 節省機制、HANDOFF/MEMORY 整合 |
| [`claude-subagent-delegation-generic.md`](./claude-subagent-delegation-generic.md) | **通用版**：決策框架、禁區清單建立方法、導入步驟（供其他專案使用） |
| [`cross-tool-ai-setup.md`](./cross-tool-ai-setup.md) | 跨工具協作設定（Codex / Copilot / Gemini） |
| [`backend-doc-sync-hook.md`](./backend-doc-sync-hook.md) | 跨 repo 文件同步 hook |
| `../../DESIGN.md` | UI token SoT——**任何 UI 派工必須指名** |
| `../../.claude/rules/` | P0 硬規則集，subagent 自動載入 |