# 文件 Frontmatter 規範

所有 `docs/` 下產出的文件必須包含以下 YAML frontmatter。

## 必要欄位

```yaml
---
title: 文件標題
type: feature | bug-record | widget | project | api
created: YYYY-MM-DD
status: draft | in-progress | completed
related-modules: [模組名稱]
---
```

## 欄位說明

| 欄位 | 必填 | 說明 |
|------|------|------|
| `title` | ✅ | 文件標題（繁體中文） |
| `type` | ✅ | 文件類型：`feature`（功能模組）、`bug-record`（修復紀錄）、`widget`（元件文件）、`project`（專案架構）、`api`（API 總覽） |
| `created` | ✅ | 建立日期（ISO 8601） |
| `status` | ✅ | 文件狀態 |
| `related-modules` | ✅ | 相關模組（陣列），如 `[car, order]` |
| `jira-id` | ❌ | 對應的 Jira/GitLab issue 編號 |
| `updated` | ❌ | 最後更新日期 |

## 命名規則

- **一律使用 kebab-case**：`company-switch-bug-fix.md`
- ❌ 禁止 snake_case：`company_switch_bug_fix.md`
- ❌ 禁止 camelCase：`companySwitchBugFix.md`
- ❌ 禁止全大寫：`CAR_LIST_DOCUMENTATION.md`

## 存放位置

| 類型 | 目錄 | 範例 |
|------|------|------|
| 功能模組文件 | `docs/page_architecture/` | `car-list-documentation.md` |
| Bug 修復紀錄 | `docs/bug_record/` | `company-switch-bug-fix.md` |
| Widget 元件文件 | `docs/widget/` | `station-dropdown-chip.md` |
| 專案架構文件 | `docs/` | `project-architecture.md` |
| API 總覽文件 | `docs/` | `api-reference.md` |
