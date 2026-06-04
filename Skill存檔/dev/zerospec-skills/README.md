# ZeroSpec Skills

ZeroSpec Skills 是將 ZeroSpec Prompt Pack 改造為 [Claude Code Skills](https://code.claude.com/docs/en/skills) 的實作，讓你不再需要手動複製貼上 Prompt，直接用指令觸發完整的 SDD 文件工作流程。

**版本**：v0.5.2（同步至官方 v0.5.2，含 DRIFT / IMPL / Post-Edit Self-Check）

---

## 安裝

將 `skills/` 下的各資料夾複製到 Claude Code 的 skills 目錄：

```bash
# 安裝全部
cp -r zerospec-skills/zerospec* ~/.claude/skills/

# 或只安裝特定 skill
cp -r zerospec-skills/zerospec ~/.claude/skills/
cp -r zerospec-skills/zerospec-scan ~/.claude/skills/
```

安裝後重啟 Claude Code 即可使用。

---

## 可用指令

| 指令 | 說明 | 寫入檔案 |
|---|---|---|
| `/zerospec` | 智慧入口，自動偵測狀態並執行對應步驟 | 依狀態而定 |
| `/zerospec:scan` | 掃描專案，產出結構化分析報告 | ❌ 不寫檔 |
| `/zerospec:build` | 生成 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`docs/README.md` | ✅ |
| `/zerospec:spec` | API 新增或行為變更時，生成 SPEC 文件 | ✅ `docs/spec/` |
| `/zerospec:adr` | 做出跨模組技術決策時，生成 ADR 文件 | ✅ `docs/adr/` |
| `/zerospec:sa` | 需要全系統快照時，生成 SA 文件 | ✅ `docs/analysis/` |
| `/zerospec:impl` | 複雜多模組實作（3+ Controller 或 2+ SPEC）護欄 | ✅ 程式碼 + SPEC |
| `/zerospec:drift` | 驗證 SPEC 是否仍與程式碼一致 | ❌ 不寫檔 |
| `/zerospec:update` | 專案演進後，同步更新文件 | ✅ |
| `/zerospec:audit` | 量化評估 AGENTS.md 品質（9 維度 + Actionable Fix） | ❌ 不寫檔 |

---

## 標準工作流程

### 首次使用（新專案）

```
/zerospec:scan
    └─ 掃描分析，不寫任何檔案
         └─ /zerospec:build
              └─ 生成 AGENTS.md + CLAUDE.md + GEMINI.md + docs/README.md
                   └─ /zerospec:sa          ← Brownfield 專案建議
                        └─ /zerospec:spec   ← 第一個 API 完成後開始
```

> 不確定要從哪裡開始？直接執行 `/zerospec`，它會自動偵測狀態並引導你。

### 日常開發

| 觸發情境 | 執行指令 |
|---|---|
| 新增或修改 API endpoint | `/zerospec:spec` |
| 做出跨模組技術決策 | `/zerospec:adr` |
| 複雜多模組實作（3+ Controller 或 2+ SPEC） | `/zerospec:impl` |
| 發布前或重構後驗證 SPEC 正確性 | `/zerospec:drift` |
| 專案進入新里程碑 | `/zerospec:sa` |
| 每月/每季定期維護 | `/zerospec:update` |
| AGENTS.md 越來越長或 AI 重複違規 | `/zerospec:audit` |

---

## `/zerospec` 智慧入口

不知道當前應該執行哪個步驟時，使用 `/zerospec`。它會自動偵測以下狀態：

| 狀態 | 判斷條件 | 自動執行 |
|---|---|---|
| A | `AGENTS.md` 不存在 | scan → build（含所有橋接檔） |
| B | `AGENTS.md` 存在，但 `CLAUDE.md`/`GEMINI.md`/`docs/README.md` 缺少或設定錯誤 | 補齊缺少的檔案 |
| C | 基礎文件完整，SPEC < 8 份 | 輸出狀態摘要 + 根據 git 活動給建議 |
| D | SPEC ≥ 8 份且無 `docs/spec/README.md` | 建立 SPEC 子索引 |
| E | `AGENTS.md` 超過 180 天未更新 | 執行 audit，再建議 update |

---

## 文件架構

Skills 產生的文件遵循以下架構（基於 [cross-tool-ai-setup.md](cross-tool-ai-setup.md) 的跨工具設計原則）：

```
AGENTS.md               ← 單一維護點，所有 AI 工具共用的規則
CLAUDE.md               ← @AGENTS.md（Claude Code 橋接，可加專屬補充）
GEMINI.md               ← @./AGENTS.md（Gemini CLI 橋接，可加專屬補充）
docs/
├── README.md           ← 文件治理中樞（分類規則、命名規範、AI Auto-Trigger Heuristics）
├── spec/               ← SPEC-{3碼}_{描述}.md
├── adr/                ← ADR-{3碼}_{描述}.md
└── analysis/           ← SA-{3碼}_{描述}.md
```

`CLAUDE.md` 和 `GEMINI.md` 透過 `@import` 引用 `AGENTS.md`，確保規則單一維護、自動同步，不需手動複製。

---

## 各 Skill 觸發條件快查

### `/zerospec:spec`
✅ 觸發：新增 API endpoint、修改 Request/Response、變更權限規則、行為變更的 bug fix
❌ 不觸發：純內部重構、不影響外部行為的修改

### `/zerospec:adr`
✅ 觸發：架構分層策略選擇、非此即彼技術決策（Kafka vs RabbitMQ）、跨模組共用元件設計
❌ 不觸發：新增 CRUD API、調整 TTL、簡單 bug fix

### `/zerospec:sa`
✅ 觸發：新里程碑、架構重大變更、新成員 onboarding、Brownfield 初始化

### `/zerospec:impl`
✅ 觸發：任務預計觸及 3+ Controller、影響 2+ SPEC、跨模組功能開發、大規模重構改變外部行為
❌ 不觸發：單一 controller / 單一 SPEC 的簡單任務（使用 AGENTS.md Post-Edit Self-Check 即可）

### `/zerospec:drift`
✅ 觸發：發布前驗證、大規模重構後、每月/每季檢查、懷疑 SPEC 與程式碼不同步
❌ 不觸發：已確定要直接更新 SPEC 的情況（直接用 `/zerospec:spec`）

### `/zerospec:update`
✅ 觸發：新增/移除業務模組、框架 Major/Minor 版本升級、架構層異動、定期維護

### `/zerospec:audit`
✅ 觸發：AGENTS.md 越來越長、AI 重複違反同一條規則、定期品質檢查（含 9 維度分析 + Actionable Fix List）

---

## 前置條件說明

除 `scan`、`audit`、`drift` 之外，所有 skill 執行前都會確認以下檔案：

| 檔案 | 用途 |
|---|---|
| `AGENTS.md` | 所有規則的單一來源 |
| `CLAUDE.md` | Claude Code 橋接（需含 `@AGENTS.md`） |
| `GEMINI.md` | Gemini CLI 橋接（需含 `@./AGENTS.md`） |
| `docs/README.md` | 文件治理規則與索引（含 AI Auto-Trigger Heuristics） |

若缺少任一檔案，skill 會列出缺少清單並提示執行 `/zerospec:build` 補齊。

---

## 與原 ZeroSpec Prompt Pack 的對應關係

| 原 Prompt Pack | Skill 指令 |
|---|---|
| `prompts/INIT-SCAN.md` | `/zerospec:scan` |
| `prompts/INIT-BUILD.md` | `/zerospec:build` |
| `prompts/SPEC.md` | `/zerospec:spec` |
| `prompts/ADR.md` | `/zerospec:adr` |
| `prompts/SA.md` | `/zerospec:sa` |
| `prompts/IMPL.md` | `/zerospec:impl` |
| `prompts/DRIFT.md` | `/zerospec:drift` |
| `prompts/UPDATE.md` | `/zerospec:update` |
| `prompts/AUDIT.md` | `/zerospec:audit` |
| （新增）智慧入口 | `/zerospec` |

Skills 內容直接從對應的 Prompt Pack 複製並加入跨工具整合（CLAUDE.md/GEMINI.md）、前置狀態確認、Self-Review Protocol。

---

## 相較官方 Router Skill 的額外功能

本 skills 套件在官方基礎上增加：

| 功能 | 說明 |
|---|---|
| A/B/C/D/E 狀態自動偵測 | `/zerospec` 入口自動判斷專案所在階段並直接執行 |
| CLAUDE.md / GEMINI.md 整合 | `/zerospec:build` 自動生成跨工具橋接檔 |
| 前置條件檢查表 | 每個子 skill 執行前驗證必要檔案存在且設定正確 |
| ZeroSpec 狀態摘要 | 結構化輸出目前文件完整度 |
| Self-Review Protocol | 與官方一致的 9 項靜默驗證清單 |

---

## 參考資料

- [ZeroSpec 官方部落格](https://coreynote.life/posts/2026/04/zerospec/)
- [ZeroSpec GitHub README（繁體中文）](https://github.com/corey924/ZeroSpec/blob/main/README.zh-TW.md)
- [跨工具 AI 協作設定](cross-tool-ai-setup.md)
