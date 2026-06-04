# 如何使用 doc-generator Skill

## 快速開始

### 1. 在 GitHub Copilot CLI 中觸發

當你在專案目錄中，直接對 Copilot 說：

```
"幫我產生所有 API 文件"
"建立 Postman Collection"
"生成流程圖"
```

### 2. Copilot 會自動執行

Skill 會自動：
1. ✅ 檢測專案中的 `API_DOCUMENT.md`
2. ✅ 執行對應的生成腳本
3. ✅ 輸出文件到 `delivery_doc/` 目錄
4. ✅ 驗證結果並報告

## 使用範例

### 範例 1: 生成所有文件

**用戶輸入**:
```
產生所有文件
```

**Copilot 行為**:
1. 檢查專案環境
2. 執行 `./generate_all.sh`
3. 確認生成：
   - ✅ washcar_api.pdf
   - ✅ washcar_api.json
   - ✅ Wash_Car_API_Flow.png
   - ✅ Table_scheme.png
4. 報告：「✅ 所有文件已成功生成在 delivery_doc/ 目錄」

### 範例 2: 只生成 Postman Collection

**用戶輸入**:
```
我只需要 Postman Collection
```

**Copilot 行為**:
1. 啟動虛擬環境
2. 執行 `python api_to_postman.py`
3. 確認 `delivery_doc/washcar_api.json` 存在
4. 提示：「可以在 Postman 中點選 Import 匯入此文件」

### 範例 3: 更新 API 文件後重新生成

**用戶輸入**:
```
我更新了 API 文件，請重新生成 PDF 和 Postman
```

**Copilot 行為**:
1. 執行 `python convert_api_pdf.py`
2. 執行 `python api_to_postman.py`
3. 報告更新完成

## 進階使用

### 自訂輸出參數

**用戶輸入**:
```
我想要更高解析度的流程圖
```

**Copilot 可能的建議**:
```python
# 修改 convert_api_to_uml_flow.py
TARGET_W = 2048  # 從 1024 提高
TARGET_H = 1536  # 從 768 提高
```

### 修改 PDF 樣式

**用戶輸入**:
```
能讓 PDF 的字體更大一點嗎
```

**Copilot 可能的建議**:
```html
<!-- 修改 template.html -->
<style>
    body {
        font-size: 13pt;  /* 從 11pt 提高 */
    }
</style>
```

## 錯誤處理範例

### 範例：環境問題

**錯誤輸出**:
```
❌ Error: python3 not found
```

**Copilot 行為**:
1. 識別問題：缺少 Python 3
2. 提供解決方案：
   ```bash
   # macOS
   brew install python3
   
   # Linux
   sudo apt-get install python3
   ```
3. 建議重新執行

### 範例：Markdown 格式錯誤

**錯誤輸出**:
```
❌ 沒解析到 endpoint
```

**Copilot 行為**:
1. 說明問題：Markdown 格式不符合規範
2. 顯示正確格式：
   ```markdown
   ### API 端點名稱
   * **URL**: `/api/path`
   * **方法**: `POST`
   ```
3. 建議檢查文件格式

## 與其他專案整合

### 複製到新專案

```bash
# 複製 Skill 到新專案
cp -r .github/skills/doc-generator /path/to/new-project/.github/skills/

# 複製必要的來源文件
cp API_DOCUMENT.md /path/to/new-project/
cp ORDER_TRADE_INVOICE_DB_*.md /path/to/new-project/
```

### 安裝為全域 Skill

```bash
# 所有專案都可以使用
cp -r .github/skills/doc-generator ~/.copilot/skills/
```

## 提示詞範例

### 推薦的觸發提示詞

1. ✅ "產生 API 文件"
2. ✅ "建立所有文件"
3. ✅ "生成 Postman Collection"
4. ✅ "產生流程圖"
5. ✅ "建立資料庫架構圖"
6. ✅ "重新生成所有文件"
7. ✅ "只需要 PDF"

### 避免使用的模糊提示

1. ❌ "幫我生成一些東西" （太模糊）
2. ❌ "做文件" （不明確）
3. ❌ "執行那個腳本" （不清楚哪個）

## 常見問題

### Q: 為什麼腳本在 scripts/ 目錄但執行時找不到檔案？

**A**: 腳本設計為從**專案根目錄**執行，讀取根目錄的 `API_DOCUMENT.md`。

### Q: 可以修改複製的腳本嗎？

**A**: 可以，但建議：
1. 先修改專案根目錄的原始腳本
2. 測試無誤後
3. 重新複製到 `.github/skills/doc-generator/scripts/`
4. 更新版本號

### Q: 如何更新 Skill 版本？

**A**: 
1. 修改 `SKILL.md` 的 `version` 欄位
2. 在 `CHANGELOG.md` 記錄變更
3. 提交變更到版本控制

### Q: 可以在 VS Code 中使用嗎？

**A**: 可以！GitHub Copilot 在 VS Code 中也支援 Agent Skills。

## 總結

doc-generator Skill 提供了完整的對話式文件生成體驗。只需簡單地告訴 Copilot 你的需求，它就會自動處理所有技術細節。
