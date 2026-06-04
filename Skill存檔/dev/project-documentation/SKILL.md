---
name: project-documentation
description: >-
  自動化產出專案技術文件，支援多種技術棧。
  完整支援 Flutter (Riverpod/Bloc) 和 Spring Boot (Spring Data JDBC)。
  提供五種文件類型：(1) 專案架構文件；(2) 功能模組文件；(3) API 總覽文件；
  (4) Bug 修復紀錄；(5) Widget 元件文件。
  觸發關鍵字："產出文件"、"記錄功能"、"建立架構文件"、"整理 API"、
  "bug 紀錄"、"修復紀錄"、"widget 文件"、"元件文件"。
metadata:
  version: 2.0.0
  last-updated: 2026-04-28
---

# Project Documentation

自動化產出專案技術文件，支援多種技術棧的可擴展文件系統。

## 支援狀態

| 技術棧 | 狀態 | 檢測方式 |
|-------|-----|---------|
| **Flutter (Riverpod/Bloc)** | ✅ 完整支援 | `pubspec.yaml` |
| **Spring Boot (Data JDBC)** | ✅ 完整支援 | `pom.xml` + `@SpringBootApplication` |
| **Android** | 🔧 框架就緒 | `app/build.gradle` |

✅ = 完整支援 | 🔧 = 框架就緒（待擴展）

## 文件規範

所有產出的文件必須遵守統一規範，詳見 [frontmatter-spec.md](references/frontmatter-spec.md)：

- **Frontmatter**：每個文件必須有 `title`、`type`、`created`、`status`、`related-modules`
- **命名規則**：一律使用 **kebab-case**（如 `car-list-documentation.md`）
- **語言**：繁體中文（zh-TW），技術術語保留英文

## 五種文件類型

### 1. 專案架構文件
**產出**: `docs/project-architecture.md`
**內容**: 技術棧、架構模式、目錄結構、環境配置、開發工作流程
**觸發**: "project"、"專案架構"

### 2. 功能模組文件
**產出**: `docs/page_architecture/[模組]-documentation.md`
**內容**: API 端點、數據模型、狀態管理/業務邏輯、UI 組件/Controller、權限控制
**觸發**: "feature"、特定模組名稱

### 3. API 總覽文件
**產出**: `docs/api-reference.md`
**內容**: 所有 REST API endpoints（分組、HTTP方法、Request/Response）
**觸發**: "api"、"API 清單"

### 4. Bug 修復紀錄
**產出**: `docs/bug_record/[問題名稱].md`
**內容**: 問題描述、錯誤現象、根因分析、修復方式、驗證方式
**觸發**: "bug"、"修復紀錄"、"bug record"
**範本**: [templates/bug-record.md](references/templates/bug-record.md)

### 5. Widget 元件文件
**產出**: `docs/widget/[元件名稱].md`
**內容**: 元件概述、使用方式、參數表格、狀態管理、使用位置、注意事項
**觸發**: "widget"、"元件文件"、"component"
**範本**: [templates/widget-doc.md](references/templates/widget-doc.md)

## 工作流程

### Step 1: 檢測專案類型

```bash
# Flutter
ls pubspec.yaml
grep "flutter_riverpod\|flutter_bloc" pubspec.yaml

# Spring Boot
ls pom.xml
grep "@SpringBootApplication" -r src/ ssgs-b2b-app/src/ 2>/dev/null

# Android (TODO)
ls app/build.gradle
```

### Step 2: 載入上下文與範本

- **Flutter**: [stack-context/flutter.md](references/stack-context/flutter.md) + [templates/flutter-feature.md](references/templates/flutter-feature.md)
- **Spring Boot**: [stack-context/springboot.md](references/stack-context/springboot.md) + [templates/springboot-feature.md](references/templates/springboot-feature.md)
- **Android**: [stack-context/android.md](references/stack-context/android.md) 🔧
- **通用**（bug/widget）: [templates/bug-record.md](references/templates/bug-record.md) / [templates/widget-doc.md](references/templates/widget-doc.md)

### Step 3: 載入文件規範

讀取 [frontmatter-spec.md](references/frontmatter-spec.md) 確保產出符合統一規範。

### Step 4: 執行文件產出

依技術棧和文件類型執行對應流程（見下方）。

## Flutter 文件產出（完整支援）

### 專案架構文件

1. 讀取 [stack-context/flutter.md](references/stack-context/flutter.md) 和 `CLAUDE.md`
2. 探索關鍵檔案：
   - `lib/api/connector/task_manager.dart`
   - `lib/page/page_route.dart`
   - `lib/api/connector/auth_service.dart`
3. 產出 `docs/project-architecture.md`

### 功能模組文件

**輸入**: 模組名稱（order、driver、car等）

**步驟**:
1. 定位主頁面：`lib/page/[模組]/[模組]_page.dart`
2. 提取 API：從 `rest_client.dart` Grep `@(GET|POST|PATCH|DELETE)\(.*/[模組]`
3. 分析狀態：讀取 `lib/api/notifier/[模組]/[模組]_state_notifier.dart`
4. 提取模型：搜索 `lib/api/request/[模組]/` 和 `lib/api/response/[模組]/`
5. 列舉組件：探索 `lib/page/[模組]/widgets/`
6. 搜索權限：Grep `Authorities.[Resource]`
7. 使用範本：[templates/flutter-feature.md](references/templates/flutter-feature.md)
8. 產出：`docs/page_architecture/[模組]-documentation.md`

### API 總覽文件

1. 讀取 `lib/api/restclient/rest_client.dart`
2. Grep `@(GET|POST|PUT|PATCH|DELETE)` 提取所有端點
3. 解析方法簽名（參數、回傳類型、行號）
4. 依路徑前綴分組
5. 產出 `docs/api-reference.md`

## Spring Boot 文件產出（完整支援）

### 專案架構文件

1. 讀取 [stack-context/springboot.md](references/stack-context/springboot.md)
2. 分析 `pom.xml` 依賴和模組結構
3. 搜索 `@Configuration`、`@Bean` 配置類別
4. 分析 `SecurityConfig.java` 安全配置
5. 產出 `docs/project-architecture.md`

### 功能模組文件

**輸入**: 模組名稱（car、order、driver、invoice 等）

**步驟**:
1. 定位 Controller：Grep `@RestController` + `@RequestMapping("/[模組]")` in `ssgs-b2b-app/.../controllers/`
2. 提取 API：Grep `@(Get|Post|Patch|Put|Delete)Mapping` 提取所有端點
3. 提取權限：Grep `@PreAuthorize` 取得權限要求
4. 提取 Swagger 標註：`@Operation(summary = "...")` 取得 API 摘要
5. 定位 Entity：讀取 `ssgs-b2b-dao/.../domain/[Name]Entity.java`
6. 定位 Repository：讀取 `ssgs-b2b-dao/.../repositories/[Name]Repository.java`
7. 提取自訂 SQL：Grep `@Query` 取得自訂查詢
8. 定位 Service：搜索 `ssgs-b2b-lib/.../services/` 相關服務
9. 定位 DTO：搜索 `ssgs-b2b-app/.../dto/` 和 `ssgs-b2b-lib/.../domain/requests/`
10. 提取驗證：Grep `@Valid` 相關自訂約束
11. 使用範本：[templates/springboot-feature.md](references/templates/springboot-feature.md)
12. 產出：`docs/page_architecture/[模組]-documentation.md`

### API 總覽文件

1. 搜索所有 Controller：`find ssgs-b2b-app -name "*Controller.java"`
2. Grep `@(Get|Post|Patch|Put|Delete)Mapping` 提取所有端點
3. 提取 `@RequestMapping` 前綴
4. 提取 `@Operation(summary = "...")` 摘要
5. 提取 `@PreAuthorize` 權限
6. 依 Controller（`@Tag`）分組
7. 產出 `docs/api-reference.md`

## Bug 修復紀錄產出（通用）

適用於所有技術棧，不需要檢測專案類型。

**步驟**:
1. 讀取 [templates/bug-record.md](references/templates/bug-record.md)
2. 讀取 [frontmatter-spec.md](references/frontmatter-spec.md)
3. 向使用者收集以下資訊（互動式）：
   - 問題描述和錯誤現象
   - 重現步驟
   - 根因分析
   - 修復方式
4. 使用 `git diff` 或 `git log` 提取相關變更
5. 產出：`docs/bug_record/[問題名稱].md`（kebab-case）

## Widget 元件文件產出（Flutter）

**步驟**:
1. 讀取 [templates/widget-doc.md](references/templates/widget-doc.md)
2. 讀取 [frontmatter-spec.md](references/frontmatter-spec.md)
3. 定位 Widget 原始碼：`find lib -name "[widget_name]*.dart"`
4. 分析建構子參數（required/optional、型別、預設值）
5. 搜索使用位置：Grep `[WidgetName](` 全專案
6. 分析 Provider 依賴：Grep `ref.watch\|ref.read` in widget file
7. 產出：`docs/widget/[元件名稱].md`（kebab-case）

## Android 文件產出（框架就緒）

> **TODO**: 以下為預期流程，待實作。

### 專案架構文件
1. 讀取 [stack-context/android.md](references/stack-context/android.md)
2. 分析 `build.gradle`
3. 識別架構模式（MVVM/MVI）
4. 產出文件

### 功能模組文件
1. 定位 Activity/Fragment
2. 分析 ViewModel
3. 提取 Repository 和 Data Source
4. 使用範本：[templates/android-feature.md](references/templates/android-feature.md)

## 文件格式標準

- **語言**: 繁體中文（zh-TW）
- **格式**: Markdown + YAML frontmatter
- **命名**: kebab-case
- **代碼標註**: 完整路徑 + 行號
- **風格**: 技術性且簡潔

詳見 [frontmatter-spec.md](references/frontmatter-spec.md)。

## 探索策略

- **Glob**: 搜索檔案模式（`lib/page/order/**/*.dart`、`*Controller.java`）
- **Grep**: 搜索代碼模式（`@POST.*orders`、`@PreAuthorize`）
- **Read**: 讀取特定檔案內容

**優先順序**: Glob → Grep → Read

## 擴展到新技術棧

1. 創建 `references/stack-context/[stack].md`（專案概述、技術棧、目錄結構）
2. 創建 `references/templates/[stack]-feature.md`（章節結構）
3. 更新 SKILL.md Step 1 添加檢測邏輯
4. 實作工作流程
5. 測試驗證

## 使用範例

**Flutter - 產出訂單功能文件**:
```
用戶: "產出訂單功能的文件"

1. 檢測 Flutter (pubspec.yaml)
2. 載入 flutter.md 上下文
3. 探索 lib/page/order/
4. 提取 API、StateNotifier、DTO、UI
5. 使用 flutter-feature.md 範本
6. 產出 docs/page_architecture/order-documentation.md
```

**Spring Boot - 產出車輛功能文件**:
```
用戶: "產出車輛 API 的文件"

1. 檢測 Spring Boot (pom.xml)
2. 載入 springboot.md 上下文
3. 讀取 CarController.java
4. 提取 API、@PreAuthorize、@Operation
5. 讀取 CarEntity.java、CarRepository.java
6. 搜索相關 Service 和 DTO
7. 使用 springboot-feature.md 範本
8. 產出 docs/page_architecture/car-documentation.md
```

**Bug 修復紀錄**:
```
用戶: "記錄這次的 bug 修復"

1. 載入 bug-record.md 範本
2. 互動式收集問題資訊
3. 從 git diff 提取變更
4. 產出 docs/bug_record/[問題名稱].md
```

**Widget 元件文件**:
```
用戶: "產出 StationDropdown 的元件文件"

1. 載入 widget-doc.md 範本
2. 定位 Widget 原始碼
3. 分析參數、Provider、使用位置
4. 產出 docs/widget/station-dropdown.md
```

## Resources

### Stack Context Files
專案上下文資訊（技術棧、目錄結構、架構模式）

- [flutter.md](references/stack-context/flutter.md) ✅
- [springboot.md](references/stack-context/springboot.md) ✅
- [android.md](references/stack-context/android.md) 🔧

### Template Files
文件的標準格式範本

- [flutter-feature.md](references/templates/flutter-feature.md) ✅ 功能模組（Flutter）
- [springboot-feature.md](references/templates/springboot-feature.md) ✅ 功能模組（Spring Boot）
- [android-feature.md](references/templates/android-feature.md) 🔧 功能模組（Android）
- [bug-record.md](references/templates/bug-record.md) ✅ Bug 修復紀錄（通用）
- [widget-doc.md](references/templates/widget-doc.md) ✅ Widget 元件（Flutter）

### Specification Files
文件規範

- [frontmatter-spec.md](references/frontmatter-spec.md) ✅ Frontmatter 與命名規範
