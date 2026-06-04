# v4.1 完整流程測試清單

## 前置準備
- [ ] Claude Code 已重啟（若複製了新 skill）
- [ ] Copilot CLI 已驗證：`copilot --version`
- [ ] Gemini CLI 已驗證：`gemini --version`

## Skill 發現與基本觸發
- [ ] 在 Claude Code 中輸入 `/ai-pair`，驗證命令提示是否出現
- [ ] 在 Claude Code 中輸入 `ai pair dev-team`，驗證是否認可該觸發詞
- [ ] 查看 Skill 的 description 是否完整

## 模型驗證（快速）
### Copilot 模型
- [ ] `copilot --model gpt-5-mini -p "hello"` ✅ 應成功
- [ ] `copilot --model gpt-4.1 -p "hello"` ✅ 應成功
- [ ] `copilot --model claude-sonnet-4.6 -p "hello"` ✅ 應成功

### Gemini 模型  
- [ ] `gemini --model gemini-2.5-flash -p "hello"` ✅ 應成功
- [ ] `gemini --model gemini-3-flash-preview -p "hello"` ✅ 應成功（若可用）

## Tier 系統驗證
- [ ] SKILL.md 中有 Tier System 章節
- [ ] 4 個 Tier 定義清楚（FREE / LOW / STANDARD / COMPLEX）
- [ ] 說明文件.md 中的模型 Tier 對應正確

## 高信心偏誤防護機制
- [ ] SKILL.md 中有「Bias Mitigation」章節
- [ ] 說明了「自動升級規則」和「override 檢查」

## 已知限制文檔
- [ ] SKILL.md 有「Known Limitations & Resolutions」章節
- [ ] 列舉了 4 項限制及解決方案

## Phase 1 驗證簽核
- [ ] SKILL.md 末尾有「Phase 1 Validation Closure」章節
- [ ] 版本號標記為 4.1.0
- [ ] 變更清單完整

## 參考文檔結構
- [ ] `reference/agents-prompts.md` 包含 8 個 Agent 提示
- [ ] `reference/cli-invocation-ref.md` 包含 3 個 CLI 協議
- [ ] SKILL.md 中所有超連結指向 `reference/` 正確

## 測試流程（選項：手動運行）
如果想測試實際流程，可選擇：

### 最小流程（15 分鐘）
1. 建立簡單的任務：
   ```bash
   cat > /tmp/task-test.md << 'TASK'
   # Task: Add hello world endpoint
   
   ## Project Context
   - Project path: /tmp/test-project
   - Tech stack: Flask
   
   ## Requirement
   Add a GET /hello endpoint that returns {"message": "hello world"}
   
   ## Files to Modify
   - app.py
   TASK
   ```

2. 在 Claude Code 中執行：
   ```
   /ai-pair dev-team test-project
   ```

3. 依照提示，複製 /tmp/task-test.md 給 Team Lead

4. 觀察 copilot-developer 是否正常執行

### 驗收標準
- [ ] copilot-developer 能正常啟動
- [ ] Team Lead 能識別並顯示結果
- [ ] 無 ERR:MODEL 或 ERR:CLI_MISSING 出現

