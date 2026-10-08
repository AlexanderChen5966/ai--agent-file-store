# 路徑 A · Day 1：把 APP 跑起來

> 基準：**`main` 分支**（`190038a9`）。行號與檔案規模皆以此為準；
> 在 feature 分支上數字會不同，對不上時以原始碼為準。

目標：**當天在模擬器或實機跑起 dev，進到首頁。**
手機專案比 Web 專案長（Xcode + CocoaPods + 憑證），時間抓 60 分鐘起跳。

---

## 1. 環境需求

| 項目 | 說明 | 檢查 |
|---|---|---|
| Flutter SDK | `pubspec.yaml` 要求 Dart SDK `>=3.5.0 <4.0.0`（README 那份 `flutter doctor` 範例寫 3.7.3，是舊紀錄，別當目標） | `flutter --version` |
| Xcode | iOS 必備；專案最低支援 **iOS 15.0**（commit `097a6258`） | `xcodebuild -version` |
| CocoaPods | iOS 相依管理 | `pod --version` |
| Android Studio | 含 Android SDK、Flutter/Dart plugin | `flutter doctor` |

```bash
flutter doctor      # iOS + Android 兩列都要 ✓（本專案不做 Web）
```

---

## 2. 取得相依

```bash
cd /Users/alexander/GitLab/app01-double
flutter pub get
cd ios && pod install && cd ..     # iOS 額外一步
```

iOS 還需 Xcode 憑證：開 `ios/Runner.xcworkspace` → Runner → Signing & Capabilities →
Team 選山隆（帳號需已加入 App Store Connect 且有開發權限）。詳見 `README.md`。

---

## 3. 選對入口檔與 flavor（本專案最容易卡的地方）

**沒有單一 `main.dart` 可以直接跑。** `lib/main.dart` 只放共用的 `mainCommon()`，
真正入口是六支 `main_*.dart`，各自設定 flavor 與 API base URL：

| 入口檔 | 平台 | flavorName | 打哪台後端 |
|---|---|---|---|
| `lib/main_ios_dev.dart` | iOS | Dev | https://customer.dev.ssgsslc.com |
| `lib/main_ios_staging.dart` | iOS | Staging | https://customer.staging.ssgsslc.com |
| `lib/main_ios_release.dart` | iOS | Release | https://customer.ssgsslc.com |
| `lib/main_android_debug.dart` | Android | Dev | 同上 dev |
| `lib/main_android_staging_debug.dart` | Android | Staging | 同上 staging |
| `lib/main_android_release_debug.dart` | Android | Release | 同上正式 |

URL 常數在 `lib/app/controller/repository_api.dart:24-26`。

### ⚠️ 兩個平台的 flavor 名稱不一樣，別互相照抄

| 環境 | iOS（Xcode scheme） | Android（gradle productFlavors） |
|---|---|---|
| dev | `dev` | `dev` |
| staging | **`stage`** | **`staging`** |
| 正式 | **`Runner`（預設，run config 不帶 flavor 參數）** | **`product`** |

iOS 的 scheme 檔在 `ios/Runner.xcodeproj/xcshareddata/xcschemes/`（`dev.xcscheme`／
`stage.xcscheme`／`Runner.xcscheme`）；Android 的定義在
`android/app/build.gradle.kts:107`（product）／`:114`（staging）／`:121`（dev）。

**最省事的作法：用 `.run/` 附的六組 run configuration**，在 IDE 裡都能正常跑——
scheme／flavor 是由 `buildFlavor` 欄位帶出 `--flavor` 的，不是靠 `additionalArgs`。
（iOS release 那支沒有 `buildFlavor`，走預設 scheme `Runner`，符合上表。）

> ⚠️ **但不要把 `additionalArgs` 整串複製到命令列。** iOS dev／staging 兩支裡的
> `--target dev`／`--target stage` 是冗餘的——`--target` 就是 `-t` 的長名，會被後面的
> `-t lib/main_ios_xxx.dart` 覆蓋掉。在 IDE 內無害（真正的 scheme 來自 `buildFlavor`），
> 但照抄到命令列就**完全沒有指定 scheme**。命令列請用下面的 `--flavor` 版本。

命令列版本：

```bash
# Android dev
flutter run --flavor dev -t lib/main_android_debug.dart
# Android 正式（注意是 product 不是 release）
flutter run --flavor product -t lib/main_android_release_debug.dart
# iOS dev（走 scheme，不是 gradle flavor）
flutter run --flavor dev -t lib/main_ios_dev.dart --no-enable-impeller
```

### ⚠️ `FlavorConfig` 設了但沒被讀

入口檔長這樣：

```dart
FlavorConfig(flavorName: 'Dev', values: {'apiBaseUrl': apiDevUrl});
BASE_URL = apiDevUrl;      // ← 實際生效的是這行全域變數
mainCommon();
```

`repository_api.dart` 裡 `FlavorConfig.getValue("apiBaseUrl")` 那行是**註解掉的**，
真正決定打哪台的是 `BASE_URL`（同檔 `:29`）。查「為什麼打到錯的環境」看 `BASE_URL`。

---

## 4. `.venv` 與那三支 python 是什麼（新人一定會問）

```
cicd_revise_flutter_yaml_dev.py       # CI：版本代碼 +1
cicd_revise_flutter_yaml_stage.py     # CI：版本代碼 +2
cicd_revise_flutter_yaml_release.py   # CI：版本代碼 +3
auto_git_push_flutter_pubspec_yaml.py
```

**本機開發用不到**，是 `.gitlab-ci.yml` 在 pipeline 裡呼叫、自動累加 `pubspec.yaml` 版本代碼用的。
`.venv` 是它們的 Python 環境。規則見 `.claude/rules/release-checklist.md`，**準備上架前才需要理解**。

---

## 5. 常見卡點

| 症狀 | 解法 |
|---|---|
| `pod install` 失敗 / iOS build 一堆錯 | `cd ios && pod repo update && pod install`；仍不行 `flutter clean` 重來 |
| build 失敗說找不到 flavor | 對照上面的名稱表——staging 在 iOS 叫 `stage`、正式版 Android 叫 `product` |
| 打到錯的後端 | 看 `BASE_URL`（`repository_api.dart:29`），不是 `FlavorConfig` |
| 畫面全白 / 卡啟動 | 漏了 `-t lib/main_xxx.dart`；直接跑 `main.dart` 不會初始化 flavor 與 BASE_URL |
| Bottom Sheet 崩潰 `parentDataDirty` | 用錯元件，見 `.claude/rules/flutter-ui-pitfalls.md` 第 2 條 |
| 改了設定但別的畫面沒更新 | 狀態同步問題，見 `.claude/rules/riverpod-state-sync.md` |

---

## 6. 驗證指令

```bash
flutter analyze     # CI 的 flutter_analyzer stage 會跑
flutter test
```

CI（`.gitlab-ci.yml`）stage 順序：
`update_pubspec` → `flutter_analyzer` → `osv_scanner`（相依套件弱點掃描）
→ `debug_build_android/ios` → `staging_build_*` → `release_build_*`。

---

## Day 1 驗收

- [ ] `flutter doctor` 的 iOS 與 Android 兩列都通過
- [ ] `flutter analyze` 沒有 error
- [ ] dev 在模擬器或實機跑起來，能進首頁
- [ ] 知道自己現在打的是哪一台後端，以及該平台的 flavor 叫什麼
