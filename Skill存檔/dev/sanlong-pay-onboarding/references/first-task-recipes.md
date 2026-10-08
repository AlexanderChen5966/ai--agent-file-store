# 路徑 C · 第一個任務食譜

> 基準：**`main` 分支**（`190038a9`）。
> 原則：**照抄既有實作**，每道食譜都先指出樣板檔案。改動範圍以「達成需求的最小改動」為界，
> 不順帶重構、不動不相關檔案。

---

## 食譜 0：動手前的自檢

- [ ] 有沒有現成工具可用？→ 先查 `lib/app/utils/`（`.claude/rules/dev-resources.md` 明訂必查）
- [ ] 要改共用元件嗎？→ 先 `grep -rn "<元件名>" lib/` 確認使用範圍，**需使用者同意**
- [ ] 要引入新套件嗎？→ **需使用者同意**（維護中、Stars > 1000、無已知漏洞）
- [ ] 要動原生 iOS / Android 設定嗎？→ **需使用者同意**
- [ ] 要拆 SLController / 改資料模型核心結構嗎？→ **先提計畫並取得同意**

改 UI 前讀 `DESIGN.md`；碰 Bottom Sheet／固定高度排版前讀 `.claude/rules/flutter-ui-pitfalls.md`；
動 provider 前讀 `.claude/rules/riverpod-state-sync.md`。

---

## 食譜 1：新增一個畫面（Screen）

路由是自製的，**三個地方要一起改**，漏一個就是白畫面或崩潰：

1. **`lib/app/router/config.dart`** — `Screen` enum 加一個值
2. **`lib/app/router/router_delegate.dart:46` 的 `_screenOf()`** — switch 加 case
   ```dart
   case Screen.myNewScreen:
     return const MyNewScreen();
   ```
   需要帶參數時照 `case Screen.article`（同檔 `:58`）的寫法從 `config.data` 取並做型別檢查
3. **`lib/app/ui/<功能>/my_new_screen.dart`** — 畫面本體，用 `ConsumerStatefulWidget`

導航進去：

```dart
_router.pushMain(NavConfig(
  screen: Screen.myNewScreen,
  data: 要傳的資料,
  isTopPadding: true,
  isDraggable: false,   // ⚠️ 見下方
));
```

⚠️ **`isDraggable` 決定動畫方向**：不帶或 `false` = 側面滑入；`true` = **底部彈出**（下拉可關）。
想要「和帳號設定一樣側滑進入」卻帶了 `true`，畫面會從底部冒出來——參數名完全沒有暗示，
是本專案最常被踩的坑之一。

---

## 食譜 2：新增一支 API

樣板：`lib/app/controller/repository_api.dart` 內任一方法。

1. **路徑常數** → `lib/app/const/api_path.dart`
   （該檔慣例會把 response JSON 範例寫成註解放在常數下方，照做）
2. **DTO** → `lib/app/common/dto/api.dart`，Freezed 寫法：
   ```dart
   @freezed
   class MyRequestDto with _$MyRequestDto {
     const MyRequestDto._();
     const factory MyRequestDto({
       @intCv int? page,
     }) = _MyRequestDto;
     factory MyRequestDto.fromJson(Map<String, dynamic> json) =>
         _$MyRequestDtoFromJson(json);
   }
   ```
   型別轉換用 `dto/converter.dart` 的 `@intCv` 等 annotation。
3. **跑產生器（必須）**：
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```
   產物 `api.freezed.dart` / `api.g.dart`，**不要手改**。
4. **Repository 方法** → `repository_api.dart`，用
   `_network.request(url: BASE_URL, path: ..., method: ...)`；
   回應統一先包 `ResponseDto.fromJson(r)` 再取 `dto.data` 轉成自己的 DTO
5. **Controller 方法** → `controller.dart`，命名 `on{Screen}{Action}`，UI 從這裡呼叫

❌ UI 層不可跳過 controller 直接呼叫 repository。

---

## 食譜 3：新增一個顏色

1. 先搜 `lib/app/const/color.dart`（92 行）有沒有接近的既有常數
2. 真的沒有才新增在該檔：
   ```dart
   static const myNewColor = Color.fromRGBO(1, 156, 222, 1.0);
   ```
   本專案慣用 `Color.fromRGBO`，`SLColor` 是 `extension SLColor on Color`
3. 使用：`SLColor.myNewColor`

❌ **Widget 內硬編碼 `Color(0xff...)` / `Color.fromRGBO(...)` 是紅線。**
另有大量功能域專屬 token（`storeMoney*` / `quickMode*` / `washCar*` 等），使用前先查該檔。

---

## 食譜 4：新增／修改一句文案（最適合當第一個練手）

1. 開 `assets/zh-tw.csv`（473 行，格式 `key,中文`，首行 `str,zh_TW`）
2. **先 grep 有沒有現成 key**
3. 新增時**沿用該畫面既有的前綴**——key 是畫面代碼式，不是語義式：
   ```
   A1.1.0.title,歡迎使用山隆PAY
   B6.1.0.recordTitle,...
   C1.0.0.fuelTitle,...
   ```
   不確定新畫面該用什麼代碼就問，別自己發明一組。
4. 使用：`'A1.1.0.title'.tr()`（easy_localization）

❌ **不可用中文字串當 key**，❌ 不可在 Widget 內硬編碼中文。

---

## 食譜 5：做一個 Bottom Sheet

**先讀 `.claude/rules/flutter-ui-pitfalls.md` 第 2 條**，結論：

- ✅ 用 `showModalBottomSheet` 並帶 `isScrollControlled: true`（必要，才能貼底並自訂高度）
- ❌ 不要用 `showFlexibleBottomSheet`——會定位在畫面中間，且搭 `ConsumerStatefulWidget`
  會丟 `parentDataDirty` assertion 崩潰
- 鍵盤頂起：內容 `Padding` 加 `bottom: MediaQuery.of(context).viewInsets.bottom + 16`
- 底部按鈕被 home indicator 切掉 → 最外層包 `SafeArea`
- **樣板**：`ui/quick_pass_setting/quick_fuel_bottom_sheet.dart:304`、
  `quick_wash_bottom_sheet.dart:418`（兩處都是 `showModalBottomSheet<bool>(`）；
  通用封裝在 `utils/dialog_utils.dart`

---

## 食譜 6：跳一個提示對話框

**選型別搞錯會白做工**（`.claude/rules/flutter-ui-pitfalls.md` 第 9 條，來源 SSGS-11615）：

| 要做的事 | 用什麼 |
|---|---|
| 標準提示／確認／警告（icon＋title＋body＋按鈕列） | **`DialogDisplay`**（`ui/widget/dialog.dart`），controller 內 `dialog = DialogDisplay(...)`，**不需 BuildContext**、不能 await |
| Bottom Sheet、客製版型、需**等回傳值** | `DialogUtils` / `showDialog`（`utils/dialog_utils.dart`），UI 層帶 context，可 await |

⚠️ **不要為了改樣式就改用 `showDialog`**——`DialogDisplay` 的 `titleColor` / `titleFontSize` /
`bodyFontSize` 等全是 optional 參數，調樣式**傳參數**即可；改 `showDialog` 重刻會失去全 APP 統一的
`margin: horizontal 32`。icon 走 `iconName`（`assets/img/<name>.png`），**固定 120×120，放不了任意 widget**。
完整參數用法參照 `controller/controller.dart` 內既有呼叫點。

---

## 食譜 7：加一個「送出」類動作（防重複提交）

照抄 `onStoreMoneyScreenAddMoney`（`controller.dart:1267`）：

1. 在 `loading_state.dart` 的 `SLAction` 加一個 action
2. controller 內加 getter / setter 委派給 `_loading`：
   ```dart
   bool get isXxx => _loading.getLoading(SLAction.xxx);
   set isXxx(bool value) => _loading.setLoading(SLAction.xxx, value);
   ```
3. 方法開頭擋住重入：
   ```dart
   if (isXxx) return;
   isXxx = true;
   try { ... } catch (e) { isXxx = false; ... }
   ```
4. UI 讀同一份狀態顯示 loading：`ref.watch(loadingAct(SLAction.xxx))`

⚠️ **擋在 controller，不是在 UI 層 disable 按鈕**——這是專案慣例，直覺會做錯。

---

## 食譜 8：改到「會被多個畫面讀取的設定」

本專案 bug 最密集的地方（SSGS-13122 來回修三輪）。**必讀 `.claude/rules/riverpod-state-sync.md`**：

```dart
// ❌ 上傳完就結束，provider 還是舊值
await c.uploadQuickModelSetting(request);

// ✅ 上傳成功後主動重取，讓所有讀這個 provider 的畫面同步
final success = await c.uploadQuickModelSetting(request);
if (!success) return;              // 失敗不要往下走
await c.getQuickModelSetting();
```

排查手法比記規則有用：

> 改完狀態後，`grep` 一下這個 provider 還有誰在讀。
> **每一個讀它的畫面都是潛在的「顯示舊值」現場。**

該規則檔末尾有一份**七項快速檢查清單**（含 `autoDispose` null 分支、request 主鍵欄位、
toast 與關頁順序），動手前逐條過一遍。

---

## 食譜 9：準備上架（改版本代碼）

**先讀 `.claude/rules/release-checklist.md`。** CI 各環境從同一基底獨立累加——
dev +1、stage +2、**production +3**。

```
基底 = Play Store / App Store 現行最大版本代碼 + 1
production 實際上架代碼 = 基底 + 3
```

改 `pubspec.yaml` 的 `version:`（`main` 目前是 `2.25.0+710`）那個 `+數字`，
改前先確認現行最大代碼、以及有沒有其他 feature branch 佔用。

---

## 食譜 10：送出前

```bash
flutter analyze     # CI 的 flutter_analyzer stage 會跑
```

- 實機或模擬器跑過一次，確認動線正常
- Commit 訊息用**繁體中文**並含 issue 編號：`SSGS-XXXX`
- 分支：`main`（正式）／`feature/SSGS-XXXX`

---

## 建議的第一個真任務

**「調整某個輸入欄位的長度限制」**——會同時碰到 UI 層、controller 與 i18n 字串，
但風險極低、驗收明確。可參考近期同型 commit（暱稱／聯絡我們主旨／回饋內容長度調整）。
