# Document Translator Skill v3.2.2 - Release Notes

> 🐛 **Bug Fix Release** | 2026-02-06

## 🎯 主要修復

這個版本主要修復了 **macOS 使用者無法使用瀏覽器翻譯** 的問題，並改進了程式穩定性。

## ✅ 修復清單

### 1. macOS 瀏覽器連接問題 ✅

**問題描述**：
```
Failed to connect to browser
One of the causes could be when you are running as root.
In that case you need to pass no_sandbox=True
```

**解決方案**：
- 在 `chatgpt_translator.py` 加入 `sandbox=False` 參數
- 在 `chatgpt_proofreader.py` 加入 `sandbox=False` 參數
- 加入 macOS 專用的瀏覽器啟動參數

**影響範圍**：macOS 使用者

---

### 2. Asyncio 事件循環錯誤 ✅

**問題描述**：
```python
Exception in atexit callback <function deconstruct_browser>:
AttributeError: 'NoneType' object has no attribute 'disconnect'
```

**解決方案**：
- 修復 `__del__` 方法，安全地處理事件循環關閉的情況
- 在 `translate()` 和 `proofread()` 方法的 finally 區塊正確關閉瀏覽器
- 加入事件循環存在性檢查

**影響範圍**：所有使用者

---

### 3. Chrome Profile 資料損壞 ✅

**問題描述**：
- 舊的 Chrome profile 資料可能導致連接失敗

**解決方案**：
- 更新資料夾名稱：`chrome-profile` → `chrome-profile-v3`
- 使用全新的 profile 資料夾，避免舊資料衝突

**影響範圍**：升級使用者

---

## 🆕 新增功能

### CAPTCHA 處理說明

在 README.md 和 SKILL.md 中新增完整的 CAPTCHA 處理指南：

**方式 1：手動驗證一次**
```bash
python scripts/translate.py --mode chatgpt --no-headless docs/en/FILE.md
```
驗證完成後，狀態會保存，後續不再需要驗證。

**方式 2：使用 Google + ChatGPT 校稿（推薦）**
```bash
python scripts/translate.py --mode google+proofread --proofreader chatgpt docs/en/FILE.md
```
完全不會遇到 CAPTCHA，品質也很好（⭐⭐⭐⭐）。

---

## 📝 文件更新

- ✅ 更新 README.md 加入 CAPTCHA 處理說明
- ✅ 更新 SKILL.md 版本資訊
- ✅ 更新 INSTALL.md 安裝指南
- ✅ 更新 VERSION.txt 版本號
- ✅ 新增 CHANGELOG.md 變更日誌
- ✅ 新增本發布說明

---

## ✅ 測試確認

所有修復都已經過測試確認：

| 測試項目 | 狀態 | 說明 |
|---------|------|------|
| nodriver 啟動 | ✅ | 瀏覽器可正常啟動 |
| macOS sandbox | ✅ | 不再出現連接錯誤 |
| 事件循環清理 | ✅ | 不再出現 asyncio 錯誤 |
| Google + 校稿 | ✅ | 翻譯功能正常 |
| 實際翻譯測試 | ✅ | 成功翻譯文件 |

---

## 📦 打包檔案

- **Linux/macOS**: `document-translator-skill-v3.2.2.tar.gz` (52KB)
- **Windows**: `document-translator-skill-v3.2.2.zip` (67KB)

---

## 🚀 升級指南

### 從 v3.2.1 升級

1. **備份自訂配置**（如有修改）：
   ```bash
   cp scripts/config/glossary.json ~/glossary.json.bak
   ```

2. **解壓縮新版本**：
   ```bash
   tar -xzf document-translator-skill-v3.2.2.tar.gz
   ```

3. **安裝依賴**（建議重新安裝）：
   ```bash
   cd document-translator/scripts
   pip install -r requirements.txt
   ```

4. **恢復自訂配置**（如需要）：
   ```bash
   cp ~/glossary.json.bak scripts/config/glossary.json
   ```

5. **測試**：
   ```bash
   python translate.py --help
   ```

### 舊的 Chrome Profile 會自動失效

- 舊資料夾：`~/.chatgpt-translator/chrome-profile/`（不再使用）
- 新資料夾：`~/.chatgpt-translator/chrome-profile-v3/`
- 如需清除舊資料：`rm -rf ~/.chatgpt-translator/chrome-profile/`

---

## ⚠️ 已知問題

### CAPTCHA 驗證

首次使用 ChatGPT Translate 時可能遇到 CAPTCHA（正常現象）。

**解決方案**：
- 使用 `--no-headless` 手動驗證一次，或
- 改用 `google+proofread` 模式（不會遇到 CAPTCHA）

---

## 🙏 致謝

感謝回報問題的使用者，讓我們能夠及時發現並修復這些 bug。

---

## 📞 問題回報

如遇到問題：
1. 查看 [troubleshooting.md](document-translator/references/troubleshooting.md)
2. 查看 [CHANGELOG.md](CHANGELOG.md)
3. 使用 `--verbose` 參數查看詳細日誌

---

**Version**: 3.2.2
**Release Date**: 2026-02-06
**Status**: Stable ✅
