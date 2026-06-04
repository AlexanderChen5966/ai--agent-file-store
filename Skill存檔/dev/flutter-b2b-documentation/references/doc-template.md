# 功能文件範本格式

此文件定義功能模組文件的標準格式，基於現有的 DRIVER_LIST_DOCUMENTATION.md 和 CAR_LIST_DOCUMENTATION.md。

## 標準結構

功能模組文件應包含以下章節：

### 1. 標題與目錄
```markdown
# [功能名稱]列表功能文件

## 目錄
1. [功能概述](#功能概述)
2. [API端點](#api端點)
3. [數據模型](#數據模型)
4. [頁面組件](#頁面組件)
5. [權限控制](#權限控制)
```

### 2. 功能概述
簡要說明功能的核心能力（3-7點列表）

範例：
```markdown
## 功能概述

[功能名稱]功能提供對[實體]的完整管理，包括：
- 搜索和查看列表
- 新增[實體]
- 編輯[實體]資料
- 刪除[實體]
- 批量操作
- 導出列表

**主頁面路徑：** `lib/page/[feature]/[feature]_page.dart`
```

### 3. API端點
列出所有相關的 REST API endpoints

格式：
```markdown
## API端點

### 1. [操作名稱]
\`\`\`
[HTTP_METHOD] /api/path
\`\`\`
**說明：** [詳細說明]

**請求參數：** `RequestClassName`
- `field1`: 說明（必填/可選）
- `field2`: 說明（必填/可選）

**回應：** `ResponseClassName`

**代碼位置：** `lib/api/restclient/rest_client.dart:行號`

---
```

### 4. 數據模型
定義主要的資料結構

格式：
```markdown
## 數據模型

### ModelName（用途說明）

\`\`\`dart
class ModelName {
  final Type field1;              // 說明
  final Type field2;              // 說明
}
\`\`\`

**定義位置：** `lib/api/[request|response]/path/file.dart`
```

### 5. 頁面組件
列出 UI 頁面和子組件

格式：
```markdown
## 頁面組件

### 主頁面

#### PageName
- **路徑：** `lib/page/[feature]/[feature]_page.dart`
- **組件名稱：** `PageName`
- **類型：** `StatefulHookConsumerWidget`
- **路由：** `/route_name`

**功能：**
- 功能點1
- 功能點2

### 子組件

#### 1. ComponentName
- **路徑：** `lib/page/[feature]/widgets/component.dart`
- **功能：** 說明

### 狀態管理

#### StateNotifier
- **路徑：** `lib/api/notifier/[feature]/[feature]_state_notifier.dart`
- **Provider：** `featureStateNotifier`

**主要方法：**

| 方法名稱 | 說明 | 代碼位置 |
|---------|------|---------|
| `methodName` | 說明 | 行號範圍 |
```

### 6. 權限控制
列出功能所需的權限

格式：
```markdown
## 權限控制

### 需要的權限

#### [操作名稱]
- 權限：`Authorities.[Resource]` 的 `AuthoritiesAction.[Action]`
- 代碼位置：`file.dart:行號`
```

### 7. 頁尾
```markdown
---

**文件版本：** 1.0
**最後更新：** YYYY-MM-DD
**維護者：** Development Team
```

## 撰寫指引

1. **代碼位置標註**：所有提到的檔案都應包含完整路徑和行號
2. **繁體中文**：所有說明文字使用繁體中文
3. **技術性**：說明應簡潔且準確，避免冗長描述
4. **結構化**：使用清晰的標題層級和列表
5. **完整性**：涵蓋 API、狀態管理、UI、權限四大面向
