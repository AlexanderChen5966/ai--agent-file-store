# 路徑 E · 業務名詞與環境

> 基準：**`main` 分支**（`190038a9`）。
> sanlong（山隆 PAY）是**加油站的消費者端 APP**：加油站服務、儲值金管理、會員點數。
> 使用者是一般車主。

> ⚠️ 名詞由 `Screen` enum、UI 目錄與文案推得，**業務語意以 PM 說明為準**，有疑問直接問。

---

## 核心概念

```
會員（註冊 / 簡訊驗證 / 升級帳號）
  ├── 儲值金（先儲值後消費，加油享折扣）
  ├── 會員點數（消費累點）
  ├── 支付工具：儲值金 / 綁定信用卡
  └── 消費場景：加油（QR / 快速加油）、洗車預約、超商
```

## 名詞表

| 名詞 | 說明 | Screen enum / 目錄 |
|---|---|---|
| 儲值金 | APP 內預付金，加油折扣的主要來源 | `storedMoney`、`storeMoneyResult`、`ui/store_money/` |
| 會員點數 | 消費累積的點數，與儲值金是兩回事 | `memberPoint`、`ui/member_point/` |
| 快速加油 | 免逐步操作的加油流程 | `quickRefueling`、`quickModeSetting`、`ui/refuel_setting/` |
| B2B 快速加油 / 綁定 | 企業客戶用的加油流程與綁定 | `b2bQuickRefueling`、`b2bBind` |
| B2C 條碼 | 消費者出示的付款條碼 | `b2cBarCode`、`ui/qrcode/` |
| 站點 QR | 掃加油站的 QR 進入流程 | `stationQrCode` |
| 支付設定 / 快速通行設定 | 選預設支付方式；**bug 最密集區**（SSGS-13122） | `paymentSetting`、`quickPassSetting`、`ui/quick_pass_setting/` |
| 預約洗車 | 選車 → 下單 → 訂單明細 | `carWashSelectCar`、`carWash`、`carWashOrder`、`carWashOrderDetail`、`ui/car_wash/` |
| 消費紀錄 | 交易明細，含超商明細專屬頁 | `record`、`recordDetail`、`recordConvientStoreDetail` |
| 油價 | 油價查詢與提醒設定 | `fuelPrice`、`fuelPriceSetting` |
| 站點 | 列表／篩選／地圖 | `stationList`、`stationFilter`、`stationMap`、`ui/station/` |
| 發票設定 | 載具／發票相關 | `receiptSetting` |
| 車號設定 | 綁定車牌 | `carNumberSetting`、`userDataAndCarNumberSetting` |
| 升級帳號 | 從試用／輕量帳號轉正式會員 | `upgradeAccount`、`trial` |
| 公告 | 站內文章／公告 | `information`、`informationDetail`、`article` |

完整清單看 `lib/app/router/config.dart`（82 行，`Screen` enum 就是全站畫面地圖）。

---

## 環境

| 環境 | 後端 API | 入口檔 |
|---|---|---|
| dev | https://customer.dev.ssgsslc.com | `main_ios_dev.dart` / `main_android_debug.dart` |
| staging | https://customer.staging.ssgsslc.com | `main_ios_staging.dart` / `main_android_staging_debug.dart` |
| 正式 | https://customer.ssgsslc.com | `main_ios_release.dart` / `main_android_release_debug.dart` |

URL 常數：`lib/app/controller/repository_api.dart:24-26`；實際生效的是 `BASE_URL`（同檔 `:29`）。

⚠️ **flavor 名稱兩平台不一致**：staging 在 iOS 叫 `stage`、Android 叫 `staging`；
正式版 iOS 用預設 scheme `Runner`（不帶參數）、Android 叫 `product`。詳見 `day1-setup.md`。

APP 顯示名稱也隨 flavor 變（`android/app/build.gradle.kts`）：
`DEV山隆Pay` / `Stage山隆Pay` / `山隆Pay`，icon 也不同——**看手機上的名字就知道自己裝的是哪個環境**。

---

## 資料與儲存

| 位置 | 放什麼 |
|---|---|
| `lib/app/controller/local.dart` | SharedPreferences（本地偏好、旗標） |
| `lib/app/service/crypto.dart` | 密碼雜湊（`argon2`）、敏感資料加密（`encrypt`） |
| `lib/app/common/dto/api.dart` | Freezed DTO（1415 行），API 進出的型別 |
| `lib/app/common/data/data.dart` | Data Model（800 行），APP 內部使用的模型 |

❌ 密碼／Token 不可存明文，❌ 不可在 URL 傳敏感資料，❌ 不可自行挑加解密方案。

---

## 多語系

只有一份 `assets/zh-tw.csv`（473 行），走 `easy_localization`，用 `.tr()` 讀。
key 是**畫面代碼式**（`A1.1.0.title`、`B6.1.0.recordTitle`、`C1.0.0.fuelTitle`），
新增時沿用該畫面既有前綴；❌ 不可用中文字串當 key。

---

## 分支與版本

- 分支：`main`（正式）／`feature/SSGS-XXXX`；commit 訊息用繁體中文並含 `SSGS-XXXX`
- 版本：`pubspec.yaml` 的 `version:`（`main` 目前 `2.25.0+710`）
- 版本代碼由 CI 自動累加：dev +1／stage +2／production +3（`.claude/rules/release-checklist.md`）
