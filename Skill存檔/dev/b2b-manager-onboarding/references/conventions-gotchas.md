# 路徑 D · 硬規則與地雷

這份是「被 review 打槍前先知道」。**每條都有血淚來源**，不是風格偏好。
完整版在 `.claude/rules/`（Claude Code 會自動載入）與 `docs/claude/claude-troubleshooting.md`。

---

## 🔴 絕對禁止（不用討論，直接不做）

| 禁止事項 | 為什麼 |
|---|---|
| 改 OAuth2 PKCE 核心流程 | 動到就登不進去，且影響三個環境 |
| 移除／替換 TaskManager 單例（`lib/api/connector/task_manager.dart`） | 它擋的是重複授權／refresh 請求，拿掉會撞 rate limit |
| 直呼 `handleAuthorizationResponse()` / `refreshAccessToken()` | 同上，一律經 TaskManager |
| 動環境配置邏輯（dev/staging/release） | 會打到錯的後端 |
| `pub upgrade` 或任意改 `external_libs/` | 那是專案 fork 過的套件，upgrade 會直接蓋掉客製 |
| 未經要求的大規模重構 / 換掉 Riverpod・GoRouter・OAuth2 | 超出任何任務的授權範圍 |

## ⚠️ 高風險（做之前先取得使用者確認）

- API endpoint / DTO / Retrofit 定義（要評估 `build_runner` 與後端契約）
- `lib/page/page_route.dart`（全站存取控制）
- Riverpod 狀態結構
- DataTable 欄寬（`fixedWidth` / `ColumnSize`）、排序（`sortColumnIndex` / `onSort`）、DataCell 游標

---

## 1. screenutil：新程式碼禁用 `.w / .h / .sp`

```dart
SizedBox(height: 40)        // ✅
SizedBox(height: 40.h)      // ❌ 新程式碼禁止
Container(height: 600)      // ✅ 表格容器高度必須固定 px
```

- 舊程式碼不強制遷移；但**你改到的尺寸**建議順手改成固定 px
- `SpacerWidget`、`kAppRadius` 本來就不加 `.w/.h`，維持原寫法
- 基準解析度 1920×1024

## 2. UI 一律走 token

| 要什麼 | 用什麼 | 在哪 |
|---|---|---|
| 顏色 | `SLColor` | `lib/util/effect/color_style.dart` |
| 文字 | `SLText` | `lib/util/view/sl_text.dart` |
| 間距 | `SpacerWidget` | `lib/util/view/spacer_util.dart` |
| 圓角 | `kAppRadius` | `lib/util/effect/radius_style.dart` |

❌ 不 hardcode HEX、不散落 `TextStyle`。改 UI 前讀 `DESIGN.md`。

## 3. 表格（本專案最大地雷區）

`ApiPaginatedDataTable` 的模型是「**一次抓一批 200 筆、批內本地分頁**」，不是每頁打一次 API。

1. search request 的 `size` = `PaginatedDataTable2.BATCH_SIZE`（200）
2. `fetchDataListFromApi` 開頭必須 `if (isClear) requestFirstPage();`
   → 少了它，翻頁後 `request.page` 永久停在該頁，之後重抓帶錯頁 → 顯示「尚無資料」但 total 有值
3. **單筆** CRUD 後重抓用 `isClear: false`
   → `true` 會清空 `perPageList` → 該幀換成 `NoDataWidget` → 表格 unmount → 記頁次的 `_firstRowIndex` 隨 State dispose → **跳回第 1 頁**
   → 例外：**筆數大幅變動（大量匯入）或離開後重進頁面**時用 `true` 才對，
   判準是「使用者原本那一頁操作後還存在嗎」。實例與待釐清處見
   `references/first-task-recipes.md` 食譜 3
4. 讀頁次用 `paginatorController.currentRowIndex`，**不可用 `currentPage`**（全專案沒人呼叫 `setCurrentPage()`，該值恆為 1）
5. 排序 `orderBy` 由前端傳、且傳在 fetch 處
   → 後端 `BaseSearchExportService` 在 `Sort.unsorted()` 時 SQL **完全沒有 `ORDER BY`**，順序由 MySQL 自行決定
6. `sortColumnIndex` **不可加 `+1`**（DataTable2 最小回傳 columnIndex=1，加 1 造成全表排序偏移）
7. 雙行 cell 的 vertical padding **必須 ≤ 2px**，否則 RenderFlex overflow
8. `pageSyncApproach` 預設 `doNothing`：刪光當前頁不會自動收斂，刪除流程末端需自行 `goToPreviousPage()`

DataCell 游標三態：

| `onTap` | 游標 | 用途 |
|---|---|---|
| `null`（無 SelectionArea） | ↖ 箭頭 | 空格子 / 純展示（`cellText.isEmpty \|\| cellText == '-'`） |
| `null` + `SelectionArea` | I I-beam | 有文字、可選取複製 |
| `callback` | 👆 手指 | 可點擊操作 |

> 🐛 已知未修：`api_paginated_data_table.dart:85` 誤用 `currentPage`（該式恆為 0），影響全站 20 個表格。
> 屬高風險共用元件，**不要順手修**，需另開任務並取得確認。

報表分析用的新引擎 `VirtualDataTable` 另有邊框／高度預算規則 → `docs/claude/claude-datatable-rules.md` 第 7 節。

## 4. Riverpod

- `ref.watch` 監聽並重建／`ref.read` 一次性讀取／`ref.listen` 監聽不重建
- ❌ **禁止在 build phase 直接改 provider 狀態**；必要時用 `Future(() {})` 延遲

## 5. 權限 gating

- 操作入口（按鈕、icon）→ **隱藏**，不要 disable（全站 18:0；曾短暫改 disable 後又改回來）
- 表單欄位值 → **保留可見、改唯讀**
- 判斷用 `hasPermission(ref, Authorities.X, AuthoritiesAction.Y)`，❌ 不可用 `Rule.authorities`
- 前端 gating 只是體驗層，真正防護在後端 `@PreAuthorize`

## 6. 列表頁篩選列版面

最小寬度 **1270 px + 水平捲軸**，❌ 不可改用 `Wrap` 換行、❌ 不可裸 `Row`（會 overflow）。
骨架與範例見 `.claude/rules/list-page-header.md`。

## 7. enum 契約

非 nullable 的 `$enumDecode` 遇到後端新增值 → **整批解析失敗、整頁空白**。
新增／修改 `lib/models/enums/` 前先確認後端 SoT，並補上契約測試。
（2026-07-29 操作紀錄頁全毀的真實案例：`docs/shared/enum_decode_hardening.md`）

## 8. build_runner 必跑情境

改到以下任一路徑後**必跑**，否則編譯錯或行為對不上：

- `lib/api/restclient/`、`lib/api/request/`、`lib/api/response/`、新增 `@JsonSerializable()`

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

---

## 踩到怪事時的查詢順序

1. `docs/bug_record/` — 歷史 bug 復盤（表格 loading 卡住、公司切換、圖表、發票下載…）
2. `docs/claude/claude-troubleshooting.md` — 已知陷阱總表
3. `docs/shared/*.md` — 相關任務文件，通常已寫明風險與邊界
4. `git log --oneline -- <檔案>` — 這段程式碼為什麼長這樣

---

## 溝通與輸出慣例

回報變更時用這個格式（`.claude/rules/output-style.md`）：

```
⚠️ 風險分析
此變更會影響 [模組]，可能導致 [風險]。

✅ 建議方案
[具體步驟]

📝 測試清單
- [ ] 項目 1
```

一律繁體中文台灣用語；技術術語與識別符保留英文。