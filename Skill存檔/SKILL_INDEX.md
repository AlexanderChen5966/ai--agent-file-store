# Skill 索引總覽

> 整理日期：2026-05-25（最後更新：2026-11-13 — 流程 v5（借 slc marketplace 的做法）：requirements v1.8.0、stack-review v1.10.0 改薄入口（細節移到 references/），doc-update v1.4.0 加提議編號、記憶附查證、單向門判準；新增設計類 3 個：anti-ai-look v0.1.0、design-review v0.1.0、design-md-init v0.1.0；個人 plugin 新增 design／research／teaching，marketplace 搬到 `~/.agents/marketplace/`，見「作用中安裝位置」；2026-11-11 — plugin 補測後修正：stack-review v1.9.0 加 React web 清單、requirements v1.7.3、doc-update v1.3.1、figma-to-requirements v1.0.2、project-documentation v2.2.2、tdd 本機修改、新增 flutter-ui-compare v0.1.1；Claude Code 改由個人 plugin 載入，見「作用中安裝位置」；2026-11-11 — stack-review v1.8.0 加 iOS 與 React Native 清單；2026-11-11 — 四個 v3 機制加退場條件：doc-update v1.3.0 Step 8 結案補追蹤、doubt-check v0.3.2；2026-11-11 — doubt-check v0.3.1 加退場條件；2026-11-11 — 共用元件／全站樣式納入 doubt-check：requirements v1.7.2、doubt-check v0.3.0；2026-11-11 — source-driven 補「官方文件不全以 lock 版本型別為準」：requirements v1.7.1、stack-review v1.7.1；2026-11-11 — doubt-check 改由任務文件標記觸發：requirements v1.7.0、stack-review v1.7.0、doubt-check v0.2.0；2026-11-09 — 借來的做法整合（流程 v3）：requirements v1.6.0、stack-review v1.6.0、doc-update v1.2.0、新增 doubt-check v0.1.0；2026-11-09 — Matt Pocock 截長補短：新增 mattpocock-skills（7 個共用）；requirements v1.5.0 需求模糊叫 grilling；stack-review v1.5.0 加 spec 審查；2026-10-21 — point-reading-diy v0.4.0：打包流程完成、Dear Zoo 實測成功；multiagent-handoff v0.6.0 加「建議記憶」（銜接長期記憶 `~/.agents/memory/`）；handoff 改名為 multiagent-handoff v0.5.0；2026-10-20 新增 handoff v0.4.1：跨 AI agent 專案接力；7 個自訂 skill 改為跨工具共用安裝於 `~/.agents/skills/`，ai-pair 留在 Claude，見「作用中安裝位置」）
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
  - [b2b-manager-onboarding](#17-b2b-manager-onboarding)
  - [sanlong-pay-onboarding](#18-sanlong-pay-onboarding)
  - [multiagent-handoff](#19-multiagent-handoff)
  - [mattpocock-skills（外部）](#20-mattpocock-skills外部)
  - [doubt-check](#21-doubt-check)
  - [flutter-ui-compare](#22-flutter-ui-compare)
- [通用類（general）](#通用類general)
  - [media-processor](#9-media-processor)
  - [sign-off-generator](#10-sign-off-generator)
  - [document-translator](#11-document-translator)
  - [translategemma-translator](#12-translategemma-translator)
  - [discussion-organizer](#13-discussion-organizer)
  - [cross-platform-archive-agent](#14-cross-platform-archive-agent)
  - [point-reading-diy ✅ 可用（測試版）](#15-point-reading-diy--可用測試版)
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
- [設計類（design）](#設計類design)
  - [anti-ai-look](#1-anti-ai-look)
  - [design-review](#2-design-review)
  - [design-md-init](#3-design-md-init)
- [作用中安裝位置（2026-10-20 起）](#作用中安裝位置2026-10-20-起)
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
| **版本** | `1.10.0` |
| **路徑** | `dev/stack-review/` |
| **最後更新** | 2026-11-13（v1.10.0 SKILL.md 改薄入口：457→257 行，reviewer 呼叫範本、spec 提示、摘要格式、技術棧範例移到 `references/`）；2026-11-11（v1.9.0 加 React web 清單 `react-web.md`、子資料夾技術棧偵測、註明 plugin 版 agent 名稱 `dev:code-reviewer`；v1.8.0 加 iOS 與 React Native 清單；v1.7.1 common.md 框架出處：文件矛盾時要求 node_modules 檔案行號；v1.7.0 spec 審查檢查 doubt-check 紀錄；v1.6.0 變更範圍與框架出處檢查、常見藉口表；v1.5.0 加 spec 審查；v1.3.0 Step 1 fetch 前置；v1.4.0 common.md 補跨服務契約檢查）|

**新增功能（v1.10.0，2026-11-13）：薄入口**

- 新增 `references/code-reviewer-call.md`、`spec-review-prompt.md`、`summary-format.md`、`stack-notes.md`；SKILL.md 保留各步驟要做什麼與必填欄位

> 🔎 **起因**：同 requirements v1.8.0（slc 借鑒 #3）。

> 📌 作用中本體 `~/.agents/skills/stack-review/` 的檔頭先前一直停在 `1.1.0`（v1.3.0／v1.4.0 內容都在，只是沒改檔頭），2026-11-09 直接改為 `1.5.0`。

> 📌 **版本號說明**：本條目原本檔頭寫 `1.1.0`，但下方功能段與其他章節的交叉引用（第 166、199 行）
> 都已寫 `v1.2.0`（指 Step 7）——存檔原本即存在此不一致。故本次修訂編為 **1.3.0**，
> 避免與既有的 v1.2.0 重號。

**描述：**
在 v2 多技術棧基礎上，新增 Step 7：review 通過後自動檢查 `docs/shared/` 是否有「待實作」任務文件，有則提示執行 `/doc-update`，形成完整的開發工作流程閉環。

> ⚠️ **2026-05-25 重命名**：因 Claude Code v2.1.147 將內建 `/simplify` 改名為 `/code-review`，造成同名衝突，故將此自訂 skill 重命名為 `stack-review`。觸發指令改為 `/stack-review`。

> 💡 **定位說明（2026-05-25）**：主線工作流已改為 `requirements → ai-pair → doc-update`，ai-pair 的三個 reviewer 已覆蓋正式 review 需求。`stack-review` 定位為**輕量替代**，適合小改動（單檔 bug fix、typo、i18n）不值得啟動 ai-pair 的情境。

**新增功能（v1.2.0）：**
- Step 7：Overall Status ✅ Approved 時，自動掃描 `docs/shared/*.md`
- 若有「待實作」文件 → 提示 `💡 建議執行 /doc-update 將任務文件標記為已完成`
- 若無對應文件或目錄不存在 → 略過
- Status ⚠️ / ❌ 時不提示（仍有問題未解決）

**新增功能（v1.3.0，2026-07-29）：**

Step 1 由單一步驟拆成 1a / 1b，補上**建立正確 review 基準**的前置要求：

- **1a. 必須先 `git fetch origin`**，並用 `git log --oneline HEAD..origin/main` 確認分支是否落後
- **diff 基準改用遠端 ref**：`git diff origin/main...HEAD`，❌ 不可用本地 `main`（可能過期數週）
- **分支落後時 → 先合併再 review**：否則 review 結論描述的是合併後不存在的狀態，且事後發現衝突還得重跑一輪
- **1b.** 明確區分「僅未 commit 變更」與「整分支 vs 目標分支」；MR review 幾乎都是後者
- 產生檔（`*.g.dart`、`lib/generated/**`）、lockfile、vendored 目錄一律排除在 findings 之外

> 🔎 **觸發此次修訂的實際事故（2026-07-29，b2b-manager）**：以 `git diff main...HEAD` 執行 review，
> 而本地 `main` 已落後 **7 週**。一個上游 **13 天前就已合併**的任務（SSGS-12729）在分支上被重複實作，
> review 乾淨通過、無任何警示，重複問題直到開 MR 時才以**合併衝突**的形式浮現。
> 教訓：**基準過期會讓整份 review 失去意義**——不只漏看上游已完成的工作，連「這是新檔案」之類的判斷都可能是錯的。

**新增功能（v1.4.0，2026-07-29）：**

`references/common.md` 於「可維護性」前新增一節 **「跨服務契約（enum / DTO）」**，適用前後端分離／多 repo 專案。
diff 動到「會從 API 回應解析的 enum 或 DTO 欄位」時檢查：

- enum 常數值是否與**後端原始碼**逐字一致（❌ 不可只看 API 文件——文件常落後或誤植）
- 解析是 **fail-hard 還是 fail-soft**：fail-hard（`$enumDecode`、非 nullable）遇未知值會拋錯，
  而 `fromJson` 是整批解析 → **一筆未知值會讓整個列表失敗、整頁空白**
- fail-hard 是否有**契約測試**鎖住值清單
- 是否考慮 `unknownEnumValue` fallback；若採用，未知值是否記 log（靜默 fallback 會把問題藏起來）
- 該 enum 的 `values` 是否為 UI 下拉選項來源（若是，`UNKNOWN` 會出現在使用者可見選單，需過濾）

> ⚠️ **同時寫明 review 的能力邊界**：此清單只攔得住「本次 diff 新增或修改」的 enum。
> 最常見的失效模式是「**後端新增值、前端零改動**」——那種情況前端沒有任何 diff，
> **code review 不可能發現**，只能靠契約測試或 fail-soft 解析。
> 故發現 fail-hard 時應直接建議加契約測試，而非只確認「這次改對了」。

> 🔎 **觸發此次修訂的實際事故（2026-07-29，b2b-manager）**：後端為報表排程稽核新增
> `EntityType.REPORT_SCHEDULE`，前端 enum 未同步，`$enumDecode` 拋錯導致
> **操作紀錄頁完全空白**（30 筆中 28 筆是新值）。當時同時查出前端還缺 4 個同類值，
> 且全專案有 **16 個 enum** 處於相同無防護狀態。
> ⚠️ 注意：**這次事故本身 review 抓不到**（前端零 diff），本節的價值在於**防止新增曝險**，
> 而非修復既有漂移。

**新增功能（v1.5.0，2026-11-09）：Step 4b 對照 spec 審查**（吸收 Matt Pocock `matt-code-review` 的 Spec 軸）

- 有 `docs/shared/` 任務文件時，與 code-reviewer **同一則訊息平行派** spec subagent（general-purpose）
- 找任務文件順序：使用者給的路徑 → `**分支編號：**` 對到分支／commit 的 Jira key → 狀態「進行中／待實作」且 `**影響路徑：**` 重疊；多份或找不到就問，使用者說沒有就跳過並在摘要註明
- spec subagent 只看四件事：漏做／部分、多做（scope creep）、看似做了但行為不對、後端依賴／跨服務契約是否照文件處理；每項引任務文件原句＋ file:line
- 摘要新增「Spec Check」一節，**不併入 🔴/🟡/🟢、不跨軸重排**（一軸過、另一軸不過時才看得出來）
- 沒有 subagent 的 agent：先做完規範審查再做 spec 審查，兩份筆記分開

> 🔎 **起因**：開發流程與 Matt Pocock 截長補短（桌面〈開發流程升級_2026-11-09/開發流程與MattPocock截長補短.md〉5.2）——原本 stack-review 只問「寫得好不好」，不問「是不是任務要的」。

**新增功能（v1.8.0，2026-11-11）：iOS 與 React Native 清單**

- 新增 `references/ios.md`（Swift、Objective-C；SwiftUI 與 UIKit）：循環引用、Swift Concurrency、狀態擁有者、Keychain、權限用途說明、Privacy Manifest 等 14 節
- 新增 `references/react-native.md`（含 Expo）：Hooks 與清理、store selector、導覽、列表效能、安全儲存、兩平台權限、OTA 更新與原生變更等 13 節
- SKILL.md Step 2 加兩種偵測條件，並註明**先判斷跨平台**：Flutter、React Native 專案內的 `android/`、`ios/` 不算原生專案，diff 動到原生程式才加看 `android.md`／`ios.md`
- Step 3 加兩種技術棧的審查重點
- ⚠️ 兩份清單依通用做法撰寫，還沒在實際專案跑過

> 🔎 **起因**：角色切換的 App 工程師要能處理原生 iOS 與 React Native（`tms-driver-app`）；2026-11-11 plugin 試裝時 stack-review 對 React 回報沒有專用清單。見桌面〈開發流程升級_2026-11-09/角色分類草案.md〉第 7 節第 12、13 項。

**新增功能（v1.7.0，2026-11-11）：檢查 doubt-check 紀錄**

- Step 4b spec subagent 加 (e)：任務文件標了「需 doubt-check：是」的任務，「實作注意事項」有沒有複查結果；沒有、或程式和複查的版本不同就回報
- 摘要的 Spec Check 加「Doubt-check」一行

> 🔎 **起因**：2026-11-10 操作紀錄 02 實測，agent 沒有自己觸發 doubt-check（先寫後審）。見桌面〈開發流程升級_2026-11-09/v3實測報告_02-log-drawer.md〉第 6 節。

**新增功能（v1.6.0，2026-11-09）：借來的做法整合**

- `references/common.md`「8. 變更政策 → 最小化變更」加**行層級**檢查（觀念來自 Karpathy 準則「外科式修改」，自己的寫法）：逐個 hunk 問「為了哪條需求」，順手改的格式／註解／改名列 🟡；自己造成的孤兒沒清列 🟡；刪了原有死碼列 🟡（建議還原、改成回報）
- `common.md` 新增「框架與套件用法出處」（觀念來自 Addy source-driven）：新框架用法要有官方文件出處或標未驗證；用到已棄用 API 列 🔴
- SKILL.md 新增「Common Excuses（常見藉口）」表（格式借 Addy 的反合理化表，內容是自己的事故，例：本地 main 落後 7 週）
- Integration 加 doubt-check 的分工說明

> 🔎 **起因**：桌面〈開發流程升級_2026-11-09/借來的做法整合方案.md〉3.2、3.6。

**與 v2 的差異：** 新增 Step 7（v1.2.0）、Step 1 的 fetch 前置（v1.3.0）、common.md 跨服務契約檢查（v1.4.0）、Step 4b spec 審查（v1.5.0）、行層級變更範圍與框架出處檢查（v1.6.0），其餘審查邏輯與支援技術棧不變。

**配合使用：** 建議搭配 `requirements` v1.0.0 和 `doc-update` v1.0.0 形成完整工作流程。

---

### 4. requirements

| 欄位 | 內容 |
|------|------|
| **名稱** | `requirements` |
| **版本** | `1.8.0` |
| **路徑** | `dev/requirements/` |
| **最後更新** | 2026-11-13（v1.8.0 SKILL.md 改薄入口：387→309 行，可信度判斷細節、框架用法、後端契約同步模式移到 `references/`，底線規則留在 SKILL.md）；2026-11-11（v1.7.3 叫 grilling 時註明 plugin 名稱 `core:grilling`） |

**新增功能（v1.8.0，2026-11-13）：薄入口**

- 新增 `references/reference-credibility.md`、`framework-docs.md`、`backend-contract-sync.md`；SKILL.md 只留步驟與沒讀細節也要守的底線（JSON 鍵不採信文件、沒有 `source-commit` 視為未驗證）

> 🔎 **起因**：借 slc marketplace 的「SKILL.md 薄入口、大檔放同目錄」（〈plugin分組草案〉第 11 節 #3）。workflow-bench v5：14/14、附屬檔實際被讀到；費用沒有下降（$4.77），保留理由是好維護。

> ⚠️ 本條目原記為 `1.1.0` / 2026-03-18，但 v1.2.0（2026-05-27，metadata header 格式統一）當時未同步至本索引。
> 已於 2026-07-30 一併補正。

**描述：**
將模糊需求轉換為標準化任務文件，存入 `docs/shared/`。**先讀既有架構／API 參考文件（含上游 repo）並判斷可信度，再翻原始碼補足**；自動分析影響範圍（含**跨服務 enum／DTO 契約**）、拆解實作任務、確認風險清單，產出可直接交給 AI agent 實作的任務文件。

**用途：**
- 接收模糊需求描述 → 詢問補充資訊 → 探索相關程式碼 → 產出完整任務文件
- 自動對照 CLAUDE.md 風險清單（OAuth2、TaskManager、build_runner、DataCell 游標等）
- 任務文件包含：背景說明、需求說明、影響範圍分析、實作任務（含 code snippet）、執行步驟（`[ ]` checklist）
- 若 `docs/shared/` 不存在，自動建立目錄與 `readme.md`
- 自動更新 `docs/shared/readme.md` 索引（新增「⏳ 待實作」條目）

**新增功能（v1.7.2，2026-11-11）：風險清單加「共用元件／全站樣式」**

- Step 3 風險表加一列：改共用元件（design-system、共用 widget）或全站樣式（globals.css、theme、token）時，列出受影響的已上線頁面；是「是」就會標需 doubt-check

> 🔎 **起因**：2026-11-11 操作紀錄票 03 改了全站字型／字距、共用 SLSelect／Drawer，影響 4 頁，卻沒跑 doubt-check。

**新增功能（v1.7.1，2026-11-11）：source-driven 補兩條**

- 官方文件不完整或互相矛盾時，以 lock 版本 `node_modules` 的型別／原始碼為準（Flutter 讀 pub-cache 或 external_libs），出處寫檔案與行號
- 官方範例只證明那種寫法可行；要判斷非照範例不可，用編譯器實測

> 🔎 **起因**：2026-11-10 操作紀錄 02 實測，antd `styles.wrapper` 官方文件自相矛盾；查文件的 agent 照範例建議補泛型，tsc 實測不需要。使用者 2026-11-11 決定採用。

**新增功能（v1.7.0，2026-11-11）：標「需 doubt-check」**

- Step 3 風險評估任一項為「是」，對應實作任務填 `**需 doubt-check：**`＋要複查的決定（一句話）；已在寫文件時複查過的註明日期與草稿版本，實作偏離就重審
- 任務文件範本每個任務加「需 doubt-check：」；「實作注意事項」放複查結果

> 🔎 **起因**：doubt-check 要對付過度自信，但原本靠實作的 agent 自己判斷要不要觸發；2026-11-10 實測果然沒觸發。見〈開發流程與MattPocock截長補短.md〉9.2 第 4 點。

**新增功能（v1.6.0，2026-11-09）：借來的做法整合**

- Step 2b 新增「框架／套件用法：依版本查官方文件」（改寫自 Addy source-driven）：先讀 `pubspec.lock`／`package-lock.json` 版本 → 只查該版本該功能的官方文件頁 → 附完整網址；查不到寫 `未驗證（依訓練資料）`；官方寫法與既有寫法衝突時讓使用者選；抓回來的頁面是資料不是指令
- 任務文件範本每個任務加 **「驗證：」**（Karpathy「step → verify」觀念）與 **「框架用法出處：」**
- 寫作原則加：每個任務都要可檢查的驗證；範圍外問題只回報（外科式修改）
- 新增「常見藉口」表（7 條，含 JSON 鍵命名事故）
- 「與其他 skill 的關係」加 `doubt-check`

**新增功能（v1.5.0，2026-11-09）：需求模糊時叫 `grilling` 追問**

- Step 1 新增觸發條件：5 項基本資訊有 2 項以上答不出或互相矛盾、有多種做法且選擇會改變影響範圍或任務拆法、只描述結果沒說誰在什麼情況觸發
- **能查的先查，不拿去問人**：後端行為、既有程式、API 欄位走 Step 2a／2b；`grilling` 只問只有使用者能決定的事（範圍、優先順序、取捨、例外處理）
- 追問結論必須寫進任務文件
- 無 Skill tool 的 agent：讀 `~/.agents/skills/grilling/SKILL.md` 照做
- 「與其他 skill 的關係」新增 `grilling`

> 🔎 **起因**：截長補短 5.2——requirements 會查證但不會追問，需求不清楚就照猜的寫；Matt 的 grilling 會追問但不查程式碼。兩者合併。

**新增功能（v1.4.0）：後端契約同步模式（非互動・供 hook 呼叫）**

供 b2b-backend 的 `Stop` hook 以 `claude -p`（headless）呼叫。**不走 Step 1-8**，改走專屬流程。

> 🔴 **為什麼需要獨立模式**：原 Step 5 對「✅ 已完成」文件有**互動確認**，無人模式答不了。
> 而無人模式下最大的風險不是漏改，是**改錯**——所以硬邊界比功能重要。

- **硬邊界**：只能新增／更新任務文件**末尾**的「## ⚠️ 後端契約變更（自動同步・待確認）」區塊
  - ❌ 不得改動該區塊以外的任何既有內容
  - ❌ 不得改 `狀態`／`完成日期`／`優先級` 等 metadata
  - ❌ **不得新建任務文件**（要不要開新任務是人的決定）
  - ❌ 不得改 `readme.md` 索引、不得執行 `git commit`／`build_runner`
- **命中 0 份任務文件時只寫 log，不准猜**——猜錯改到不相關的文件，比漏掉更糟
- 缺 `後端依賴` 宣告的文件：只記錄「無法判斷」，留給人決定
- 寫 `docs/shared/_backend_sync_log.md` 記錄每次同步
- 收尾回報：命中幾份／改了哪些檔／哪些因宣告缺失無法判斷

**新增功能（v1.3.0）：接上 `project-documentation` 的交接斷點**

> 🔴 **起因**：`project-documentation` 的定位是「產出給 `requirements` 參考的依據，不夠再翻程式碼」，
> 但 v1.2.0 的 Step 2 直接 `ls`/`grep` 原始碼，**完全沒有讀參考文件這一步**——
> 這個設想在 skill 層從未存在，實際每次都從零翻程式碼。

- **Step 2 拆為 2a / 2b**
  - **Step 2a（新增）先讀既有參考文件**：本 repo 的 `docs/`，以及**上游 repo**（如 b2b-backend）的 `ARCHITECTURE.md`／`API_DOCUMENTATION.md`／`UPDATE_RECORD.md`
  - **可信度判斷表**：標 `⚠️ 推導未驗證` → 必翻原始碼；`source-commit` 與 HEAD 差距大 → 視為過期；**無 `source-commit` 欄位 → 全部視為未驗證**
  - **JSON 鍵命名／包裝層數／分頁欄位名預設不採信文件**，除非該處明確標示已從序列化配置確認（曾因此發生 P0：文件寫 camelCase、實際 snake_case，前端照抄後 runtime 解析失敗、整頁空白）
  - **Step 2b** 保留原程式碼探索，並要求記錄「哪些結論來自文件、哪些來自原始碼」，發現文件與程式碼不符時回報
- **Step 3 風險清單新增 3 項**：跨服務契約（enum）、跨服務契約（DTO）、權限資源。
  附說明「此類風險在前端零 diff，code review 不可能發現」
- **metadata header 新增 2 欄**
  - **`後端依賴`**：宣告章節編號／類別檔名／enum 名稱。**這是把上游變動接到下游任務的唯一缺口**——沒有它只能靠人記得，無法自動化
  - **`參考文件基準`**：記下引用時參考文件的 `source-commit`，日後才能判斷期間有無影響本任務的變更
- **任務文件範本新增「契約依據」章節**：鍵命名策略／回應包裝欄位／分頁包裝欄位／錯誤格式／enum 值／**前端 enum 解析容錯性**，每列都要附來源行號
- **新增「與其他 skill 的關係」**：明確 `project-documentation` 為上游、`docs/shared/` 由本 skill 專屬維護

**新增功能（v1.1.0）：**
- **Step 5（新增）**：寫入前先檢查同名文件是否已存在
  - 「⏳ 待實作」/ 「🔄 進行中」→ 直接覆寫，狀態不變
  - 「✅ 已完成」→ 提示使用者確認後才覆寫，狀態改為「🔄 進行中」
- **Step 7 強化**：重新開啟已完成文件時，readme.md 狀態改回「🔄 進行中」
- **Step 8（新增）**：重新開啟已完成文件時，更新 CHANGELOG.md（`Changed` 分類）

**觸發關鍵字：** `/requirements`、「討論作法」、「需求分析」、「寫任務文件」、「規劃功能」

**包含 references：**
- `references/task-doc-template.md`：標準任務文件模板
- `references/readme-template.md`：`docs/shared/readme.md` 初始格式（v1.3.0 新增「契約依據」章節於 task-doc-template）

**配合使用：** `project-documentation` v2.1.0（上游，提供參考依據）→ 本 skill（模糊時叫 `grilling`）→ 開發（高風險決定叫 `doubt-check`）→ `stack-review` v1.6.0 或 `ai-pair dev` → `doc-update` v1.1.0

---

### 5. doc-update

| 欄位 | 內容 |
|------|------|
| **名稱** | `doc-update` |
| **版本** | `1.4.0` |
| **路徑** | `dev/doc-update/` |
| **最後更新** | 2026-11-13（v1.4.0 沉澱判斷：提議編號、記憶附查證、單向門判準）；2026-11-11（v1.3.1 註明 retro 只能由使用者手動叫；v1.3.0 Step 8 退場追蹤） |

**新增功能（v1.4.0，2026-11-13）：提議編號與單向門**

- 每個沉澱提議編號 `S-YYYYMMDD-n`，下次先查上一次的結論；被否決過的不再提
- 寫成記憶時結尾附 `（驗證：哪天、在哪、跑了什麼、看到什麼）`，沒驗證過寫 `uncertain`
- 改到「煞車本身」（hook、權限、禁止 commit、檢查項、風險清單）、或放寬／移除規則，一律先問使用者

> 🔎 **起因**：借 slc marketplace 的知識標準與定期回顧（〈plugin分組草案〉第 11 節 #5、#7、#8）。workflow-bench v5 實測出現編號 `S-20261113-1`。

**新增功能（v1.3.0，2026-11-11）：Step 8 退場追蹤**

- 結案時在桌面〈開發流程升級_2026-11-09/v3實測報告_02-log-drawer.md〉第 8 節的四張表各補一列（doubt-check、source-driven、沉澱判斷、藉口表）；沒用到寫「不適用」；表滿後照條件判斷、交使用者決定，不自行移除

> 🔎 **起因**：〈開發流程與MattPocock截長補短.md〉9.2 第 3 點「只加不減」，使用者 2026-11-11 決定四個機制都加退場條件。

**新增功能（v1.2.0，2026-11-09）：Step 7 沉澱判斷**（觀念借自 Every Compound Engineering 的 `/ce-compound`，原作無授權檔，自己的寫法）

- 門檻三條都成立才留：不明顯、長期有用、忘了會出事；反事實檢驗「這份紀錄不存在，下一個人看程式會不會重犯」
- 選最便宜、能擋住重犯的形式：測試 → 專案規則（AGENTS.md、`.claude/rules/`）→ 三層記憶 → 專案文件（Bug 修復紀錄）→ slc-core `/knowledge-capture`
- 先找重複，有就更新舊的；**先給使用者看，同意後才寫入**（使用者 2026-11-09 決定）；非互動情境只提議不寫
- 與 `retro`（環境改善）、`/knowledge-capture`（第 5 級的寫入流程）分工
- 新增「常見藉口」表

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

> ⚠️ 此 Skill 為 B2B Manager 專案專屬，已被 `project-documentation` 取代。

---

### 7. project-documentation

| 欄位 | 內容 |
|------|------|
| **名稱** | `project-documentation` |
| **版本** | `2.2.2` |
| **路徑** | `dev/project-documentation/` |
| **最後更新** | 2026-11-11（v2.2.2 bug-record 範本補必填的 `updated`、`source-commit`，原本和 frontmatter-spec 矛盾） |

**描述：**
多技術棧可擴展文件產出系統，為 `flutter-b2b-documentation` 的通用化進化版。v2.0.0 新增 Spring Boot 完整支援、Bug 修復紀錄與 Widget 元件文件兩種新類型。**v2.1.0 為可信度強化版**：加入「不得產出流程未要求的內容」硬約束、`⚠️ 推導未驗證` 標記規範、`source-commit` 必填、wire 契約推導階段、更新（非覆蓋）流程與產出自檢，並新增「變更歷程文件」類型。**v2.2.0 補上專案自有版本／日期慣例的處理**：部分專案（如 b2b-backend）文件不用 YAML frontmatter，而是自己的「文件版本」／「最後更新」footer + 版本總覽表；Step 0 新增判斷規則（視為 frontmatter 等價物，需找出所有出現位置同步更新），Step 5 自檢明確要求日期用**文件實際撰寫當下**、不可誤用最後一個 commit 的日期。

**用途（六種文件類型）：**

| 類型 | 觸發關鍵字 | 產出位置 |
|------|-----------|---------|
| 專案架構文件 | "project"、"專案架構"、"建立架構文件" | `docs/project-architecture.md` |
| 功能模組文件 | "feature"、"記錄功能"、模組名稱 | `docs/page_architecture/[模組]-documentation.md` |
| API 總覽文件 | "api"、"API 清單"、"整理 API" | `docs/api-reference.md` |
| Bug 修復紀錄 | "bug"、"修復紀錄"、"bug record" | `docs/bug_record/[問題名稱].md` |
| Widget 元件文件 | "widget"、"元件文件"、"component" | `docs/widget/[元件名稱].md` |
| **變更歷程文件** | "變更歷程"、"更新紀錄"、"update record" | `UPDATE_RECORD.md` |

> ⚠️ v2.1.0 起產出位置**以專案既有慣例為準**，上表為新建專案時的預設值。
> 實際如 b2b-backend 用 `ARCHITECTURE.md`／`API_DOCUMENTATION.md`、b2b-manager 用 `docs/claude/`。

**支援狀態：**

| 技術棧 | 狀態 |
|--------|------|
| Flutter（Riverpod/Bloc） | ✅ 完整支援 |
| Spring Boot（Spring Data JDBC） | ✅ 完整支援 |
| Android | 🔧 框架就緒（待擴展） |

**新增功能（v2.2.0）：**

> 🔴 **起因**：b2b-backend 的三份文件（`ARCHITECTURE.md`／`API_DOCUMENTATION.md`／`UPDATE_RECORD.md`）
> 不是用本 skill 規範的 YAML frontmatter，而是自己的「**文件版本**」／「**最後更新**」footer + 頂部版本總覽表。
> 用本 skill 更新文件時，這套自有慣例沒被同步更新；修正後第一次填日期，還誤填成最後一個 commit 的日期，
> 而非文件實際撰寫當下的日期——兩者常常不同，尤其事後才補文件、或一次處理多個 commit 時。

- **Step 0 新增「專案自有版本／日期慣例」處理規則**：無 YAML frontmatter 但有自己版本追蹤慣例的專案，
  視為該專案的 frontmatter 等價物，一體適用同樣的更新規則
- **找出所有出現位置**：這類慣例常見不只一處（文件自身 footer、彙總表格、changelog 表頭），逐一確認同步
- **日期規則明確化**：一律填**文件實際撰寫／更新當下的日期**，🔴 不可誤用「最後一個 commit 的日期」
- **Step 5 自檢對應更新**：原「frontmatter 六個必填欄位」檢查項擴充為涵蓋無 frontmatter 專案的等價檢查

**修正（v2.2.1）：消除原則 3 的指令衝突**

> 🔴 v2.2.0 加入「專案自有版本／日期慣例」後，與**原則 3「frontmatter 必填 `source-commit`」產生衝突**：
> 原則層說無條件必填，流程層說可用等價物替代。實測後果——後端三份文件 `source-commit` **0 處**，
> 模型仲裁衝突時選了流程層，等於讓一條「最高優先原則」靜默失效。

- **原則 3 改為描述原則**（依「有沒有例外」測試：有例外就不該是絕對指令）——
  「文件必須帶**可判斷版本的標記**」，下分**形式 A**（YAML frontmatter）／**形式 B**（專案自有慣例），二擇一不可混用
- **`frontmatter-spec.md` 補「形式 B」整節**（原本 0 處提及，是最大缺口）：典型出現位置、四條規則、自檢清單
- **Step 0 改為「先判斷用哪種形式」**的決策表 ＋ grep 指令，細節指向 spec（依「指令只寫一次」收斂重複）
- **Step 5 自檢**依形式分流
- 指出**形式 B 的結構性弱點**：多數自有慣例只有版本號＋日期、**沒有 commit hash**，
  能回答「文件改過」卻回答不了「對應哪個程式碼狀態」→ changelog 條目的 commit 範圍是唯一可追溯來源，務必維持

**新增功能（v2.2.0）：專案自有版本／日期慣例**

- Step 0 新增該節；Step 5 自檢對應加項
- 關鍵易錯點：出現位置**通常不只一處**（footer／彙總表／changelog 表頭），漏改任一處即自相矛盾
- 日期須填**文件實際撰寫當下**，🔴 不可誤用最後一個 commit 的日期

**新增功能（v2.1.0）：**

> 🔴 **起因**：一份 AI 生成的後端 API 文件，JSON 範例鍵命名全錯（camelCase 396 處 vs 實際 snake_case），
> 分頁包裝類五個欄名全錯，下游前端照抄成 DTO 後 runtime 解析失敗、整頁空白。
> 根因不是推導能力不足，而是**範本只要求寫型別名稱，AI 為求完整自行補上了整份 JSON 範例**。

- **核心原則（優先於其餘所有內容）**
  - 原則 1「不得產出流程未要求的內容」——最高優先約束。補推導步驟不足以解決問題，只要「自行發揮」沒被禁止，AI 就會在其他未被規範處重演
  - 原則 2「標記可信度」——確定性抽取的不標記，憑慣例推導的一律標 `⚠️ 推導未驗證`（AI 判斷不出自己哪裡在猜，但可被要求區分「讀到的」與「補的」）
  - 原則 3「記錄 `source-commit`」——描述性文件會漂移，沒有 commit hash 就無法判斷該不該重生成
- **frontmatter**：`source-commit` 新增為必填、`updated` 由選填改必填
- **wire 契約推導階段（階段 B）**：Spring Boot 補 B1 序列化命名策略（⚠️ 可能有多個 ObjectMapper，策略各異）／B2 包裝類實際欄位與層數／B3 錯誤格式／B4 enum 值清單／B5 `@JsonProperty` 等逐欄例外；Flutter 補 `fieldRename` 配置、**手寫 `toJson` 覆寫**、`$enumDecode` 解析容錯性
- **Step 0 新建 vs 更新判斷**：`source-commit` 相同則停止；較舊走更新流程，**只重生成受影響章節、不可直接覆蓋**（既有文件可能含人工修正過的正確內容）
- **Step 5 產出自檢**：逐條核對來源行號、無未要求內容、回報「已驗證／推導未驗證／留空」三個數字
- **命名與路徑改為配合專案既有慣例**：原規範硬禁 snake_case 與全大寫，與實際全面不符且自身矛盾（目錄名 `page_architecture` 本身就是 snake_case）
- **規模控制**：單檔 > 1500 行分檔 + 索引
- **明確劃出邊界**：不產出／不改動 `docs/shared/*`（屬 `/requirements`）、`AGENTS.md`、`CLAUDE.md`、`DESIGN.md`

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
- `references/templates/change-log.md`：**變更歷程範本（v2.1.0 新增）**——跨 repo 消費者最依賴的一份，commit hash／`⚠️` 行為變更標記／影響章節編號三者缺一不可

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
| **版本** | `5.0.0` |
| **路徑** | `ai-pair-main-v5.0/`（存檔：完整快照含 archive／examples；live 安裝版已精簡）|
| **最後更新** | 2026-07-30 |

**描述：**
異構 AI 協作團隊 Skill。**v5.0 為結構性改版**，核心原則轉為「**Claude 額度只花在協調決策與 review 驗證；探索與實作外包給 external CLI**」——依據是資源不可替代性：Claude 額度耗盡時 Team Lead 本身停擺，整個流程無法運作，而 Copilot Credits 耗盡只需降級。五項主要變更：①新增 `explorer` 角色（探索常態外包，附四道護欄）②developer 改雙引擎，**copilot 為預設**、native subagent 為品質升級（含「連續 2 輪 BLOCK 出局」護欄）③**廢除 v4.x「reviewer 不得讀 source」禁令**——該禁令廢掉了跨檔案／跨 repo 查證能力，正是 ai-pair 過去輸給 `stack-review` 的主因 ④傳遞層改 **manifest 路徑**（不再嵌 payload）⑤模型層改執行期發現，developer 建立 **A/B 准入制**（回報誠實性為淘汰項）。

**用途：**
- `/ai-pair dev-team [project]` — Level 2 標準 review（預設）
- `/ai-pair dev-team [project] --quick` — Level 1 快速掃描（agy only，~30s）
- `/ai-pair dev-team [project] --deep` — Level 3 深度 review（三 reviewer 並行）
- `/ai-pair dev-team [project] --dev=copilot|native|auto` — developer 引擎選擇
- `/ai-pair dev-team [project] --conserve` — 節約模式（Team Lead 自身也收斂）
- `/ai-pair content-team [topic]` / `/ai-pair team-stop`

**前置需求：**
- Claude Code（Team Lead + native subagent runtime）
- GitHub Copilot CLI（`copilot`）：explorer／developer／copilot-reviewer
- Antigravity CLI（`agy`）：gemini-reviewer。🔴 **headless 必須加 `--dangerously-skip-permissions`**

**Frontmatter（v5.0 新增）：**
`disable-model-invocation: true`（會燒 Copilot Credits，屬有副作用流程，僅手動觸發）、`allowed-tools`、`argument-hint`

**團隊架構：**

| 角色 | 引擎 | 負責面向 |
|------|------|---------|
| Team Lead | 當前 session（高階模型） | 協調、判斷、決策。**不做大範圍探索、不做實作** |
| explorer | external CLI（常態外包） | 找相關檔案、既有 pattern、契約面盤點 |
| developer | **copilot（預設）／native（升級）** | 依 TASK context file 實作 |
| copilot-reviewer | copilot CLI | bugs、安全性、效能、邊界條件 |
| claude-reviewer | native subagent ⛔ **不可省略** | 架構、可維護性、**跨檔案／跨 repo 契約查證** |
| gemini-reviewer | agy | spec compliance、需求對齊、遺漏情境 |

**核心設計：**
- **manifest-based review（四段）**：裁決清單／審查範圍／🔴**契約面清單**／指示。reviewer **可讀任何驗證所需檔案**但不得擴張範圍
- **Inter-Agent Protocol v2**：結構化輸出（agy `--json-schema`；copilot `-s` + prompt 約束），新增 `CONFLICT` 訊息型別
- **機械驗證**：`DONE:{files}` 用 `git diff --stat` 比對；findings 路徑須經**共用正規化函式**驗證（產生 scope 與驗證 findings 必須同一實作）
- **原始輸出一律落檔留存（含失敗）**——既是稽核證據，也是零成本回歸測試資料
- **reviewer 不是預算調節閥**：依任務風險調數量可以，依預算壓力削減不行

**上線驗收（2026-07-30）：**

| 項目 | 結果 |
|---|---|
| reviewer 全路徑 | ✅ 首跑 10 個真實 findings、0 捏造路徑 |
| **契約面清單有效性 A/B** | ✅ **唯一經實驗證明「原本抓不到、現在抓得到」**：嚴格 A（無清單）PASS/0 → 嚴格 B（有清單）BLOCK/1 Critical |
| developer 雙引擎 | ✅ copilot 實作成功；native 正確回報 `CONFLICT:` 並停止（零改動） |
| developer 模型 gate | ✅ 8/8（同時揭露並修正一個 live 邏輯矛盾：tier 是成本分級非品質分級） |
| findings 路徑正規化 | ✅ 9/9（修正前 0/9 全被誤殺） |

**⚠️ 已知未驗**：兩次 BLOCK 出局、`--conserve`／`--dev=auto`、content-team、跨模型測試。皆為「失敗會明確報錯」類型，詳見 `reference/known-limitations.md`。

**版本歷程：**

| 版本 | 日期 | 重點 |
|------|------|------|
| v3.0.0 | 2026-04-29 | 三 reviewer 架構、Inter-Agent Protocol v1、分層 review、fallback chain |
| v4.2.5 | 2026-06-01 | Copilot Credit 適應、Tier 加成本欄 |
| v4.3.0 | 2026-06-22 | Gemini CLI → Antigravity CLI（`agy`）遷移 |
| v4.3.5 | 2026-06-25 | 修正 Copilot CLI 不讀 stdin（改 `-p` 嵌入）；MAI-Code-1-Flash 經 A/B 判定不採用 |
| v4.3.6 | 2026-06-26 | 環境相容性：無 `TeamCreate`/`TeamDelete` 時的等效流程 |
| **v5.0.0** | **2026-07-30** | **結構性改版：Claude 額度只花在協調與 review；新增 explorer（四道護欄）；developer 改雙引擎（copilot 預設）＋A/B 准入制；廢除「reviewer 不得讀 source」禁令；傳遞層改 manifest 路徑；模型層改執行期發現；結構化輸出＋幻覺路徑機械攔阻。文件符合官方硬規格（SKILL.md 465→479 行 ≤500、8 份 ref 皆有 TOC、一層引用）** |

**v5.0 過程中被實測推翻的初稿主張（記錄以免重犯）：**

| 初稿主張 | 實測結果 |
|---|---|
| agy 模型名稱格式全錯、被靜默降級掩蓋 | ❌ **錯**——agy 同時接受 slug 與顯示名；v1.1.8 對無效模型明確報錯且零 token 消耗 |
| `agy models` 白名單可做前置驗證 | ❌ **會引入故障**——只輸出 slug，會誤殺有效的顯示名 |
| copilot `-s` 的 stdout 就是乾淨 JSON | ❌ **只在單輪短任務成立**；多步驟工具呼叫時過程敘述混入 |
| developer 禁用 LOW/FREE tier | ❌ **與自己的預設模型矛盾**——tier 是成本分級非品質分級 |

> 📌 共同教訓：**寫進文件不等於驗證過。** 這些全是「不發聲的失敗」——不會拋錯，只會靜默給出看似正常的錯誤結果。

**與 `multi-tool-coordination` 的定位差異：**

| 面向 | `ai-pair` | `multi-tool-coordination` |
|---|---|---|
| 類型 | 執行型（Agent 自動化） | 知識型（人工操作指南） |
| 工具範圍 | Claude + Copilot CLI（GPT／Claude／Gemini／Grok／Kimi）+ agy | Claude + Copilot + Codex + Gemini |
| 操作模式 | Agent 間結構化輸出自動溝通 | 人工切換工具、手動傳遞上下文 |
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
| **版本** | `1.0.2` |
| **路徑** | `dev/figma-to-requirements/`（備份）；作用中本體於**跨工具共用** `~/.agents/skills/figma-to-requirements/`（2026-10-20 自 `~/.claude/skills/` 搬入）；2026-11-11 起 Claude Code 由個人 plugin `dev-app` 載入 |
| **最後更新** | 2026-11-11（v1.0.2 交棒時註明 plugin 名稱 `dev:requirements`） |

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

### 17. b2b-manager-onboarding

| 欄位 | 內容 |
|------|------|
| **名稱** | `b2b-manager-onboarding` |
| **版本** | `1.1.0` |
| **路徑** | `dev/b2b-manager-onboarding/`（存檔）；**目前未安裝於任何作用中位置** |
| **最後更新** | 2026-08-25 |

**描述：**
b2b-manager（山隆 B2B 智慧平台，Flutter Web）專案的新人快速上手導覽。仿 ECPay `ecpay-api-skill`
的架構：SKILL.md 當**決策樹路由**，references 分層 progressive disclosure。
定位是「路由器不是教科書」——專案已有 CLAUDE.md／AGENTS.md／DESIGN.md／docs/ 一大堆文件，
新人的問題是不知道該讀哪份、什麼順序。

**用途：**
- 判斷來者卡在哪 → 給最短路徑 → 只載入必要的 reference（A 環境／B 地圖／C 食譜／D 地雷／E 名詞）
- 三種入口：四小時一條龍（第一天）、十分鐘版（老手接手）、單點查詢（路由表）
- 內建 10 題新人自我測試，答錯導回對應 reference
- 硬性要求「絕不憑記憶回答，每個答案落地到檔案路徑或指令」

**檔案結構：**
```
SKILL.md（118 行，決策樹）
references/
├── day1-setup.md          # 環境建置→登入成功；port 9001 原因、等帳號時的替代動作
├── codebase-map.md        # 目錄地圖 + 車輛列表「垂直切片」6 檔案（附真實行號）
├── first-task-recipes.md  # 七道食譜：API／頁面／列表頁／顏色／i18n／權限／送出前
├── conventions-gotchas.md # 禁止事項、高風險區、表格 8 條硬規則、DataCell 游標
└── glossary-domain.md     # 業務名詞、Authorities 權限模型、三環境、瀏覽器儲存
```

**觸發關鍵字：**
「我是新人」、「剛接手 b2b-manager」、「怎麼開始」、「專案怎麼跑」、「程式碼在哪」、
「幫我導覽專案」、「新增頁面/API 該從哪開始」

**⚠️ 專案專屬，不可跨專案共用：** 內容價值全在「car 模組第 71 行傳 `isClear: true`」這種具體行號，
抽象化後會退化成一般 Flutter 教學。其他專案請複製結構、重寫內容，命名沿用 `<repo 名>-onboarding`。

**已知待釐清：** `car_drawer.dart:51` 傳 `isClear: false`，同行註解卻寫「批次大量刪除車子或大量加車，
用舊的 page number 會錯」——註解與參數對不上，文件中已標記為勿當範本。

---

### 18. sanlong-pay-onboarding

| 欄位 | 內容 |
|------|------|
| **名稱** | `sanlong-pay-onboarding` |
| **版本** | `1.0.0` |
| **路徑** | `dev/sanlong-pay-onboarding/`（存檔）；**目前未安裝於任何作用中位置** |
| **最後更新** | 2026-08-25 |
| **來源專案** | `app01-double`（sanlong／山隆 PAY），基準 **`main` 分支 `190038a9`** |

**描述：**
山隆 PAY（iOS + Android Flutter APP，加油站服務／儲值金／會員點數）的新人上手導覽。
與 `b2b-manager-onboarding` 同架構（SKILL.md 決策樹路由 + references 分層），
但**內容完全不同**——那支是 Flutter Web + Riverpod + GoRouter，這支是手機 APP +
自製 SLRouter + 單一大型 SLController。

**用途：**
- A 環境／B 地圖／C 食譜／D 地雷／E 名詞五條路徑，只載入需要的那份
- 三種入口：四小時一條龍、十分鐘版（六句話）、單點查詢
- 10 題自我測試（已驗證答案全數落在 references 內）

**檔案結構（857 行）：**
```
SKILL.md（130 行）
references/
├── day1-setup.md          # 147 行；六支入口檔、兩平台 flavor 名稱不一致、.venv 那三支 python
├── codebase-map.md        # 154 行；UI→SLController→Repository 分層、「按下儲值」垂直切片
├── first-task-recipes.md  # 224 行；十道食譜（畫面／API／顏色／文案／BottomSheet／Dialog／防重複／狀態同步／上架／送出前）
├── conventions-gotchas.md # 114 行；NEVER 清單、UI 11 坑、Riverpod 同步六點
└── glossary-domain.md     # 88 行；Screen enum 畫面地圖、環境、i18n key 規則
```

**這支收錄的專案特有地雷**（其他 Flutter 專案沒有）：
- `pushMain` 的 `isDraggable: true` 會讓畫面**從底部彈出**而非側滑，參數名毫無暗示
- 防重複提交擋在 **SLController**（`_loading.getLoading(SLAction.xxx)`），不是 UI disable 按鈕
- 待支付檢查是 **APP 端本地 `isWaiting`**，不是 API 欄位（新人會去翻 API 文件白找）
- **本專案無 screenutil**——同時碰 b2b-manager 的人照抄 `.w/.h/.sp` 會破壞版面
- `FlavorConfig` 設了但**沒被讀**（`repository_api.dart` 那行是註解掉的），實際生效的是 `BASE_URL`
- flavor 名稱兩平台不一致：staging → iOS `stage` / Android `staging`；正式 → iOS 預設 scheme `Runner`（不帶參數）/ Android `product`
- `.run/` 的 `additionalArgs` **不可複製到命令列**：iOS 的 `--target dev` 會被後面的 `-t` 覆蓋（`--target` 就是 `-t` 的長名），IDE 內無害（scheme 來自 `buildFlavor` 欄位）但命令列照抄就靜默失去 scheme

**測試紀錄（2026-08-25，由 app01-double session 協作驗證）：**
- ✅ 手動叫用、frontmatter 解析、五條路徑檔案齊全
- ✅ 事實正確性在 `main` 上逐條抽驗（入口檔／scheme／gradle 行號／垂直切片 10 個行號／CI job 順序／iOS 15.0）
- ✅ 10 題自我測試答案覆蓋率全中
- ⏸️ **自動觸發未驗**（需使用者親手打字，非 agent 自行叫用可證）
- ⏸️ **實跑 flavor build 未驗**（無可用裝置／模擬器）
- 🔧 過程中修掉一次過度擴大的判斷：原誤判「iOS run config 參數全壞」，實際只有「複製到命令列」才會出事

**⚠️ 專案專屬，不可跨專案共用**：價值全在具體行號與專案慣例。其他專案請複製架構、重寫內容，
命名沿用 `<repo 名>-onboarding`。

---

### 19. multiagent-handoff

| 欄位 | 內容 |
|------|------|
| **名稱** | `multiagent-handoff`（v0.5.0 前為 `handoff`） |
| **版本** | `0.6.0` |
| **路徑** | `dev/multiagent-handoff/`（備份）；作用中本體 `~/.agents/skills/multiagent-handoff/`（六個工具共用，見下方「作用中安裝位置」） |
| **最後更新** | 2026-10-21 |

**v0.6.0（2026-10-21）：** save 交接檔與 report 任務單加「建議記憶」；其他 agent 不直接寫長期記憶，由 Claude 在 resume／review 判斷層級、給使用者看過後寫入。

**改名：** v0.5.0（2026-10-21）由 `handoff` 改名為 `multiagent-handoff`，避免與 Matt Pocock 的 `/handoff`（b2b-manager 專案層 `.claude/skills/handoff/`）撞名。`.handoff/`、`refs/handoff/`、`handoff.py` 沿用舊名，既有交接檔與任務單不受影響。

**描述：**
跨 AI agent 的專案接力：存狀態、接手、分派任務、回報、驗收。適用 Claude Code、Codex、Copilot CLI、opencode、agy、Cursor
等任何能讀檔與執行 shell 的 agent。**狀態以 git 為準，交接檔只補 git 看不出來的部分**（意圖、決定、下一步）。

**用途：**
- **換手**：`save`（交出方寫 `.handoff/CURRENT.md`）→ `resume`（接手方比對 diff；找不到交接檔時從 Claude Code／Codex／agy 本機對話紀錄還原）
- **分派**：`delegate` 開任務單並記錄**分派基準**（`git stash create`，含當下未 commit 的修改，存成 `refs/handoff/<id>`）→ 對方 `report` → 主 agent `review`（列出實際變動、自動標 🟡 範圍外／🔴 禁止範圍）
- **`--run`**：以非互動模式叫起指定 agent（codex／agy／copilot／opencode／cursor），**以任務單是否變成「已回報」判斷成敗，不看 exit code**（防假成功）

**檔案結構：**
```
SKILL.md              # 154 行，給 agent 執行的流程
README.md             # 267 行，給人看的使用說明（含安裝位置、各 agent 實測表）
scripts/handoff.py    # 565 行：init／snapshot／new-task／run／review／sessions／log
```

**觸發關鍵字：**
「/multiagent-handoff」、「交接」、「換手」、「接手」、「額度快用完」、「交給 Codex／Copilot 繼續」、「分派給其他 agent」、「驗收」、「resume」

**測試紀錄：**
- ✅ scratch repo：五個 agent 的 `--run` 全數通過（opencode 須指定模型——預設模型會重複讀任務單直到逾時）
- ✅ **實戰 SSGS-14167（2026-10-20）**：拆兩張單依序派給 Copilot（claude-sonnet-5.5，50 秒）與 Codex（gpt-5.6-terra，35 秒），皆驗收通過、使用者 UI 實測通過；派第 ② 張時第 ① 張的 9 檔未 commit，review 仍只列 Codex 的 2 檔（分派基準機制成立）
- 🔧 實戰抓到並修正：Codex `workspace-write` sandbox 跑不了 `flutter analyze` → Flutter 專案自動 `--add-dir` SDK `bin/cache`、`~/.dart-tool`、`~/.pub-cache`
- ⏸️ `save → resume` 換手尚未實戰；`AGENTS.md` 尚未加交接規則

**與 ai-pair 的邊界：** 要多模型交叉 review 或自動重試 → ai-pair；換手、或只要某個 agent 做完給我驗收 → multiagent-handoff（`--run` 只叫起一次、不重試）。

**規劃文件：** b2b-manager `docs/agent-handoff/agent-handoff-規劃.md`；安裝包快照 `docs/agent-handoff/install/`

---

### 20. mattpocock-skills（外部）

| 欄位 | 內容 |
|------|------|
| **名稱** | grilling、grill-me、diagnosing-bugs、tdd、pr、writing-for-agents、retro（7 個） |
| **版本** | 上游 mattpocock/skills@5beb35b（plugin v1.3.1，2026-10-19），MIT |
| **路徑** | `dev/mattpocock-skills/`（備份，含 `LICENSE-mattpocock`、`MATTPOCOCK-SOURCE.md`）；作用中本體 `~/.agents/skills/<name>/` |
| **最後更新** | 2026-11-11（tdd 加「新測試一寫就綠不算紅燈」的處理） |

**來源：** 2026-10-21 裝在 b2b-manager `.claude/skills/` 測試 Matt 整套流程；2026-11-09 依〈開發流程升級_2026-11-09/開發流程與MattPocock截長補短.md〉把不需 repo 設定的 7 個搬到共用位置，b2b-manager 的同名副本與 Matt `handoff` 已刪除（handoff 與 multiagent-handoff 重複）。

**在主流程的位置：**

| skill | 插在哪 | 怎麼叫 |
|---|---|---|
| `grilling`／`grill-me` | ① Jira 確認需求後 | requirements Step 1 需求模糊時自動叫；grill-me 只能手動 |
| `diagnosing-bugs` | ④ 開發卡在 bug | 自動觸發或手動 |
| `tdd` | ④ 新程式（如 `next/`） | 自動觸發或手動 |
| `pr` | ⑥ doc-update 之後 | 手動，寫 MR 說明 |
| `writing-for-agents` | 改 skill／AGENTS.md／CLAUDE.md | 自動觸發 |
| `retro` | session 結束 | 只能手動；結論照三層記憶規則寫 |

**本機修改：** `tdd` 叫 `codebase-design` 改為「repo 有才叫」；重構歸屬改指 `stack-review`（細節見 `MATTPOCOCK-SOURCE.md`）。

**仍只在 b2b-manager 的 Matt skill：** to-tickets、implement、implement-spec、matt-code-review、to-spec、triage 等，React 遷移結束後回顧去留。ask-matt 內文仍提到 `/handoff`（未改）。

**⚠️ 注意：** 同名 skill 不可再放進任何 repo 的 `.claude/skills/`，專案版會蓋過共用版。

---

### 21. doubt-check

| 欄位 | 內容 |
|------|------|
| **名稱** | `doubt-check` |
| **版本** | `0.3.2` |
| **路徑** | `dev/doubt-check/`（備份）；作用中本體 `~/.agents/skills/doubt-check/` |
| **最後更新** | 2026-11-11 |

**來源：** 改寫自 `addyosmani/agent-skills` 的 doubt-driven-development（MIT，附 `LICENSE-addyosmani`）。

**描述：** 開發中途對**單一高風險決定**做對抗式複查——ai-pair 的輕量版。派一個新 context 的 reviewer，只給產物＋契約、不給主張與推理，提示詞要求「找問題、不准背書」。

**流程：** 主張 → 抽出 → 質疑 → 分類（契約沒寫清楚／要修／接受的取捨／雜訊）→ 停止（最多 3 輪，之後交給使用者）。

**觸發：** 認證／TaskManager、路由與權限、跨服務 enum／DTO、狀態管理結構、資料表排序與欄寬、不可逆操作，或要宣稱型別驗不出的性質；專案有風險清單時以專案為準。改文字／樣式／改名不觸發。

**v0.3.1（2026-11-11）：** 加退場條件：從 0.2.0 起算接下來 3 張標記的卡都沒找到要修的問題、或標記規則沒發揮作用，就移除並把檢查點併進 stack-review；追蹤表在桌面〈v3實測報告〉。

**v0.3.0（2026-11-11）：** 觸發條件加「改共用元件或全站樣式」：主張寫成「不會讓 A、B、C 頁壞掉」、契約附受影響頁面；不負責判斷畫面是否與設計稿／舊版一致（那要實際量測）。「不要用」改成單一頁面的文字或樣式。

**v0.2.0（2026-11-11）：** 任務文件標了「需 doubt-check」的任務一定要跑，時機是寫程式之前（用草稿當產物），不要做完才補審；文件註明已複查的，實作偏離就重審。跨模型改成每次叫用只在第 1 輪後問一次（原本每輪都問）。

**跨模型：** 每次叫用問使用者一次（Copilot CLI、Codex、agy 或跳過）；每次呼叫都要使用者確認完整指令並授權，一律唯讀（`codex exec --sandbox read-only`、`agy --mode plan`、`copilot --deny-tool`）；非互動情境一律跳過並寫明。

**分工：** doubt-check（④ 中途、單一決定）／stack-review（⑤ 做完、整個 diff）／ai-pair（整個任務一開始就複雜）。

**測試狀態：** 2026-11-10 用操作紀錄 02 實測兩次（草稿、成品），都找到問題；agent 沒有自己觸發，促成 v0.2.0。

---

### 22. flutter-ui-compare

| 欄位 | 內容 |
|------|------|
| **名稱** | `flutter-ui-compare` |
| **版本** | `0.1.1` |
| **路徑** | `dev/flutter-ui-compare/`（備份）；作用中本體 `~/.agents/claude-only/skills/flutter-ui-compare/`（Claude 專屬，其他 agent 不讀），由個人 plugin `dev-web` 載入 |
| **最後更新** | 2026-11-11 |

**描述：** 網頁畫面（React 等）與 Flutter Web 並排量測比對。用使用者的 Chrome（Claude in Chrome）真實點擊；React 用 DOM 量，Flutter（canvas）用已知元素換算截圖比例。`SKILL.md` 8 步、每步有完成條件；`KNOWN-CAUSES.md` 收 12 種已知差異（症狀、原因、驗算、修法）。

**來源：** 跨專案記憶〈reference_flutter_web_ui_compare〉與 b2b-manager 遷移回顧文件；只收跨專案成立的做法，專案專屬數值沒收。

**v0.1.1（2026-11-11）：** 第 1 步的畫面清單一定要包含頁面外框（標題列、側選單、標誌、帳號選單）。起因：推薦紀錄頁實跑時漏比外框，由使用者發現。

**測試狀態：** 2026-11-11 推薦紀錄頁首次實跑，8 步走完、KNOWN-CAUSES 用上「行高」；擴充功能對 localhost 的點擊與 zoom 時好時壞，hover 沒驗到。

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

### 15. point-reading-diy ✅ 可用（測試版）

| 欄位 | 內容 |
|------|------|
| **名稱** | `point-reading-diy` |
| **版本** | `0.4.0` |
| **路徑** | `point-reading-diy/`（存檔根目錄，尚未歸入 general/） |
| **最後更新** | 2026-10-21 |
| **狀態** | 可用（0.x 測試版）、**未安裝**；打包流程完成、Dear Zoo 實測成功。升 1.0 前待驗：`pack.py` 實際打包上筆、單字表比對／國語台語／`synth.py`／智能書名貼等情境 |

**描述：**
把整段錄音切成一句一檔，對應到卡米點讀筆「內容貼」的碼號，最後打包成 DAB 點讀包，讓沒有點讀碼的一般書變成點讀書。

**用途：**
- 書附 CD／自己錄的整段音檔 → 切成一句（或一頁）一檔
- 有背景音樂、找不到靜音的錄音 → 改用 Whisper 時間點切
- 產生本機審核網頁，人工逐段確認切點與內容
- 依單字表模糊比對或照順序，對應內容貼碼號並改名
- 無錄音時用 Mac `say` 從單字清單直接合成

**觸發關鍵字：** 「點讀筆」、「卡米」、「內容貼」、「書名貼」、「點讀包」、「DAB」、「切音檔」、「一句一檔」

**流程：**
```
原始音檔 → ① 切檔 → ② 語音辨識 → ③ 人工審核 → ④ 對應內容貼 → ⑤ 打包 DAB → 放進筆
```

**功能腳本清單：**

| 腳本 | 功能 |
|------|------|
| `split.py` | ① 依靜音切檔（ffmpeg silencedetect），回報段數與疑似黏在一起的片段供調參 |
| `split_asr.py` | ①' 依 Whisper 逐字時間點切檔，可把多句合成一段；切點取兩句間音量最低處 |
| `transcribe.py` | ② 語音辨識（mlx-whisper／whisper.cpp），國語經 OpenCC 轉台灣繁體 |
| `review.py` | ③ 產生單一 HTML 審核頁（波形、播放、標記、快捷鍵），匯出 `review.json` |
| `assign.py` | ④ 照順序或單字表依序對齊（容忍多／少一段），輸出 `<碼號>.mp3` |
| `synth.py` | Mac `say` 批次合成 |
| `pack.py` | ⑤ `out/<號碼>.mp3` → `NNN-1-書名.dab`；印刷號碼自動 +25000、寫入書名、打包後讀回逐段驗證 |
| `dab_tool.py` | ⑤ DAB 讀寫函式庫（AP4 → DAB 專案逆向所得） |
| `template_header.dab` | ⑤ 範本檔頭（取自 535-高频词32.dab，舊卡米筆實測可用） |

**系統需求：** FFmpeg、mlx-whisper + OpenCC（venv：`~/.venvs/point-reading-diy`，Homebrew Python 不允許直接 pip install）

**實測：** 《Dear Zoo》英文朗讀（含整段背景音樂）→ 靜音切檔無效，改 `split_asr.py` 切成 18 段，人工審核全數通過，輸出 `0001–0018.mp3` → 打包成 `001-1-DearZoo.dab`，放進筆實測 0001～0018 全部成功

**卡米規則（2026-10-10 報碼實測）：** 普通書名貼 N = 碼 56000+N，檔名 `NNN-1-書名.dab`（少 `-1` 不反應）；內容貼 N = 碼 25000+N；智能書名貼 001 → `001-`

**版本歷程：**
- `v0.4.0`（2026-10-21）：新增 `pack.py` 打包腳本與 `template_header.dab` 範本；寫入卡米規則實測結果（普通書名貼 `NNN-1-`、內容貼 +25000）；`--codes` 範例改為印刷號碼（`1-18 --width 4`）
- `v0.3.2`（2026-10-08）：放入 `dab_tool.py`；SKILL.md 步驟 ⑤ 改寫為 `write_dab()` 實際用法（需範本 DAB）
- `v0.3.1`（2026-10-08）：審核結果綁定切檔版本識別碼，重切後拒用舊 review.json（修正審核頁沿用上一版暫存的 bug）
- `v0.3.0`（2026-10-08）：`split_asr.py` 切點改取音量最低處；`assign.py --width` 補零檔名；新增翻翻書分段、重切前保存舊版等原則
- `v0.2.0`（2026-10-08）：新增 `split_asr.py`（有背景音樂時）
- `v0.1.0`（2026-10-06）：依規劃文件建立 SKILL.md 與 split／transcribe／review／assign／synth

---

## 知識管理類（pkm）

### 1. knowledge-organizer

| 欄位 | 內容 |
|------|------|
| **名稱** | `knowledge-organizer` |
| **版本** | `1.6.1` |
| **路徑** | `pkm/knowledge-organizer/` |
| **最後更新** | 2026-08-13 |

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
| **版本** | `1.5.0` |
| **路徑** | `pkm/daily-brief-generator/` |
| **最後更新** | 2026-08-13 |

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
| **版本** | `1.8.0` |
| **路徑** | `pkm/wiki-health-check/` |
| **最後更新** | 2026-09-03 |

**描述：**
每月知識庫健康檢查。掃描 wiki/ 找出七類品質問題：矛盾偵測、缺乏來源、知識缺口、連結品質（孤立/懸空）、過時內容、未處理素材（.processed 標記 + 幽靈標記偵測）、精粹過時偵測。報告末尾附 5A+ 階段評估（當前階段 + 理由 + 下一步建議）。v1.8.0 三項方法修正：精粹過時改用「來源清單集合差」（廢止 source_count vs glob 總數比大小，該法會假陰性）、連結掃描前須剝除程式碼區塊並解析路徑寫法、執行流程新增「先讀前一份報告」以免重複列出已判定的誤報且必須覆核前次矛盾是否已修。

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
| **版本** | `1.9.1` |
| **路徑** | `pkm/raw-pipeline/` |
| **最後更新** | 2026-08-13 |

**描述：**
軟編排型 Skill，調度三個子 Agent 協作批次處理 `raw/` 素材：Agent A 摘要、Agent B 分類打標、Agent C 建立 wiki 條目與更新索引。支援 12 種格式（.md .txt .html .pdf .png .jpg .jpeg .webp .gif .srt .vtt .ipynb .csv）。適合 raw/ 積壓 10 篇以上的場景。v1.7.0 起 .md/非 .md 統一用 `.processed` 旁車標記制；v1.8.0 修正非 .md 掃描指令 bug + 新增處理報告「排除項目」滾動日誌區塊（區分刻意排除 vs 遺漏積壓）。

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

## 設計類（design）

2026-11-13 新增。UI/UX 設計師角色用，在個人 plugin `design`；作用中本體在 `~/.agents/skills/`。三個都是**試用中**：清單初稿來自〈角色分類草案〉第 5 節，還沒用真實畫面試過。

### 1. anti-ai-look

| 欄位 | 內容 |
|------|------|
| **名稱** | `anti-ai-look` |
| **版本** | `0.1.0` |
| **路徑** | `design/anti-ai-look/`（備份）；作用中本體 `~/.agents/skills/anti-ai-look/` |
| **最後更新** | 2026-11-13 |

**描述：** 檢查畫面、icon、文案有沒有沒經過選擇的 AI 預設值：視覺、第二層 AI 味（奶油底加赤陶色等）、真實性、文案、一致性五組清單，逐條寫成立／不成立／沒法判斷；做 icon 加看 `references/icon-spec.md`。

> 🔎 **起因**：〈角色分類草案〉第 5 節「去 AI 味」清單，原註明之後做成規則檔或小 skill。

### 2. design-review

| 欄位 | 內容 |
|------|------|
| **名稱** | `design-review` |
| **版本** | `0.1.0` |
| **路徑** | `design/design-review/`（備份）；作用中本體 `~/.agents/skills/design-review/` |
| **最後更新** | 2026-11-13 |

**描述：** 唯讀的畫面 review：找 DESIGN.md、實際開頁截圖看各狀態，規格／去 AI 味／使用三軸分開列，每個發現要有證據；不改任何檔案，要修的交給開發角色。

> 🔎 **起因**：〈角色分類草案〉第 9 節第 2 項，使用者決定 UI/UX 角色新增「畫面 review」用法（唯讀）。

### 3. design-md-init

| 欄位 | 內容 |
|------|------|
| **名稱** | `design-md-init` |
| **版本** | `0.1.0` |
| **路徑** | `design/design-md-init/`（備份）；作用中本體 `~/.agents/skills/design-md-init/` |
| **最後更新** | 2026-11-13 |

**描述：** 專案或作品還沒有 DESIGN.md 時，先讀既有素材，只問人能決定的事（一次一個、附具體選項），依 `references/design-md-template.md` 寫出色彩、字型、間距、圓角、元件、icon 規格；已有就不覆蓋。

> 🔎 **起因**：〈角色分類草案〉的 uiux-designer 角色規定「還沒有 DESIGN.md 先建一份再開始畫」。

---

## 作用中安裝位置（2026-10-20 起）

自訂 skill 的**作用中**位置已改為跨工具共用。本索引其他段落的「路徑」欄皆指**本存檔資料夾內的備份位置**。

| 位置 | 內容 | 哪些工具讀得到 |
|------|------|------|
| `~/.agents/skills/`（本體） | **2026-11-13 加設計類 3 個**：anti-ai-look、design-review、design-md-init（共 18 個）；**2026-11-09 加 doubt-check**（共 15 個）；自訂 7 個：multiagent-handoff、stack-review、requirements、doc-update、project-documentation、figma-to-requirements、cross-platform-archive-agent；**2026-11-09 加 Matt Pocock 7 個**：grilling、grill-me、diagnosing-bugs、tdd、pr、writing-for-agents、retro（共 14 個） | Codex、Copilot CLI、opencode、Cursor 原生讀取；agy 經 symlink；Claude Code 經個人 plugin（2026-11-11 起） |
| `~/.claude/skills/` | **2026-11-11 起不再放自訂 skill**：15 個 symlink 拿掉、ai-pair 移走（備份 `~/.claude/backups/plugin-switch-20261111-141317/`） | — |
| `~/.agents/claude-only/` | **2026-11-11 新增**：Claude 專屬本體 ai-pair、flutter-ui-compare（`skills/`）、code-reviewer（`agents/`） | 其他 agent 不讀；Claude Code 經個人 plugin |
| `~/.agents/marketplace/` | **2026-11-13 起 Claude Code 從這裡載入**（從桌面〈開發流程升級_2026-11-09〉複製過來，桌面那份不再載入）：個人 plugin core／dev／dev-app／dev-web／design 是上面兩處本體的複本，本體改完跑 `scripts/sync-plugins.sh sync`、`check`；**research／teaching 的本體是 `~/Desktop/紀錄文件資料夾/` 的 notebooklm-v2.1.2-kit 與 notebooklm-teaching-v1.1-kit**，改完跑 `scripts/sync-kits.sh sync`、`check` | Claude Code（名稱帶前綴，例如 `dev:requirements`；依資料夾啟用） |
| `~/.gemini/config/skills/` | 上述 15 個的 symlink | agy 1.4.2（⚠️ 官方網頁寫的 `~/.gemini/antigravity-cli/skills/` 實測讀不到） |
| `~/.copilot/backups/code-review-20261020/` | Copilot 舊的 code-review（stack-review 2026-01 舊副本），已停用 | 無（不在讀取路徑） |

- 六個工具皆實測：7 個共用 skill 各看到恰好 1 份（2026-11-09 新增的 Matt 7 個：Claude Code 已確認載入，其他工具未重測）
- symlink 由 `~/.agents/link-skills.sh`（link／check／unlink）管理；安裝包快照與重建步驟見 b2b-manager `docs/agent-handoff/install/`
- 搬移前備份：`~/.claude/backups/skills-20261020-pre-move.tar.gz`

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
| `project-documentation`（內建） | 專案文件產出 | 同本地 v2.1.0 版本（見上方） |
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
| **stack-review** | **1.3.0** | **2026-07-29** | **dev** | **Step 1 補「必須先 fetch、用 `origin/main` 當 diff 基準、落後就先合併」；起因是實際發生 review 基準落後 7 週而漏看重複實作** |
| **stack-review** | **1.4.0** | **2026-07-29** | **dev** | **`references/common.md` 新增「跨服務契約（enum / DTO）」檢查；並明確標示 review 的能力邊界——「後端新增值、前端零 diff」的漂移 review 抓不到，須靠契約測試或 fail-soft 解析** |
| **stack-review** | **1.5.0** | **2026-11-09** | **dev** | **Step 4b：有 `docs/shared/` 任務文件時平行派 spec subagent（漏做／多做／做錯／契約），結果獨立一節不跨軸重排；吸收自 matt-code-review** |
| **requirements** | **1.1.0** | **2026-03-18** | **dev** | **新增：同名文件檢查、已完成重開流程、Step 8 CHANGELOG** |
| **requirements** | **1.5.0** | **2026-11-09** | **dev** | **Step 1 需求模糊叫 `grilling` 追問；能查的先查，只問只有人能決定的事；結論寫進任務文件** |
| **requirements** | **1.6.0** | **2026-11-09** | **dev** | **Step 2b 框架依版本查官方文件（source-driven）；範本每任務加「驗證：」「框架用法出處：」；常見藉口表** |
| **stack-review** | **1.6.0** | **2026-11-09** | **dev** | **common.md 行層級變更範圍（外科式修改）＋框架用法出處檢查；常見藉口表** |
| **doc-update** | **1.1.0** | **2026-03-18** | **dev** | **新增：支援「🔄 進行中」狀態** |
| **doc-update** | **1.2.0** | **2026-11-09** | **dev** | **Step 7 沉澱判斷（觀念借自 /ce-compound）：門檻三條＋最便宜形式（測試 > 規則 > 記憶 > 文件 > knowledge-capture），先給使用者看才寫** |
| **doc-update** | **1.3.0** | **2026-11-11** | **dev** | **Step 8：結案時補四個 v3 機制（doubt-check、source-driven、沉澱判斷、藉口表）的退場追蹤表（桌面〈v3實測報告〉第 8 節），表滿後判斷交給使用者** |
| **doubt-check** | **0.3.2** | **2026-11-11** | **dev** | **退場追蹤改由 doc-update Step 8 補** |
| **doubt-check** | **0.1.0** | **2026-11-09** | **dev** | **新增：開發中途單一高風險決定的對抗式複查（改寫自 Addy doubt-driven，MIT）；跨模型每次問、唯讀；未實測** |
| **requirements** | **1.7.0** | **2026-11-11** | **dev** | **Step 3 碰到風險的任務標「需 doubt-check」；範本每任務加該欄位** |
| **stack-review** | **1.7.0** | **2026-11-11** | **dev** | **spec 審查檢查標了「需 doubt-check」的任務有沒有複查紀錄** |
| **doubt-check** | **0.2.0** | **2026-11-11** | **dev** | **任務文件標記時必跑、寫程式之前跑；跨模型改成每次叫用問一次** |
| **requirements** | **1.7.1** | **2026-11-11** | **dev** | **source-driven：文件不全或矛盾時以 lock 版本 node_modules 型別為準；範例不等於唯一寫法，用編譯器實測** |
| **stack-review** | **1.7.1** | **2026-11-11** | **dev** | **common.md 框架出處：文件矛盾時出處須為 node_modules 檔案行號** |
| **stack-review** | **1.8.0** | **2026-11-11** | **dev** | **新增 `ios.md`、`react-native.md` 清單；偵測先判斷跨平台專案** |
| **requirements** | **1.7.2** | **2026-11-11** | **dev** | **風險清單加「共用元件／全站樣式」** |
| **doubt-check** | **0.3.0** | **2026-11-11** | **dev** | **觸發條件加共用元件／全站樣式；不判斷畫面是否一致** |
| **doubt-check** | **0.3.1** | **2026-11-11** | **dev** | **退場條件：3 張標記的卡都沒找到要修的問題就移除、併進 stack-review** |
| **stack-review** | **1.9.0** | **2026-11-11** | **dev** | **新增 `react-web.md`（React web／Next.js 清單）；子資料夾技術棧偵測；註明 plugin 版 `dev:code-reviewer`。起因：plugin 補測時 React 頁面只能用 common＋react-native 湊** |
| **requirements** | **1.7.3** | **2026-11-11** | **dev** | **叫 grilling 時註明 plugin 名稱 `core:grilling`** |
| **doc-update** | **1.3.1** | **2026-11-11** | **dev** | **註明 retro 只能由使用者手動叫（disable-model-invocation）** |
| **project-documentation** | **2.2.2** | **2026-11-11** | **dev** | **bug-record 範本補必填的 `updated`、`source-commit`** |
| **figma-to-requirements** | **1.0.2** | **2026-11-11** | **dev** | **交棒時註明 plugin 名稱 `dev:requirements`** |
| **flutter-ui-compare** | **0.1.1** | **2026-11-11** | **dev** | **新增（0.1.0）：網頁與 Flutter Web 並排量測比對；0.1.1 畫面清單要含頁面外框。Claude 專屬，備份 `dev/flutter-ui-compare/`** |
| **requirements** | **1.8.0** | **2026-11-13** | **dev** | **薄入口：可信度判斷、框架用法、後端契約同步移到 `references/`（slc 借鑒 #3）** |
| **stack-review** | **1.10.0** | **2026-11-13** | **dev** | **薄入口：reviewer 呼叫範本、spec 提示、摘要格式、技術棧範例移到 `references/`** |
| **doc-update** | **1.4.0** | **2026-11-13** | **dev** | **沉澱提議編號 `S-YYYYMMDD-n`、記憶附查證、單向門判準（slc 借鑒 #5、#7、#8）** |
| **anti-ai-look** | **0.1.0** | **2026-11-13** | **design** | **新增：去 AI 味檢查清單（含 icon 規格）；試用中** |
| **design-review** | **0.1.0** | **2026-11-13** | **design** | **新增：唯讀畫面 review，規格／去 AI 味／使用三軸；試用中** |
| **design-md-init** | **0.1.0** | **2026-11-13** | **design** | **新增：建立 DESIGN.md（色彩、字型、間距、圓角、元件、icon）；試用中** |
| flutter-b2b-documentation | 1.0.0 | 無記錄 | dev | 已由 project-documentation 取代 |
| **project-documentation** | **2.0.0** | **2026-04-28** | **dev** | **Spring Boot 完整支援；新增 Bug 修復紀錄、Widget 元件文件；kebab-case 命名；frontmatter 規範** |
| doc-generator | 1.0.0 | 無記錄 | dev | |
| multi-tool-coordination | 1.0.0 | 無記錄 | dev | 人工操作指南；執行型版本見 ai-pair |
| context-sharing | 1.0.0 | 2025-01-28 | dev | |
| dev-doc-organizer | 1.0.0 | 無記錄 | dev | |
| **ai-pair** | **4.3.6** | **2026-06-26** | **dev** | **環境相容性：無 `TeamCreate`/`TeamDelete` 時改用 Bash 直呼 CLI + Agent subagent 等效流程（實測 PASS）；承 v4.3.5 Copilot `-p` 傳遞修正（存檔：`ai-pair-main-v4.3.6/`）** |
| **ai-pair-v4-test** | **4.1.0** | **2026-05-14** | **dev** | **v4 測試分支（Phase 1 驗證中）；v4.1 校正誤判 2 項、新增缺口 4 項** |
| **figma-to-flutter** | **1.0.0** | **2026-03-18** | **dev** | **Figma 截圖 → Flutter UI 代碼（B2B 專屬，路徑：`dev/figma-to-flutter/`）** |
| **b2b-manager-onboarding** | **1.1.0** | **2026-08-25** | **dev** | **b2b-manager 新人上手導覽（決策樹路由 + 5 份 reference，仿 ECPay skill 架構）；專案專屬不可共用，存檔於 `dev/b2b-manager-onboarding/`，目前未安裝** |
| **sanlong-pay-onboarding** | **1.0.0** | **2026-08-25** | **dev** | **sanlong（山隆 PAY，iOS+Android APP）新人上手導覽；同架構但內容全異（手機 APP／自製 SLRouter／單一大型 SLController）。基準 `main@190038a9`；事實面已逐條驗證，自動觸發與實跑 build 未驗。存檔於 `dev/sanlong-pay-onboarding/`，目前未安裝** |
| **multiagent-handoff** | **0.6.0** | **2026-10-21** | **dev** | **跨 AI agent 接力（save／resume／delegate／report／review＋`--run`）；分派基準含未 commit 修改、以任務單狀態判斷成敗。實戰 SSGS-14167 通過（Copilot＋Codex 依序派工）。v0.5.0 由 handoff 改名。作用中本體 `~/.agents/skills/multiagent-handoff/`，備份 `dev/multiagent-handoff/`** |
| **mattpocock-skills（外部）** | **上游 5beb35b** | **2026-11-09** | **dev** | **Matt Pocock 7 個（grilling、grill-me、diagnosing-bugs、tdd、pr、writing-for-agents、retro）搬到 `~/.agents/skills/` 共用；MIT；tdd 有本機修改。備份 `dev/mattpocock-skills/`** |
| media-processor | 2.0.0 | 2025-12-31 | general | |
| sign-off-generator | 1.0.0 | 2026-01-06 | general | |
| document-translator | 1.0.0 | 無記錄 | general | |
| translategemma-translator | 1.1.0 | 無記錄 | general | |
| discussion-organizer | 1.0.0 | 2026-03-12 | general | |
| cross-platform-archive-agent | 1.0.0 | 2026-03-03 | general | |
| **point-reading-diy** | **0.4.0** | **2026-10-21** | **general** | **✅ 可用（測試版）、未安裝：卡米點讀筆 DIY 點讀包（切檔 → 辨識 → 審核 → 對應內容貼 → `pack.py` 打包 DAB）；打包流程完成、Dear Zoo 實測成功（`001-1-DearZoo.dab`，18 段全數可點）。存檔於 `point-reading-diy/`** |
| **knowledge-organizer** | **1.6.1** | **2026-08-13** | **pkm** | **TBRC 四層框架、資產化價值公式；.md 標記改回 frontmatter status** |
| **daily-brief-generator** | **1.5.0** | **2026-08-13** | **pkm** | **五區塊每日簡報、SCQA 建議行動；raw .md 判斷改回只看 frontmatter** |
| **wiki-health-check** | **1.8.0** | **2026-09-03** | **pkm** | **七項健康檢查；精粹過時改用來源清單集合差（廢止 glob 總數比大小／會假陰性）、連結掃描先剝程式碼區塊、須先讀前次報告並覆核舊矛盾** |
| **raw-pipeline** | **1.9.1** | **2026-08-13** | **pkm** | **三 Agent 軟編排；標記制度改分流（.md frontmatter／非 md 旁車標記）** |
| **knowledge-synthesizer** | **1.0.0** | **2026-05-13** | **pkm** | **CAVE 框架精粹（共識/視角/缺口/精華）；同主題 3 篇以上使用** |
| **alignment-check** | **1.0.0** | **2026-05-22** | **pkm** | **wiki 補充資料段落歸屬對齊檢查；找出放錯位置的內容並建議搬移** |
| **knowledge-elevation** | **1.1.0** | **2026-05-22** | **pkm** | **三層昇華：E 層加深 / meta-synthesis → wiki/concepts/** |
| obsidian-second-brain | — | — | **pkm** | Karpathy LLM Wiki 進化版；自動維護 Vault |
| scientific-brainstorming | — | — | **pkm** | 開放式研究腦力激盪、跨學科連結探索 |
| **zerospec-skills** | **0.4.3** | **2026-05-08** | **dev** | **ZeroSpec AI 文件協作系統；含 8 個指令（scan/build/spec/adr/sa/update/audit/智慧入口）；新增驗收自我測試規範** |
