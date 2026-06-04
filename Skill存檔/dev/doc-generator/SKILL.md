---
name: doc-generator
version: 1.0.0
description: |
  自動化 API 文件生成工具，支援多種格式輸出。
  從 Markdown 來源文件產生 PDF、Postman Collection、UML 流程圖、資料庫架構圖。
  
  觸發關鍵字：「產生文件」「建立 API 文件」「生成 Postman」「產生流程圖」「建立資料庫架構圖」
---

# 文件生成工具 Agent Skill

## 概述

這是一個專為 API 文件自動化生成設計的 Agent Skill，能夠從單一 Markdown 來源文件產生多種格式的輸出文件。

### 主要功能

1. **API 文件轉 PDF** - 將 Markdown 格式的 API 文件轉換為格式化的 PDF
2. **Postman Collection 生成** - 自動產生可匯入 Postman 的 API 測試集合
3. **API 流程圖生成** - 使用 PlantUML 產生完整的 API 呼叫時序圖
4. **資料庫架構圖生成** - 從資料庫架構文件產生 ER 圖（Entity-Relationship Diagram）

### 輸出文件位置

所有生成的文件都會存放在 `delivery_doc/` 資料夾中：
- `washcar_api.pdf` - API 文件 PDF 版本
- `washcar_api.json` - Postman Collection JSON 文件
- `Wash_Car_API_Flow.png` - API 調用流程圖（1024x768）
- `Wash_Car_API_Flow.puml` - PlantUML 原始檔
- `Table_scheme.png` - 資料庫架構 ER 圖

## 使用指南

### 觸發方式

當用戶說出以下關鍵字時，應該啟動此 skill：

- "產生 API 文件"
- "建立所有文件" 
- "生成 Postman Collection"
- "產生流程圖"
- "建立資料庫架構圖"
- "生成所有文件"

### 執行步驟

#### 步驟 1: 檢查專案環境

首先確認專案中存在必要的文件：

```bash
# 檢查 API 文件來源
ls -la API_DOCUMENT.md

# 檢查資料庫架構文件
ls -la ORDER_TRADE_INVOICE_DB_*.md

# 檢查生成腳本
ls -la *.py generate_all.sh
```

#### 步驟 2: 確認需求

詢問用戶要生成哪些文件：

**選項 A - 全部生成（推薦）**：
```bash
./generate_all.sh
```

**選項 B - 個別生成**：
- PDF: `python convert_api_pdf.py`
- Postman: `python api_to_postman.py`  
- UML 流程圖: `python convert_api_to_uml_flow.py`
- DB Schema: `python dbml_to_png.py`

#### 步驟 3: 執行生成

使用以下命令執行：

```bash
# 確保在專案根目錄
cd /path/to/washcar

# 執行一鍵生成腳本
./generate_all.sh
```

#### 步驟 4: 驗證輸出

確認所有文件已成功生成：

```bash
ls -la delivery_doc/
```

預期輸出應包含：
- ✅ `washcar_api.pdf`
- ✅ `washcar_api.json`
- ✅ `Wash_Car_API_Flow.png`
- ✅ `Table_scheme.png`

## 技術細節

### 系統需求

- **Python**: 3.7+
- **作業系統**: macOS 或 Linux
- **套件管理**: Homebrew (macOS) 或 apt-get (Linux)

### 關鍵依賴

- **WeasyPrint** - PDF 生成引擎（需要 glib/pango/cairo）
- **PlantUML** - UML 圖表生成（需要 Java）
- **Graphviz** - 圖表渲染引擎
- **Pillow** - 圖片處理
- **Markdown** - Markdown 解析
- **Jinja2** - HTML 模板引擎

### 環境設定

`generate_all.sh` 會自動處理：
1. 檢查 Python 3
2. 建立/啟動虛擬環境 `.venv`
3. 安裝系統相依套件
4. 安裝 Python 套件
5. 設定環境變數（macOS 需要）

## 各功能詳細說明

### 1. Postman Collection 生成

**腳本**: `api_to_postman.py`

**輸入**: `API_DOCUMENT.md`  
**輸出**: `delivery_doc/washcar_api.json`

**功能**:
- 解析 Markdown 中的 API 端點
- 提取 URL、HTTP 方法、請求 Body
- 生成符合 Postman v2.1 格式的 Collection
- 包含環境變數 `{{baseUrl}}`

**Markdown 格式要求**:
```markdown
## API 群組名稱

### API 端點標題

* **URL**: `/api/v1/path`
* **方法**: `POST`

##### 請求 JSON 結構

```json
{
  "field": "value"
}
```
```

**使用生成的文件**:
1. 開啟 Postman
2. 點選 "Import"
3. 選擇 `delivery_doc/washcar_api.json`
4. Collection 會自動分組並填入請求內容

### 2. API PDF 文件生成

**腳本**: `convert_api_pdf.py`

**輸入**: 
- `API_DOCUMENT.md` - API 文件來源
- `template.html` - HTML 模板

**輸出**: `delivery_doc/washcar_api.pdf`

**功能**:
- Markdown 轉 HTML（支援表格、程式碼區塊）
- 使用 Jinja2 模板渲染
- WeasyPrint 轉換為 PDF
- 完整中文字型支援

**自訂樣式**:
編輯 `template.html` 可修改 PDF 外觀：
- 頁面設定（邊距、大小）
- 字型和顏色
- 標題格式
- 程式碼區塊樣式

### 3. UML 流程圖生成

**腳本**: `convert_api_to_uml_flow.py`

**輸入**: `API_DOCUMENT.md`

**輸出**: 
- `delivery_doc/Wash_Car_API_Flow.puml` - PlantUML 原始檔
- `delivery_doc/Wash_Car_API_Flow.png` - 流程圖（1024x768）
- `delivery_doc/Wash_Car_API_Flow_raw.png` - 原始尺寸

**功能**:
- 解析所有 API 端點
- 生成 PlantUML 時序圖語法
- 使用 plantuml 命令渲染
- Pillow 後處理圖片尺寸

**流程圖結構**:
```
Client -> Server: POST /api/endpoint
Server --> Client: Response
```

### 4. 資料庫架構圖生成

#### 選項 A: DBML 版本（基礎）

**腳本**: `dbml_to_png.py`

**輸入**: `ORDER_TRADE_INVOICE_DB_DBML.md`  
**輸出**: `delivery_doc/Table_scheme.png`

**功能**:
- 解析 DBML 格式
- 生成 Graphviz DOT 語法
- 渲染 ER 圖

#### 選項 B: SQL Schema 版本（進階）

**腳本**: `draw_schema.py`

**輸入**: `ORDER_TRADE_INVOICE_DB_SCHEME.md`  
**輸出**: `delivery_doc/washcar_database_schema2.png`

**功能**:
- 解析 SQL CREATE TABLE 語句
- 智能推論表關聯（外鍵、自然鍵、複合鍵）
- 自動佈局優化
- 視覺化主鍵和外鍵

## 錯誤處理

### 常見錯誤與解決方案

#### 1. 找不到 Markdown 文件

**錯誤**: `找不到 API_DOCUMENT.md`

**解決方案**:
```bash
# 確認文件存在
ls -la API_DOCUMENT.md

# 確認當前目錄
pwd
```

#### 2. WeasyPrint 動態函式庫錯誤 (macOS)

**錯誤**: `dyld: Library not loaded: @rpath/libglib-2.0.0.dylib`

**解決方案**:
```bash
# 使用 generate_all.sh（會自動設定環境變數）
./generate_all.sh

# 或手動設定
export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix)/lib:/usr/lib"
```

#### 3. PlantUML 執行失敗

**錯誤**: `plantuml 執行失敗`

**解決方案**:
```bash
# 檢查 PlantUML 是否已安裝
plantuml -version

# macOS 安裝
brew install plantuml

# Linux 安裝
sudo apt-get install -y plantuml default-jre
```

#### 4. 沒有解析到任何 endpoint

**錯誤**: `沒解析到 endpoint`

**原因**: Markdown 格式不符合預期

**檢查清單**:
- URL 格式：`* **URL**: `/api/path``
- 方法格式：`* **方法**: `POST``
- 必須有端點標題：`### 端點名稱`

#### 5. PDF 中文顯示方塊

**原因**: 缺少中文字型

**解決方案**:
```bash
# Linux
sudo apt-get install -y fonts-noto-cjk fonts-wqy-zenhei
fc-cache -fv
```

## 工作流程建議

### 日常使用流程

1. 更新 `API_DOCUMENT.md` 或資料庫架構文件
2. 執行 `./generate_all.sh`
3. 檢查 `delivery_doc/` 中的輸出
4. 將更新的文件交付給團隊

### 僅更新 API 文件

如果只修改了 API 文件：

```bash
source .venv/bin/activate
python api_to_postman.py
python convert_api_pdf.py
python convert_api_to_uml_flow.py
```

### 僅更新資料庫架構

如果只修改了資料庫架構：

```bash
source .venv/bin/activate
python dbml_to_png.py
python draw_schema.py
```

## Agent 行為指引

### 當用戶請求「產生所有文件」時

1. **確認環境**：檢查是否在正確的專案目錄
2. **執行生成**：運行 `./generate_all.sh`
3. **監控進度**：觀察輸出訊息，確認每個步驟成功
4. **驗證結果**：檢查 `delivery_doc/` 目錄中的文件
5. **報告狀態**：告知用戶哪些文件已成功生成

### 當用戶請求「只生成 Postman」時

1. **確認虛擬環境**：`source .venv/bin/activate`
2. **執行腳本**：`python api_to_postman.py`
3. **驗證輸出**：確認 `delivery_doc/washcar_api.json` 存在
4. **提供使用說明**：告知如何匯入 Postman

### 當遇到錯誤時

1. **讀取錯誤訊息**：仔細檢查完整的錯誤輸出
2. **查找解決方案**：參考上方的錯誤處理章節
3. **提供修復建議**：告知用戶具體的解決步驟
4. **重新執行**：修復後再次嘗試生成

### 當用戶詢問自訂需求時

1. **了解需求**：確認用戶想要修改什麼（樣式、尺寸、格式等）
2. **定位文件**：告知需要修改哪個文件（腳本或模板）
3. **提供範例**：給出具體的修改範例
4. **協助測試**：幫助用戶驗證修改後的效果

## 技術架構說明

### 整體處理流程

```
Markdown 文件 (API_DOCUMENT.md)
    │
    ├─→ api_to_postman.py → washcar_api.json
    ├─→ convert_api_pdf.py → washcar_api.pdf
    ├─→ convert_api_to_uml_flow.py → Wash_Car_API_Flow.png
    │
資料庫架構文件 (ORDER_TRADE_INVOICE_DB_*.md)
    │
    └─→ dbml_to_png.py → Table_scheme.png
```

### 設計原則

1. **單一來源原則** - 所有文件從同一個 Markdown 來源生成
2. **關注點分離** - 每個腳本專注於單一任務
3. **自動化優先** - 一鍵生成所有文件
4. **格式無關性** - 從 Markdown 產生多種輸出格式

## 擴展性

### 新增輸出格式

如需支援新的輸出格式（如 OpenAPI、Swagger）：

1. 建立新的 Python 腳本（例如 `convert_api_to_openapi.py`）
2. 重用現有的 Markdown 解析邏輯
3. 實作新格式的生成器
4. 在 `generate_all.sh` 中加入執行步驟

### 自訂腳本參數

所有腳本開頭都有可自訂的參數：

```python
# 範例：api_to_postman.py
INPUT_MD_FILE = "API_DOCUMENT.md"
OUTPUT_POSTMAN_FILE = "delivery_doc/washcar_api.json"
COLLECTION_NAME = "山隆洗車機API"
BASE_URL_DEFAULT = "http://localhost:8080"
```

## 版本資訊

**當前版本**: 1.0.0

### 支援的技術棧

- Python 3.7+
- Markdown
- WeasyPrint
- PlantUML
- Graphviz
- Pillow
- Jinja2

## 注意事項

### 不要修改原始程式碼

此 Skill 設計為**唯讀**模式，只執行現有腳本，不修改原始程式碼。

### 環境隔離

所有操作都在 Python 虛擬環境 `.venv` 中進行，不影響系統全域環境。

### 平台限制

- **完整支援**: macOS, Linux
- **有限支援**: Windows (需透過 WSL)

## 總結

這個 Skill 提供了完整的 API 文件自動化生成解決方案。通過簡單的命令，可以從單一 Markdown 來源產生多種格式的專業文件，大幅提升文件維護效率。
