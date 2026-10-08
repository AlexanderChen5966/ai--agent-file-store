# 路徑 C · 第一個任務食譜

每道食譜都是「照抄既有樣板」。**先找到同類型的現成實作，複製它的結構**，不要自創寫法。

---

## 食譜 0：動手前的自檢（每次都做）

- [ ] 這個改動影響哪些模組？
- [ ] 有沒有碰到 OAuth2 / TaskManager？（碰到 → 停，先問）
- [ ] 有沒有碰到 `page_route.dart` / `external_libs/` / DataTable 欄寬與排序？（碰到 → 需使用者確認）
- [ ] 需不需要跑 `build_runner`？
- [ ] 是不是破壞性變更？（是 → 先提選項給使用者）

改 UI 之前**必讀 `DESIGN.md`**；改表格之前**必讀 `.claude/rules/datatable-safety.md`**。

---

## 食譜 1：新增一支 API

樣板：`lib/api/restclient/rest_client.dart` 內任一 `fetchCars` 風格的端點。

1. 端點定義 → `lib/api/restclient/rest_client.dart`
   ```dart
   @GET('/api/v1/cars')
   Future<PageSearchResult<CarResult>> fetchCars(@Queries() CarSearchRequest request);
   ```
2. Request DTO → `lib/api/request/<功能>/xxx_request.dart`，加 `@JsonSerializable()`
3. Response DTO → `lib/api/response/<功能>/xxx_result.dart`，加 `@JsonSerializable()`
4. **必跑**：
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```
5. 在 notifier 呼叫：`ApiConnector.getClient().fetchXxx(...)`

⚠️ Response DTO 內若有 enum 欄位，**確認 `lib/models/enums/` 已涵蓋後端所有可能值**，
否則後端一加新值就整頁空白（見 `docs/shared/enum_decode_hardening.md`）。

---

## 食譜 2：新增一個頁面

1. 建目錄 `lib/page/<功能>/`，頁面檔 `<功能>_page.dart`
   ```dart
   class MyFeaturePage extends HookConsumerWidget {
     static const String ROUTE_NAME = '/my-feature';
     @override
     Widget build(BuildContext context, WidgetRef ref) { ... }
   }
   ```
2. 掛路由 → `lib/page/page_route.dart`
   ⚠️ **高風險檔案**：影響全站存取控制，改前需取得使用者確認，並確認 redirect 與登入狀態。
   ⚠️ 目前 redirect **只檢查登入狀態、沒有 per-page 權限**，直接輸入 URL 仍進得去
   （已知缺口：`docs/shared/page_route_permission_guard.md`）。
3. 需要狀態就建 notifier → `lib/api/notifier/<功能>/<功能>_state_notifier.dart`
4. 需要出現在側邊選單 → `lib/page/home/widgets/menu/side_menu_widget.dart`，並用
   `hasPermission(ref, Authorities.X, AuthoritiesAction.Read)` 包起來

---

## 食譜 3：新增一個「列表頁」（本專案最常見的任務）

**照抄 car 或 driver 這一組**，五個檔案缺一不可：

| 檔案 | 抄哪個 |
|---|---|
| 頁面 | `lib/page/car/car_page.dart` |
| 篩選列 | `lib/page/car/widgets/car_tab_bar_header.dart` |
| 表格 | `lib/page/car/widgets/car_data_table.dart` |
| notifier | `lib/api/notifier/car/car_state_notifier.dart` |
| request | `lib/api/request/car/car_search_request.dart` |

**五條不可違反的硬規則**（違反的症狀都很難 debug）：

1. `XxxSearchRequest.empty()` 的 `size` 用 `PaginatedDataTable2.BATCH_SIZE`（200），不可自訂小值
2. `fetchDataListFromApi` 開頭必寫 `if (isClear) requestFirstPage();`
3. **單筆新增／編輯／刪除後重抓用 `isClear: false`**（停在原本那一頁）；
   進頁 `initState` 與篩選變更／清空用 `true`
   **例外——筆數大幅變動或離開後重進頁面時用 `true`**：
   - 匯入檔案大量新增（`pick_upload_car_file.dart:32`）
   - 批次編輯完成後 `context.replace(CarPage.ROUTE_NAME)` 回列表（`batch_edit_car_page.dart:198`）
     ——這其實等同重新進頁，`true` 才對
   判準：**這次操作後，使用者原本那一頁還存在嗎？** 存在 → `false`；
   整批洗掉或根本換了頁面 → `true`
   ⚠️ `car_drawer.dart:51` 傳 `false`，但同行註解寫「批次大量刪除車子或大量加車，用舊的
   page number 會錯」——**註解與參數看起來對不上，屬待釐清**，不要拿它當範本
4. 讀當前頁次用 `paginatorController.currentRowIndex`，**不可用 `currentPage`**（恆為 1）
5. 排序 `orderBy` 傳在 notifier 的 fetch 處：`state.request.copyWith(orderBy: ['create_time.desc', 'id.desc'])`
   （後端不會自己排序；只放在 `empty()` 會被 `applyFilters` 洗掉）

篩選列版面另有規則（最小寬度 1270 + 水平捲軸，不可換行）→ `.claude/rules/list-page-header.md`。

---

## 食譜 4：新增一個顏色

1. 先確認 `lib/util/effect/color_style.dart` 的 `SLColor` 真的沒有接近的顏色
2. 在對應用途區塊後新增：`static const orderStatusPending = Color(0xFFXXXXXX); // 用途說明`
3. 命名 camelCase 依用途（`orderStatusPending` ✅／`lightOrange` ❌），功能專用加前綴

❌ **禁止在 widget 內 hardcode HEX。**

---

## 食譜 5：新增／修改一句文案（最適合當第一個練手）

1. 三個檔案都要加：`lib/l10n/intl_zh_TW.arb`、`intl_zh_CN.arb`、`intl_en.arb`
2. `flutter pub run intl_utils:generate`
3. 使用：`S.of(context).myNewKey`

⚠️ 只加 zh_TW 不加 en，產生器會生不出來或 fallback 到 key 名。
`lib/generated/` 是產物，**不要手改**。

---

## 食譜 6：加權限控制

判斷一律用 `hasPermission(ref, Authorities.X, AuthoritiesAction.Y)`
（❌ 不可用 `Rule.authorities`，那份只是對照後端用的文件性質清單）。

- **操作入口（按鈕、表格 icon）→ 隱藏，不要 disable**（全站 18:0 一致）
  ```dart
  if (hasPermission(ref, Authorities.Cars, AuthoritiesAction.Create)) PositiveButton(...)
  ```
  在 `Row(spaceBetween)` 內隱藏時用 `const SizedBox.shrink()` 佔位，避免版面位移。
- **表單欄位值 → 保留可見、改唯讀顯示**（設定值本身是資訊）
  ```dart
  option: isEditing ? <輸入元件> : SLText.medium(text: 目前值),
  ```
  分區權限要**各區用各區的 update 權限**，不可共用單一 `_isEditing`（樣板：`setting_notify_page.dart`）。

細節見 `.claude/rules/permission-gating.md`。

---

## 食譜 7：送出前

```bash
flutter analyze --no-fatal-infos --no-fatal-warnings --pub
```

- 自己先跑一次 dev 環境實機驗證（列表要翻頁、CRUD 後表格不能跳回第 1 頁）
- 想要 AI 幫忙 review：`/stack-review`
- 任務文件流程（需求 → 實作 → 收尾）：`/requirements`、`/doc-update`；
  任務文件都放 `docs/shared/`，索引在 `docs/shared/readme.md`

---

## 找第一個真任務

`docs/shared/readme.md` 中狀態為 **⏳ 待實作**、且描述裡標「純前端」的票，最適合新人。
挑好之後把該份任務文件整份讀完再動手——裡面通常已經把影響範圍與風險列好了。