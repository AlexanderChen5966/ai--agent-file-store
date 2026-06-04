# Directive: 建立多 AI 憲章檔案系統

> 此指令用於在新專案或尚未建立憲章的專案中，自動生成 AGENTS.md、CLAUDE.md、GEMINI.md 三份憲章檔案。
> 觸發時機：專案根目錄缺少上述任一檔案，或使用者明確要求初始化 AI 分工系統。

---

## 角色定位

你是**編排者（第二層）**。你的工作是：
1. 收集專案資訊
2. 判斷哪些憲章檔案尚未存在
3. 依序呼叫 `execution/generate-charter.py` 生成對應檔案
4. 驗證產出結果

你不直接撰寫憲章內容，而是透過腳本生成，確保格式一致。

---

## 輸入

執行前需收集以下資訊（若使用者未提供，主動詢問）：

| 欄位 | 說明 | 範例 |
|------|------|------|
| `project_name` | 專案名稱 | `my-app` |
| `platforms` | 涉及平台（可複選） | `web, api, ios, android` |
| `tech_stack` | 各平台技術棧 | `web: Next.js, api: Node.js, ios: SwiftUI` |
| `build_commands` | 各平台 build/test/lint 指令 | `web: npm run build / npm test / npm run lint` |
| `repo_structure` | 專案目錄結構（可貼上 tree 輸出） | `/web /api /mobile/ios /mobile/android /shared` |
| `existing_files` | 已存在的憲章檔案 | `AGENTS.md 已存在，其他不存在` |

**快速收集方式：** 若使用者在專案根目錄，直接執行以下指令自動偵測：
```bash
# 偵測專案結構
find . -maxdepth 2 -type f -name "package.json" -o -name "*.xcodeproj" -o -name "build.gradle" | head -20
ls -la | grep -E "AGENTS|CLAUDE|GEMINI"
```

---

## 執行流程

### Step 1 — 偵測現有憲章

```bash
python execution/detect-charters.py --project-root .
```

輸出：哪些檔案存在、哪些需要建立。**已存在的檔案不覆蓋，除非使用者明確要求。**

### Step 2 — 生成缺少的憲章

依偵測結果，對每個缺少的檔案執行：

```bash
# 生成 AGENTS.md（核心共識，最先建立）
python execution/generate-charter.py \
  --type agents \
  --project-name "{project_name}" \
  --platforms "{platforms}" \
  --tech-stack "{tech_stack}" \
  --build-commands "{build_commands}" \
  --repo-structure "{repo_structure}" \
  --output ./AGENTS.md

# 生成 CLAUDE.md（規劃者 + 審查者行為）
python execution/generate-charter.py \
  --type claude \
  --project-name "{project_name}" \
  --platforms "{platforms}" \
  --output ./CLAUDE.md

# 生成 GEMINI.md（執行者行為）
python execution/generate-charter.py \
  --type gemini \
  --project-name "{project_name}" \
  --platforms "{platforms}" \
  --output ./GEMINI.md
```

**生成順序：AGENTS.md → CLAUDE.md → GEMINI.md**（後兩者會引用前者）

### Step 3 — 設定 Codex CLI fallback（若使用者有安裝 Codex）

```bash
python execution/setup-codex-config.py \
  --add-fallback CLAUDE.md \
  --add-fallback GEMINI.md
```

這會在 `~/.codex/config.toml` 加入 fallback，讓 Codex 也能讀取 CLAUDE.md 和 GEMINI.md。

### Step 4 — 驗證

```bash
python execution/validate-charters.py --project-root .
```

檢查項目：
- [ ] 三份檔案均存在
- [ ] CLAUDE.md 和 GEMINI.md 包含 `@AGENTS.md` 引用
- [ ] 各檔案包含必要的 section（見下方模板規格）

---

## 憲章模板規格

> 以下為各檔案的**必要 section 清單**，`generate-charter.py` 依此生成。

### AGENTS.md 必要 sections
```
# 專案結構        ← 目錄樹 + 各平台說明
# Build & Test   ← 各平台指令表
# Coding 規範     ← commit 格式、禁止行為
# 分工協議        ← 三者角色定義（規劃/執行/審查）
# Task 交接格式   ← task.md 的標準欄位定義
# 跨平台規範      ← 若 platforms > 1，加入 API contract 同步規則
```

### CLAUDE.md 必要 sections
```
# （頂部）@AGENTS.md 引用
# 角色定義        ← Planning Mode / Review Mode 說明
# Planning Mode  ← 收到需求時的固定步驟
# task.md 格式   ← 完整欄位模板
# Review Mode    ← 審查流程 + review-result.md 格式
# 禁止行為        ← 規劃不寫碼、審查不改碼
```

### GEMINI.md 必要 sections
```
# （頂部）@AGENTS.md 引用
# 角色定義        ← 執行者，不規劃
# 收到任務的流程  ← 讀 task.md → 確認 AC → 實作
# 自我檢查清單   ← AC 對照 + lint/test + scope 確認
# 禁止行為        ← 不修改 task.md、不引入新套件、不跨平台
```

---

## 邊界情況

| 情況 | 處理方式 |
|------|---------|
| 憲章已存在 | 跳過，不覆蓋。告知使用者哪些已存在 |
| 使用者要更新現有憲章 | 需明確說「更新 AGENTS.md」才執行，且先備份原檔 |
| 偵測不到技術棧 | 產出通用模板，並在檔案頂部加 `TODO: 填入實際技術棧` 標記 |
| 只有單一平台（非 cross） | AGENTS.md 省略跨平台規範 section |
| Codex config 不存在 | 建立 `~/.codex/config.toml`，加入最小設定 |

---

## 自退火循環

若 `validate-charters.py` 回報問題：
1. 讀取錯誤訊息，判斷是哪份檔案的哪個 section 缺失
2. 重新執行對應的 `generate-charter.py` 指令（加上 `--section {section_name}` 補充）
3. 再次執行驗證
4. 若連續失敗兩次，停下來回報使用者具體問題

---

## 預期輸出

成功完成後，專案根目錄應有：

```
./
├── AGENTS.md          ← 所有 AI 共讀的核心共識
├── CLAUDE.md          ← Claude Code 專屬（規劃 + 審查）
├── GEMINI.md          ← Gemini CLI 專屬（執行）
└── .github/
    └── copilot-instructions.md  ← （可選）Copilot 補充說明
```

以及 `~/.codex/config.toml` 更新（若已安裝 Codex CLI）：

```toml
project_doc_fallback_filenames = ["CLAUDE.md", "GEMINI.md"]
```

完成後輸出摘要，說明：
- 哪些檔案是新建的
- 哪些檔案因已存在而跳過
- Codex config 是否更新
- 任何需要使用者手動填寫的 TODO 項目
