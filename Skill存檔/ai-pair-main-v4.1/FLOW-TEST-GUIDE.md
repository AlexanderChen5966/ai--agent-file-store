# v4.1 完整流程測試指南（基於批次車輛編輯需求）

## 📋 準備清單

### ✅ 已完成
- [x] 本機整合測試通過（版本、檔案結構、超連結）
- [x] ai-pair-v4-test 已複製到 ~/.claude/skills/
- [x] Task Context 已準備：/tmp/batch-edit-car-undo-task.md
- [x] 流程測試檢查點已生成

### ⚙️ 前置檢查
```bash
# 驗證 CLI 可用性
copilot --version      # 應顯示 version
gemini --version       # 應顯示 version
claude --version       # Claude Code CLI
```

---

## 🚀 執行步驟

### Step 1：啟動 /ai-pair dev-team
在 Claude Code 中輸入：
```
/ai-pair dev-team b2b-manager
```

預期輸出：
```
Team ready.

Team: b2b-manager-dev
Members:
  - copilot-developer: ready (claude-sonnet-4.6)
  - copilot-reviewer: ready (gpt-4.1)
  - claude-reviewer: ready (Claude)
  - gemini-reviewer: ready (gemini-2.5-flash)

Review level: Level 2 (default) — use --quick or --deep to change

Awaiting your first task.
```

### Step 2：分派任務
複製以下內容，貼到 Claude Code 給 Team Lead：

```markdown
# Task: 實作批次車輛編輯 10 分鐘復原機制

## Project Context
- Project path: /Users/alexander/GitLab/b2b-manager
- Tech stack: Flutter Web + Riverpod + Retrofit
- Relevant files:
  - lib/page/car/batch_edit/ (批次編輯模組)
  - lib/page/car/car_page.dart (車輛列表頁)
  - lib/api/connector/api_connector.dart (API 連接器)

## Requirement
實作完全在前端完成的 10 分鐘復原機制...

[複製 /tmp/batch-edit-car-undo-task.md 的完整內容]
```

### Step 3：監控流程執行（約 5-11 分鐘）

#### 階段 A：copilot-developer 執行（2-5 分鐘）
觀察項目：
- [ ] 是否顯示「正在實作...」或類似進度訊息
- [ ] 是否讀取相關檔案（batch_edit_car_page.dart, car_page.dart 等）
- [ ] 最後是否輸出 `DONE:{files}` 訊息

**檢查超連結：**
- [ ] 若提及「詳見 reference/cli-invocation-ref.md」，記錄此次成功超連結使用

#### 階段 B：3 位 Reviewer 並行審查（3-6 分鐘）
分別觀察每位 reviewer 的輸出：

**copilot-reviewer（GPT-4.1，FREE tier）：**
- [ ] 輸出壓縮格式：`C|file.dart:line|issue|fix`
- [ ] 最後顯示 `VERDICT:PASS` 或 `VERDICT:WARN` 或 `VERDICT:BLOCK`

**claude-reviewer（Claude subagent）：**
- [ ] 無 CLI 依賴，應 100% 成功
- [ ] 同樣使用壓縮格式輸出

**gemini-reviewer（Gemini 2.5-flash，STANDARD tier）：**
- [ ] 若 quota 耗盡，檢查 fallback 是否啟動
- [ ] 若成功，同樣輸出壓縮格式

#### 階段 C：Team Lead 彙整結果（<1 分鐘）
- [ ] 是否正常彙整 3 位 reviewer 的結果
- [ ] 是否呈現人類可讀的評論
- [ ] 是否提示最終判定（PASS/WARN/BLOCK）

---

## ✅ 檢查點清單（在流程執行中檢驗）

### Tier 系統
- [ ] copilot-developer 使用 STANDARD tier（claude-sonnet-4.6）✓
- [ ] copilot-reviewer fallback 到 FREE tier（gpt-4.1）✓
- [ ] gemini-reviewer 使用 STANDARD tier✓

### v4.1 新增特性
- [ ] 檔案超連結正確指向 reference/ 資料夾
- [ ] 壓縮格式使用 `|` 分隔符（非 `/`）
- [ ] 偏誤防護：Team Lead 是否提示 reviewer 權重

### 模型驗證
- [ ] 所有 3 位 reviewer 都成功執行
- [ ] 無 ERR:MODEL 或 ERR:CLI_MISSING 出現
- [ ] 若有錯誤，檢查 fallback chain 是否啟動

### 文檔完整性
- [ ] copilot-developer 輸出是否涵蓋 4 個 Step
- [ ] 每個 Step 內容是否完整
- [ ] 是否有遺漏的實作細節

---

## 📊 預期結果

### ✅ 成功標誌
```
Team Lead 最終輸出：
"所有 reviewer 確認無阻擋問題，可合併。"

或

"copilot-reviewer 發現 1 個警告：XXX，建議修正後再提交。"
```

### ⚠️ 潛在問題 & 解決方案

| 問題 | 原因 | 解決方案 |
|------|------|--------|
| copilot-developer 超時 | 任務過複雜或 API 延遲 | 增加 timeout 或簡化任務 |
| Gemini QUOTA 耗盡 | Gemini 免費額度用完 | 檢查 fallback chain 是否啟動 |
| 超連結死連 | reference/ 路徑相對位置錯誤 | 檢查 SKILL.md 中的超連結路徑 |
| 壓縮格式不一致 | Reviewer 沒有遵守協議 | 檢查 Agent Prompt 是否清晰 |

---

## 🎯 測試完成後

### 若成功 ✅
1. 移除測試版本：`rm -rf ~/.claude/skills/ai-pair-v4-test`
2. 部署正式版本：`cp -r /Users/alexander/GitLab/b2b-manager/ai-pair-main-v4.1 ~/.claude/skills/ai-pair`
3. 重啟 Claude Code
4. 驗證 `/ai-pair` 可正常觸發（應識別為 v4.1.0）

### 若失敗 ❌
1. 記錄錯誤訊息和 stack trace
2. 檢查 SKILL.md 中相關章節（如超連結、模型配置）
3. 修改 ai-pair-main-v4.1 並重新測試

---

## 💾 重要路徑

- 本機測試版本：`~/.claude/skills/ai-pair-v4-test/`
- 原始檔案：`/Users/alexander/GitLab/b2b-manager/ai-pair-main-v4.1/`
- 備份原版本：`~/.claude/skills/ai-pair-v3.1-backup/`（如果有的話）
- Task Context：`/tmp/batch-edit-car-undo-task.md`

---

**預計總耗時：15-20 分鐘**

開始前請確保所有 CLI 工具已就緒，祝你測試順利！ 🚀
