# v5.0 首跑成效紀錄 — SSGS-12853

**執行日期：** 2026-07-30
**受測分支：** `feature/SSGS-12853`（報表自動寄送設定 + 角色權限同步）
**Review base：** `f3fa0cd7^1...f3fa0cd7^2`（該分支併入 main 的 54 檔，排除 generated/assets/lockfile 後 40 檔）
**流程：** v5.0 完整 review 路徑（explorer → manifest → Level 3 三 reviewer 並行 → 機械驗證）
**對照基準：** 2026-07-29 的 `stack-review`（結論：0 Critical、3 Warning、2 Suggestion，皆已修）

---

## 一、結論摘要

| 指標 | 結果 |
|---|---|
| 新發現的真實缺陷 | **10 個**（2 W + 1 W + 7 S），其中 **3 個 W 級為前次 stack-review 未涵蓋** |
| 捏造路徑 | **0**（10/10 findings 路徑經機械驗證真實存在） |
| 跨 repo 契約查證 | ✅ **實際發生**（claude-reviewer 讀取後端 Java 於另一分支） |
| 順帶暴露的 v5.0 規格缺口 | **2 個**（已修正並寫回 skill，見 §五） |
| Ground truth 偵測 | ❌ **0/3 reviewer 找到**預埋的 `NotificationType` 契約缺口（見 §四） |

**總判定：WARN**（無 Critical；3 個 W 級需修）

---

## 二、三個 reviewer 的產出對比

| Reviewer | 引擎／模型 | Effort | Findings | Verdict | 成本 |
|---|---|---|---|---|---|
| copilot-reviewer | copilot `gpt-5.4-mini` | medium | **1**（1 W） | WARN | Copilot Credits（少量） |
| gemini-reviewer | agy `gemini-3.1-pro-high` | high | **0** | PASS | 免費額度；in 356k / cached 3.56M / out 18.9k、134s |
| **claude-reviewer** | **native subagent** | — | **9**（2 W + 7 S） | WARN | 182,755 tokens、78 次工具呼叫、531s |

### 🔴 最重要的一項數據：claude-reviewer 產出是 copilot 的 9 倍、gemini 的無限倍

這**直接驗證了 v5.0 兩個核心設計決策**：

1. **§5.2 廢除「reviewer 不得讀 source」禁令是對的。** claude-reviewer 的 9 個 findings 中，**至少 5 個必須讀取審查範圍外的檔案才可能發現**：
   - F1 讀**後端 Java 原始碼**（且在另一個分支 `origin/feat/SSGS-12855-report-schedule`）比對 `refreshPeriodAndNextRunDate()`
   - F2 全專案 grep 確認 `nextRunDate` 無任何 UI 讀取（死欄位）
   - F4／F5 以後端 `ReportScheduleController` / `ReportScheduleService.upsert()` 反駁註解宣稱
   - F8 讀其他 14 個頁面統計 `PaginatorController` 的 dispose 慣例
2. **§3.2 把 claude-reviewer 的邊際價值排在第 2 位（僅次於 Team Lead）是對的**，且 §2 紅線「claude-reviewer 不可省略」有了實證支撐——若依 v4.x 慣例把它跳過或禁止讀 source，這 9 個 findings 全部不會出現。

---

## 三、新發現的缺陷（前次 stack-review 未涵蓋）

### W 級（3 個，需修）

| # | 來源 | 位置 | 問題 | 機械驗證 |
|---|---|---|---|---|
| W1 | copilot | `report_auto_send_page.dart:157` | 刪除流程 `await notifier.deleteSchedule(...)` **丟棄回傳值**（該方法簽章為 `Future<bool>`，notifier:139），接著**無條件**重抓列表並顯示「刪除成功」→ API 失敗時使用者看到成功訊息而資料仍在 | ✅ 已確認簽章與呼叫端 |
| W2 | claude | `next_delivery_date.dart:55` | MONTHLY 的下次寄送日預覽與後端 `nextRunDate` 不一致。具體重現：今日 2026/7/8、每月、寄送日 8 → 前端顯示 **2026/8/8**，後端實際為 **2026/7/9**（後端一律 `periodEndDate + 1 天`）。WEEKLY／TEN_DAYS／SEMIMONTHLY 比對後一致，只有 MONTHLY 有落差 | ✅ 路徑存在；後端依據來自跨 repo 查證 |
| W3 | claude | `report_schedule_state.dart:28` | `visibleList` 只過濾**已載入的頁**，但表格仍傳 `totalPagesFromAPI: scheduleState.total`（`report_schedule_data_table.dart:129`）。症狀：25 筆資料、命中項在第 3 頁時，使用者在第 1 頁搜尋 → 空清單被換成 `NoDataWidget`（同檔 :56），**分頁器一起消失、無法翻頁去找** → 看似查無資料實際存在 | ✅ 三處程式碼機制與描述完全一致 |

> 📌 W2 特別值得注意：它是**跨 repo、跨分支**的契約落差。`stack-review` 當時以後端原始碼為依據做過契約查證，但未涵蓋 `nextRunDate` 的計算語意；而任何 diff-only reviewer 都不可能發現。

### S 級（7 個）

| # | 位置 | 問題 |
|---|---|---|
| S1 | `report_schedule_result.dart:63` | 註解宣稱「前端列表直接顯示 `nextRunDate`」，實際**無任何 UI 讀取**；`nextRunDate`／`periodStartDate`／`periodEndDate` 三個皆為死欄位。註解與實作矛盾會掩蓋 W2 |
| S2 | `report_schedule_state_notifier.dart:94` | 殘留過期註解「後端沒有 update 端點，POST 是 upsert…編輯必須鎖定四個 key 欄位」，與後端現況（有 `PUT`、重複回 400）相反，且同段 99–104 行已有正確版本 → 兩段互相矛盾，會誘導後人把編輯欄位鎖回去（違反 A-D3） |
| S3 | `report_schedule_create_request.dart:9` | 同類過期 doc（「這支是 upsert」），且此檔被 POST 與 PUT 共用，錯誤說明會讓人誤判 PUT 語意 |
| S4 | `report_auto_send_page.dart:30` | 類別 doc 仍寫「API 未完成，資料來源為純前端 mock」，實際已接真實 REST 端點 |
| S5 | `intl_zh_TW.arb:1081` 等 | 3 個新增但**完全未被引用**的 i18n key。其中 `report_schedule_recipient_duplicate`（「此收件人已存在」）代表**規劃的重複收件人提示未實作**——`TagChipsInput` 用 `LinkedHashSet` 靜默去重，使用者重複貼上同一 email 得不到任何回饋 |
| S6 | `report_auto_send_page.dart:43` | `_paginatorController` 未 dispose。全站 15 個使用 `PaginatorController()` 的頁面中 **12 個有 dispose**，漏掉的是 `car_delete_page` / `label_list_page` / 本頁 |
| S7 | `enum_api_contract_test.dart:20` | 任務文件 A-3 記載「現存測試 23 例」，實際 **25 例**（增加的 2 例為操作紀錄 enum 契約測試，屬合理增加，但文件數字未同步） |

---

## 四、❌ Ground truth 未被偵測（誠實記錄）

本次刻意預埋一個**已知的真實缺陷**作為量測基準：

> `GroupUserNotificationSettingsType`（`group_user_notification_settings_enum.dart`）只有 4 個值，後端 `NotificationType` 另有 `INVOICE_ARCHIVE_DOWNLOAD` / `SHARED_DRIVER_PASSWORD` / `TICKET_ASSIGNMENT`。而 `group_setting_event_result.g.dart:12` 使用**非 nullable** 的 `$enumDecode` → 後端一回傳新值，群組設定整批解析失敗，連帶打死本分支改過的 `setting_notify_page.dart`。

**結果：3 個 reviewer 沒有任何一個發現。**

### 為什麼沒找到——以及這暴露了什麼

- manifest 的審查範圍清單**沒有列入** `group_user_notification_settings_enum.dart`（它不在 diff 內）
- manifest 明確要求「findings 必須指向範圍內檔案，**不要擴張審查範圍**」——**範圍紀律反過來阻止了這個發現**
- manifest §3-2 雖然提示了「注意非 nullable `$enumDecode` 的風險」，但沒有把**該檢查哪些契約面**列成清單

### 🔴 對 v5.0 的改進建議（尚未實作）

manifest 應新增一段 **「契約面清單」（contract surfaces to verify）**，由 Team Lead 依 explorer 的結果**主動列出**待驗證的契約點，而不是期待 reviewer 自行發現：

```markdown
## 2b. 契約面清單（逐項驗證，可讀範圍外檔案）
- 全專案 28 個非 nullable `$enumDecode(` 位點 → 對應前端 enum 是否覆蓋後端全部值
  （清單見 explorer 回報；本次分支改動的 4 個 enum 另需逐字比對）
- API DTO 的 wire format：snake_case 欄名、`{"data":...}` 包裝層級
```

**教訓：** 「不要擴張範圍」與「找出範圍外的相依缺陷」是張力關係。v5.0 靠 reviewer 自律解決，實測證明不夠——必須由 Team Lead **在 manifest 裡把契約面明列出來**。這條要寫進 §5.4。

---

## 五、順帶暴露的 v5.0 規格缺口（已修正）

| # | 缺口 | 症狀 | 修正 |
|---|---|---|---|
| E7 | 🔴 **agy headless 缺 `--dangerously-skip-permissions`** | `--add-dir` 只給檔案讀取權；grep/glob 的 `command` 權限在 headless 無法提示 → 自動拒絕。**但仍回 `status:"SUCCESS"`**、`response` 空、無 `structured_output` → **假成功** | 加旗標 + 補空手偵測（`SUCCESS` 但 `structured_output` 空 → `ERR:MODEL`） |
| E6-bis | 🔴 **copilot `-s` 的 stdout 不保證乾淨** | E6 在單輪短任務驗證通過就寫成通則。真實負載（`--allow-all-tools` + 讀 40 檔）下過程敘述混入 stdout，JSON 在尾端 → `jq` 直接讀失敗 | 一律抽取：`grep -o '{"findings".*}' \| tail -1` |

兩者皆已寫回 `SKILL.md` / `cli-invocation-ref.md` / `agents-prompts.md` / `README.md`，並記入 `phase-v5-cli-probe.md` E6-bis／E7 與 `重構建議-v5.0.md` §6.1。

**E7 是「假成功」故障**——若只判 `status`，會把「什麼都沒審」誤讀為「review 通過」。第一次執行的原始證據留存於 `gemini-reviewer.attempt1-permission-denied.json`。

---

## 六、Step 1（review base）的實際價值

v5.0 的 Review Context Protocol Step 1（`git fetch` + 檢查是否落後 target）在本次**立即發揮作用**：

執行時發現分支**已被合併進 `origin/main`**（`f3fa0cd7`，squash 為 `34bd8d1d`），且本地 HEAD 也已移動。原先預期的 `origin/main...HEAD` 範圍變成**空的**。

若沒有這一步，會用一個空 diff 或錯誤基準跑完整輪 review 並得出「無問題」——正是移植自 `stack-review` Step 1a 所要防範的失效模式（該處記錄的真實事故是本地 `main` 過期 7 週）。

**這步的成本是兩個 git 指令，避免的是一整輪無效 review。**

---

## 七、⚠️ 執行者自身的失誤（記錄以免重犯）

**我違反了自己訂的護欄二。** 派 explorer 後，我用 `tail -60` 截取輸出，**把搜尋軌跡（執行過的 grep/glob 與命中數）整段丟掉**——那正是護欄二存在的目的。

後果：無法判斷 explorer 對 28 個 `$enumDecode` 位點的覆蓋面，也**無法區分「explorer 漏了 `GroupUserNotificationSettingsType`」與「我截掉了」**。§四的 ground truth 分析因此只能歸因到 manifest 設計，而不能歸因到 explorer 品質。

**修正：** explorer 輸出一律 `tee` 到檔案完整留存，不可用 `head`/`tail` 截斷。這條應寫進 explorer 協定。

---

## 八、成本與效益的一個誠實張力

| 產出 | 消耗的資源 | 可替代性 |
|---|---|---|
| 9 findings（含全部 3 個 W 中的 2 個） | claude-reviewer：**182k Claude tokens** | ❌ 不可替代 |
| 1 finding（1 個 W） | copilot：少量 Credits | ✅ 可替代 |
| 0 findings | agy：免費額度 | ✅ 可替代 |

**產出最高的 reviewer，正是消耗不可替代資源的那一個。**

這**不違背** §3.2——該節的邊際價值排序本就把 claude-reviewer 放在第 2 位、並在 §2 紅線寫明「不可省略」。本次實測把它從「設計判斷」升級為「有數據支撐的結論」：**Claude 額度花在 review 上是有回報的；該外包的是 implementation 與 explore，不是 review。**

### gemini-reviewer 0 findings 是待釐清的問題

它燒了 356k input / 3.56M cached tokens、跑了 134s，然後回 PASS。同一份 manifest 下 claude 找到 9 個。可能原因（未驗證）：

- prompt 只聚焦 spec compliance，而多數 findings 屬「註解與實作矛盾」「死程式碼」類型，不在其視角內
- `--json-schema` 的剛性可能抑制了「無法歸入 findings 結構」的觀察
- agy 的工具存取雖已修好，實際 grep 深度仍不明（無搜尋軌跡可稽核）

**不宣稱它失敗，但也不宜視為「確認通過」。** 下次應要求它同樣回報搜尋軌跡。

---

## 九、下一步

1. 修 3 個 W 級缺陷（W1 刪除流程、W2 MONTHLY 日期、W3 搜尋分頁）——**W1／W3 影響使用者可見行為**
2. 清理 4 個過期註解（S1–S4）——它們正在誘導錯誤修改
3. manifest 新增「契約面清單」段（§四的改進建議）
4. explorer 協定補「輸出不可截斷」（§七）
5. `NotificationType` 缺 3 值另開任務（非本分支造成，但已在 main 上）

---

*2026-07-30 | v5.0 首跑 | 10 findings（3 W + 7 S）／0 捏造路徑／2 個規格缺口已修正／1 個 ground truth 未偵測*
