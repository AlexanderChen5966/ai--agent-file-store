# TASK CONTEXT — Phase 2 LOW Tier Developer 實測

> 本檔透過 stdin pipe 給 Copilot CLI developer：
> `cat TASK_FILE.md | copilot --model {MODEL} --allow-all-tools --autopilot -p "..."`
> 兩個受測模型使用**完全相同**的本檔內容，僅 `--model` 不同。

---

## Tier

LOW（developer 候選模型 A/B 測試）

## 隔離規則（重要）

- 所有產出檔案**只能**寫在本任務指定的輸出目錄：`./output/`（相對本 TASK_FILE 所在目錄）
- ❌ 禁止修改 `lib/`、`pubspec.yaml` 或專案任何既有檔案
- ❌ 禁止執行任何 git 指令
- 若 `./output/` 不存在請自行建立

## 專案規則（必須遵守）

- 純 Dart / Flutter，繁體中文台灣用語註解
- ❌ 禁止使用 `.w` / `.h` / `.sp`（screenutil）；尺寸用固定 px
- 命名、風格貼近一般 Flutter 專案慣例
- 不得引入額外第三方套件（僅用 Dart SDK / Flutter SDK）

---

## 任務目標

實作一組「車號（車牌）驗證工具」，共 **3 個檔案**，需彼此正確引用：

### 檔案 1：`output/plate_validator.dart`

提供 `PlateValidator` class，純邏輯、無 UI，包含：

1. `static PlateValidationResult validate(String input)`
   - 規則：
     - 去除前後空白後再驗證
     - 長度必須為 **2~7 碼**（含 2 與 7）；不符回傳 `tooShort` 或 `tooLong`
     - 只允許「大寫英文字母 A–Z、數字 0–9、一個連字號 `-`」；含其他字元回傳 `invalidChar`
     - 連字號不可出現在頭或尾，且最多一個；違反回傳 `invalidHyphen`
     - 全部通過回傳 `valid`
   - 自動將輸入的小寫英文轉成大寫後再驗證（normalize）
2. `static String normalize(String input)` — 去空白 + 轉大寫，供外部重用

### 檔案 2：`output/plate_validation_result.dart`

- `enum PlateValidationFailReason { tooShort, tooLong, invalidChar, invalidHyphen }`
- `class PlateValidationResult`：
  - 欄位 `bool isValid`、`String normalized`、`PlateValidationFailReason? reason`
  - 具名建構子 `PlateValidationResult.valid(String normalized)` 與 `PlateValidationResult.fail(PlateValidationFailReason reason, String normalized)`
  - `String get message` — 依 reason 回傳繁體中文錯誤訊息（valid 時回傳「車號格式正確」）

### 檔案 3：`output/plate_validator_test.dart`

- 用 Dart 內建 `package:test` 風格撰寫（`test()` / `expect()`）
- 至少涵蓋 **8 個案例**：合法（純數字、含字母、含中間連字號、含小寫需轉大寫各 1）、太短、太長、非法字元、連字號位置錯誤
- 測試需可直接對應檔案 1/2 的 API

---

## 驗收標準（Acceptance Criteria）

- [ ] 3 個檔案皆產生於 `./output/`，互相 import 正確
- [ ] `PlateValidator.validate` 完整實作上述 6 條規則，邊界值（2 碼、7 碼）正確
- [ ] enum / result class 結構與簽章符合規格
- [ ] 繁體中文錯誤訊息齊全且語意正確
- [ ] 測試檔涵蓋 ≥ 8 案例且邏輯能通過自身實作
- [ ] 無 `.w/.h/.sp`、無多餘第三方套件、無修改既有專案檔案
- [ ] 程式碼可通過 `dart analyze`（無 error）

## 輸出要求

完成後以繁體中文輸出實作摘要，列出：產生的檔案清單、各檔行數、是否自評通過全部驗收項。
