# 路徑 A · Day 1：把專案跑起來

目標：**當天在 `http://localhost:9001` 登入到首頁儀表板。**

---

## 1. 環境需求

| 項目 | 版本 | 檢查指令 |
|---|---|---|
| Flutter | **3.38.0 stable**（2026-08-25 團隊實測可跑的版本；`pubspec.yaml` 下限只寫 3.3.0+，但別拿它當目標） | `flutter --version` |
| Dart SDK | >=3.3.0 <4.0.0 | 隨 Flutter |
| Chrome | 最新 | 唯一開發目標平台 |
| Docker | 選配 | 只有要驗證部署映像時才需要 |

```bash
flutter doctor          # Web 那列要是 ✓；iOS/Android 沒過不影響（本專案不支援）
flutter config --enable-web
```

---

## 2. 取得相依

```bash
cd /Users/alexander/GitLab/b2b-manager
flutter pub get
```

⚠️ `external_libs/` 底下是**專案特製的 fork 套件**（`data_table_2`、`filter_list`、
`flutter_json_view`、`font_awesome_flutter`、`multiselect_dropdown`），以 path dependency 引入。
**不可 `flutter pub upgrade`**，要改只能直接編輯原始碼（見 `.claude/rules/external-libs.md`）。

---

## 3. 產生程式碼（第一次必跑）

`.g.dart` 不進版控的部分需要自己生；缺了會是一堆 `_$XxxFromJson` undefined。

```bash
flutter pub run build_runner build --delete-conflicting-outputs   # Retrofit + json_serializable
flutter pub run intl_utils:generate                                # i18n（lib/generated/）
```

---

## 4. 跑起來

**port 必須是 9001。** OAuth2 callback 白名單是寫死的
（`http://localhost:9001/callback`、`http://localhost:9001/frontchannel_logout`），
換 port 會在登入導回時失敗。

```bash
flutter run -d chrome \
  -t lib/main_dev.dart \
  --dart-define=DEPLOY=dev \
  --dart-define=FLUTTER_WEB_USE_SKIA=true \
  --no-enable-impeller \
  --web-port=9001
```

JetBrains / Android Studio 使用者：專案已附三組 run configuration（`.run/main_dev.dart.run.xml`、
`main_staging_dart`、`main_release_dart`），直接選 `main_dev.dart` 執行即可，參數同上。

入口檔對應：`lib/main_dev.dart` / `lib/main_release.dart`。環境由 `--dart-define=DEPLOY` 決定：
`lib/main.dart:50` 讀成全域 `DEPLOY`，再用 `lib/api/flavor_config.dart` 的
`Flavor.fromString()` 轉成 `dev / staging / release`（無值時預設 `dev`）決定打哪台後端。

| DEPLOY | 前端 | 後端 API |
|---|---|---|
| `dev` | https://b2bmanager.dev.ssgsslc.com | https://b2b-backend.dev.ssgsslc.com |
| `staging` | https://b2bmanager.staging.ssgsslc.com | https://b2b-backend.staging.ssgsslc.com |
| `release` | https://b2bmanager.ssgsslc.com | https://b2b-backend.ssgsslc.com |

> 新人一律先用 **dev**。跑 staging／release 前先問過負責人。

---

## 5. 登入

### 先拿到 dev 帳號

dev 環境帳號要跟團隊索取。**目前沒有固定的申請窗口或表單**——直接在團隊群組問，
或問帶你進來的人；不必等特定某個人。

**等帳號的期間不要空轉**，以下都不需要登入就能做完：

- 第 2～3 節的 `pub get` 與兩支產生器（build_runner / intl_utils）先跑完
- `flutter analyze` 跑一次，確認本機環境乾淨
- 讀 `references/codebase-map.md` 的「垂直切片」——那 6 個檔案純讀原始碼，不用跑起來
- 讀 `references/conventions-gotchas.md`，先把地雷認完
- 掃一遍 `docs/shared/readme.md`，看團隊最近在做什麼

換句話說：**四小時路線的第 2、4、5 步都不卡帳號**，拿到帳號再回頭補第 1 步的驗收即可。

### 登入流程

**OAuth2 Authorization Code + PKCE**：

```
點登入 → auth_service.dart 發起 → OAuth server → 授權
→ 導回 /callback?code=XXX → handleAuthorizationResponse()（經 TaskManager）
→ 換 token → CookieManager 儲存 → 401 時 Interceptor 自動 refresh（同樣經 TaskManager）
```

相關檔案：`lib/api/connector/auth_service.dart`、`oauth_connector.dart`、
`task_manager.dart`、`secure_storage.dart`、`lib/api/interceptor/`。

---

## 6. 常見卡點

| 症狀 | 原因 / 解法 |
|---|---|
| 登入後一直轉圈或回到登入頁 | port 不是 9001，callback 對不上 |
| `_$XxxFromJson` undefined、`.g.dart` 找不到 | 沒跑 build_runner；或跑了但沒加 `--delete-conflicting-outputs` |
| `S.of(context).xxx` 不存在 | 沒跑 `intl_utils:generate`，或 `.arb` 只加了 zh_TW 沒加 en |
| build_runner 卡住／衝突 | `flutter pub run build_runner clean` 後重跑；仍不行 `flutter clean && flutter pub get` |
| CORS / 跨網域被擋 | run config 的 `--disable-web-security` 是給 attach 用的；優先確認打的是 dev 後端 |
| 畫面元素亂掉、overflow | 視窗不是 1920 寬。基準解析度 1920×1024，先把瀏覽器拉滿再判斷 |
| 表格 RenderFlex overflowed | 幾乎都是雙行 cell 的 vertical padding > 2px，見 `.claude/rules/datatable-safety.md` |

---

## 7. 驗證與建置指令（CI 也跑這些）

```bash
flutter analyze --no-fatal-infos --no-fatal-warnings --pub   # 送 MR 前必跑
flutter test --platform chrome                                # Web-only，缺 --platform 會失敗
flutter build web --release --web-renderer html
```

> ⚠️ 測試套件目前有已知問題（見 `docs/shared/test_runnability_ci_gate.md`）：
> `test/task_manager_test.dart` 的相對 import 會讓整套編譯失敗、`widget_test.dart` 仍是預設樣板。
> 跑測試失敗**先確認是不是踩到這個已知狀況**，不要以為是自己弄壞的。

Docker（要驗部署才用）：

```bash
docker build -t b2b_manager .
docker run -p 8089:8089 b2b_manager
# 或 docker-compose -f docker-compose.yml up
```

---

## Day 1 驗收

- [ ] `flutter analyze` 通過（warning 可接受，error 不行）
- [ ] `localhost:9001` 能登入進首頁儀表板
- [ ] 側邊選單各分頁都能點開、列表有資料
- [ ] 改一個 `SLText` 的字，hot reload 看到畫面變化（**改完還原，不要 commit**）