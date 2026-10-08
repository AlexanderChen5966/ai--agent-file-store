# 路徑 B · 專案地圖：東西在哪

原則：**先找垂直切片，不要橫向讀完整層。** 任何功能都由「頁面 + notifier + request/response + rest client」四件套組成，
挑一個熟悉的功能（建議：**車輛管理**）把四件套讀完，比讀完 `lib/util/` 有用得多。

---

## 1. 一分鐘目錄圖

```
lib/
├── main.dart / main_dev.dart / main_release.dart   # 入口，DEPLOY 環境變數
├── api/
│   ├── connector/      # ApiConnector、OAuth2、TaskManager⚠️、SecureStorage
│   ├── interceptor/    # 加 token、錯誤處理、重複請求攔截
│   ├── restclient/     # Retrofit 端點定義（rest_client.dart + .g.dart）
│   ├── request/        # Request DTO（依功能分子目錄）
│   ├── response/       # Response DTO
│   └── notifier/       # ⭐ Riverpod 狀態（本專案主要邏輯層都在這）
│       └── page/       # PageStateNotifier 基底：列表頁分頁/搜尋的共同行為
├── page/               # UI，依功能分目錄（car / driver / invoices / balance / …）
│   ├── common/widgets/ # ⭐ 共用元件庫，寫新 UI 前先來這裡找有沒有現成的
│   ├── home/           # 儀表板、側邊選單（權限判斷 hasPermission 在這）
│   ├── main_page.dart  # ShellRoute 外殼
│   └── page_route.dart # ⚠️ GoRouter 路由表（高風險，改前需確認）
├── models/enums/       # ⭐ 與後端對齊的列舉（改動前先確認後端 SoT）
├── notifier/           # 少數非 API 的本地狀態（home / select_file / timer）
├── util/               # effect/（SLColor、kAppRadius）、view/（SLText、SpacerWidget）、各種 utils
├── l10n/               # intl_zh_TW / zh_CN / en 的 .arb
└── generated/          # 自動產生：l10n.dart、intl messages（勿手改）
```

`external_libs/`：專案特製 fork 套件（`data_table_2` 等），**不可 upgrade，只能直接改原始碼**。

---

## 2. 垂直切片：「車輛列表」從點擊到畫面（新人必讀）

依序打開這 5 個檔案，就懂了本專案 80% 的資料流：

| # | 檔案 | 角色 |
|---|---|---|
| 1 | `lib/page/car/car_page.dart` | 頁面骨架：篩選列 + 表格 + Drawer |
| 2 | `lib/page/car/widgets/car_tab_bar_header.dart` | 篩選列（搜尋／下拉／清空／新增按鈕；權限 gating 在這） |
| 3 | `lib/page/car/widgets/car_data_table.dart` | 表格欄位定義、cell 游標、排序 |
| 4 | `lib/api/notifier/car/car_state_notifier.dart` | ⭐ 業務邏輯：fetch、CRUD、分頁、錯誤處理 |
| 5 | `lib/api/notifier/page/page_state_notifier.dart` | 列表頁共同基底（`originalLists` / `perPageList` / 分頁行為） |

搭配 `lib/api/request/car/car_search_request.dart`（送出去的參數）與
`lib/api/response/car/car_result.dart`（收回來的資料）。

### 資料流一句話版

```
Widget（HookConsumerWidget）
  → ref.read(carStateNotifier.notifier).fetchDataListFromApi(context, isClear)
  → ApiConnector.getClient().fetchCars(request.copyWith(orderBy: ['id.desc']))
  → Dio Interceptor（塞 token、401 → refresh，經 TaskManager）
  → 後端
  → clearMapAndReassignNewPage() 更新 originalLists / perPageList
  → state = state.copyWith(...) → ref.watch 的 widget 重建
```

⚠️ 三個一眼可見的慣例，全站列表頁都一樣，缺一就會出 bug：
- `fetchDataListFromApi` 開頭必有 `if (isClear) requestFirstPage();`
- 排序 `orderBy` 傳在 **fetch 處**（後端不會自己排序）
- search request 的 `size` 用 `PaginatedDataTable2.BATCH_SIZE`（200）

細節與原因見 `.claude/rules/datatable-safety.md`。

---

## 3. 「我要改 X，該打開哪個檔案」對照表

| 想改什麼 | 去哪 |
|---|---|
| 某頁面的版面 | `lib/page/<功能>/<功能>_page.dart` 及同層 `widgets/` |
| 列表的欄位、排序、游標 | `lib/page/<功能>/widgets/*_data_table.dart`（⚠️ 高風險，先讀 rules） |
| 篩選列（搜尋／下拉／清空／新增） | `lib/page/<功能>/widgets/*_tab_bar_header.dart`（版面規則見 `.claude/rules/list-page-header.md`） |
| 呼叫 API 的邏輯、CRUD 後重抓 | `lib/api/notifier/<功能>/*_state_notifier.dart` |
| API 端點、參數 | `lib/api/restclient/rest_client.dart` ＋ `request/`、`response/`（改完**必跑 build_runner**） |
| 列舉值（狀態、類型） | `lib/models/enums/`（⚠️ 與後端契約對齊，見下方） |
| 路由、新頁面掛載 | `lib/page/page_route.dart`（⚠️ 高風險，需使用者確認） |
| 顏色 | `lib/util/effect/color_style.dart`（`SLColor`），禁止 hardcode HEX |
| 文字樣式 | `lib/util/view/sl_text.dart`（`SLText`） |
| 間距 / 圓角 | `lib/util/view/spacer_util.dart`、`lib/util/effect/radius_style.dart` |
| 多語系文案 | `lib/l10n/intl_*.arb` ＋ `intl_utils:generate` |
| 共用對話框 / 按鈕 / 下拉 / 日期選 | `lib/page/common/widgets/`（先找現成，別重造） |
| 側邊選單項目、權限顯示 | `lib/page/home/widgets/menu/side_menu_widget.dart`（`hasPermission`） |
| 登入 / token / 登出 | `lib/api/connector/auth_service.dart`、`task_manager.dart`（⚠️ 禁改核心流程） |

---

## 4. 共用元件速查（`lib/page/common/widgets/`）

寫新 UI 前先掃一眼這份清單，重複造輪子是 code review 最常見退件原因：

- 表格：`api_paginated_data_table.dart`（列表頁標配）、`build_data_table.dart`、`data_cell_with_tip.dart`
- 表格（報表分析新引擎）：`lib/page/common/widgets/virtual_data_table.dart`
- 輸入：`search_input_with_button.dart`、`search_input_with_debounce.dart`、`build_dropdown_menu.dart`
- 選日期：`build_date_selector.dart`、`single_date_selector_widget.dart`、`month_selector.dart`
- 容器／互動：`custom_dialog.dart`、`custom_drawer.dart`、`custom_button.dart`、`custom_card.dart`
- 狀態：`no_data_widget.dart`、`shimmer_loading.dart`、`loading_overlay.dart`
- 其他：`build_tooltip.dart`、`build_choice_chip_widget.dart`、`icon_label.dart`、`tab_bar_manager_widget.dart`

---

## 5. 跨服務契約（知道就好，前端新人不必深入）

- `lib/models/enums/` 的列舉與後端 `b2b-backend` 的 enum 一一對應。
  **後端新增值而前端沒補 → 非 nullable 的 `$enumDecode` 會整批解析失敗、整頁空白**
  （2026-07-29 操作紀錄頁全毀就是這個原因，見 `docs/shared/enum_decode_hardening.md`）。
- API 契約副本在 `docs/api/api_documentation_v16.md`（注意 frontmatter 的 `source-commit` 與 `status`，
  `superseded` 的版本直接跳過）。
- 開 session 時的「跨 repo 契約漂移報告」由 `.claude/scripts/contract_drift_check.py` 產生，
  新人看不懂可以先略過，但**不要無視紅字**——那代表文件可能已過期。

---

## 6. 找東西的實用指令

```bash
# 找某個中文字串出現在哪個 arb / 頁面
grep -rn "報表寄送" lib --include=*.dart --include=*.arb | head

# 找某個 API 端點的定義與呼叫點
grep -rn "fetchCars" lib | head

# 找某個路由對應的頁面
grep -rn "ROUTE_NAME" lib/page/page_route.dart | head -50

# 這個 bug 以前發生過嗎
ls docs/bug_record/ && grep -rl "關鍵字" docs/bug_record docs/shared
```