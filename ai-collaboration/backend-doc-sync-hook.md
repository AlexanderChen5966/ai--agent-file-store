# 跨 repo 文件同步 hook：b2b-backend ↔ b2b-manager

**建立日期：** 2026-07-30
**最後改寫：** 2026-08-04（架構簡化為「兩個 SessionStart」，移除上游推送）
**最後更新：** 2026-10-19（② 改為自動偵測最新版契約複本；補 ①a「版本未變」分支說明）
**狀態：** ✅ 運作中，已完成真實流程驗證
**涵蓋 repo：** `b2b-backend`（上游）、`b2b-manager`（下游）

---

## 這解決什麼問題

`b2b-backend/docs/` 的三份參考文件（`API_DOCUMENTATION.md` / `ARCHITECTURE.md` /
`UPDATE_RECORD.md`）**由人手動以 `project-documentation` 產出**，
b2b-manager 的 `/requirements` 與 `docs/shared/` 消費它們描述的契約。

過去兩端沒有連動，靠人記得。2026-07-29 因此出過 P0：後端新增
`EntityType.REPORT_SCHEDULE`，前端 enum 沒同步 → 操作紀錄頁整頁空白。
**這類漂移在前端沒有任何 diff，code review 不可能發現。**

---

## 架構：兩個 `SessionStart`，各守一個缺口

| repo | hook | 回答什麼問題 | 沒事時 |
|---|---|---|---|
| **b2b-backend** | `SessionStart` → `check_docs_lag.py` | 「`docs/` 落後程式碼了嗎？」→ 催你跑 `project-documentation` | 靜默 |
| **b2b-manager** | `SessionStart` → `contract_drift_check.py` | 「後端文件更新了嗎？」→ 我立即同步 `docs/shared/` | 說「不需要做任何事」|

```
後端工程師改程式碼
      ↓
開 b2b-backend → 🤖「docs/ 落後 N 個 commit，其中 M 個契約相關」
      ↓
你跑 project-documentation              ← 唯一手動環節
      ↓
開 b2b-manager → 🤖 ①a「後端文件已更新」→ 我同步 docs/shared/ → --ack
```

**不論先開哪一邊，都會被導向對的下一步。**

### 為什麼「產出文件」不自動化

1. **長操作**——實測 3 分 56 秒，每次開 session 都跑不合理
2. **會做判斷**——`project-documentation` Step 0 路徑 4 明訂「先列出將被移除的內容給使用者確認」
3. **會改寫既有文件**——未經確認就覆蓋人工修正過的內容是風險

→ hook 只**偵測並提示**，產出由你決定何時執行。

---

## 📌 設計沿革：為什麼不是「上游推送」

初版（2026-07-30 ~ 08-04）是 **b2b-backend `Stop` hook → 寫 queue 檔 → 下游讀**，
並曾嘗試以背景 `claude -p` 自動更新下游文件（`AUTO_INVOKE`）。**已於 2026-08-04 退役。**

當時主張「上游 hook 不可省」，理由是：

> 「commit 範圍只有在變更當下捕捉得到——`source-commit` 一被覆寫，舊值就消失了。」

🔴 **那個論點是錯的。** 那是「把 state 存在上游」造成的限制，不是事實。
**state 存在消費端**（`b2b-manager/.claude/.backend_docs_state.json`）就沒有這個問題——
「上次處理到哪」由需要知道的一方保存，commit 範圍與版本差異事後都重建得出來。
兩個 repo 在同一台機器，b2b-manager 直接讀 `~/GitLab/b2b-backend/docs/` 即可。

**留下的教訓**：先問「這個資訊該由誰保存」，再決定要不要建推送機制。

`notify_downstream.py` 保留但標記退役（可逆性優先）。若日後兩個 repo 不在同一台機器，
把 `hooks.Stop` 加回去即可復用。

---

## 檔案與職責

| 檔案 | Repo | 用途 |
|---|---|---|
| `.claude/scripts/check_docs_lag.py` | backend | 偵測 `docs/` 是否落後程式碼 |
| `.claude/settings.local.json` → `hooks.SessionStart` | backend | 觸發點 |
| `.claude/scripts/contract_drift_check.py` | manager | 五節報告 ①a／①b／②③④⑤ ＋ `--ack` |
| `.claude/settings.local.json` → `hooks.SessionStart` | manager | 觸發點 |
| `.claude/.backend_docs_state.json` | **manager** | **state：上次處理到的後端文件狀態**（hash／版本／commit）|
| `docs/shared/_backend_sync_log.md` | manager | 同步歷程 |
| ~~`.claude/scripts/notify_downstream.py`~~ | backend | ⛔ 已退役，未被任何 hook 呼叫 |

---

## 報告的五個小節

| 節 | 問題 | 資料來源 |
|---|---|---|
| **①a** | 後端文件更新了嗎（**主驅動**）| 後端 `docs/*.md` hash vs 消費端 state |
| **①b** | 後端文件落後程式碼嗎 | `UPDATE_RECORD` 最新條目的 commit 範圍 vs 後端 HEAD |
| ② | 前端複本 `docs/api/api_documentation_vN.md`（**自動取版本號最大者**）過期嗎 | 其 `source-commit` vs 後端 HEAD |
| ③ | 前後端 enum 差集 | 直接比對兩邊原始碼 |
| ④ | 哪些任務文件受影響 | `docs/shared/*.md` 的 `後端依賴` 宣告 |
| ⑤ | 有沒有忘記整併的待確認區塊 | 掃 `docs/shared/*.md` |

### 🔴 ①a 的輸出是**指令**，不是資訊

偵測到更新時，報告會列出「👉 要執行的動作」並明說**立即執行、不必等使用者開口**。

> 📌 這是實測改出來的：舊版只寫「依同步模式處理」，讀起來像背景資訊，
> 結果 session 開始後沒人動作，使用者得追問「為什麼沒更新」。

### ①a 的兩種「已更新」

| 情況 | 報告怎麼說 | 要做什麼 |
|---|---|---|
| 版本號或 `UPDATE_RECORD` 最新條目有變 | 🔴 列出同步步驟（讀變更 → 更新 `docs/shared/` → 寫 sync log → `--ack`）| 照步驟立即執行 |
| hash 變了，但版本號與最新條目都沒變 | ⚪「多半只是日期／格式更正」| 確認無實質差異後直接 `--ack` |

> 第二種情況仍可能藏實質變更（見「已知限制」2：產出端忘了 bump 版本號），所以是「確認後」才 ack，不是無條件 ack。

### ② 的契約複本自動偵測（2026-10-19）

`REF_DOC` 由 `latest_ref_doc()` 決定：掃 `docs/api/` 下符合 `api_documentation_v<數字>.md` 的檔案，
**以數字比較**取最大者（`v10` > `v9`，不是字串排序）。報告標題會印出實際比對的檔名。

> 📌 改前是寫死 `v17`：後端文件每升一版都要手動改腳本，漏改時 ② 會**默默比對舊檔**，
> 報告看起來正常但結論是錯的。
> ⚠️ 新版文件必須照命名規則（`api_documentation_v18.md`），`_draft`、`.bak` 等變體不會被選中——這是刻意的。

### `--ack`

處理完務必執行 `python3 .claude/scripts/contract_drift_check.py --ack` 更新基準，
否則下次開 session 會重複提醒同一批變更。這句警語也印在報告裡。

### ③ 的風險分級

「前端缺後端已有的值」依**在哪裡被解析**分三級，不是有沒有被解析：

| 級 | 條件 | 後果 |
|---|---|---|
| 🔴 解析風險 | **response DTO** 的非 nullable `$enumDecode` | 收到未知值 → 整批解析失敗、整頁空白 |
| 🟡 次要 | 只在 **request DTO** | 前端只 `toJson()` 送出，`fromJson` 實務上不會被呼叫 |
| ⚪ 功能缺口 | 不經 json_serializable | UI 下拉／本地 switch key，缺值不會壞畫面 |

> ⚠️ 這個區別容易搞錯：`FileType` 確實有一處非 nullable decode，但在 request DTO 裡，不是風險。

---

## ✅ 已驗證的事實（實測，非推論）

| 項目 | 結果 |
|---|---|
| `SessionStart` 的 stdout 是否進 context | ✅ **會**——報告完整出現在 session 開頭 |
| `Stop` hook 的 stdout 是否顯示給使用者 | ❌ **不顯示**（退役前實測）——只寫 log |
| 從 hook 內以 `Popen` 啟動 `claude -p` | ✅ 不被擋，完整跑完分析 |
| 該背景程序能否寫檔 | ❌ **不能**——非互動 session 所有寫入被權限層拒絕 |
| 效能 | backend lag 檢查 ~60ms／manager 全報告 ~200ms |

### 🔴 「自動寫檔」這條路已確認走不通

背景 `claude -p` 可以做完完整比對，但**改不了任何檔案**。要真全自動得加權限旗標，
等於授權無人程序寫你的檔案——`requirements` v1.4.0 的硬邊界只是 prompt 層約束，
**真正的護欄是權限層**。刻意未採用。

---

## ⚠️ 已知限制

1. **①b 依賴 changelog 的 commit 範圍**。`UPDATE_RECORD` 最新條目若沒有
   `commits <起> ~ <迄>`，①b 就失效（會提示補上）。
   → 這是形式 B（專案自有版本慣例）唯一的可追溯欄位，
   `project-documentation` 的 `frontmatter-spec.md` 已列為必要項。

2. **版本號的可信度依賴產出端**。若 `project-documentation` 忘記 bump 版本號，
   ①a 會誤判成「僅日期變更」。**這是信任問題不是能力問題**——無法機械驗證。

3. **④ 是 substring 比對**（`token in dep`）→ 短 token 會過度命中
   （enum 名 `Role` 會命中任何含 "Role" 的宣告）。**寧可誤報也不要漏**，但要知道有假陽性。

4. **② 的 pattern 曾漏報**。`CONTRACT_PATTERNS` 原本不含 `/configs/`，
   導致 `GlobalExceptionHandler.java` 完全不被列出——而那正是解除
   `export_empty_result_400.md` T1 阻塞的關鍵 commit。
   → 2026-08-04 補了 pattern，**並改為「未命中 pattern 的原始碼變動也要列出」**。
   **pattern 永遠追不完，所以「有東西被丟掉」必須看得見。**

5. **兩個 repo 的 `.claude/` 都在 `.gitignore`** → 整套機制**只存在這台機器**，
   換機器不會轉移，也不分享給團隊（腳本硬編 `~/GitLab/` 路徑）。**重建見文末。**

6. **只監看三份文件**（`WATCH_DOCS`）。後端新增其他參考文件要手動加。
   （前端側的契約複本則已自動偵測，見「② 的契約複本自動偵測」。）

7. **`後端依賴` 宣告缺失的任務文件無法路由**。2026-07-30 才加進 `requirements` skill，
   舊文件需補。已補：`page_route_permission_guard`／`report_auto_send_task`／
   `role_permission_sync_setting_gate`／`export_empty_result_400`。

---

## 故障排除

**開 session 沒看到任何輸出**

正常——兩邊都沒事時本來就靜默（backend）或只印「不需要做任何事」（manager）。
想確認 hook 還活著：

```bash
cd ~/GitLab/b2b-backend  && python3 .claude/scripts/check_docs_lag.py; echo "exit=$?"
cd ~/GitLab/b2b-manager  && python3 .claude/scripts/contract_drift_check.py | head -20
```

**一直重複提醒同一批變更**

忘了跑 `--ack`：

```bash
cd ~/GitLab/b2b-manager && python3 .claude/scripts/contract_drift_check.py --ack
```

**state 亂了 / 想重建基準**

```bash
rm ~/GitLab/b2b-manager/.claude/.backend_docs_state.json
cd ~/GitLab/b2b-manager && python3 .claude/scripts/contract_drift_check.py   # 首次執行只建基準
```

**hook config 不見了**

```bash
python3 -c "import json,io;print(json.load(io.open('.claude/settings.local.json'))['hooks'])"
```

**② 比對的不是最新那份契約複本**

看報告 ② 標題印的檔名。若不是預期的版本，檢查 `docs/api/` 下新檔是否符合
`api_documentation_v<數字>.md`（不可有 `_draft`、`-new` 等後綴）。

**想暫時停用**

移除 `.claude/settings.local.json` 的 `hooks` 段，或把 command 換成 `true`。腳本留著不影響。

---

## 🔧 重建清單（換機器 / 重裝時）

`.claude/` 與 `docs/` 都不進 git，**本文件就是重建指引**。

### 三個檔案

| 路徑 | 說明 |
|---|---|
| `~/GitLab/b2b-backend/.claude/scripts/check_docs_lag.py` | 上游偵測（`chmod +x`）|
| `~/GitLab/b2b-manager/.claude/scripts/contract_drift_check.py` | 下游偵測 ＋ 同步指令（`chmod +x`）|
| `~/GitLab/b2b-manager/docs/ai-collaboration/backend-doc-sync-hook.md` | 本文件 |

依賴的 skill：`project-documentation` v2.2.1+、`requirements` v1.4.0+（需含「後端契約同步模式」）。
兩者皆有存檔：`Desktop/紀錄文件資料夾/實驗用文件/Skill存檔/dev/`。

### 兩份 hook config

`~/GitLab/b2b-backend/.claude/settings.local.json`：

```json
"hooks": {
  "SessionStart": [{ "hooks": [{ "type": "command",
    "command": "python3 .claude/scripts/check_docs_lag.py || true" }] }]
}
```

`~/GitLab/b2b-manager/.claude/settings.local.json`：

```json
"hooks": {
  "SessionStart": [{ "hooks": [{ "type": "command",
    "command": "python3 .claude/scripts/contract_drift_check.py || true" }] }]
}
```

⚠️ **`|| true` 不可省**：偵測到項目時 exit 1，不加會被當成 hook 失敗。

### 重建後第一步

```bash
cd ~/GitLab/b2b-manager && python3 .claude/scripts/contract_drift_check.py
# 應輸出「⚙️ 首次執行，已建立基準（不觸發同步）」
```

**必須先跑這一步**，否則第一次真實觸發會把既有狀態全部誤判成新變更。

### 腳本內要確認的常數

- `check_docs_lag.py`：`CONTRACT_PATTERNS`
- `contract_drift_check.py`：`FE_REPO`／`BE_REPO`／`API_DIR`（`REF_DOC` 已自動偵測，不需手改）／`WATCH_DOCS`／
  `CONTRACT_PATTERNS`／`ALIAS`（前後端 enum 命名不一致對應表）

---

## 相關文件

- `docs/shared/_backend_sync_log.md` —— 每次同步的歷程與判定
- `docs/shared/enum_decode_hardening.md` —— ③ 節為何重要（含已修的 P0）
- `docs/api/api_documentation_vN.md`（最新版）—— 前端側的後端 API 複本
- `~/.claude/skills/requirements/SKILL.md` >「後端契約同步模式」—— 無人模式的硬邊界
- `~/notes/my-knowledge-base/rules/decision-framework.md` —— 五情境中「〔讀〕現況層」的定位
