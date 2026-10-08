# 路徑 D · 紅線與地雷

> 基準：**`main` 分支**（`190038a9`）。
> 這份是「被 review 打回來之前先知道」。完整版在 `AGENTS.md`、`.claude/rules/`（會依
> `paths:` 條件自動載入）與 `DESIGN.md`；本檔負責排序與導讀。

---

## 🔴 NEVER（`AGENTS.md`，無例外）

| 禁止 | 正確做法 |
|---|---|
| `setState()` 管理全域狀態 | 用 Riverpod |
| UI 層直接呼叫 API | 一律經 SLController |
| Widget 內硬編碼 `Color(0xff...)` / `Color.fromRGBO(...)` | 用 `SLColor.*`，缺色加進 `lib/app/const/color.dart` |
| Widget 內硬編碼中文字串 | `assets/zh-tw.csv` 的 key ＋ `.tr()`；**不可用中文字串當 key** |
| 使用 `flutter_screenutil`（`.w`/`.h`/`.sp`） | **本專案未導入**，見下方第 1 條 |
| 密碼／Token 存明文、URL 傳敏感資料 | — |
| 自行挑加解密方案 | 密碼雜湊用 `argon2`、敏感資料加密用 `encrypt`，實作集中在 `lib/app/service/crypto.dart` |

## ⚠️ 需先取得使用者同意才動手

- 修改共用元件（先 `grep -rn "<元件名>" lib/` 確認使用範圍）
- 引入新第三方套件（維護中、Stars > 1000、無已知漏洞、不與現有套件衝突）
- 修改原生 iOS / Android 設定
- 跨模組重構、拆 SLController、換狀態管理方案、改資料模型核心結構

---

## 1. 這個專案**沒有** screenutil

`.w` / `.h` / `.sp` 在本專案不存在。**同時碰 b2b-manager 的人照抄會破壞版面**——
那邊是 Flutter Web、有 screenutil 的歷史包袱；這邊是手機 APP，字級為固定邏輯像素、不縮放
（`DESIGN.md` ②）。

## 2. `isDraggable` 決定導航動畫方向

`pushMain(NavConfig(...))`：不帶或 `false` = **側面滑入**；`true` = **底部彈出**（下拉可關的 modal）。

❌ 想要「和帳號設定一樣側滑進入」而加了 `isDraggable: true` → 變成從底部彈出。
參數名完全沒有暗示，要看畫面才發現。

## 3. 防重複提交擋在 controller，不是 UI

直覺會在 UI 層 disable 按鈕，本專案慣例是 SLController 內用 loading flag
（`isStoringMoney` → `_loading.getLoading(SLAction.addStoreMoney)`）。
作法見 `references/first-task-recipes.md` 食譜 7。

## 4. 待支付檢查是 APP 端本地 flag

`isWaiting` 是**本地狀態，不是 API 提供的欄位**。新人會去翻 API 文件找，找不到。
（`CLAUDE.md` >「模型不易自行發現的專案慣例」）

## 5. Riverpod 狀態同步——本專案 bug 最密集處

來源 SSGS-13122（支付設定改版），來回修三輪。六個點在
`.claude/rules/riverpod-state-sync.md`，最常踩的兩個：

1. **上傳成功後要主動刷新對應 provider**——Repository 的 upload **不會**自動更新 provider
2. **把 provider 值抄成 local state 的畫面要用 `ref.listen` 同步**——只在 `initState` 讀一次，
   之後 provider 再怎麼變畫面都不知道

其餘：`autoDispose` 沒有 listener 時會重置（讀之前要有 null 分支）、上傳失敗不可走成功流程、
request 要帶齊主鍵欄位、提示與導頁的順序（先關頁再 toast）。
該檔末尾有**七項快速檢查清單**，動狀態前逐條過。

> 排查手法比記規則有用：改完狀態後 `grep` 這個 provider 還有誰在讀，
> **每一個讀它的畫面都是潛在的「顯示舊值」現場。**

## 6. UI 排版的十一個坑

`.claude/rules/flutter-ui-pitfalls.md`（來源 SSGS-12507 / 11615 / 13122，每條都是實際發生過的失敗）。
新人最容易撞到的：

| # | 坑 |
|---|---|
| 2 | Bottom Sheet 要貼底用 `showModalBottomSheet` + `isScrollControlled: true`；`showFlexibleBottomSheet` 會定位在中間並丟 `parentDataDirty` 崩潰 |
| 3 | `text_util.dart` 的 `buildLeftText` / `buildRightText` 回傳 `Container(width: double.infinity)`，**不能直接當 `Row` 的 child**（要 `Expanded` 包，或改用純 `Text`） |
| 4 | `column_util.dart` 的 `buildLeftColumn` 是 `MainAxisSize.max`，放進固定高度容器會 overflow |
| 5 | 內部已含 `CustomScrollView` 的元件外層別再包 `SingleChildScrollView` |
| 6 | Scaffold 底部按鈕被 home indicator 切掉 → 包 `SafeArea` |
| 8 | 「隱藏但保留高度」用 `Visibility` 的三個 `maintain*` 旗標（`maintainSize` 需同時開另兩個） |
| 9 | Dialog 選型：標準提示用 `DialogDisplay`，需 await 回傳值才用 `showDialog` |
| 10 | `LongButton` 不會自己撐寬 |
| 11 | 虛線外框要自繪，專案沒有 dashed border 套件，repo 內目前也沒有可參照的實作 |

## 7. 共用元件先確認使用範圍再改

修改任何 UI 元件前先 `grep -rn "<元件名>" lib/ --include="*.dart"`。
✅ 新功能加在 **wrapper 頁**，不改共用元件本身。
**例外**：需求明確要求「新舊樣式一致」時，就該直接改共用元件本體而非複製一份
（SSGS-13122 一開始另建 `AddCreditCardCell`，後因兩頁需一致而改共用並刪檔）。

## 8. 上架版本代碼

CI 各環境從同一基底獨立累加：dev +1、stage +2、**production +3**。
基底 = 商店現行最大代碼 + 1。詳見 `.claude/rules/release-checklist.md`。

---

## 命名與 Git

- Controller 方法：`on{Screen}{Action}`（例 `onStoreMoneyScreenAddMoney`），其餘沿用 Dart 慣例
- 分支：`main`（正式）／`feature/SSGS-XXXX`
- Commit 訊息用**繁體中文**並含 issue 編號（`SSGS-XXXX`）

---

## 踩到怪事時的查詢順序

1. `.claude/rules/` 四份規則檔（UI 陷阱／狀態同步／開發資源／上架檢查）
2. `docs/bug_record/`、`docs/issue/` 歷史復盤 ⚠️ `docs/` 未進版控，需向團隊索取
3. `git log --oneline -- <檔案>` — 這段程式碼為什麼長這樣
4. 規則檔引用的行號會隨改動位移，**對不上時以原始碼為準**
