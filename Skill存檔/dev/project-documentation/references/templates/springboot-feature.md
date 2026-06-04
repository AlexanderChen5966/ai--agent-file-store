# Spring Boot 功能文件範本

此範本適用於 B2B Backend 的功能模組文件。

## 標準結構

### 1. 標題與目錄

```markdown
---
title: [功能名稱]功能文件
type: feature
created: YYYY-MM-DD
status: completed
related-modules: [模組名稱]
---

# [功能名稱]功能文件

## 目錄
1. [功能概述](#功能概述)
2. [API 端點](#api-端點)
3. [數據模型](#數據模型)
4. [業務邏輯](#業務邏輯)
5. [資料存取](#資料存取)
6. [權限控制](#權限控制)
```

### 2. 功能概述

```markdown
## 功能概述

[功能名稱]功能提供以下能力：
- 搜尋和查看列表
- 新增 / 編輯 / 刪除
- 批量操作
- 匯出

**Controller：** `ssgs-b2b-app/.../controllers/[Name]Controller.java`
**Service：** `ssgs-b2b-lib/.../services/[Name]Service.java`
**Repository：** `ssgs-b2b-dao/.../repositories/[Name]Repository.java`
**Entity：** `ssgs-b2b-dao/.../domain/[Name]Entity.java`
```

### 3. API 端點

```markdown
## API 端點

### 1. [操作名稱]
\`\`\`
[HTTP_METHOD] /[resource]/path
\`\`\`

**摘要：** `@Operation(summary = "...")`
**權限：** `@PreAuthorize("hasAuthority('[resource]:[action]')")`

**請求參數：**
| 參數 | 型別 | 來源 | 必填 | 說明 |
|------|------|------|------|------|
| `id` | `Long` | `@PathVariable` | ✅ | 資源 ID |
| `request` | `CreateXxxRequest` | `@RequestBody` | ✅ | 建立請求 |

**回應：** `Response<XxxDTO>`

**Controller 方法：** `XxxController.methodName()` — `XxxController.java:行號`
**Service 方法：** `XxxService.methodName()` — `XxxService.java:行號`

---
```

### 4. 數據模型

```markdown
## 數據模型

### Entity: [Name]Entity

**位置：** `ssgs-b2b-dao/.../domain/[Name]Entity.java`
**資料表：** `@Table("table_name")`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | `Long` | 主鍵（`@Id`） |
| `field1` | `String` | 說明 |
| `createdAt` | `LocalDateTime` | 建立時間（`@CreatedDate`） |

### DTO: [Name]DTO

**位置：** `ssgs-b2b-app/.../dto/responses/[Name]DTO.java`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | `Long` | 資源 ID |

### Request: Create[Name]Request

**位置：** `ssgs-b2b-lib/.../domain/requests/Create[Name]Request.java`

| 欄位 | 型別 | 驗證 | 說明 |
|------|------|------|------|
| `field1` | `String` | `@NotBlank` | 說明 |
```

### 5. 業務邏輯

```markdown
## 業務邏輯

### [Name]Service

**位置：** `ssgs-b2b-lib/.../services/[Name]Service.java`

| 方法 | 說明 | 代碼位置 |
|------|------|---------|
| `search(request)` | 搜尋列表 | 行號範圍 |
| `create(request)` | 新增 | 行號範圍 |
| `update(id, request)` | 更新 | 行號範圍 |
| `delete(id)` | 刪除 | 行號範圍 |

### 匯出服務

**位置：** `ssgs-b2b-lib/.../services/[Name]SearchExportService.java`
**繼承：** `BaseSearchExportService`

### 自訂驗證

| 驗證器 | 位置 | 驗證內容 |
|--------|------|---------|
| `@ValidXxx` | `ssgs-b2b-lib/.../constraints/ValidXxx.java` | 說明 |
```

### 6. 資料存取

```markdown
## 資料存取

### [Name]Repository

**位置：** `ssgs-b2b-dao/.../repositories/[Name]Repository.java`
**繼承：** `CrudRepository<[Name]Entity, Long>`, `CustomRepository`

| 方法 | 查詢類型 | 說明 |
|------|---------|------|
| `findByIdAndGroupIdIn()` | 方法名推導 | 依 ID 和群組查詢 |
| `customQuery()` | `@Query` (SQL) | 自訂查詢 |

### 自訂 SQL 查詢

\`\`\`sql
-- 查詢名稱：[用途說明]
SELECT ... FROM ... WHERE ...
\`\`\`
```

### 7. 權限控制

```markdown
## 權限控制

| API | 權限 | 說明 |
|-----|------|------|
| `POST /[resource]/search` | `[resource]:read` | 搜尋 |
| `POST /[resource]` | `[resource]:create` | 新增 |
| `PATCH /[resource]/{id}` | `[resource]:update` | 更新 |
| `DELETE /[resource]/{id}` | `[resource]:delete` | 刪除 |
```

### 8. 頁尾

```markdown
---

**文件版本：** 1.0
**最後更新：** YYYY-MM-DD
```

## 撰寫指引

1. **三層對照**：每個 API 都要標出 Controller → Service → Repository 的對應關係
2. **SQL 查詢要列出**：`@Query` 中的自訂 SQL 是重要的業務邏輯
3. **驗證規則要列出**：自訂的 `@Valid` 約束對理解業務規則很重要
4. **權限表格化**：一眼看出哪些角色能存取什麼
