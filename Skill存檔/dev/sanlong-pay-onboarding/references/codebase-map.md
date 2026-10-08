# 路徑 B · 專案地圖：東西在哪

> 基準：**`main` 分支**（`190038a9`）。223 個 dart 檔全在 `lib/app/` 底下。
> **先讀一條垂直切片，不要橫向掃完整層。**

---

## 1. 分層（固定，不可繞過）

```
UI (ConsumerStatefulWidget)
   ↓  ref.watch(controller) 取得 SLController
SLController（lib/app/controller/controller.dart，3418 行）
   ↓  _repo.xxx()
Repository（repository_api.dart，1435 行）
   ↓
資料層：Dio（API）／ SharedPreferences（local.dart）
```

❌ **UI 層直接呼叫 API 是紅線**（`AGENTS.md` NEVER 清單），一律經 SLController。

## 2. 目錄圖

```
lib/
├── main.dart                    # mainCommon()，共用初始化
├── main_ios_dev.dart 等 6 支      # 真正的入口，各設 flavor 與 BASE_URL
└── app/
    ├── router/
    │   ├── config.dart          # ⭐ Screen enum（82 行，全站畫面清單）
    │   └── router_delegate.dart # ⭐ 路由映射 _screenOf()（291 行）
    ├── controller/
    │   ├── controller.dart      # ⭐ SLController，單一大型（3418 行）
    │   ├── repository_api.dart  # ⭐ API 呼叫 + BASE_URL（1435 行）
    │   ├── local.dart           # SharedPreferences（151 行）
    │   └── loading_state.dart   # LoadingController / SLAction（防重複提交底層）
    ├── common/
    │   ├── dto/api.dart         # ⭐ Freezed DTO（1415 行）
    │   └── data/data.dart       # Data Model（800 行）
    ├── const/
    │   ├── color.dart           # ⭐ SLColor（92 行）
    │   ├── api_path.dart        # API 路徑常數（含 response 範例註解）
    │   └── const.dart / tag.dart
    ├── ui/                      # 依功能分目錄，見下表
    ├── utils/                   # ⭐ 通用工具，動手前必查
    ├── service/                 # auth / crypto / location / network
    ├── notify/ push/            # 推播
    └── log_utils.dart
```

`assets/zh-tw.csv`（473 行）＝ 所有中文文案。

### UI 功能目錄

| 目錄 | 檔數 | 內容 |
|---|---|---|
| `ui/car_wash/` | 17 | 洗車服務 |
| `ui/qrcode/` | 14 | QR 出示 / 掃碼付款 |
| `ui/refuel_setting/` | 11 | 加油設定 |
| `ui/station/` | 10 | 站點列表／篩選／地圖 |
| `ui/authentication/` | 9 | 註冊、登入、簡訊驗證、升級帳號 |
| `ui/profile/` | 9 | 個人設定 |
| `ui/store_money/` | 7 | 儲值 |
| `ui/home/` | 7 | 首頁、Tab |
| `ui/credit_card/` | 6 | 信用卡綁定 |
| `ui/consume_record/` | 4 | 消費紀錄 |
| `ui/quick_pass_setting/` | 3 | 快速通關設定（含兩支 Bottom Sheet 樣板） |
| `ui/fuel_price/` `ui/information/` `ui/member_point/` `ui/trial/` | 1-3 | 油價／公告／點數／試用 |
| `ui/widget/` | 27 | ⭐ 共用元件（`SLText`、`DialogDisplay` 等） |

---

## 3. 兩件必須先講清楚的事（否則新人會誤判）

**① `controller.dart` 3418 行是刻意的單一大型 controller，不是技術債沒清。**
新人看到會想拆——**不要自己動手**。拆 SLController 屬於「先提計畫並取得使用者同意」的範圍
（`AGENTS.md` >「修改範圍原則」）。

**② 路由是自製的 SLRouter + NavStack，不是 go_router / Navigator 2.0。**
官方文件查不到，要看 `lib/app/router/router_delegate.dart`。新增畫面要同時改
`config.dart` 的 `Screen` enum 與 `router_delegate.dart:46` 的 `_screenOf()` switch。

---

## 4. 垂直切片：「按下儲值」從點擊到結果頁

依序看這幾行，就懂了完整資料流：

| # | 位置 | 做什麼 |
|---|---|---|
| 1 | `ui/store_money/store_money_screen.dart:127` | `final c = ref.watch(controller);` 取得 SLController |
| 2 | 同檔 `:219` | `isLoading: ref.watch(loadingAct(SLAction.addStoreMoney))` 讀 loading |
| 3 | 同檔 `:227` | `c.onStoreMoneyScreenAddMoney(context, c, 金額, retry)` ← 命名慣例 `on{Screen}{Action}` |
| 4 | `controller/controller.dart:1267` | 方法本體 |
| 5 | 同檔 `:1268` | `if (isStoringMoney) { return; }` ← **防重複提交擋在 controller，不是 UI** |
| 6 | 同檔 `:1273` | `final r = await _repo.storeMoney(controller, value);` 進 Repository |
| 7 | 同檔 `:1279` | `_router.pushMain(NavConfig(screen: Screen.storeMoneyResult, ...))` |

**⚠️ 文件與程式碼的落差**：`CLAUDE.md` 寫「防重複提交用 SLController 內的 bool flag（如 `isStoringMoney`）」，
實際上 `isStoringMoney`（`controller.dart:1261`）是 getter，底層委派給
`_loading.getLoading(SLAction.addStoreMoney)`。所以它**同時**是防重複的閘門與 UI 的 loading 來源
——UI 用 `ref.watch(loadingAct(SLAction.xxx))` 讀同一份狀態。
新增這類流程照抄這個模式，不要另外宣告一個裸 bool。

---

## 5. 「我要改 X，該打開哪個檔案」

| 想改什麼 | 去哪 |
|---|---|
| 某畫面的版面 | `lib/app/ui/<功能>/<功能>_screen.dart` |
| 新增／修改畫面路由 | `router/config.dart`（Screen enum）＋ `router/router_delegate.dart:46`（`_screenOf`） |
| 業務邏輯、API 呼叫時機 | `controller/controller.dart`，方法名 `on{Screen}{Action}` |
| API 端點、request/response | `controller/repository_api.dart` ＋ `const/api_path.dart` |
| DTO 欄位 | `common/dto/api.dart`（Freezed，改完要跑 build_runner） |
| 本地儲存 | `controller/local.dart` |
| 顏色 | `const/color.dart`（`SLColor`），❌ 不可 inline `Color(0xff...)` |
| 中文文案 | `assets/zh-tw.csv`，用 `.tr()` 讀 |
| 標準提示對話框 | `ui/widget/dialog.dart` 的 `DialogDisplay` |
| Bottom Sheet / 客製對話框 | `utils/dialog_utils.dart` |
| loading / 防重複 | `controller/loading_state.dart` 的 `SLAction` |

---

## 6. 動手前必查 `lib/app/utils/`

`.claude/rules/dev-resources.md` 明訂：**開發前必須先查有沒有現成工具**。常用的有
`dialog_utils.dart`、`date_format_utils.dart`、`string_utils.dart`、`button_util.dart`、
`text_util.dart`、`column_util.dart` / `row_util.dart`、`view_util.dart`、
`permission_utils.dart`、`store_money_in_quick_mode.dart`。

⚠️ 但 `text_util.dart` / `column_util.dart` 有已知陷阱（回傳 `Container(width: double.infinity)`、
`MainAxisSize.max`）——用之前先讀 `.claude/rules/flutter-ui-pitfalls.md` 第 3、4 條。

---

## 7. 找東西的實用指令

```bash
# 某句中文出現在哪
grep -n "歡迎使用" assets/zh-tw.csv

# 某個 Screen 怎麼被推出來的
grep -rn "Screen.storedMoney" lib/app | head

# 某個 provider 還有誰在讀（改狀態前必做）
grep -rn "quickModeProvider" lib/app | head

# 這個 bug 以前發生過嗎（docs/ 未進版控，需先向團隊索取）
ls docs/bug_record/ docs/issue/ 2>/dev/null
```

> ⚠️ `docs/` 在 `.gitignore:57`，**clone 下來不會有**。需要 `docs/onboarding.html`、
> `docs/page_architecture/PROJECT_ARCHITECTURE.md` 等資料時要請團隊成員直接傳給你。
