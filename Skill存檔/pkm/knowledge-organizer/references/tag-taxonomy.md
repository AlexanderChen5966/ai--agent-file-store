# 標籤分類表（Tag Taxonomy）

標籤使用階層式結構，以 `/` 分隔。每篇筆記指定 1-3 個 tag。

---

## AI 相關

| Tag | 說明 | 範例 |
|-----|------|------|
| `ai/claude` | Claude 模型、功能、用法 | Claude Skill、Prompt 技巧 |
| `ai/agent` | AI Agent 設計與協作 | 多 Agent 編排、Soft Orchestration |
| `ai/mcp` | Model Context Protocol | MCP Server 設定、工具整合 |
| `ai/prompt-engineering` | Prompt 設計技巧 | Context Engineering、TBRC Prompt |
| `ai/workflow` | AI 輔助工作流程 | 自動化、AI 整合場景 |

## 個人知識管理（PKM）

| Tag              | 說明             | 範例                     |
| ---------------- | -------------- | ---------------------- |
| `pkm/obsidian`   | Obsidian 工具與設定 | 插件、Vault 設定            |
| `pkm/workflow`   | 知識管理工作流程       | Karpathy 方法、PARA       |
| `pkm/automation` | 自動化知識整理        | Claude Code + Obsidian |
| `pkm/framework`  | 知識管理框架         | MAPS、TBRC、SCQA、5A+     |

## 軟體開發

| Tag | 說明 | 範例 |
|-----|------|------|
| `dev/flutter` | Flutter 開發 | Widget、狀態管理 |
| `dev/dart` | Dart 語言 | 語法、模式 |
| `dev/spring-boot` | Spring Boot 後端 | API 設計、JPA |
| `dev/architecture` | 軟體架構 | 設計模式、SOLID |
| `dev/testing` | 測試 | Playwright、單元測試 |
| `dev/ci-cd` | CI/CD 流程 | GitLab CI、Docker |

## 專案

| Tag | 說明 | 範例 |
|-----|------|------|
| `project/b2b-manager` | 山隆 B2B 平台相關 | 功能需求、Bug 記錄 |
| `project/knowledge-base` | 本知識庫系統建設 | 架構規劃、工具設定 |

## 方法論

| Tag              | 說明        | 範例                  |
| ---------------- | --------- | ------------------- |
| `method/maps`    | MAPS 框架   | 資產化、Mindset         |
| `method/tbrc`    | TBRC 四層結構 | 知識整理框架              |
| `method/scqa`    | SCQA 溝通框架 | 問題陳述、回顧             |
| `method/5a-plus` | 5A+ 迭代循環  | AIM→ACQUIRE→ATTEMPT |

---

## 內容類型（type/）

用於路線三查詢時的交叉過濾。**等 wiki 超過 50 篇再開始加**，條目少時不需要。

| Tag | 說明 | 範例 |
|-----|------|------|
| `type/how-to` | 有具體步驟的操作型條目 | 安裝指南、設定流程 |
| `type/concept` | 概念定義與解釋型條目 | 什麼是 RAG、MCP 是什麼 |
| `type/comparison` | 工具或方法的比較 | Skills vs MCP、Notion vs NotebookLM |

> **為什麼要加 type/？** 主題 tag（`ai/agent`）回答「這篇關於什麼」，但當同主題條目變多（> 10 篇），用 `ai/agent` + `type/how-to` 交叉過濾，可以從 20 篇縮到 3 篇，大幅提升查詢效率。

---

## 選 Tag 的判斷規則

1. **最多 3 個 tag**，優先選最具體的那個
2. 同時有 `dev/flutter` 和 `project/b2b-manager` → 選 `project/b2b-manager`（更具體）
3. 工具類文章 → 選工具對應的 tag（`pkm/obsidian`、`ai/mcp`）
4. 方法論文章 → 選 `method/xxx`
5. 不確定時 → 選父層（`ai/`、`dev/`）
6. **wiki > 50 篇後**：加上 `type/xxx` 作為第三個 tag，方便路線三交叉過濾
