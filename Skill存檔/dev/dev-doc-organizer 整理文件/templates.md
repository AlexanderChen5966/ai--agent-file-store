# Dev Doc Organizer — 文件模板

四種文件類型的半結構模板。
標記說明：`[MUST]` = 必填，`[OPT]` = 選填，`[AUTO]` = 由 Skill 自動填入。

---

## 目錄

- [PRD 需求文件模板](#prd-需求文件模板)
- [API 文件模板](#api-文件模板)
- [ARCH 架構文件模板](#arch-架構文件模板)
- [TASK Agent 任務文件模板](#task-agent-任務文件模板)

---

## PRD 需求文件模板

```markdown
# [MUST] 功能名稱

**文件版本：** [MUST]
**建立日期：** [MUST]
**適用範圍：** [MUST] 說明這份需求影響哪些頁面或模組

---

## 背景與動因

[MUST] 說明：
- 目前的問題是什麼
- 為什麼現在需要解決
- API 或後端有哪些變更（若有）

---

## 影響範圍

[MUST] 列出所有會被修改的檔案路徑：

- `lib/path/to/file.dart` — 說明為何影響此檔案
- `lib/path/to/another.dart` — 說明為何影響此檔案

---

## 不在範圍內

[OPT] 明確排除的項目，防止 Agent 做多：

- 不修改 XXX 的行為
- 不影響 YYY 頁面

---

## 詳細需求

### [功能模塊名稱]

**檔案：** `lib/path/to/file.dart`

1. [MUST 或 OPTIONAL] 具體行為描述，一條一件事
2. [MUST 或 OPTIONAL] 具體行為描述，一條一件事

**互動邏輯（若有）：**

| 條件 | 行為 |
|------|------|
| 使用者選擇 A | 執行 X |
| 使用者選擇 B | 執行 Y，並禁用 Z |

---

## API 變更（若有）

[OPT] 說明後端 API 的新增/修改欄位：

```
ENDPOINT: POST /path/to/api
新增欄位: field_name (型別, 必填/選填)
變更欄位: old_field → new_field (說明差異)
```

---

## 錯誤處理

[OPT] 每種錯誤情況的處理方式：

| 錯誤情況 | 處理方式 |
|---------|---------|
| API 回傳 400 | 顯示錯誤訊息 X |
| 欄位為 null | 使用預設值 Y |

---

## 驗收條件

[MUST] 每條必須可以客觀驗證，不能只寫「功能正常」：

- [ ] 當[具體條件]時，[具體行為]符合預期
- [ ] 當[具體條件]時，[具體行為]符合預期
- [ ] API 請求包含欄位 X，值為 Y

---

## 相依功能

[OPT] 執行此需求前需要確認的狀態或其他功能：

- depends on: [其他功能名稱或 PR]
```

---

## API 文件模板

```markdown
# [MUST] API 端點名稱

**版本：** [MUST]
**最後更新：** [MUST]

---

## 基本資訊

| 項目 | 值 |
|------|----|
| Method | [MUST] GET / POST / PUT / DELETE |
| Path | [MUST] `/path/to/endpoint` |
| 認證 | [MUST] Bearer Token + x-group-id Header |
| Content-Type | [MUST] application/json |

---

## Request

### Headers

| Header | 必填 | 說明 |
|--------|------|------|
| Authorization | MUST | Bearer {token} |
| x-group-id | MUST | 當前操作的群組 ID |

### Body 參數

| 欄位名稱 | 型別 | 必填 | 預設值 | 說明 |
|---------|------|------|--------|------|
| field_name | String | MUST | — | 說明 |
| optional_field | String | OPTIONAL | null | 說明，null 表示不篩選 |
| list_field | List\<Int\> | OPTIONAL | null | null 與空陣列 [] 的差異：[說明] |
| page | Int | MUST | — | 頁碼，從 1 開始 |
| size | Int | MUST | — | 每頁筆數，上限 [X] |
| order_by | List\<String\> | MUST | — | 格式：`field.asc` 或 `field.desc` |

### Request 範例

```json
{
  "field_name": "example_value",
  "optional_field": null,
  "page": 1,
  "size": 50,
  "order_by": ["created_at.desc", "id.desc"]
}
```

---

## Response

### 成功回應 (200)

| 欄位名稱 | 型別 | Nullable | 說明 |
|---------|------|----------|------|
| data | List\<Object\> | NO | 資料陣列 |
| page | Int | NO | 當前頁碼 |
| size | Int | NO | 每頁筆數 |
| total | Int | NO | 總筆數 |
| pages | Int | NO | 總頁數 |

#### data 陣列元素結構

| 欄位名稱 | 型別 | Nullable | 說明 |
|---------|------|----------|------|
| id | Int | NO | 唯一識別碼 |
| field_a | String | YES | 說明，null 代表[具體意義] |
| field_b | String | NO | 說明 |

### 成功回應範例

```json
{
  "data": [
    { "id": 1, "field_a": "value", "field_b": "value" }
  ],
  "page": 1,
  "size": 50,
  "total": 123,
  "pages": 3
}
```

---

## 錯誤碼

| 狀態碼 | 情境 | Agent 處理方式 |
|--------|------|---------------|
| 400 | Request 格式錯誤 | 檢查必填欄位 |
| 401 | Token 無效或過期 | 重新取得 Token |
| 403 | 無權限操作此群組 | 確認 x-group-id 與 Token 對應 |
| 404 | 資源不存在 | 回傳空結果，非錯誤 |
| 500 | 伺服器錯誤 | 記錄錯誤，顯示系統錯誤訊息 |

---

## 情境說明

[OPT] 說明在哪些使用情境下呼叫此 API：

**情境 1：[情境名稱]**
- 觸發條件：[具體條件]
- 傳入參數：[列出非預設的參數]
- 預期行為：[回傳結果的說明]
```

---

## ARCH 架構文件模板

```markdown
# [MUST] 架構名稱

**版本：** [MUST]
**最後更新：** [MUST]
**適用範圍：** [MUST] 明確列出哪些頁面或模組 MUST 遵循此架構

---

## 概述

[MUST] 一段話說明此架構解決什麼問題、核心設計原則是什麼。

---

## 使用規則

[MUST] 明確的 MUST / MUST NOT 清單：

**MUST：**
- MUST 繼承 `XxxBaseClass`
- MUST 定義靜態常數 `ROUTE_NAME`
- MUST 在 `initState` 中呼叫 `super.initState()`

**MUST NOT：**
- MUST NOT 直接修改 `state.field = value`（破壞 immutability）
- MUST NOT 在 Widget 層直接呼叫 API

---

## 決策樹

[MUST] 當有多種選擇時，提供明確的判斷條件：

```
頁面有複雜搜尋條件 且 需保留查詢狀態？
  → YES: 使用 CacheableState
  → NO: 頁面需要任務管理（多步驟非同步操作）？
    → YES: 使用 SingleTaskState
    → NO: 使用 ConsumerState
```

---

## 核心元件

[MUST] 每個元件的職責說明：

### [元件名稱]

**位置：** `lib/path/to/file.dart`
**職責：** [一句話說明]
**提供的 API：**

| 方法/屬性 | 說明 | 使用時機 |
|----------|------|---------|
| `methodName()` | 說明 | 什麼情況下呼叫 |

---

## 資料流

[MUST] 說明資料的來源、流向、儲存位置：

```
使用者操作
  → Widget 層呼叫 Notifier 方法
  → Notifier 更新 State
  → Riverpod 通知 Widget 重建
  → Widget 讀取 State 渲染 UI
```

---

## 參考實作

[OPT] 具體的範例檔案，Agent 可以對照：

- 完整範例：`lib/page/order/changelog/group_account_change_log_page.dart`
- 最簡範例：`lib/page/simple/example_page.dart`

---

## 不適用場景

[OPT] 明確說明何時不應使用此架構：

- 對話框（Dialog）：使用 `showDialog`，不適用此架構
- 無狀態的展示元件：直接使用 `StatelessWidget`
```

---

## TASK Agent 任務文件模板

這是給 Agent 直接執行的指令文件，歧義容忍度最低。

```markdown
# [MUST] 任務名稱

**任務 ID：** [OPT] 用於追蹤
**建立日期：** [MUST]
**優先級：** [OPT] HIGH / MEDIUM / LOW

---

## 任務目標

[MUST] 一句話說明「完成」是什麼樣子：

> 完成後，[具體可觀察的結果]

---

## 前置條件

[OPT] Agent 開始前必須確認的狀態：

- [ ] [條件 1]
- [ ] [條件 2]

---

## 輸入

[MUST] Agent 執行此任務所需的所有資訊：

| 輸入項目 | 來源 | 說明 |
|---------|------|------|
| [輸入名稱] | [檔案路徑 / API / 使用者提供] | 說明 |

---

## 不在範圍內

[MUST] 明確排除，防止 Agent 做多：

- MUST NOT 修改 [具體檔案或功能]
- MUST NOT 新增未在需求中列出的功能

---

## 執行步驟

[MUST] 每步只做一件事，標明依賴關係：

### 步驟 1：[動作描述]

- **depends on:** 無（或：步驟 X 完成）
- **輸入：** [具體說明]
- **操作：** [具體說明，避免模糊動詞]
- **輸出：** [具體說明]
- **完成標準：** [如何確認這步完成了]

### 步驟 2：[動作描述]

- **depends on:** 步驟 1 完成
- **輸入：** 步驟 1 的輸出 [具體說明]
- **操作：** [具體說明]
- **輸出：** [具體說明]
- **若失敗：** [具體處理方式，不能只寫「回報錯誤」]

---

## 輸出

[MUST] Agent 執行後應產生的所有成果：

| 輸出項目 | 類型 | 位置 | 說明 |
|---------|------|------|------|
| [輸出名稱] | 檔案 / 代碼 / 結果 | [路徑或描述] | 說明 |

---

## 完成條件

[MUST] 可以客觀驗證的標準，每條必須可測試：

- [ ] [具體可測試條件 1]
- [ ] [具體可測試條件 2]
- [ ] 沒有 [forbidden action]

---

## 約束條件

[MUST] 執行過程中的限制：

- MUST 遵循 [架構規範文件] 的設計原則
- MUST NOT 改動 [具體檔案] 的現有邏輯
- MUST 在每個步驟完成後輸出確認訊息

---

## 錯誤處理

[OPT] 遇到問題時的處理方式：

| 錯誤情況 | 處理方式 |
|---------|---------|
| [錯誤情況 1] | [具體處理，不能是「通知使用者」這種模糊描述] |
| [錯誤情況 2] | [具體處理] |

---

## 參考文件

[OPT] 執行時可能需要查閱：

- 架構規範：[文件名稱及路徑]
- API 文件：[文件名稱及路徑]
- 範例實作：[檔案路徑]
```
