---
name: zerospec
metadata:
  version: 0.5.2
description: ZeroSpec 智慧入口。自動偵測專案狀態並執行對應步驟。觸發時機：/zerospec、開始使用 ZeroSpec、不知道要執行哪個步驟、zerospec 初始化、查看 zerospec 狀態。
---

# ZeroSpec — 智慧入口

自動偵測目前專案狀態，判斷應執行哪個步驟，並直接執行。

---

## 使用說明

| 指令 | 用途 |
|---|---|
| `/zerospec` | **智慧入口**：自動偵測狀態，判斷並執行對應步驟 |
| `/zerospec:scan` | 掃描專案，產出分析報告（不寫檔） |
| `/zerospec:build` | 生成 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`docs/README.md` |
| `/zerospec:spec` | API 新增或行為變更時，生成 SPEC 文件 |
| `/zerospec:adr` | 做出架構決策時，生成 ADR 文件 |
| `/zerospec:sa` | 需要系統快照時，生成 SA 文件 |
| `/zerospec:impl` | 複雜多模組實作（3+ Controller 或 2+ SPEC）時的護欄 |
| `/zerospec:drift` | 驗證 SPEC 是否仍與程式碼一致（不寫檔） |
| `/zerospec:update` | 專案演進後，同步更新文件 |
| `/zerospec:audit` | 量化評估 AGENTS.md 品質（不寫檔） |

### 標準工作流程

```
首次使用
  └─ /zerospec:scan   → 掃描分析（不寫檔）
       └─ /zerospec:build  → 生成 AGENTS.md + docs/README.md
            └─ /zerospec:sa  → （Brownfield 專案建議）生成系統快照
                 └─ /zerospec:spec → 每次 API 新增或變更時執行

日常維護
  ├─ /zerospec:spec   → API 有新增或行為變更
  ├─ /zerospec:adr    → 做出跨模組技術決策
  ├─ /zerospec:impl   → 複雜多模組實作（3+ Controller 或 2+ SPEC）
  ├─ /zerospec:drift  → 發布前或重構後，驗證 SPEC 是否仍正確
  ├─ /zerospec:update → 專案演進，每月/每季同步
  └─ /zerospec:audit  → 評估 AGENTS.md 品質（可搭配 update 使用）
```

---

## 自動狀態偵測與執行

依序執行以下偵測步驟，判斷專案目前狀態，然後直接執行對應動作：

### Step 1：偵測專案狀態

檢查以下檔案是否存在且正確：

1. 根目錄是否有 `AGENTS.md`
2. 根目錄是否有 `CLAUDE.md`，且包含 `@AGENTS.md`
3. 根目錄是否有 `GEMINI.md`，且包含 `@./AGENTS.md` 或 `@AGENTS.md`
4. 根目錄是否有 `docs/README.md`
5. `docs/spec/` 下有多少個 `SPEC-*.md` 檔案
6. `docs/spec/README.md` 是否存在
7. 距上次 `AGENTS.md` 修改時間（用 git log 或檔案 mtime 估算）

### Step 2：判斷狀態並執行

根據偵測結果對應以下狀態，**直接執行**，不需要詢問確認：

---

#### 狀態 A：全新專案（AGENTS.md 不存在）

**判斷條件**：`AGENTS.md` 不存在

**執行動作**：
1. 告知使用者：「偵測到尚未初始化，開始執行 ZeroSpec 初始化流程。」
2. 執行 `/zerospec:scan` 的完整掃描邏輯
3. 掃描完成後，詢問使用者：「以上分析是否正確？確認後將生成 AGENTS.md、CLAUDE.md、GEMINI.md 與 docs/README.md。」
4. 使用者確認後，執行 `/zerospec:build` 的完整建立邏輯（含 Step 3.5 生成 CLAUDE.md 與 GEMINI.md）

---

#### 狀態 B：已有 AGENTS.md，但缺少橋接檔或 docs/README.md

**判斷條件**：`AGENTS.md` 存在，但以下任一缺少：
- `CLAUDE.md` 不存在或不包含 `@AGENTS.md`
- `GEMINI.md` 不存在或不包含 `@./AGENTS.md` / `@AGENTS.md`
- `docs/README.md` 不存在

**執行動作**：
1. 列出所有缺少的項目，告知使用者：「偵測到以下檔案缺少或設定不正確：{缺少清單}，補齊中。」
2. 針對缺少的檔案執行對應生成邏輯（沿用 AGENTS.md 現有內容，不重新詢問 C-class）：
   - 缺 `CLAUDE.md` → 生成含 `@AGENTS.md` 的橋接檔
   - 缺 `GEMINI.md` → 生成含 `@./AGENTS.md` 的橋接檔
   - 缺 `docs/README.md` → 重新掃描 A/B-class 資訊後生成

---

#### 狀態 C：基礎文件完整，日常開發中

**判斷條件**：`AGENTS.md`、`CLAUDE.md`（含 import）、`GEMINI.md`（含 import）、`docs/README.md` 皆正確存在，SPEC 數量 < 8

**執行動作**：
1. 輸出目前狀態摘要：

```
ZeroSpec 狀態摘要
─────────────────────────────
✅ AGENTS.md          已存在
✅ CLAUDE.md          已存在（含 @AGENTS.md）
✅ GEMINI.md          已存在（含 @./AGENTS.md）
✅ docs/README.md     已存在
📄 SPEC 文件          {n} 份（docs/spec/）
📄 ADR 文件           {n} 份（docs/adr/）
📄 SA 文件            {n} 份（docs/analysis/）
最後更新              {AGENTS.md 的 git 最後修改日期}
─────────────────────────────
```

2. 根據 git log 判斷近期活動，提供建議：
   - 若近 30 天有 Controller/API 相關異動 → 建議：「建議執行 `/zerospec:spec` 補齊 API 規格」
   - 若 AGENTS.md 超過 90 天未更新且有明顯程式碼異動 → 建議：「建議執行 `/zerospec:update` 同步文件」
   - 若無明顯異動 → 建議：「文件狀態良好，無立即需要的動作」

---

#### 狀態 D：SPEC 數量達門檻，需建立子索引

**判斷條件**：SPEC 文件 ≥ 8 份 且 `docs/spec/README.md` 不存在

**執行動作**：
1. 告知使用者：「SPEC 文件已達 8 份，建議建立子索引以利導覽。」
2. 直接執行 `/zerospec:update` 的 Step 3.5 子索引建立邏輯

---

#### 狀態 E：文件嚴重落差（長時間未更新）

**判斷條件**：`AGENTS.md` 超過 180 天未更新（透過 git log 確認）

**執行動作**：
1. 告知使用者：「偵測到 AGENTS.md 已超過 6 個月未更新，建議先執行 AUDIT 再更新。」
2. 執行 `/zerospec:audit` 的完整審查邏輯
3. 審查完成後提示：「建議執行 `/zerospec:update` 根據上方報告更新文件。」

---

### Step 3：執行後輸出

每次執行完畢，在對話末尾輸出一行：

```
下一步建議：{根據目前狀態給出的下一個推薦指令，例如 /zerospec:spec}
```

## 規則

- 偵測到狀態後直接執行，不要詢問「是否要執行 XXX？」
- 狀態摘要保持簡潔，不超過 10 行
- 若同時符合多個狀態，優先處理編號較小的狀態（A > B > C > D > E）
- 狀態 B 的橋接檔缺少問題，若同時出現多個缺少項目，一次全部補齊，不分多次執行
- 所有版本號只寫 Major.Minor，不含 Patch

---

## Self-Review Protocol

每個 skill 執行完畢後，**靜默**套用對應的驗證清單。發現問題時先修正再輸出最終結果 — **不要把清單本身顯示給使用者**。

| Task | Self-Review Checklist |
| --- | --- |
| scan | ① 掃描結果與實際檔案系統一致 ② 未遺漏關鍵目錄或設定檔 ③ Greenfield/Brownfield 判斷有具體證據支持 |
| build | ① 輸出符合 ZeroSpec 結構（Quick Constraints / Domain Map / Commands） ② 無虛構的檔案路徑或指令 ③ 每項 SCAN 發現都已處理 |
| spec | ① 所有描述的端點/行為都已涵蓋 ② 無虛構的 request 或 response 欄位 ③ Changelog 格式與既有 SPEC 一致 |
| adr | ① 各方案優缺點客觀完整 ② 無遺漏的替代方案 ③ 結論邏輯上承接分析 |
| sa | ① 系統邊界與實際架構一致 ② 無遺漏的模組相依 ③ 停留在架構層級，不涉及實作細節 |
| impl | ① 受影響的程式碼區域和 SPEC 已在編碼前識別 ② `### Docs Impact` 出現在含程式碼異動的回覆末尾 ③ SPEC 更新/不更新的理由明確 |
| drift | ① 每個 DRIFTED 判定都引用具體檔案路徑或行號 ② CLEAN 判定未忽略不一致之處 ③ 嚴重程度等級有合理依據 |
| update | ① 變更反映實際程式碼演進 ② 不與既有文件內容矛盾 ③ 無段落膨脹（新增內容時舊內容已精簡） |
| audit | ① 總分與各維度分析一致 ② 每個修正建議都引用對應維度 ③ 無過高或過低評分 |
