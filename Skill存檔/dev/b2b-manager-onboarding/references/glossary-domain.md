# 路徑 E · 業務名詞與環境

B2B Manager（山隆 B2B 智慧平台）是**石油／加油 B2B 管理系統**的管理端。
使用者是企業客戶的管理者，管的是「自家車隊在加油站的消費與帳務」。

> ⚠️ 本頁名詞由程式碼與 UI 文案推得，**業務語意以團隊 PM／後端說明為準**。
> 有疑問時直接問，不要憑這頁下結論。

---

## 核心概念鏈

```
群組（Group，一家企業客戶）
  ├── 使用者 Users（管理者帳號，有角色與權限）
  ├── 車輛 Cars（車牌、油品限制、標籤）
  ├── 司機 Drivers（可綁車、有出勤狀態）
  ├── 群組帳戶 GroupAccounts（餘額、儲值、額度分配）
  └── 交易 Orders（加油消費紀錄）→ 發票 Invoices → 報表 Reports
```

---

## 名詞表

| 名詞 | 說明 | 程式碼落點 |
|---|---|---|
| 群組 Group | 一家企業客戶；系統多數資料都掛在群組下，切換群組會換整個資料視角 | `lib/api/notifier/group/`、cookie `X_Group_Tax_No` |
| 車輛管理 | 車牌、油品類別限制、批次匯入／匯出、批次編輯、標籤 | `lib/page/car/` |
| 司機管理 | 司機資料、出勤狀態、匯入匯出 | `lib/page/driver/` |
| 標籤 Label | 給車輛／司機分類用的標籤 | `lib/page/setting/`（`LabelListPage`）、`Authorities.Labels` |
| 交易 / 消費紀錄 Order | 加油交易明細，報表分析的資料來源 | `lib/page/order/`、`lib/api/notifier/order/` |
| 報表分析 | 多種統計表格（總交易紀錄等），用 `VirtualDataTable` 新引擎 | `lib/page/order/`（`ReportPage`） |
| 報表寄送設定 | 排程自動寄送報表（頻率／收件人／報表類型） | `ReportAutoSendPage`、`send_frequency_enum.dart` |
| 發票 Invoice | 開立與下載（A4／A5／證明聯格式），可批次寄送 | `lib/page/invoices/`、`invoice_status.dart` |
| 儲值 Recharges | 群組帳戶加值 | `RechargesPage`、`recharge_type.dart` |
| 額度分配 Balance Distribute | 把群組餘額分配下去 | `lib/page/balance/`、`BalanceDistributePage` |
| 異動紀錄 ChangeLog | 群組帳戶的餘額異動 | `GroupAccountChangeLogPage`、`account_balance_adjustment_type.dart` |
| 操作紀錄 Log | 使用者操作稽核紀錄 | `lib/page/log/`、`entity_type_enum.dart`、`operation_type_enum.dart` |
| 客服單 Ticket | 客服／申請單 | `lib/page/clientservice/`、`ticket_status.dart`、`ticket_type.dart` |
| 推薦紀錄 Referral | 推薦人／被推薦紀錄 | `ReferralRecordPage`、`Authorities.Referees` |
| Onboarding / EIP | 企業客戶開通流程（與 app 內「新人導覽」無關） | `lib/page/onboard/`、`on_boarding_step.dart` |
| 加油限制 Refueling Settings | 油品／額度等加油條件設定 | `refueling_constraint_type_enum.dart`、`setting/` |
| 對帳 / 帳務設定 Billing Settings | 結算週期、最低餘額門檻等 | `billing_cycle_enum.dart`、`setting/` |

---

## 權限模型

格式：`<resource>:<action>`，由 API 回傳的 `userData.authorities` 決定。

**resource**（`lib/models/enums/authorities_enum.dart`）：
`groups`、`users`、`cars`、`drivers`、`orders`、`invoices`、`group_accounts`、`logs`、
`billing_settings`、`notification_settings`、`refueling_settings`、`labels`、`label`、
`recharges`、`referees`、`tickets`、`report_schedules`

**action**：`create`、`read`、`update`、`delete`、`download`

判斷方式：

```dart
hasPermission(ref, Authorities.Cars, AuthoritiesAction.Create)
```

- SoT 是後端 `Role.java`；前端 `Rule` enum（`rule_enum.dart`）**只是對照用，程式不讀它**
- `MOCK_USER` 的非 Read 動作一律被擋掉（只能瀏覽）
- 呈現方式：操作入口隱藏、表單欄位唯讀（見 `.claude/rules/permission-gating.md`）

---

## 環境與網址

| 環境 | 前端 | 後端 API |
|---|---|---|
| dev | https://b2bmanager.dev.ssgsslc.com | https://b2b-backend.dev.ssgsslc.com |
| staging | https://b2bmanager.staging.ssgsslc.com | https://b2b-backend.staging.ssgsslc.com |
| release（正式） | https://b2bmanager.ssgsslc.com | https://b2b-backend.ssgsslc.com |
| 本機 | http://localhost:9001（port 固定） | 由 `--dart-define=DEPLOY` 決定 |

- 環境切換：`--dart-define=DEPLOY=dev|staging|release`，讀取處 `lib/main.dart:50`
  ＋ `lib/api/flavor_config.dart`（`Flavor.fromString()`，無值時預設 `dev`）
- 新人一律用 **dev**；動 staging／release 前先問負責人
- 後端 repo 在 `../b2b-backend`（前端新人不必深入，但契約有疑問時可查）
- Postman collection 連結在 `README.md`

---

## 瀏覽器儲存

統一由 `lib/api/cookie_manager.dart` 管理，實際上混用四種載體：

| 載體 | 放什麼 |
|---|---|
| `document.cookie` + Session Storage | `saveCookie()` 兩邊同時寫（群組、驗證碼等短期資料） |
| SharedPreferences（Local Storage） | `LoginTokenTAG`、`IdTokenTAG`、`RefreshTAG`、`X-Group-Id_TAG`、`X_Group_Tax_No_TAG`、偏好設定 |
| Secure Storage（Web Crypto API） | OAuth2 credentials，`lib/api/connector/secure_storage.dart` |

⚠️ 送 API 的群組標頭是 `X-Group-Id` / `X-Group-Tax-No`（`_KEY` 常數），
本機儲存的鍵是 `_TAG` 常數，兩者不同，別搞混。

---

## 多語系

zh_TW（主要）／zh_CN／en，檔案在 `lib/l10n/intl_*.arb`，產物在 `lib/generated/`。
**三個 arb 都要加**，然後跑 `flutter pub run intl_utils:generate`。