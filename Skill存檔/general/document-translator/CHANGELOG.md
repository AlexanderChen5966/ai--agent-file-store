# Changelog

All notable changes to this project will be documented in this file.

## [3.2.2] - 2026-02-06

### 🐛 Bug Fixes

- **macOS 瀏覽器連接問題**
  - 修復 nodriver 無法在 macOS 上啟動瀏覽器的問題
  - 加入 `sandbox=False` 參數
  - 加入 `--no-sandbox` 和 `--disable-setuid-sandbox` 瀏覽器參數
  - 問題：`Failed to connect to browser` 錯誤
  - 影響範圍：macOS 使用者

- **Asyncio 事件循環錯誤**
  - 修復 `chatgpt_translator.py` 的 `__del__` 方法錯誤
  - 修復 `chatgpt_proofreader.py` 的 `__del__` 方法錯誤
  - 問題：`AttributeError: 'NoneType' object has no attribute 'disconnect'`
  - 解決方案：在清理資源前檢查事件循環是否存在
  - 影響範圍：所有使用者

- **Chrome Profile 損壞問題**
  - 將 Chrome Profile 資料夾名稱從 `chrome-profile` 更新為 `chrome-profile-v3`
  - 避免舊資料導致瀏覽器連接失敗
  - 問題：舊的 profile 資料可能損壞導致無法連接
  - 影響範圍：升級使用者

### 📝 Documentation

- 在 README.md 新增 CAPTCHA 處理說明
- 在 SKILL.md 更新版本資訊和修復說明
- 更新所有文件中的版本號到 3.2.2
- 新增詳細的錯誤訊息和除錯資訊

### ✅ Testing

- 測試 Google + ChatGPT 校稿模式 ✅
- 測試 nodriver 瀏覽器啟動 ✅
- 測試實際翻譯功能 ✅
- 確認所有修復都已生效 ✅

### 📦 Package

- 更新打包檔案
  - `document-translator-skill-v3.2.2.tar.gz` (52KB)
  - `document-translator-skill-v3.2.2.zip` (67KB)
- 更新 INSTALL.md 安裝指南
- 更新 VERSION.txt 版本資訊

## [3.2.1] - 2026-02-06

### Added

- 新增「支援的檔案格式」章節到 SKILL.md
- 新增 FAQ「如何翻譯 Word/PDF 檔案？」到 SKILL.md
- 新增「範例 9: 翻譯純文字檔案」到 examples.md
- 新增「問題 9: 無法翻譯 Word/PDF 檔案」到 troubleshooting.md

### Changed

- 更新 description 加入檔案格式資訊
- 更新所有文件版本號到 3.2.1

### Documentation

- 建立 README.md 快速開始指南
- 建立 INSTALL.md 安裝指南
- 建立 VERSION.txt 版本資訊
- 建立 .gitignore 檔案
- 建立 install.sh 自動安裝腳本

## [3.2.0] - 2025-01-20

### Added

- 新增 `--doc-type` 參數（api/srs/design/user-guide/tutorial/readme/changelog/general）
- 校稿提示詞自動加入文件類型背景資訊
- 強化程式碼區塊保護規則（最高優先級）
- ChatGPT 校稿器使用內容穩定偵測機制

## [3.1.0] - 2025-01-20

### Added

- 新增 ChatGPT 校稿器（使用 chatgpt.com 對話頁面）
- 新增 `google+proofread` 翻譯模式
- 校稿器與翻譯器共用 Chrome Profile

## [3.0.0] - 2025-01-20

### Changed

- 從 Playwright 遷移到 nodriver
- CAPTCHA 觸發率降至 <5%
- 自動下載 Chrome，安裝更簡單
- 瀏覽器資料持久化

## [2.0.0] - 2025-01-18

### Changed

- 從 Selenium 遷移到 Playwright + Stealth
- CAPTCHA 觸發率降至 ~10%

## [1.0.0] - 2025-01-16

### Added

- 初始版本
- 智慧降級翻譯策略
- ChatGPT Translate 優先（Selenium）

---

**Format**: Based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
**Versioning**: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
