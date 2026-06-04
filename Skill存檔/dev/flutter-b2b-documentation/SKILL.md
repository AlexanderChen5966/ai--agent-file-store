---
name: flutter-b2b-documentation
version: "1.0.0"
description: 自動化產出 Flutter Web B2B 專案的技術文件。支援三種文件類型：(1) 專案整體架構文件 - 使用 'project' 模式產出完整的專案技術棧、架構模式、目錄結構說明；(2) 功能模組文件 - 使用 'feature [模組名稱]' 模式自動探索並記錄特定功能的 API、狀態管理、UI 組件、數據模型；(3) API 總覽文件 - 使用 'api' 模式提取所有 REST API endpoints 清單。當用戶要求「產出文件」、「記錄功能」、「建立架構文件」或「整理 API」時使用此 skill。
---

# Flutter B2B Documentation

自動化產出 B2B Manager Flutter Web 專案的技術文件。

## 使用方式

此 skill 提供三種文件產出模式，根據用戶需求選擇：

### 模式 1：專案整體架構文件

**觸發關鍵字：** "project"、"專案架構"、"整體文件"

**產出內容：**
- 專案概述與技術背景
- 完整技術棧清單
- 核心架構模式（Riverpod、GoRouter、OAuth2、TaskManager）
- 目錄結構說明
- 環境配置
- 開發工作流程

**產出位置：** `docs/PROJECT_ARCHITECTURE.md`

**使用範例：**
- "產出專案整體架構文件"
- "建立專案技術文件"
- "記錄 B2B Manager 的架構"

---

### 模式 2：功能模組文件

**觸發關鍵字：** "feature"、"功能"、特定模組名稱（order、driver、car、balance 等）

**產出內容：**
- 功能概述
- 完整 API 端點清單（從 `rest_client.dart` 提取）
- 數據模型（Request/Response DTO）
- 狀態管理（StateNotifier 方法列表）
- UI 組件樹（頁面和子組件）
- 權限控制

**產出位置：** `docs/page_architecture/[模組名稱]_DOCUMENTATION.md`

**使用範例：**
- "產出訂單功能的文件"（自動探索 `lib/page/order/`）
- "記錄 balance 模組"（自動探索 `lib/page/balance/`）
- "整理司機管理功能的 API 和狀態"

**自動化流程：**
1. 定位功能主頁面：`lib/page/[模組]/[模組]_page.dart`
2. 搜索相關 API：`lib/api/restclient/rest_client.dart` 中匹配的端點
3. 分析狀態管理：`lib/api/notifier/[模組]/[模組]_state_notifier.dart`
4. 提取數據模型：`lib/api/request/[模組]/` 和 `lib/api/response/[模組]/`
5. 列舉 UI 組件：`lib/page/[模組]/widgets/`
6. 搜索權限控制：`Authorities.[Resource]` 使用情況

---

### 模式 3：API 總覽文件

**觸發關鍵字：** "api"、"API 清單"、"所有端點"

**產出內容：**
- 所有 REST API endpoints 完整清單
- 依功能模組分組
- HTTP 方法、路徑、說明
- Request/Response 類型
- 代碼位置標註

**產出位置：** `docs/API_REFERENCE.md`

**使用範例：**
- "產出完整的 API 參考文件"
- "列出所有 API 端點"
- "整理 REST API 清單"

**自動化流程：**
1. 讀取 `lib/api/restclient/rest_client.dart`
2. 提取所有 `@GET`、`@POST`、`@PUT`、`@PATCH`、`@DELETE` 標註
3. 解析方法簽名（參數、回傳類型）
4. 依路徑前綴分組（/drivers, /cars, /orders 等）
5. 產出結構化的 Markdown 表格

---

## 文件格式標準

所有產出的文件遵循統一格式：

### 基本要求
- **語言：** 繁體中文（zh-TW）
- **格式：** Markdown
- **代碼標註：** 所有提及的檔案包含完整路徑和行號（例：`file.dart:123-145`）
- **風格：** 技術性且簡潔

### 標準章節結構
功能模組文件應包含：
1. 標題與目錄
2. 功能概述
3. API 端點（完整列表含參數說明）
4. 數據模型（Request/Response DTO）
5. 頁面組件（主頁面、子組件、狀態管理）
6. 權限控制
7. 文件版本資訊

詳細格式規範請參考：[references/doc-template.md](references/doc-template.md)

---

## 專案特定知識

此 skill 針對 B2B Manager 專案設計，理解以下架構模式：

### 核心架構
- **狀態管理：** Riverpod（StateNotifierProvider 模式）
- **網路層：** Retrofit + Dio
- **路由：** GoRouter
- **認證：** OAuth2 with PKCE
- **特殊機制：** TaskManager 單例模式（防重複 API 呼叫）

### 目錄結構
```
lib/
├── api/
│   ├── notifier/[feature]/        # StateNotifier（業務邏輯）
│   ├── restclient/rest_client.dart # Retrofit API 定義
│   ├── request/[feature]/          # API 請求 DTO
│   └── response/[feature]/         # API 回應 DTO
├── page/[feature]/                 # UI 頁面
│   ├── [feature]_page.dart        # 主頁面
│   └── widgets/                    # 子組件
└── models/                         # 資料模型與列舉
```

完整專案上下文請參考：[references/project-context.md](references/project-context.md)

---

## 執行工作流程

### 模式 1：專案架構文件

1. 讀取專案上下文：[references/project-context.md](references/project-context.md)
2. 讀取專案根目錄的 `CLAUDE.md`（包含完整專案規則）
3. 探索以下關鍵檔案：
   - `lib/api/connector/task_manager.dart`（TaskManager 實作）
   - `lib/page/page_route.dart`（路由配置）
   - `lib/api/connector/auth_service.dart`（OAuth2 流程）
4. 結構化產出 `docs/PROJECT_ARCHITECTURE.md`，包含：
   - 專案概述
   - 技術棧（分類說明）
   - 核心架構模式（含代碼範例）
   - 目錄結構（帶說明）
   - 環境配置（dev/staging/release）
   - 開發工作流程（build_runner、測試、部署）

### 模式 2：功能模組文件

**輸入：** 模組名稱（例如：order、driver、car）

**步驟：**

1. **定位主頁面**
   - 搜索：`lib/page/[模組]/[模組]_page.dart`
   - 提取：路由名稱（`ROUTE_NAME`）、組件類型

2. **提取 API 端點**
   - 讀取：`lib/api/restclient/rest_client.dart`
   - 使用 Grep 搜索匹配的 API（例如：`@(GET|POST|PATCH|DELETE)\(.*/[模組]`）
   - 解析：HTTP 方法、路徑、參數、回傳類型
   - 記錄：代碼位置（行號）

3. **分析狀態管理**
   - 讀取：`lib/api/notifier/[模組]/[模組]_state_notifier.dart`
   - 提取：StateNotifier 類別名稱、Provider 名稱
   - 列出：所有公開方法（含參數和回傳類型）
   - 記錄：每個方法的代碼位置

4. **提取數據模型**
   - 搜索：`lib/api/request/[模組]/` 和 `lib/api/response/[模組]/`
   - 對每個檔案：
     - 提取類別定義
     - 列出所有欄位（含類型和說明）
     - 記錄：`@JsonSerializable` 標註
   - 識別：Request 和 Response DTO 的對應關係

5. **列舉 UI 組件**
   - 搜索：`lib/page/[模組]/widgets/` 目錄
   - 對每個組件檔案：
     - 提取組件類別名稱
     - 識別組件類型（StatelessWidget、HookConsumerWidget 等）
     - 簡述功能（從類別名稱推斷）

6. **搜索權限控制**
   - 在主頁面和組件中搜索：`Authorities.[Resource]`
   - 提取：`AuthoritiesAction.Create/Update/Delete` 使用情況
   - 記錄：每個權限檢查的代碼位置

7. **參考格式範本**
   - 載入：[references/doc-template.md](references/doc-template.md)
   - 依據範本結構化產出文件

8. **產出文件**
   - 寫入：`docs/page_architecture/[模組名稱]_DOCUMENTATION.md`
   - 使用繁體中文
   - 包含完整代碼位置標註

### 模式 3：API 總覽文件

1. **提取 API 定義**
   - 讀取：`lib/api/restclient/rest_client.dart`
   - 使用 Grep 搜索：`@(GET|POST|PUT|PATCH|DELETE)`
   - 提取每個端點的：
     - HTTP 方法
     - API 路徑
     - 方法名稱
     - 參數列表（含類型）
     - 回傳類型
     - 代碼位置（行號）

2. **分組整理**
   - 依 API 路徑前綴分組（例如：/drivers、/cars、/orders）
   - 每組內依 HTTP 方法排序（GET、POST、PUT、PATCH、DELETE）

3. **產出文件**
   - 寫入：`docs/API_REFERENCE.md`
   - 格式：Markdown 表格
   - 包含：模組名稱、HTTP 方法、路徑、說明、Request/Response 類型、代碼位置

---

## 重要提醒

### 探索策略
- 使用 **Glob** 工具搜索檔案模式（例如：`lib/page/order/**/*.dart`）
- 使用 **Grep** 工具搜索代碼模式（例如：`@POST.*orders`、`Authorities.Orders`）
- 使用 **Read** 工具讀取特定檔案內容
- **優先順序：** Glob（找檔案）→ Grep（找模式）→ Read（讀內容）

### 代碼位置標註
- 所有提及的檔案**必須**包含完整路徑
- API 定義和方法實作**必須**包含行號
- 格式：`lib/path/to/file.dart:123` 或 `lib/path/to/file.dart:123-145`

### 避免重複工作
- 在探索前，先檢查是否已有現成文件（`docs/page_architecture/`）
- 如果現有文件存在但過時，可以參考其格式進行更新

### 繁體中文一致性
- 所有說明文字使用繁體中文
- 技術術語保持英文（例如：StateNotifier、Provider、OAuth2）
- 範例代碼中的註解使用繁體中文

---

## Resources

### references/project-context.md
專案的核心上下文資訊，包含技術棧、目錄結構、架構模式。在產出任何文件前應先載入此檔案。

### references/doc-template.md
功能模組文件的標準格式範本，定義章節結構、撰寫指引、格式要求。產出功能文件時應遵循此範本。