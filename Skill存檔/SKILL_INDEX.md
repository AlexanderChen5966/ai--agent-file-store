# Skill 索引總覽

> 整理日期：2026-05-25
> 說明：本文件整理所有自訂 Skill 的名稱、描述、用途與版本號

---

## 目錄

- [開發類（dev）](#開發類dev)
  - [code-review v1](#1-code-review-v1)
  - [code-review v2](#2-code-review-v2)
  - [code-review v3](#3-code-review-v3)
  - [requirements](#4-requirements)
  - [doc-update](#5-doc-update)
  - [flutter-b2b-documentation](#6-flutter-b2b-documentation)
  - [project-documentation](#7-project-documentation)
  - [doc-generator](#8-doc-generator)
  - [multi-tool-coordination](#9-multi-tool-coordination)
  - [context-sharing](#10-context-sharing)
  - [dev-doc-organizer](#11-dev-doc-organizer)
  - [ai-pair](#12-ai-pair)
  - [figma-to-flutter ⚠️ 已退役](#13-figma-to-flutter--已退役歸檔2026-06-23)
  - [figma-to-requirements](#16-figma-to-requirements)
  - [zerospec-skills](#14-zerospec-skills)
  - [ai-pair-v4-test](#15-ai-pair-v4-test)
- [通用類（general）](#通用類general)
  - [media-processor](#9-media-processor)
  - [sign-off-generator](#10-sign-off-generator)
  - [document-translator](#11-document-translator)
  - [translategemma-translator](#12-translategemma-translator)
  - [discussion-organizer](#13-discussion-organizer)
  - [cross-platform-archive-agent](#14-cross-platform-archive-agent)
- [知識管理類（pkm）](#知識管理類pkm)
  - [knowledge-organizer](#1-knowledge-organizer)
  - [daily-brief-generator](#2-daily-brief-generator)
  - [wiki-health-check](#3-wiki-health-check)
  - [raw-pipeline](#4-raw-pipeline)
  - [knowledge-synthesizer](#5-knowledge-synthesizer)
  - [alignment-check](#6-alignment-check)
  - [knowledge-elevation](#7-knowledge-elevation)
  - [obsidian-second-brain](#8-obsidian-second-brain)
  - [scientific-brainstorming](#9-scientific-brainstorming)
- [系統內建 Skill（Claude Code 提供）](#系統內建-skillclaude-code-提供)

---

## 開發類（dev）

### 1. code-review v1

| 欄位 | 內容 |
|------|------|
| **名稱** | `code-review` |
| **版本** | `1.0.0` |
| **路徑** | `dev/code-review-v1/` |
| **最後更新** | 無記錄 |

**描述：**
專為 Flutter + Riverpod 專案設計的 Code Review Skill，自動呼叫 code-reviewer subagent 進行深度分析。

**用途：**
- 使用者請求 code review（如 `/review`、「review this code」）時觸發
- 完成功能開發後進行品質審查
- 驗證架構合規性（ConsumerState / SingleTaskState / CacheableState）
- 檢查 Riverpod 使用模式（ref.watch vs ref.read）
- OAuth2 安全性稽查
- 產出分級報告（🔴 Critical / 🟡 Warning / 🟢 Suggestion）

**支援技術棧：**
Flutter + Riverpod（專屬版，限 B2B Manager 專案）

---

### 2. code-review v2

| 欄位 | 內容 |
|------|------|
| **名稱** | `code-review` |
| **版本** | `1.1.0` |
| **路徑** | `dev/code-review-v2/` |
| **最後更新** | 2026-01-08 |

**描述：**
多技術棧 Code Review，具備自動偵測專案類型功能，涵蓋 Flutter（Riverpod/Bloc）、Java Spring Boot、Android（Java/Kotlin）。

**用途：**
- 自動偵測專案類型（讀取 `pubspec.yaml` / `pom.xml` / `build.gradle`）
- 依技術棧套用對應的審查清單
- 支援混合專案（前端 Flutter + 後端 Spring Boot 同時審查）
- 呼叫 code-reviewer subagent 深度分析
- 輸出各技術棧的架構合規報告

**支援技術棧：**

| 技術棧 | 檢查清單 |
|--------|---------|
| Flutter + Riverpod | `references/flutter-riverpod.md` |
| Flutter + Bloc | `references/flutter-bloc.md` |
| Spring Boot | `references/springboot.md` |
| Android（Java/Kotlin） | `references/android.md` |
| 通用（所有棧） | `references/common.md` |

---

### 3. stack-review (原 code-review v3)

| 欄位 | 內容 |
|------|------|
| **名稱** | `stack-review` |
| **版本** | `1.1.0` |
| **路徑** | `dev/stack-review/` |
| **最後更新** | 2026-05-25（重命名，避免與內建 `/code-review` 衝突） |

**描述：**
在 v2 多技術棧基礎上，新增 Step 7：review 通過後自動檢查 `docs/shared/` 是否有「待實作」任務文件，有則提示執行 `/doc-update`，形成完整的開發工作流程閉環。

> ⚠️ **2026-05-25 重命名**：因 Claude Code v2.1.147 將內建 `/simplify` 改名為 `/code-review`，造成同名衝突，故將此自訂 skill 重命名為 `stack-review`。觸發指令改為 `/stack-review`。

> 💡 **定位說明（2026-05-25）**：主線工作流已改為 `requirements → ai-pair → doc-update`，ai-pair 的三個 reviewer 已覆蓋正式 review 需求。`stack-review` 定位為**輕量替代**，適合小改動（單檔 bug fix、typo、i18n）不值得啟動 ai-pair 的情境。

**新增功能（v1.2.0）：**
- Step 7：Overall Status ✅ Approved 時，自動掃描 `docs/shared/*.md`
- 若有「待實作」文件 → 提示 `💡 建議執行 /doc-update 將任務文件標記為已完成`
- 若無對應文件或目錄不存在 → 略過
- Status ⚠️ / ❌ 時不提示（仍有問題未解決）

**與 v2 的差異：** 僅新增 Step 7，其餘審查邏輯與支援技術棧不變。

**配合使用：** 建議搭配 `requirements` v1.0.0 和 `doc-update` v1.0.0 形成完整工作流程。

---

### 4. requirements

| 欄位 | 內容 |
|------|------|
| **名稱** | `requirements` |
| **版本** | `1.1.0` |
| **路徑** | `dev/requirements/` |
| **最後更新** | 2026-03-18 |

**描述：**
將模糊需求轉換為標準化任務文件，存入 `docs/shared/`。自動分析影響範圍、拆解實作任務、確認風險清單，產出可直接交給 AI agent 實作的任務文件。

**用途：**
- 接收模糊需求描述 → 詢問補充資訊 → 探索相關程式碼 → 產出完整任務文件
- 自動對照 CLAUDE.md 風險清單（OAuth2、TaskManager、build_runner、DataCell 游標等）
- 任務文件包含：背景說明、需求說明、影響範圍分析、實作任務（含 code snippet）、執行步驟（`[ ]` checklist）
- 若 `docs/shared/` 不存在，自動建立目錄與 `readme.md`
- 自動更新 `docs/shared/readme.md` 索引（新增「⏳ 待實作」條目）

**新增功能（v1.1.0）：**
- **Step 5（新增）**：寫入前先檢查同名文件是否已存在
  - 「⏳ 待實作」/ 「🔄 進行中」→ 直接覆寫，狀態不變
  - 「✅ 已完成」→ 提示使用者確認後才覆寫，狀態改為「🔄 進行中」
- **Step 7 強化**：重新開啟已完成文件時，readme.md 狀態改回「🔄 進行中」
- **Step 8（新增）**：重新開啟已完成文件時，更新 CHANGELOG.md（`Changed` 分類）

**觸發關鍵字：** `/requirements`、「討論作法」、「需求分析」、「寫任務文件」、「規劃功能」

**包含 references：**
- `references/task-doc-template.md`：標準任務文件模板
- `references/readme-template.md`：`docs/shared/readme.md` 初始格式

**配合使用：** → `stack-review` v1.2.0 → `doc-update` v1.1.0

---

### 5. doc-update

| 欄位 | 內容 |
|------|------|
| **名稱** | `doc-update` |
| **版本** | `1.1.0` |
| **路徑** | `dev/doc-update/` |
| **最後更新** | 2026-03-18 |

**描述：**
Code review 通過後，將 `docs/shared/` 的任務文件狀態從「待實作」或「進行中」標記為「已完成」，並同步更新 CHANGELOG.md 與 docs/shared/readme.md 索引。

**用途：**
- 更新任務文件 `## 狀態` 區塊：`**⏳ 待實作**` 或 `**🔄 進行中**` → `**✅ 已完成**（YYYY-MM-DD）`
- 各任務標題加 ✅、執行步驟加 ✅、驗收清單 `[ ]` → `[x]`
- 若實際實作與計劃有差異，追加「## 實際實作備註」區塊
- 更新 `CHANGELOG.md` 的 `[Unreleased]` 區塊（Added / Changed / Fixed）
- 更新 `docs/shared/readme.md` 任務狀態索引表（`⏳ 待實作` → `✅ 已完成`）
- 若文件已完成 → 立即停止，不重複操作
- 若 `docs/shared/` 不存在 → 提示並停止

**新增功能（v1.1.0）：**
- 同時處理「⏳ 待實作」與「🔄 進行中」兩種狀態（v1.0.0 僅處理「待實作」）

**觸發關鍵字：** `/doc-update`、「更新任務文件」、「mark as done」、「標記完成」

**包含 references：**
- `references/readme-format.md`：`docs/shared/readme.md` 目標格式說明

**配合使用：** `requirements` v1.1.0 → `stack-review` v1.2.0 → `doc-update` v1.1.0

---

### 6. flutter-b2b-documentation

| 欄位 | 內容 |
|------|------|
| **名稱** | `flutter-b2b-documentation` |
| **版本** | `1.0.0`（B2B 專案專屬） |
| **路徑** | `dev/flutter-b2b-documentation/` |
| **最後更新** | 無記錄 |

**描述：**
針對 Flutter Web B2B Manager 專案量身打造的自動化技術文件產出工具。

**用途（三種模式）：**

| 模式 | 觸發關鍵字 | 產出位置 |
|------|-----------|---------|
| 專案整體架構 | "project"、"專案架構" | `docs/PROJECT_ARCHITECTURE.md` |
| 功能模組文件 | "feature"、模組名稱 | `docs/page_architecture/[模組]_DOCUMENTATION.md` |
| API 總覽 | "api"、"API 清單" | `docs/API_REFERENCE.md` |

**功能模組文件自動化流程：**
- 探索 `lib/page/[模組]/`
- 提取 REST Client API 端點
- 分析 StateNotifier 方法
- 整理 Request/Response DTO
- 記錄 UI 組件與權限控制

> ⚠️ 此 Skill 為 B2B Manager 專案專屬，已被 `project-documentation` v1.1.0 取代。

---

### 7. project-documentation

| 欄位 | 內容 |
|------|------|
| **名稱** | `project-documentation` |
| **版本** | `2.0.0` |
| **路徑** | `dev/project-documentation/` |
| **最後更新** | 2026-04-28 |

**描述：**
多技術棧可擴展文件產出系統，為 `flutter-b2b-documentation` 的通用化進化版。v2.0.0 新增 Spring Boot 完整支援、Bug 修復紀錄與 Widget 元件文件兩種新類型，並統一 frontmatter 規範與 kebab-case 命名。

**用途（五種文件類型）：**

| 類型 | 觸發關鍵字 | 產出位置 |
|------|-----------|---------|
| 專案架構文件 | "project"、"專案架構"、"建立架構文件" | `docs/project-architecture.md` |
| 功能模組文件 | "feature"、"記錄功能"、模組名稱 | `docs/page_architecture/[模組]-documentation.md` |
| API 總覽文件 | "api"、"API 清單"、"整理 API" | `docs/api-reference.md` |
| Bug 修復紀錄 | "bug"、"修復紀錄"、"bug record" | `docs/bug_record/[問題名稱].md` |
| Widget 元件文件 | "widget"、"元件文件"、"component" | `docs/widget/[元件名稱].md` |

**支援狀態：**

| 技術棧 | 狀態 |
|--------|------|
| Flutter（Riverpod/Bloc） | ✅ 完整支援 |
| Spring Boot（Spring Data JDBC） | ✅ 完整支援 |
| Android | 🔧 框架就緒（待擴展） |

**新增功能（v2.0.0）：**
- Spring Boot 升為完整支援（Controller、Entity、Repository、Service、DTO、@PreAuthorize、@Operation）
- 新增文件類型：Bug 修復紀錄（通用，互動式收集 + `git diff`）
- 新增文件類型：Widget 元件文件（Flutter，分析建構子參數、Provider 依賴、使用位置）
- 統一 frontmatter 規範（`title`、`type`、`created`、`status`、`related-modules`）
- 文件命名全面改為 kebab-case（如 `order-documentation.md`）

**包含 references：**
- `references/frontmatter-spec.md`：Frontmatter 與命名規範
- `references/stack-context/flutter.md`、`springboot.md`：技術棧上下文
- `references/templates/flutter-feature.md`、`springboot-feature.md`：功能模組範本
- `references/templates/bug-record.md`：Bug 修復紀錄範本
- `references/templates/widget-doc.md`：Widget 元件文件範本

---

### 8. doc-generator

| 欄位 | 內容 |
|------|------|
| **名稱** | `doc-generator` |
| **版本** | `1.0.0` |
| **路徑** | `dev/doc-generator/` |
| **最後更新** | 無記錄 |

**描述：**
自動化 API 文件生成工具，從單一 Markdown 來源產生多種格式輸出。

**用途：**
- 將 API Markdown 文件轉換為 **PDF**（WeasyPrint）
- 生成 **Postman Collection**（v2.1 格式）
- 產生 **API UML 時序圖**（PlantUML）
- 繪製**資料庫 ER 圖**（Graphviz）
- 一鍵執行 `./generate_all.sh` 產生所有格式

**觸發關鍵字：**
「產生文件」、「建立 API 文件」、「生成 Postman」、「產生流程圖」、「建立資料庫架構圖」

**輸出文件清單：**

| 文件 | 格式 | 路徑 |
|------|------|------|
| API 文件 | PDF | `delivery_doc/washcar_api.pdf` |
| Postman Collection | JSON | `delivery_doc/washcar_api.json` |
| API 流程圖 | PNG | `delivery_doc/Wash_Car_API_Flow.png` |
| 資料庫 ER 圖 | PNG | `delivery_doc/Table_scheme.png` |

**系統需求：** Python 3.7+、WeasyPrint、PlantUML（需 Java）、Graphviz

---

### 9. multi-tool-coordination

| 欄位 | 內容 |
|------|------|
| **名稱** | `multi-tool-coordination` |
| **版本** | `1.0.0` |
| **路徑** | `dev/multi-tool-coordination 協調 AI 工具分工skills/` |
| **授權** | Apache-2.0 |
| **最後更新** | 無記錄 |

**描述：**
協調多個 AI 編碼工具（Claude Code、GitHub Copilot、Codex、Gemini）進行複雜開發任務的**知識型指南**（人工操作）。教導如何根據任務特性選擇工具與傳遞上下文，不涉及 Agent 自動化。

**用途：**
- 根據任務特性選擇最適合的 AI 工具
- 規劃工具間的協作流程與上下文傳遞
- 適用場景：複雜功能開發、技術選型、問題排查
- 節省單一工具使用額度（工具分流）

**工具分工建議：**

| 工具 | 最適合的場景 |
|------|------------|
| Claude Code | 架構設計、多檔案分析、代碼審查、技術決策 |
| GitHub Copilot CLI | 快速代碼生成、樣板代碼、Shell 腳本 |
| Codex CLI | 演算法實作、資料處理、ML 相關代碼 |
| Gemini CLI | 技術研究、方案比較、最新技術調研 |

**協作模式：**
1. 設計 → 實作 → 審查（Claude → Copilot → Claude）
2. 研究 → 規劃 → 實作（Gemini → Claude → Copilot）
3. 快速查詢 → 深度分析（Copilot → Claude）

**是否需要搭配 `context-sharing`：**

所有工具切換本質上都是獨立 process，上下文無法自動共享。部分 CLI（如 `copilot --model gpt-4.1 -p ""`）支援 stdin pipe，可臨時注入內容；但並非所有 CLI agent 都提供 pipe 介面，且即使支援 pipe，多輪協作與跨 session 場景仍需共享文件持久化狀態。

| 情境 | 需要？ | 說明 |
|------|--------|------|
| CLI 工具支援 stdin pipe、單輪執行 | 💡 可選 | 可用 `cat file \| copilot -p "..."` 直接注入，省去共享文件；但內容複雜或多任務時仍建議用文件 |
| CLI 工具**不支援** stdin pipe | ✅ 需要 | 無法臨時注入，共享文件是唯一橋接方式 |
| Claude 規劃需求 → 任意 CLI 工具執行 | ✅ 需要 | 規劃結果須外部化，對方才能讀取 |
| 多輪跨工具循環（執行 → 審查 → 修改） | ✅ 需要 | 審查意見與修改歷史需要持久化，pipe 無法跨輪保留 |
| 任務跨多天、多工作階段進行 | ✅ 需要 | 工具重啟後上下文歸零，pipe 內容隨 session 消失 |
| 多人協作（不同人用不同工具） | ✅ 需要 | 共享文件是唯一的狀態同步機制 |
| 快速查詢、一次性問答 | ❌ 不需要 | 任務結束即完成，無需持久化 |

**與 `ai-pair` 的定位比較：**

| 面向 | `multi-tool-coordination` | `ai-pair` |
|---|---|---|
| 類型 | 知識型（人工操作指南） | 執行型（Agent 自動化） |
| 工具範圍 | Claude + Copilot + Codex + Gemini | Claude + GitHub Copilot（GPT-4.1） |
| 操作模式 | 人工切換工具、手動傳遞上下文 | Agent 間透過 SendMessage 自動溝通 |
| 需要 context-sharing | 跨工具協作時通常需要 | 同 session 內不需要；跨 session 重啟時有幫助 |
| 適用情境 | 技術選型、Codex/Gemini 參與的多工具流程 | Claude + GPT 雙重審查的自動化工作流 |

---

---

### 10. context-sharing

| 欄位 | 內容 |
|------|------|
| **名稱** | `context-sharing` |
| **版本** | `1.0.0` |
| **路徑** | `dev/context-sharing 上下文共享Skills/` |
| **授權** | Apache-2.0 |
| **最後更新** | 2025-01-28 |

**描述：**
透過標準化 Markdown 文件系統，在多個 AI 工具之間維持共享上下文，解決 AI 協作中最大的痛點：上下文丟失。

**用途：**
- 跨工具協作（Claude Code + GitHub Copilot + Codex + Gemini）時維持上下文一致
- 追蹤長期專案的任務進度與技術決策
- 跨工作階段保留上下文（今天做到一半，明天繼續）
- 新成員快速了解專案狀態

**核心文件系統：**

| 文件 | 用途 | 更新時機 |
|------|------|---------|
| `CLAUDE.md` | 專案配置、AI 工具分工、工作流程 | 專案初始化、策略調整 |
| `TASKS.md` | 任務追蹤、進度管理 | 新增/開始/完成任務 |
| `ARCHITECTURE.md` | 系統架構、設計文檔 | 架構變更、新增模組 |
| `DECISIONS.md` | 技術決策記錄（ADR 格式） | 技術選型、重大設計決策 |

**協作模式：**
1. Claude → Copilot 協作（規劃 → 實作 → 審查）
2. 團隊協作（多開發者透過文件交接任務）
3. 跨時間維護（跨工作階段延續上下文）

**輔助腳本：**
- `init-project.py` — 一鍵初始化所有標準文件
- `validate-format.py` — 驗證文件格式合規
- `generate-architecture.py` — 從代碼自動生成架構文檔
- `generate-stats.py` — 產生專案進度統計報告

**相關 Skill：** `multi-tool-coordination`

---

### 11. dev-doc-organizer

| 欄位 | 內容 |
|------|------|
| **名稱** | `dev-doc-organizer` |
| **版本** | `1.0.0` |
| **路徑** | `dev/dev-doc-organizer 整理文件/` |
| **最後更新** | 無記錄 |

**描述：**
將原始開發內容結構化為 Agent 可執行、人類可稽核的標準文件，透過三層處理流程消除歧義與格式問題。

**用途：**
- 整理需求文件（PRD）、API 文件、架構文件、Agent 任務文件
- 消除文件中的模糊語言（「一些」、「通常」、「盡快」等）
- 格式化為 Agent 可直接讀取的精確條目
- 驗證必填欄位完整性，輸出驗收報告

**觸發關鍵字：**
「整理需求文件」、「整理 API 文件」、「整理架構文件」、「幫我把這個寫成規格」、「整理成 Agent 可以讀的格式」、「幫我整理這份文件」

**支援的文件類型：**

| 類型 | 識別特徵 |
|------|---------|
| 需求文件（PRD） | 功能描述、使用者故事、驗收條件 |
| API 文件 | endpoint、參數、回傳格式、HTTP method |
| 架構文件（ARCH） | 系統元件、資料流、技術選型、設計決策 |
| Agent 任務文件（TASK） | 任務目標、輸入輸出、執行步驟、完成條件 |

**三層處理流程：**
1. **完整性檢查** — 驗證必填欄位（缺少則標記 ⚠️，不自行填入）
2. **歧義消除** — 掃描模糊數量、模糊條件、邏輯衝突，標記 ⚠️ / ❌
3. **Agent 可讀格式化** — 自然語言 → 條件句/編號步驟，明確 MUST / OPTIONAL 區分

**輸出格式：**
結構化文件 + `📋 驗收報告`（含必填欄位狀態、歧義標記數、衝突項目清單）

### 12. ai-pair

| 欄位 | 內容 |
|------|------|
| **名稱** | `ai-pair` |
| **版本** | `4.3.6` |
| **路徑** | `ai-pair-main-v4.3.6/`（存檔：`ai-pair-main-v4.3.6/`）|
| **最後更新** | 2026-06-26 |

**描述：**
自動化異構 AI 協作團隊 Skill。由 Claude Code 擔任 Team Lead，協調一個創作者（developer/author）與三個不同視角的 reviewer（GPT + Claude + agy/Gemini），形成三重審查工作流程。支援程式碼開發與內容創作兩種情境，並具備分層 review 策略、壓縮通訊協議與快取機制。**v4.3 起 gemini-reviewer 底層由停服的 Gemini CLI 遷移至 Antigravity CLI（`agy`），角色名稱保留。v4.3.5 修正 Copilot CLI v1.0.65 不讀 stdin 的問題（任務內容改以 `-p` 傳遞），並新增 MAI-Code-1-Flash 為 LOW 候選（Phase 2 實測後維持 `gpt-5.4-mini` 主力）。v4.3.6 補環境相容性：無 `TeamCreate`/`TeamDelete`（native Agent Teams 未啟用）時，改用 Team Lead=當前 session + Bash 直呼 CLI + Agent subagent 的等效流程（實測 PASS）。**

**用途：**
- `/ai-pair dev-team [project]` — Level 2 標準 review（預設）
- `/ai-pair dev-team [project] --quick` — Level 1 快速掃描（agy only，~30s）
- `/ai-pair dev-team [project] --deep` — Level 3 深度 review（三 reviewer 並行，~3min）
- `/ai-pair content-team [topic]` — 啟動內容團隊
- `/ai-pair team-stop` — 關閉團隊，清理資源

**前置需求：**
- Claude Code（Team Lead + agent runtime）
- GitHub Copilot CLI（`copilot`）已安裝並完成驗證
- Antigravity CLI（`agy`）已安裝並完成驗證（取代已停服的 Gemini CLI）

**團隊架構：**

| 角色 | 模型 | 負責面向 |
|------|------|---------|
| copilot-developer | Claude Sonnet 4.6（via Copilot CLI） | 程式實作（dispatcher 模式） |
| copilot-reviewer | GPT-5.4 mini（via Copilot CLI） | bugs、安全性、效能、邊界條件 |
| claude-reviewer | Claude subagent | 架構、設計模式、可維護性 |
| gemini-reviewer | agy「Gemini 3.1 Pro (High)」（via Antigravity CLI） | spec compliance、需求對齊、遺漏情境 |

**Review Levels：**

| Level | 指令 | Reviewer 組合 | 適用情境 |
|-------|------|-------------|---------|
| 1 | `--quick` | agy only（Gemini 3.5 Flash (Low)） | typo、i18n、小 UI 調整 |
| 2 | 預設 | Copilot + Claude（並行） | 一般功能、bug fix |
| 3 | `--deep` | 三 reviewer 並行 | 架構變更、高風險模組 |

**核心設計：**
- **Inter-Agent Protocol v1**：agent 間使用壓縮格式通訊（`SRC|severity|file:line|issue|fix` + `VERDICT`），只有最終報告轉成人類可讀
- **diff-only review**：Team Lead 產生一份共用 `REVIEW_FILE`，透過 `REVIEW:{path}` 傳給各 reviewer；reviewer 不讀 source files（實測 tool_uses=1）
- **單任務 dispatch**：每次只 dispatch 一個小型 task context file（~30-50 行）
- **Review 結果快取**：WARN/BLOCK 時寫入 `.ai-pair-cache/review-findings/{task_id}.md`；re-review 自動附加 `Previous findings`
- **Fallback chain**：agy → Pro High → Flash Medium → Flash Low → SKIP；GPT → gpt-5.4-mini → gpt-5-mini → mai-code-1-flash-picker → SKIP；Claude 永遠可用
- **⚠️ Copilot CLI 任務傳遞（v4.3.5）**：v1.0.65 不讀 stdin、無 `-c @file`，任務／審查內容須 `BODY="$(cat $FILE)"` 後嵌入 `-p`；`cat $FILE | copilot` 會讓模型收不到內容（agy stdin pipe 不受影響）

**版本歷程：**

| 版本 | 日期 | 重點 |
|------|------|------|
| v2.3.0 | 2026-03-31 | Team Lead Planning Protocol、Copilot developer timeout 600s |
| v3.0.0 | 2026-04-29 | 三 reviewer 架構（加入 Gemini）、Inter-Agent Protocol v1、分層 review、fallback chain |
| v3.1.0 | 2026-04-30 | reviewer 改為接收 REVIEW:{path}（不讀 source files）、Review 結果快取執行層實作 |
| v4.0.0 | 2026-05-08 | Pilot Suite 模型分配邏輯，developer/reviewer 動態 tier 選擇 |
| v4.1.0 | — | ai-pair-v4-test 測試分支（Phase 1 驗證中） |
| **v4.2.0** | **2026-05-25** | **Content Team 動態模型分配、Level 定義更新、settings.local.json 新模型補充** |
| **v4.2.5** | **2026-06-01** | **Copilot Credit 適應：gpt-4.1→gpt-5.4-mini、Tier 加 Credit 成本欄、claude-haiku-4.5 加入 LOW** |
| **v4.3.0** | **2026-06-22** | **Gemini CLI → Antigravity CLI（`agy`）遷移；模型對應 Flash(Low)/Flash(Medium)/Pro(High)、新增 PREVIEW tier；角色名稱保留；`說明文件.md` 併入 `README.md`** |
| **v4.3.5** | **2026-06-25** | **🔴 修正 Copilot CLI v1.0.65 不讀 stdin（任務內容改 `-p` 傳遞）；新增 MAI-Code-1-Flash（slug `mai-code-1-flash-picker`）為 LOW 候選，Phase 2 實測維持 `gpt-5.4-mini` 主力；Tier 補 claude-sonnet-4.5/gpt-5.4** |
| **v4.3.6** | **2026-06-26** | **環境相容性：無 `TeamCreate`/`TeamDelete`（native Agent Teams 未啟用）時改用 Team Lead=當前 session + Bash 直呼 CLI（developer/copilot/agy）+ Agent subagent（claude-reviewer）等效流程，全程實測 PASS（SSGS-12664 搬移任務驗證 copilot `-p` 嵌入、agy stdin pipe、三 reviewer 壓縮格式皆正常）** |

**與 `multi-tool-coordination` 的定位差異：**

| 面向 | `ai-pair` | `multi-tool-coordination` |
|---|---|---|
| 類型 | 執行型（Agent 自動化） | 知識型（人工操作指南） |
| 工具範圍 | Claude + GPT-4.1 + Gemini 2.5 Flash | Claude + Copilot + Codex + Gemini |
| 操作模式 | Agent 間壓縮格式自動溝通 | 人工切換工具、手動傳遞上下文 |
| 適用情境 | 程式碼/內容的創作 + 三重 AI 審查 | 技術選型、多工具效率分配 |

### 13. figma-to-flutter ⚠️ 已退役歸檔（2026-06-23）

| 欄位 | 內容 |
|------|------|
| **名稱** | `figma-to-flutter` |
| **版本** | `1.0.0`（退役）|
| **路徑** | `dev/figma-to-flutter/`（僅存檔，已從 ~/.claude/skills 移除）|
| **最後更新** | 2026-03-18 |

> **退役原因（2026-06-23）：** 工作流改為 `figma-to-requirements → requirements → 對著 DESIGN.md 實作`。本 skill 的「Figma→Flutter 元件對應表」已併入各專案 DESIGN.md（元件名對齊現行 codebase）；「響應式尺寸規則」已過時（b2b DESIGN.md 慣例改以固定 px 為主，新 UI 不用 `.w/.h/.sp`；但 `flutter_screenutil` 套件與 `ScreenUtilInit` 仍保留供既有部分使用，未移除依賴）。詳見 [16. figma-to-requirements](#16-figma-to-requirements)。

**描述：**
將 Figma 截圖轉換為 Flutter UI 代碼，專為山隆 B2B 智慧平台（B2B Manager）設計，強制遵守專案規範。

**用途：**
- 接收 Figma 截圖 → 分析版面結構 → 確認元件名稱/目錄 → 輸出完整 Flutter 代碼
- 強制套用專案規範：`SLColor`（禁止 hardcode HEX）、`SLText`、`SpacerWidget`、`kAppRadius`
- 依互動性自動選擇 Widget 類型：純顯示 `ConsumerWidget`、有互動 `HookConsumerWidget`
- 響應式尺寸判斷：版面容器/padding/字體 → `.w/.h/.sp`；表格高度/常數/const Widget → 固定 px
- 每次輸出包含：檔案路徑、完整代碼（含 import）、使用方式、注意事項

**觸發關鍵字：**
「截圖轉代碼」、「把這個設計做成 Flutter」、「依照截圖生成 UI」、「Figma 截圖」、「幫我實作這個畫面」、「依照設計稿」

**包含 references：**
- `references/b2b-conventions.md`：色彩系統（含新增規則）、文字樣式、常用元件 API
- `references/component-mapping.md`：Figma UI 元素 → Flutter 元件對應表

**適用專案：** 山隆 B2B Manager（Flutter Web）

---

### 16. figma-to-requirements

| 欄位 | 內容 |
|------|------|
| **名稱** | `figma-to-requirements` |
| **版本** | `1.0.1` |
| **路徑** | `dev/figma-to-requirements/`（備份）；作用中安裝於**全域** `~/.claude/skills/figma-to-requirements/` |
| **最後更新** | 2026-06-23 |

**描述：**
把一組 Figma 設計截圖轉成「精確的 UI 任務需求草稿」，作為 `requirements` 的前處理階段。取代已退役的 figma-to-flutter。

**用途：**
- 讀「截圖所屬 repo 根目錄的 DESIGN.md」（非 CWD），將截圖元素對應到既有設計 token
- 強制三產出：**Token 對應表**、**狀態矩陣**、**待新增 token 清單**（截圖出現但 DESIGN.md 沒有的色 → 標註不 hardcode）
- 邊界：不產 code（實作階段負責）、不做風險分析（requirements 負責），做完交棒 requirements
- 輸出 `docs/shared/<功能>_task.md`，metadata header 與 requirements 對齊
- 通用設計：讀本專案 DESIGN.md，可跨 Flutter 專案（b2b-manager / app01-double 各用各的 token）

**觸發關鍵字：**
「截圖轉需求」、「Figma 轉需求」、「設計稿轉任務」、「把截圖變成需求文件」、「UI 需求分析」、「依設計稿寫需求」

**前置依賴：** 截圖所屬 repo 根目錄需有 `DESIGN.md`（設計系統 SoT）

**完整工作流：** `figma-to-requirements → requirements → Claude 開發/ai-pair（含 review）→ doc-update`

---

### 14. zerospec-skills

| 欄位 | 內容 |
|------|------|
| **名稱** | `zerospec-skills` |
| **版本** | `0.4.3` |
| **路徑** | `dev/zerospec-skills/` |
| **最後更新** | 2026-05-08 |

**描述：**
AI 文件協作系統 ZeroSpec 的 Claude Code Skills 封裝。提供 AGENTS.md、docs/README.md 等 AI 導覽文件的初始化、生成、同步與品質稽核工作流程，並支援 SPEC、ADR、SA 三種 SDD 文件類型的自動生成。

**包含的 Skill 指令：**

| 指令 | 用途 |
|------|------|
| `/zerospec` | 智慧入口：自動偵測專案狀態並執行對應步驟 |
| `/zerospec:scan` | 掃描專案，產出 A/B/C-class 分析報告（不寫檔） |
| `/zerospec:build` | 生成 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`docs/README.md` |
| `/zerospec:spec` | API 新增或行為變更時，生成或更新 SPEC 文件 |
| `/zerospec:adr` | 做出跨模組技術決策時，生成 ADR 文件 |
| `/zerospec:sa` | 需要系統快照時，生成 SA 文件 |
| `/zerospec:update` | 專案演進後，同步更新 AGENTS.md 與 docs/README.md |
| `/zerospec:audit` | 量化評估 AGENTS.md 品質，產出結構化報告（不寫檔） |

**核心設計：**
- 三類資訊分層：A-class（自動提取）、B-class（草稿待確認）、C-class（人工決策）
- Drift Prevention Rules：版本只寫 Major.Minor、不猜測、未有證據標 `[unverified]`
- 跨工具橋接：`CLAUDE.md`（`@AGENTS.md`）、`GEMINI.md`（`@./AGENTS.md`）
- 驗收自我測試：AGENTS.md 必須包含 8–12 題自我測試，涵蓋平台限制、禁止事項、核心元件、構建指令

**附屬文件：**
- `cross-tool-ai-setup.md`：跨工具 AI 協作設定（CLAUDE.md / GEMINI.md / CODEX.md 配置規範）
- `README.md`：使用說明與參考資料

**參考資料：**
- [ZeroSpec 官方部落格](https://coreynote.life/posts/2026/04/zerospec/)
- [ZeroSpec GitHub README（繁體中文）](https://github.com/corey924/ZeroSpec/blob/main/README.zh-TW.md)

---

### 15. ai-pair-v4-test

| 欄位 | 內容 |
|------|------|
| **名稱** | `ai-pair-v4-test` |
| **版本** | `4.1.0` |
| **路徑** | `dev/ai-pair-v4-test/` |
| **最後更新** | 2026-05-14 |

**描述：**
ai-pair v4 的測試分支，在 v3.1.0 架構上套用 Pilot Suite 模型分配邏輯。處於 Phase 1 驗證階段，尚未合入主線 v4.2。

**主要實驗內容：**
- developer 動態模型 tier（FREE / STANDARD / HIGH）
- reviewer 動態模型 tier（各 reviewer 各自升降）
- Level 2 移除 Gemini（保留額度）；Level 1 加入 copilot-reviewer FREE

**v4.1 校正重點（對照 v4）：**
- 移除誤判：Gemini 雙倍 Token 消耗（diff-only 已解決）
- 移除誤判：違反向下委派原則（異構生態不適用）
- 移除 Claude Haiku 4.5 tier（改用 GPT-4.1 FREE）
- 新增缺口：settings.local.json 需補充 v4 新模型

**附屬文件：**
- `重構建議-v4.md`：v4 動機與模型分配設計
- `重構建議-v4.1.md`：v4.1 校正（移除誤判、確認缺口）
- `PHASE1-驗證報告.md`：Phase 1 實機測試紀錄
- `說明文件.md`：v3.1.0 基礎架構說明

**狀態：** 🔬 Phase 1 驗證中，已部分合入正式 ai-pair v4.2

---

## 通用類（general）

### 9. media-processor

| 欄位 | 內容 |
|------|------|
| **名稱** | `media-processor` |
| **版本** | `2.0.0` |
| **路徑** | `general/media-processor/` |
| **授權** | MIT |
| **最後更新** | 2025-12-31 |

**描述：**
本地媒體檔案處理工具包，提供音訊/視訊格式轉換、批次處理、音訊提取、媒體壓縮等功能。

**用途：**
- 音訊格式轉換（WAV / FLAC / M4A → MP3）
- 從視訊提取音訊軌道
- 批次轉換整個資料夾（支援多執行緒）
- 壓縮媒體至指定大小或位元率

**功能腳本清單：**

| 腳本 | 功能 |
|------|------|
| `convert_audio.py` | 單一音訊格式轉換 |
| `extract_audio.py` | 從視訊提取音訊 |
| `batch_convert.py` | 批次轉換（多執行緒） |
| `compress_media.py` | 媒體壓縮 |

**系統需求：** FFmpeg、Python（pillow、requests）

> ⚠️ 此 Skill 僅處理**本地**媒體檔案。網路下載（YouTube、HLS）請改用 media-downloader MCP 工具。

**版本歷程：**
- `v2.0.0`（2025-12-31）：從 MCP 工具遷移至 Skills 腳本，MCP 啟動時間減少 50%
- `v1.0.0`（2025-12-10）：初始版本，13 個 MCP 工具

---

### 10. sign-off-generator

| 欄位 | 內容 |
|------|------|
| **名稱** | `sign-off-generator` |
| **版本** | `1.0.0` |
| **路徑** | `general/sign-off-generator-skill/` |
| **最後更新** | 2026-01-06 |

**描述：**
內部簽呈產生器，依照標準格式產生公司內部簽核文件。

**用途：**
- 產生 AWS 權限申請簽呈（AWS Software Developer、PMS Access）
- 支援繁體中文輸出，可選英中雙語格式
- 自動套用標準簽呈結構（主旨、說明、申請人、員編、擬辦）

**觸發時機：**
使用者要求「內部簽呈」、「公司表單」、「權限申請文件」

**支援的申請類型：**
- AWS Software Developer 權限
- PMS 專案 + AWS 服務權限（支援自訂專案與服務清單）

---

### 11. document-translator

| 欄位 | 內容 |
|------|------|
| **名稱** | `document-translator` |
| **版本** | `1.0.0` |
| **路徑** | `general/document-translator/` |
| **最後更新** | 無記錄 |

**描述：**
技術文件翻譯系統，採兩階段翻譯流程：Google Translate 初稿 → 智慧校對潤稿，輸出英文轉繁體中文文件。

**用途：**
- 翻譯 `docs/en/` 下的 Markdown 文件
- 批次翻譯整個資料夾
- 管理術語表（glossary.json）
- 選擇校對後端

**翻譯流程：**
```
docs/en/*.md → Google Translate → 校對 → docs/zh-TW/*.md
```

**支援的校對後端：**

| 後端 | 旗標 | 適用場景 |
|------|------|---------|
| 自動偵測 | （預設） | 一般使用 |
| ChatGPT | `--proofreader=chatgpt` | 免費、自動化 |
| Claude Desktop | `--proofreader=desktop` | 最高品質 |
| Claude CLI | `--proofreader=cli` | CI/CD 管道 |
| 手動 | `--proofreader=manual` | 完整控制 |

**觸發關鍵字：** "translate"、"翻譯"、"translation"、提及 `docs/en/` 下的檔案

---

### 12. translategemma-translator

| 欄位 | 內容 |
|------|------|
| **名稱** | `translategemma-translator` |
| **版本** | `1.1.0` |
| **路徑** | `general/translategemma-translator/` |
| **最後更新** | 無記錄 |

**描述：**
使用 Google 開源的 `google/translategemma-4b-it` LLM 模型進行英文至繁體中文（台灣用語）翻譯，針對 Markdown 格式優化。

**用途：**
- 單一 Markdown 檔案翻譯
- 批次翻譯多個文件
- 保留程式碼區塊、連結、Markdown 格式
- 使用台灣慣用詞彙（資料、軟體、硬體等）

**執行方式：**
```bash
./translategemma-translator/scripts/translate.sh --input FILE --token HF_TOKEN
```

**前置需求：**
- Hugging Face Access Token（模型為受控存取）
- 支援裝置：CPU、CUDA、MPS（macOS Metal）

**版本歷程：**
- `v1.1.0`：新增 `translate.sh` 自動化腳本，自動建立 venv 環境
- `v1.0.0`：初始版本，基本翻譯功能

> 💡 與 `document-translator` 的差異：此 Skill 使用本地 LLM 模型推論，不依賴 Google Translate API。

---

### 13. discussion-organizer

| 欄位 | 內容 |
|------|------|
| **名稱** | `discussion-organizer` |
| **版本** | `1.0.0` |
| **路徑** | `general/discussion-organizer整理學習筆記Skills/` |
| **最後更新** | 2026-03-12 |

**描述：**
將筆記、文章、逐字稿、字幕、個人想法透過雙軸偵測＋四層判斷流程，轉化為結構化知識文件。支援多種輸出框架（TBRC、SCQA、素材庫、情境腳本）。

**用途：**
- 整理學習筆記、技術文章（→ TBRC）
- 結構化問題分析、Bug 記錄、案例（→ SCQA）
- 整理直播逐字稿、字幕、高密度口語內容（→ 素材庫）
- 建立角色扮演訓練素材、情境對話（→ 情境腳本）
- 消除情緒性填充詞，統一術語，口語轉書面語

**觸發關鍵字：**
「整理」、「結構化」、「用 TBRC/SCQA 整理」、「幫我整理這篇文章/筆記/想法/逐字稿/字幕」、「建立素材庫」、「整理成腳本」

**雙軸偵測：**

**軸一：輸入類型（決定前處理方式）**

| 類型 | 識別特徵 | 前處理 |
|------|---------|--------|
| 直播/逐字稿 | 大量口語、重複、說話者標記、無段落 | 逐字稿前處理（去噪/去重） |
| 字幕檔 | 時間戳（00:01:23）、短句斷行 | 剔除時間戳、合併斷句 |
| 網頁文章 | 導覽列文字、廣告語、非正文區塊 | 識別正文邊界、剔除非正文 |
| 純文字筆記 | 已相對乾淨，有段落或條列 | 直接進入四層判斷 |

**軸二：輸出框架（決定結構）**

| 框架 | 最適合場景 |
|------|-----------|
| TBRC | 學習筆記、技術文章、有明確論點的內容 |
| SCQA | 問題分析、Bug記錄、案例、有衝突的敘事 |
| 素材庫 | 直播/逐字稿、內容密度高、不需套框架 |
| 情境腳本 | 角色扮演訓練素材、情境對話、教學演示 |

**四層判斷流程：**
1. **價值評分** — 5 星制篩選，低於 ⭐⭐ 直接丟棄
2. **可信度標記** — ✅ 官方來源 / ⚠️ 合理推論 / ❌ 矛盾事實
3. **提取粒度** — 🔥 直接引用 / 📝 改寫 / 🗂️ 僅標記主題
4. **語調正規化** — 口語 → 書面語，統一術語，去除情緒填充詞

**附屬檔案：**
- `sop-complete.md` — 逐字稿前處理、各框架詳細規則
- `templates.md` — TBRC / SCQA / 素材庫 / 情境腳本輸出模板

**輸出格式：**
框架結構內容 + `📊 整理摘要`（輸入類型、輸出框架、處理/保留/丟棄條數、待驗證數、建議下一步）

---

### 14. cross-platform-archive-agent

| 欄位 | 內容 |
|------|------|
| **名稱** | `cross-platform-archive-agent` |
| **版本** | `1.0.0` |
| **路徑** | `general/cross-platform-archive-agent/` |
| **最後更新** | 2026-03-03 |

**描述：**
根據目標解壓平台自動產生最佳壓縮指令，並智能排除跨平台垃圾檔（如 `.DS_Store`、`Thumbs.db`）。

**用途：**
- 壓縮/打包檔案或資料夾給不同平台使用
- 自動選擇格式（Windows → `.zip`，macOS/Linux → `.tar.gz`）
- 依目標平台組合排除規則，避免跨平台垃圾檔污染壓縮包
- 支援 dry-run 模式（僅輸出排除清單，不實際壓縮）

**觸發關鍵字：** 「壓縮」、「打包」、「archive」、「zip」、「tar」

**壓縮格式對照：**

| 目標平台 | 格式 | 工具 |
|---------|------|------|
| Windows | `.zip` | `zip` |
| macOS | `.tar.gz` | `tar` |
| Linux | `.tar.gz` | `tar` |

**排除規則邏輯：**
```
排除項目 = 通用規則（.git、.env）+ 所有「非目標平台」的 OS 垃圾檔
```

通用排除：`.git`、`.gitignore`、`.env`
macOS 專屬：`.DS_Store`、`__MACOSX`、`._*`
Windows 專屬：`Thumbs.db`、`Desktop.ini`
Linux 專屬：`.directory`、`.Trash-*`

**六步工作流程：**
解析輸入 → 確認 Build Platform → 決定格式 → 建立排除清單 → 套用語法 → 輸出指令

---

## 知識管理類（pkm）

### 1. knowledge-organizer

| 欄位 | 內容 |
|------|------|
| **名稱** | `knowledge-organizer` |
| **版本** | `1.1.0` |
| **路徑** | `pkm/knowledge-organizer/` |
| **最後更新** | 2026-05-14 |

**描述：**
使用 TBRC 四層框架處理 `raw/` 中的原始素材，產出結構化 wiki 條目。封裝「整理一篇筆記」的完整判斷邏輯。支援 `.pdf` 輸入（≤10 頁讀全文，>10 頁節錄首尾）。

**用途：**
- 處理 `raw/` 中的單篇或少量未整理素材
- 依資產化價值公式（頻率 × 耗時 × 複雜度）決定處理深度
- 自動分配 tag、判斷歸屬資料夾、建立 wikilink、更新 INDEX.md

**觸發方式：**
`knowledge-organizer`、`整理筆記`、`處理raw`、`process raw`、`organize notes`

---

### 2. daily-brief-generator

| 欄位 | 內容 |
|------|------|
| **名稱** | `daily-brief-generator` |
| **版本** | `1.2.0` |
| **路徑** | `pkm/daily-brief-generator/` |
| **最後更新** | 2026-05-14 |

**描述：**
掃描整個 Obsidian Vault，產出每日結構化簡報。涵蓋 raw/ 積壓狀況（.md/.pdf 分開計算）、wiki 最近更新、任務狀態、孤立筆記、Vault 統計。「今日建議行動」改用 SCQA 框架結構化輸出（S 現況 / C 衝突 / Q 核心問題 / A 行動）。

**用途：**
- 每日快速掌握知識庫狀態
- 提醒待處理積壓素材
- 追蹤 projects/ 任務進度

**觸發方式：**
`daily-brief`、`每日摘要`、`今日簡報`、`brief`、`知識庫狀況`

---

### 3. wiki-health-check

| 欄位 | 內容 |
|------|------|
| **名稱** | `wiki-health-check` |
| **版本** | `1.3.0` |
| **路徑** | `pkm/wiki-health-check/` |
| **最後更新** | 2026-05-14 |

**描述：**
每月知識庫健康檢查。掃描 wiki/ 找出六類品質問題：矛盾偵測、缺乏來源、知識缺口、連結品質（孤立/懸空）、過時內容、未處理素材（wiki/raw source URL cross-reference）。報告末尾附 5A+ 階段評估（當前階段 + 理由 + 下一步建議）。

**用途：**
- 每月一次維護執行
- wiki 超過 30 篇後開始定期使用
- 產出含健康指數評分的報告

**觸發方式：**
`wiki-health-check`、`健康檢查`、`health check`、`知識庫健檢`、`monthly review`

---

### 4. raw-pipeline

| 欄位 | 內容 |
|------|------|
| **名稱** | `raw-pipeline` |
| **版本** | `1.1.0` |
| **路徑** | `pkm/raw-pipeline/` |
| **最後更新** | 2026-05-14 |

**描述：**
軟編排型 Skill，調度三個子 Agent 協作批次處理 `raw/` 素材：Agent A 摘要、Agent B 分類打標、Agent C 建立 wiki 條目與更新索引。支援 7 種格式（.md .txt .html .pdf .png .jpg .jpeg .webp .gif .srt .vtt .ipynb .csv）。適合 raw/ 積壓 10 篇以上的場景。

**用途：**
- raw/ 積壓 10 篇以上時的批次處理
- 單篇處理請用 knowledge-organizer

**觸發方式：**
`raw-pipeline`、`批次處理`、`batch process`、`pipeline`、`自動整理流程`

---

### 5. knowledge-synthesizer

| 欄位 | 內容 |
|------|------|
| **名稱** | `knowledge-synthesizer` |
| **版本** | `1.0.0` |
| **路徑** | `pkm/knowledge-synthesizer/` |
| **最後更新** | 2026-05-13 |

**描述：**
把同類型的多篇 wiki 條目提煉成一篇「精粹條目」。使用 CAVE 框架（Consensus 共識 / Angles 獨特視角 / Voids 知識缺口 / Essence 精粹論點）整合跨篇洞察，去掉重複、保留密度、找出張力。

**用途：**
- 同主題累積 3 篇以上 wiki 條目時使用
- 建立高密度「精粹條目」，作為該主題的單一參考點

**觸發方式：**
`knowledge-synthesizer`、`精粹`、`synthesize`、`distill`、`知識精粹`、`合併觀點`、`跨篇整合`

---

### 6. alignment-check

| 欄位 | 內容 |
|------|------|
| **名稱** | `alignment-check` |
| **版本** | `1.0.0` |
| **路徑** | `pkm/alignment-check/` |
| **最後更新** | 2026-05-22 |

**描述：**
Wiki 內容歸屬對齊檢查。掃描所有 wiki 條目，逐一判斷每個「補充資料」段落的主題是否與該條目的 T（核心論點）一致。找出放錯位置的段落，並建議正確歸屬（搬至哪個現有條目或是否應建立新條目）。

**用途：**
- 定期維護 wiki 內容歸屬正確性
- 找出隨時間累積的「放錯位置」段落
- 作為 wiki-health-check 後的補充清理動作

**觸發方式：**
`alignment-check`、`對齊檢查`、`内容歸屬`、`check alignment`

---

### 7. knowledge-elevation

| 欄位 | 內容 |
|------|------|
| **名稱** | `knowledge-elevation` |
| **版本** | `1.1.0` |
| **路徑** | `pkm/knowledge-elevation/` |
| **最後更新** | 2026-05-22 |

**描述：**
三層知識昇華流程：自動模式偵測 / E 層加深 / 跨主題 meta-synthesis → wiki/concepts/。適合在 knowledge-synthesizer 之後進一步提煉跨主題洞察，將散落的精粹條目昇華為概念框架。

**用途：**
- 單篇精粹條目 E 層加深（提升精粹論點密度）
- 跨多篇精粹條目的 meta-synthesis（建立跨主題概念框架）
- 輸出至 `wiki/concepts/`

**觸發方式：**
`knowledge-elevation`、`昇華`、`meta-synthesis`、`概念框架`、`elevation`

---

### 8. obsidian-second-brain

| 欄位 | 內容 |
|------|------|
| **名稱** | `obsidian-second-brain` |
| **版本** | — |
| **路徑** | `pkm/obsidian-second-brain/` |
| **最後更新** | — |

**描述：**
將任何 Obsidian Vault 作為持續自我改寫的第二大腦運作（Karpathy LLM Wiki 模式的進化版：素材重寫現有頁面、矛盾自動調和、排程 Agent 在背景維護 Vault）。

**用途：**
- 建立自動化知識庫維護工作流
- 讀取、寫入、更新、搜尋 Obsidian 筆記
- 跨 session 累積知識

**觸發方式：**
`obsidian-second-brain`、直接請求管理 Obsidian 筆記

---

### 9. scientific-brainstorming

| 欄位 | 內容 |
|------|------|
| **名稱** | `scientific-brainstorming` |
| **版本** | — |
| **路徑** | `pkm/scientific-brainstorming/` |
| **最後更新** | — |

**描述：**
創意研究構想與探索。用於開放式腦力激盪、跨學科連結探索、挑戰假設或找出研究缺口。適合尚無具體觀察資料的早期研究規劃階段。

**用途：**
- 開放式研究腦力激盪
- 跨領域概念連結
- 研究缺口識別
- 假設初步生成（有資料後改用 hypothesis-generation）

**觸發方式：**
`scientific-brainstorming`、`brainstorm`、「研究構想」、「跨學科探索」

---

## 系統內建 Skill（Claude Code 提供）

以下為 Claude Code 平台提供的內建 Skill，非本地自訂版本：

| 名稱 | 描述 | 用途 |
|------|------|------|
| `update-config` | Claude Code 設定配置 | 修改 `settings.json`（hooks、permissions、env vars），自動化行為設定 |
| `keybindings-help` | 鍵盤快捷鍵客製化 | 設定 `~/.claude/keybindings.json` |
| ~~`simplify`~~ | ~~代碼品質簡化~~ | ~~已在 v2.1.147 改名為 `code-review`~~ |
| `loop` | 週期性任務 | 設定定時重複執行的任務（如 `/loop 5m /foo`） |
| `claude-api` | Claude API 應用 | 使用 Anthropic SDK 建構 AI 應用 |
| `code-review`（內建） | PR correctness bug review | v2.1.147 由 `/simplify` 改名；讀 CLAUDE.md，不讀 REVIEW.md；本地 diff review + effort level + `--comment` |
| `cross-platform-archive-agent` | 跨平台壓縮工具 | 本地自訂版，見上方通用類 #14 |
| `project-documentation`（內建） | 專案文件產出 | 同本地 v2.0.0 版本（見上方） |
| `theme-factory` | 樣式主題工具 | 套用 10 種預設主題至 Artifact |
| `webapp-testing` | Web 應用測試 | Playwright 測試本地 Web 應用 |
| `mcp-builder` | MCP Server 建構指南 | 建立 MCP 伺服器整合外部 API |
| `canvas-design` | 視覺設計 | 產生 PNG/PDF 視覺藝術作品 |
| `skill-creator` | Skill 創建指南 | 建立或更新 Claude Code Skill |
| `pdf` | PDF 工具包 | 提取、建立、合併、拆分 PDF |
| `frontend-design` | 前端設計 | 產生高品質 Web UI 元件 |
| `xlsx` | 試算表工具 | 建立、編輯、分析試算表 |
| `internal-comms` | 內部溝通文件 | 撰寫公司內部報告、更新、FAQ |
| `brand-guidelines` | 品牌規範 | 套用 Anthropic 品牌色彩與排版 |
| `doc-coauthoring` | 文件共同撰寫 | 結構化協作文件撰寫流程 |
| `algorithmic-art` | 演算法藝術 | 使用 p5.js 建立生成藝術作品 |
| `pptx` | 簡報工具 | 建立、編輯、分析 .pptx 簡報 |
| `web-artifacts-builder` | 複雜 Web Artifact | 多元件 React/Tailwind/shadcn/ui 應用 |
| `slack-gif-creator` | Slack GIF 製作 | 產生適合 Slack 的動態 GIF |
| `docx` | Word 文件工具 | 建立、編輯 .docx，支援追蹤修訂 |

---

## 版本彙整表

| Skill | 版本 | 最後更新 | 類別 | 備註 |
|-------|------|---------|------|------|
| code-review v1 | 1.0.0 | 無記錄 | dev | Flutter-only |
| code-review v2 | 1.1.0 | 2026-01-08 | dev | 多技術棧 |
| **stack-review (原 code-review v3)** | **1.1.0** | **2026-05-25** | **dev** | **重命名避免內建衝突（`dev/stack-review/`）；輕量替代，適合單檔小改動** |
| **requirements** | **1.1.0** | **2026-03-18** | **dev** | **新增：同名文件檢查、已完成重開流程、Step 8 CHANGELOG** |
| **doc-update** | **1.1.0** | **2026-03-18** | **dev** | **新增：支援「🔄 進行中」狀態** |
| flutter-b2b-documentation | 1.0.0 | 無記錄 | dev | 已由 project-documentation 取代 |
| **project-documentation** | **2.0.0** | **2026-04-28** | **dev** | **Spring Boot 完整支援；新增 Bug 修復紀錄、Widget 元件文件；kebab-case 命名；frontmatter 規範** |
| doc-generator | 1.0.0 | 無記錄 | dev | |
| multi-tool-coordination | 1.0.0 | 無記錄 | dev | 人工操作指南；執行型版本見 ai-pair |
| context-sharing | 1.0.0 | 2025-01-28 | dev | |
| dev-doc-organizer | 1.0.0 | 無記錄 | dev | |
| **ai-pair** | **4.3.6** | **2026-06-26** | **dev** | **環境相容性：無 `TeamCreate`/`TeamDelete` 時改用 Bash 直呼 CLI + Agent subagent 等效流程（實測 PASS）；承 v4.3.5 Copilot `-p` 傳遞修正（存檔：`ai-pair-main-v4.3.6/`）** |
| **ai-pair-v4-test** | **4.1.0** | **2026-05-14** | **dev** | **v4 測試分支（Phase 1 驗證中）；v4.1 校正誤判 2 項、新增缺口 4 項** |
| **figma-to-flutter** | **1.0.0** | **2026-03-18** | **dev** | **Figma 截圖 → Flutter UI 代碼（B2B 專屬，路徑：`dev/figma-to-flutter/`）** |
| media-processor | 2.0.0 | 2025-12-31 | general | |
| sign-off-generator | 1.0.0 | 2026-01-06 | general | |
| document-translator | 1.0.0 | 無記錄 | general | |
| translategemma-translator | 1.1.0 | 無記錄 | general | |
| discussion-organizer | 1.0.0 | 2026-03-12 | general | |
| cross-platform-archive-agent | 1.0.0 | 2026-03-03 | general | |
| **knowledge-organizer** | **1.1.0** | **2026-05-14** | **pkm** | **TBRC 四層框架、資產化價值公式；新增 PDF 支援** |
| **daily-brief-generator** | **1.2.0** | **2026-05-14** | **pkm** | **五區塊每日簡報；今日建議行動改用 SCQA 框架** |
| **wiki-health-check** | **1.3.0** | **2026-05-14** | **pkm** | **六項健康檢查；新增 5A+ 階段評估區塊** |
| **raw-pipeline** | **1.3.0** | **2026-05-22** | **pkm** | **三 Agent 軟編排；支援 12 種格式含 PDF/圖片** |
| **knowledge-synthesizer** | **1.0.0** | **2026-05-13** | **pkm** | **CAVE 框架精粹（共識/視角/缺口/精華）；同主題 3 篇以上使用** |
| **alignment-check** | **1.0.0** | **2026-05-22** | **pkm** | **wiki 補充資料段落歸屬對齊檢查；找出放錯位置的內容並建議搬移** |
| **knowledge-elevation** | **1.1.0** | **2026-05-22** | **pkm** | **三層昇華：E 層加深 / meta-synthesis → wiki/concepts/** |
| obsidian-second-brain | — | — | **pkm** | Karpathy LLM Wiki 進化版；自動維護 Vault |
| scientific-brainstorming | — | — | **pkm** | 開放式研究腦力激盪、跨學科連結探索 |
| **zerospec-skills** | **0.4.3** | **2026-05-08** | **dev** | **ZeroSpec AI 文件協作系統；含 8 個指令（scan/build/spec/adr/sa/update/audit/智慧入口）；新增驗收自我測試規範** |
