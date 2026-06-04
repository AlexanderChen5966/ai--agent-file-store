# AI 驅動 SDD 框架比較與整合分析

> 建立日期：2026-05-08
> 分析對象：ZeroSpec、OpenSpec、SpecKit、BMAD-METHOD

---

## 一、四套框架定位總覽

### 核心回答的問題

| 工具 | 回答的問題 |
|---|---|
| **ZeroSpec** | 「這個專案的 AI 工具需要知道什麼？」 |
| **OpenSpec** | 「這個功能要做什麼，做完後怎麼歸檔？」 |
| **SpecKit** | 「這個產品從構想到上線要怎麼治理？」 |
| **BMAD-METHOD** | 「這個系統要怎麼讓多個 AI 角色協作完成？」 |

### 層次關係

```
Layer 0 — ZeroSpec（專案 AI 導覽基礎建設）
  └─ AGENTS.md：告訴所有 AI 工具「這個專案是什麼、有哪些規則」
  └─ 先裝好，其他框架才能在上面正確運作

Layer 1 — 開發工作流框架（三選一或組合）
  ├─ OpenSpec    輕量、迭代、per-feature 規格
  ├─ SpecKit     企業級、五階段、全面治理
  └─ BMAD        多 Agent 角色協作、完整生命週期
```

**ZeroSpec 是環境層**，其他三套是**工作流層**。

---

## 二、各框架詳細說明

### ZeroSpec
- **定位**：AI 文件協作系統，生成並維護 `AGENTS.md` 作為所有 AI 工具的單一導覽入口
- **時間軸**：持續同步（程式碼實作後更新）
- **核心產出**：`AGENTS.md`、SPEC（API 合約）、ADR（架構決策）、SA（系統快照）
- **文件對象**：AI coding agent（Claude、Gemini、Copilot 等）
- **主要指令**：`/zerospec:build`、`/zerospec:spec`、`/zerospec:adr`、`/zerospec:update`、`/zerospec:audit`
- **參考**：[官方部落格](https://coreynote.life/posts/2026/04/zerospec/)、[GitHub](https://github.com/corey924/ZeroSpec/blob/main/README.zh-TW.md)

### OpenSpec
- **定位**：輕量級規格層，讓人類與 AI 在寫程式碼前對需求達成共識
- **時間軸**：功能開發前（propose → apply → archive 三階段）
- **核心產出**：`proposal.md`（為什麼做）、`specs/`（需求場景）、`design.md`（技術方案）、`tasks.md`（實作清單）
- **文件結構**：每個功能變更有獨立資料夾，完成後歸檔至 `openspec/changes/archive/`
- **哲學**：流動而非僵化、迭代而非瀑布、為 brownfield 而建
- **支援工具**：25+ AI 工具與 IDE（Claude、ChatGPT、VS Code、GitHub Copilot 等）
- **參考**：[GitHub](https://github.com/Fission-AI/OpenSpec)

### SpecKit
- **定位**：企業級規格驅動開發框架，將規格轉為可執行的實作依據
- **時間軸**：五階段從需求到實作（強制門檻）
- **五階段**：
  1. Constitution（專案原則與治理）
  2. Specify（需求與用戶故事）
  3. Plan（技術方案與架構決策）
  4. Tasks（可執行任務分解）
  5. Implement（AI 輔助執行）
- **核心產出**：Constitution、Specification、Plan、Task Breakdown
- **強項**：組織治理、企業合規、0-to-1 新專案
- **參考**：[GitHub](https://github.com/doggy8088/spec-kit)

### BMAD-METHOD
- **定位**：多 Agent 敏捷開發方法論，以 19+ 專業角色 Agent 協作完成整個開發生命週期
- **時間軸**：四階段完整生命週期（分析 → 規劃 → 解決方案 → 實施）
- **核心設計**：
  - 每個 Agent 定義在單一 Markdown 文件（Agent-as-Code）
  - Scale-Adaptive Intelligence：依專案複雜度自動調整（L0～L4）
  - Manifest System：文件 SHA256 版本控制
  - Party Mode：多 Agent 同一會話協作
- **代表 Agent**：Business Analyst、Product Manager、Architect、Developer、QA Architect、Scrum Master 等
- **`project-context.md`**：專案「憲法」，確保所有 Agent 遵循一致規則
- **參考**：[GitHub](https://github.com/bmad-code-org/BMAD-METHOD)

---

## 三、完整比較表

| 維度 | ZeroSpec | OpenSpec | SpecKit | BMAD |
|---|---|---|---|---|
| **定位** | 專案 AI 導覽基礎 | 輕量迭代規格 | 企業治理規格 | 多 Agent 開發方法論 |
| **時間軸** | 持續同步（程式碼後） | 功能前 + 歸檔 | 功能前 + 治理 | 全生命週期 |
| **文件對象** | AI coding agent | 開發者 + AI | 開發者 + PM | 多角色 Agent 團隊 |
| **核心產出** | AGENTS.md / SPEC / ADR / SA | proposal / specs / design / tasks | Constitution / PRD / Plan / Tasks | PRD / 架構 / User Story / 代碼 |
| **Agent 設計** | 無內建 Agent | 無內建 Agent | 無內建 Agent | 19+ 專業角色 Agent |
| **企業就緒性** | 中（文件治理） | 低～中 | 高 | 高 |
| **學習曲線** | 低 | 低 | 中 | 高 |
| **適用規模** | 任何規模 | 個人到中型 | 中型到大型 | 中型到企業 |
| **與 AI 關係** | AI 讀文件導覽 | AI 協助規格與實作 | AI 解釋規格生成代碼 | AI 扮演專業角色 |

---

## 四、時間軸對比

```
需求討論          規格定義          設計決策          實作          文件同步

             ←── BMAD（全生命週期，四階段）──────────────────────→

             ←── SpecKit（五階段，強制門檻）──────────────────────→

             ←── OpenSpec（propose）──→ apply ──→ archive
                                                          ↓
                                                  ZeroSpec 收尾
                                              （/spec、/adr、/update）

Layer 0: ZeroSpec AGENTS.md ────────────────────────────────────── 持續維護
```

---

## 五、SPEC 概念的重要區別

OpenSpec 的 `specs/` 和 ZeroSpec 的 SPEC 文件名稱相近，但性質完全不同：

| | OpenSpec `specs/` | ZeroSpec SPEC |
|---|---|---|
| **時機** | 實作前（意圖） | 實作後（現實） |
| **內容** | 需求場景、用戶故事 | API 合約、DTO、業務規則 |
| **維護者** | 開發者 + PM | AI agent 協助維護 |
| **生命週期** | 功能完成後歸檔 | 長期維護、隨程式碼更新 |

---

## 六、推薦組合方式

### 組合 A：ZeroSpec + OpenSpec（輕量日常開發）

**適合**：迭代快速的中小型專案、App11 這類型的維護專案

```
ZeroSpec（Layer 0）
  AGENTS.md 說明專案規則、硬體限制、禁止事項

每個 bugfix / feature 前
  OpenSpec → /opsx:propose → /opsx:apply → /opsx:archive

實作完成後
  /zerospec:spec   更新 API 文件
  /zerospec:update 同步 AGENTS.md
```

---

### 組合 B：ZeroSpec + SpecKit（新專案，需要組織治理）

**適合**：有 PM 參與的產品型專案、需要合規文件的企業專案

```
ZeroSpec（Layer 0）
  AGENTS.md = SpecKit Constitution 的 AI 可讀映射

SpecKit（Layer 1）
  Constitution → Specify → Plan → Tasks → Implement

實作完成後
  /zerospec:spec   API 合約落地
  /zerospec:adr    Plan 決策歸檔
```

---

### 組合 C：ZeroSpec + BMAD（複雜系統，多 Agent 協作）

**適合**：大型系統、需要多角色協作審查、從零到一的複雜產品

```
ZeroSpec（Layer 0）
  AGENTS.md 提供 BMAD 各角色 Agent 的專案上下文
  ⚠️ BMAD 的 project-context.md 與 AGENTS.md 職責重疊
     建議：以 AGENTS.md 為主，project-context.md 改為 @AGENTS.md 引用

BMAD（Layer 1）
  Business Analyst → PM → Architect → Developer → QA
  四階段角色協作（L0～L4 複雜度自動調整）

每個 Sprint 結束
  /zerospec:spec   API 合約
  /zerospec:adr    架構決策
  季度維護 → /zerospec:update + /zerospec:audit
```

---

## 七、選擇建議

| 情境 | 建議組合 |
|---|---|
| 現有專案日常維護（如 App11） | ZeroSpec + OpenSpec |
| 新產品從零開始、有 PM 參與 | ZeroSpec + SpecKit |
| 複雜系統、需要多角色 AI 審查 | ZeroSpec + BMAD |
| 最輕量、只需 AI 文件導覽 | ZeroSpec 單獨使用 |
| 企業級 + 多 Agent + 治理 | ZeroSpec + SpecKit + BMAD |

---

## 參考連結

| 工具 | GitHub | 其他資源 |
|---|---|---|
| ZeroSpec | [README.zh-TW.md](https://github.com/corey924/ZeroSpec/blob/main/README.zh-TW.md) | [官方部落格](https://coreynote.life/posts/2026/04/zerospec/) |
| OpenSpec | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | — |
| SpecKit | [doggy8088/spec-kit](https://github.com/doggy8088/spec-kit) | [文件](https://github.github.io/spec-kit/) |
| BMAD-METHOD | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | [官方文件](https://docs.bmad-method.org/) |
