# Document Translator Skill 創建提示詞

> 用於透過 skill-creator 創建 document-translator skill 的完整提示詞文檔

---

## 使用方式

將本文檔的「提示詞內容」部分複製貼給 Claude，Claude 將使用 skill-creator skill 自動創建 document-translator skill。

---

## 提示詞內容

```
請使用 skill-creator skill 幫我創建一個名為 "document-translator" 的 skill。

以下是詳細需求：

---

## Skill 基本資訊

**Skill 名稱**: document-translator
**目的**: 協助 Claude 理解和操作技術文檔翻譯系統（使用智慧降級翻譯策略）
**位置**: /mnt/skills/user/document-translator/

---

## Skill 功能說明

這個 skill 是為了讓 Claude 能夠：
1. 理解翻譯系統的架構和工作流程
2. 協助用戶執行翻譯操作
3. 解釋不同翻譯模式和校稿後端的差異
4. 提供翻譯系統的故障排除建議
5. 管理術語表和翻譯配置
6. **理解 Playwright + Stealth 模式的反機器人偵測機制** ⭐
7. **處理 CAPTCHA 相關問題** ⭐

---

## 核心技術

### 自動化技術
- **Playwright**: 現代化瀏覽器自動化工具
- **Stealth 模式**: 反機器人偵測技術
- **Async/Await**: 非同步程式設計（效能優化）

### 反偵測策略
1. 隱藏 `navigator.webdriver` 標記
2. 偽裝瀏覽器指紋
3. 模擬真實 Chrome 行為
4. 人類化的打字速度
5. 隨機延遲

---

## 翻譯系統架構

### 目錄結構
```
project-root/
├── docs/
│   ├── en/              # 英文原文（權威來源）
│   └── zh-TW/           # 繁體中文譯文（自動生成）
│
├── translation/         # 翻譯系統
│   ├── translate.sh     # Shell 入口點
│   ├── translate.py     # Python 主程式
│   │
│   ├── translator/      # Python 模組
│   │   ├── google_translator.py
│   │   ├── interactive_proofreader.py
│   │   ├── chatgpt_translator.py       # 使用 Playwright ⭐
│   │   ├── fallback_translator.py      # 智慧降級翻譯器 ⭐
│   │   ├── claude_desktop_proofreader.py
│   │   ├── claude_cli_proofreader.py
│   │   ├── manual_proofreader.py
│   │   └── validator.py
│   │
│   └── config/
│       ├── glossary.json
│       ├── proofreading_prompt.txt
│       └── translation_config.json
```

### 翻譯流程（智慧降級策略）
```
英文文檔 (docs/en/)
    ↓
【策略 1】ChatGPT Translate（優先）
    ↓
  成功?
    ↓ 是
  完成 ✅
    ↓ 否
【策略 2】降級：Google Translate 粗翻
    ↓
【策略 3】智慧校稿（多種後端可選）
    ↓
繁體中文文檔 (docs/zh-TW/) ✅
```

**核心策略**：
1. **優先使用 ChatGPT Translate**（品質最佳、免費）
2. **失敗時自動降級**到 Google Translate + 校稿
3. **雙重保障**確保翻譯總是能完成

---

## 翻譯模式

### Mode 1: chatgpt
- 僅使用 ChatGPT Translate
- 品質最佳、免費
- 適用場景：重要文檔、對外發布
- 品質：⭐⭐⭐⭐
- 備註：失敗時不會降級，直接報錯

### Mode 2: auto（推薦）⭐
- ChatGPT Translate（優先）+ 智慧降級
- **優先使用 ChatGPT，失敗自動降級到 Google + 校稿**
- 高品質、高可靠性、零成本
- 適用場景：所有生產文檔（推薦）
- 品質：⭐⭐⭐⭐⭐
- 成功率：95%+

### Mode 3: google
- 僅使用 Google Translate（無校稿）
- 最快速、完全免費
- 適用場景：快速草稿、內部文檔
- 品質：⭐⭐

---

## 翻譯與校稿機制

### 主要翻譯器

#### Translator 1: ChatGPT Translate（優先）⭐
- 使用 ChatGPT Translate 網頁服務
- **透過 Playwright + Stealth 模式自動化**（避免機器人偵測）
- 優勢：品質最佳、免費、完全自動化、難被偵測
- 技術：Playwright 內建反偵測功能，大幅降低 CAPTCHA 觸發
- 需求：Playwright（會自動下載瀏覽器）
- 適用：所有技術文檔（優先使用）
- 成功率：~90%+（使用 Stealth 模式）

#### Translator 2: Google Translate（備案）
- 快速、免費的機器翻譯
- 作為降級備案使用
- 需要配合校稿器提升品質

### 校稿後端（降級時使用）

當 ChatGPT Translate 失敗，系統會降級到 Google Translate，此時需要校稿提升品質：

#### Backend 1: auto（預設）
- 自動偵測可用的校稿器
- 偵測優先順序：desktop > cli > manual
- 零配置、最方便

#### Backend 2: desktop
- 使用 Claude Desktop GUI
- 透過檔案交換互動
- 優勢：品質最佳、可視覺化審查
- 需求：Claude Desktop 應用程式
- 適用：重要對外文檔

#### Backend 3: cli
- 使用 Claude CLI 命令列工具
- 完全腳本化
- 優勢：穩定、適合自動化
- 需求：安裝 Claude CLI
- 適用：CI/CD 流程

#### Backend 4: manual
- 開啟文字編輯器手動校稿
- 完全控制
- 優勢：無需任何 AI 工具
- 需求：文字編輯器（VS Code/Sublime/nano/vi）
- 適用：少量修改、最終審查

---

## 使用方式

### 基本命令
```bash
# 智慧降級模式（推薦）⭐
./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md
# → 優先 ChatGPT，失敗自動降級到 Google + 校稿

# 僅 ChatGPT Translate（不降級）
./translation/translate.sh --mode=chatgpt docs/en/IMPORTANT.md

# 僅 Google Translate（最快，無校稿）
./translation/translate.sh --mode=google docs/en/DRAFT.md

# 批量翻譯（智慧降級）
./translation/translate.sh --mode=auto docs/en/*.md

# 禁用降級機制（ChatGPT 失敗就報錯）
./translation/translate.sh --mode=auto --no-fallback docs/en/*.md

# 指定降級時的校稿器
./translation/translate.sh --mode=auto --proofreader=desktop docs/en/API.md

# 顯示瀏覽器視窗（調試用）
./translation/translate.sh --mode=auto --no-headless docs/en/API.md

# 強制覆蓋已存在的譯文
./translation/translate.sh --mode=auto --force docs/en/*.md

# 詳細日誌
./translation/translate.sh --mode=auto --verbose docs/en/API.md
```

### Claude 應該如何協助用戶

當用戶說：
- "翻譯這個文件"
- "Translate this document"
- "幫我翻譯 API 文檔"

Claude 應該：
1. 確認檔案位置（應在 docs/en/）
2. **選擇智慧降級模式（--mode=auto）** 作為預設
3. 執行翻譯命令
4. 監控翻譯狀態（ChatGPT 成功 or 降級到 Google）
5. 驗證輸出（docs/zh-TW/）
6. 使用 present_files 呈現譯文
7. **報告使用的翻譯方法**（ChatGPT or Google+校稿）

### Claude 翻譯策略建議

根據文檔類型推薦模式：

**一般文檔**（推薦）:
```bash
./translation/translate.sh --mode=auto docs/en/API.md
```

**重要對外文檔**:
```bash
# 先用 ChatGPT
./translation/translate.sh --mode=chatgpt docs/en/IMPORTANT.md
# 如果失敗，再用 auto 模式
./translation/translate.sh --mode=auto docs/en/IMPORTANT.md
```

**快速草稿**:
```bash
./translation/translate.sh --mode=google docs/en/DRAFT.md
```

---

## 術語表管理

### 術語表位置
`translation/config/glossary.json`

### 術語表結構
```json
{
  "technical_terms": {
    "API": "API",
    "endpoint": "端點",
    "request": "請求",
    "response": "回應"
  },
  
  "taiwan_terms": {
    "account": "帳號",
    "data": "資料",
    "software": "軟體",
    "network": "網路"
  },
  
  "preserve": [
    "Claude",
    "GitHub",
    "Docker"
  ]
}
```

### Claude 協助更新術語表

當用戶說：
- "新增術語到術語表"
- "更新翻譯術語"

Claude 應該：
1. 讀取現有術語表
2. 詢問要新增的術語
3. 更新 JSON 檔案
4. 確認更新成功

---

## 品質驗證

### 自動驗證項目
- [ ] 程式碼區塊數量一致
- [ ] 標題數量一致
- [ ] 連結數量一致
- [ ] 無簡體中文字元（賬、數據、軟件、網絡）
- [ ] Markdown 格式正確

### Claude 檢查清單

當翻譯完成後，Claude 應該：
1. 確認譯文已生成
2. 檢查檔案大小合理（不能為空或過小）
3. 快速掃描是否有明顯錯誤
4. 提醒用戶人工審查重要文檔

---

## 常見問題與故障排除

### 問題 1: ChatGPT Translate 遇到 CAPTCHA（常見）
**現象**:
- 網頁出現「我不是機器人」驗證
- Cloudflare 或 reCAPTCHA 攔截

**原因**:
- 自動化工具被偵測（舊版 Selenium 容易觸發）
- IP 地址被標記
- 請求頻率過高

**解決方式（Playwright + Stealth 模式已大幅改善）**:

```bash
# 方案 1: 使用 Stealth 模式（預設，自動）
./translate.sh --mode=auto docs/en/API.md
# → Playwright Stealth 模式會自動避免大部分偵測

# 方案 2: 有頭模式（讓用戶手動解決 CAPTCHA）
./translate.sh --mode=auto --no-headless docs/en/API.md
# → 瀏覽器視窗會顯示，用戶可手動完成驗證

# 方案 3: 降級到 Google（自動）
# auto 模式會自動降級，無需手動干預
```

**Playwright vs Selenium**:
- ✅ Playwright + Stealth: CAPTCHA 觸發率 <10%
- ❌ Selenium: CAPTCHA 觸發率 >50%

**預期行為（有頭模式）**:
如果遇到 CAPTCHA，系統會：
1. 偵測到 CAPTCHA 存在
2. 顯示訊息：「⏳ 請手動完成 CAPTCHA 驗證...」
3. 等待 60 秒供用戶完成
4. 驗證完成後繼續翻譯

### 問題 2: 翻譯完全失敗
**可能原因**:
- Python 環境未正確設定
- 缺少依賴套件
- 檔案路徑錯誤

**解決方式**:
```bash
# 重建虛擬環境
cd translation
rm -rf venv
./translate.sh --mode=auto docs/en/test.md
```

### 問題 3: Playwright 或瀏覽器問題
**可能原因**:
- Playwright 未正確安裝
- 瀏覽器未下載

**解決方式**:
```bash
# 重新安裝 Playwright
pip install --upgrade playwright playwright-stealth

# 安裝瀏覽器（重要！）
playwright install chromium

# 或安裝所有瀏覽器
playwright install

# 驗證安裝
playwright --version
```

**macOS 特殊問題**:
```bash
# 如果遇到權限問題
sudo playwright install chromium
```

### 問題 4: 降級機制未啟動
**可能原因**:
- 使用了 --no-fallback 參數
- 使用 chatgpt 模式而非 auto 模式

**解決方式**:
```bash
# 確保使用 auto 模式且未禁用降級
./translate.sh --mode=auto docs/en/API.md
# 不要使用 --no-fallback
```

### 問題 5: 翻譯品質不佳
**診斷**:
1. 檢查使用的翻譯方法（查看日誌）
2. ChatGPT 成功 → 品質應該不錯
3. 降級到 Google → 可能需要更好的校稿器

**解決方式**:
```bash
# 使用更好的校稿器（降級時）
./translate.sh --mode=auto --proofreader=desktop docs/en/API.md

# 或手動校稿
./translate.sh --mode=auto --proofreader=manual docs/en/API.md
```

### 問題 6: Playwright Stealth 模式失效
**現象**:
- 即使使用 Stealth 模式仍被偵測
- CAPTCHA 持續出現

**可能原因**:
- IP 地址被標記
- 請求頻率過高
- 網站升級反爬蟲機制

**解決方式**:
```bash
# 方案 1: 降低頻率（批量翻譯時）
for file in docs/en/*.md; do
    ./translate.sh --mode=auto "$file"
    sleep 10  # 每個檔案間隔 10 秒
done

# 方案 2: 使用有頭模式（手動驗證）
./translate.sh --mode=auto --no-headless docs/en/API.md

# 方案 3: 直接降級到 Google
./translate.sh --mode=google docs/en/API.md
```

### 問題 7: Async 相關錯誤
**現象**:
- 錯誤訊息包含 `asyncio`、`await` 相關字樣

**原因**:
- Python 環境不支援 async
- 事件循環問題

**解決方式**:
```bash
# 確保 Python 版本 >= 3.7
python --version

# 重建虛擬環境
cd translation
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

---

## 效能與成本比較

| 模式 | 速度 | 品質 | 成功率 | CAPTCHA率 | Token 成本 | 適用場景 |
|------|------|------|--------|----------|-----------|---------|
| chatgpt | ⚡⚡ | ⭐⭐⭐⭐ | ~90% | <10% ⭐ | $0 | 重要文檔 |
| auto（推薦）⭐ | ⚡⚡ | ⭐⭐⭐⭐⭐ | 98%+ | <10% ⭐ | $0 | 所有文檔 |
| google | ⚡⚡⚡ | ⭐⭐ | ~95% | 0% | $0 | 快速草稿 |

**Playwright Stealth 模式優勢**：
- CAPTCHA 觸發率從 50%+ 降至 <10%
- 更穩定的自動化體驗
- 更快的執行速度
- 更少的人工干預需求

### 智慧降級統計範例

執行 10 個文檔翻譯後的統計：
```
============================================================
翻譯完成
============================================================
總計: 10 個檔案
✅ 成功: 10
❌ 失敗: 0

============================================================
翻譯統計
============================================================
ChatGPT 成功: 9 (90%)  ⬆️ 比 Selenium 提升 ~10%
ChatGPT 失敗: 1 (10%)
降級到 Google: 1
ChatGPT 成功率: 90.0%
CAPTCHA 遭遇: 0 次
============================================================
```

### 品質對比

| 翻譯來源 | 術語準確度 | 語句流暢度 | 格式保留 | 自動化程度 |
|---------|----------|----------|---------|-----------|
| ChatGPT (Playwright) ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Google + Desktop校稿 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Google + Manual校稿 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Google（無校稿） | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 技術對比：Selenium vs Playwright

| 面向 | Selenium | Playwright + Stealth | 改進 |
|------|----------|---------------------|------|
| CAPTCHA 觸發率 | 50-70% | <10% | **⬆️ 85%** |
| 安裝複雜度 | 需手動管理 ChromeDriver | 自動管理瀏覽器 | **⬆️ 更簡單** |
| 效能 | 較慢 | 更快 | **⬆️ 30%** |
| API 易用性 | 繁瑣 | 簡潔 | **⬆️ 更好** |
| 反偵測能力 | 需大量手動配置 | 內建 Stealth | **⬆️ 自動化** |
| Async 支援 | ❌ | ✅ | **⬆️ 新增** |

---

## GitLab CI/CD 整合

### 自動翻譯觸發條件
- 當 `docs/en/` 目錄下的 `.md` 檔案有變更
- 推送到 `main` 或 `develop` 分支

### CI/CD 流程（智慧降級）
```
推送英文文檔變更
    ↓
偵測變更的檔案
    ↓
自動翻譯（mode=auto）
  ├─ 嘗試 ChatGPT Translate
  └─ 失敗時降級到 Google + manual 校稿
    ↓
驗證翻譯品質
    ↓
自動提交譯文到 docs/zh-TW/
```

### CI/CD 配置建議

```yaml
# .gitlab-ci.yml
variables:
  TRANSLATION_MODE: "auto"          # 使用智慧降級
  PROOFREADER: "manual"             # 降級時用手動校稿（穩定）
  CHATGPT_HEADLESS: "true"          # 無頭模式
  ENABLE_FALLBACK: "true"           # 啟用降級
```

**為什麼 CI/CD 用 manual 校稿器？**
- CI/CD 環境無法互動
- manual 模式在 CI 中會跳過校稿（回退到純 Google）
- 仍比完全失敗好

---

## 相關檔案路徑

重要檔案位置：
- 翻譯腳本：`./translation/translate.sh`
- Python 主程式：`./translation/translate.py`
- **ChatGPT 翻譯器（Playwright）**：`./translation/translator/chatgpt_translator.py` ⭐
- **智慧降級翻譯器**：`./translation/translator/fallback_translator.py` ⭐
- Google 翻譯器：`./translation/translator/google_translator.py`
- 術語表：`./translation/config/glossary.json`
- 校稿提示詞：`./translation/config/proofreading_prompt.txt`
- 翻譯配置：`./translation/config/translation_config.json`
- 英文原文：`./docs/en/`
- 中文譯文：`./docs/zh-TW/`

### Python 依賴檔案
- 依賴清單：`./translation/requirements.txt`
  - `playwright>=1.40.0` ⭐
  - `playwright-stealth>=1.0.6` ⭐
  - `requests>=2.31.0`
  - 其他...

---

## Claude 的職責

作為翻譯系統的助手，Claude 應該：

1. **理解用戶意圖**
   - 判斷用戶想翻譯哪些文檔
   - 推薦適合的翻譯模式

2. **執行翻譯**
   - 構建正確的命令
   - 使用 bash_tool 執行
   - 監控執行狀態

3. **驗證結果**
   - 確認譯文已生成
   - 檢查基本品質
   - 使用 present_files 呈現

4. **提供建議**
   - 根據文檔重要性推薦模式
   - 解釋不同後端的差異
   - 協助故障排除

5. **管理配置**
   - 協助更新術語表
   - 調整翻譯配置
   - 維護校稿提示詞

---

## 範例對話

### 範例 1: 基本翻譯（智慧降級）
```
用戶: "幫我翻譯 API 文檔"

Claude:
1. 確認檔案：docs/en/API_DOCUMENTATION.md
2. 選擇智慧降級模式（預設）
3. 執行命令：
   bash_tool: ./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md
4. 監控過程：
   - 嘗試 ChatGPT Translate...
   - [成功] 或 [失敗，降級到 Google + 校稿]
5. 檢查輸出：docs/zh-TW/API_DOCUMENTATION.md
6. 報告：「翻譯完成，使用了 ChatGPT Translate」
   或：「ChatGPT 失敗，已降級到 Google + 校稿完成翻譯」
7. present_files: API_DOCUMENTATION.md
```

### 範例 2: 批量翻譯
```
用戶: "翻譯 docs/en 下所有文檔"

Claude:
1. 列出檔案：ls docs/en/*.md
2. 確認數量
3. 執行批量翻譯：
   bash_tool: ./translation/translate.sh --mode=auto docs/en/*.md
4. 報告結果
```

### 範例 3: 術語管理
```
用戶: "新增 'container' 翻譯為 '容器' 到術語表"

Claude:
1. 讀取術語表：view translation/config/glossary.json
2. 更新 technical_terms 區段
3. 寫入檔案：str_replace
4. 確認更新
```

### 範例 4: 故障排除（降級機制）
```
用戶: "翻譯失敗了"

Claude:
1. 詢問錯誤訊息
2. 檢查使用的模式
3. 診斷：
   - 如果是 chatgpt 模式 → 建議改用 auto（有降級）
   - 如果是 auto 模式 → 檢查是否有降級發生
   - 如果完全失敗 → 檢查 Python 環境
4. 提供解決方案：
   - "請嘗試智慧降級模式："
     ./translate.sh --mode=auto docs/en/API.md
5. 協助重新執行
```

### 範例 5: 查看翻譯統計
```
用戶: "最近的翻譯使用 ChatGPT 的成功率如何？"

Claude:
1. 說明：auto 模式會在翻譯後顯示統計
2. 範例統計：
   ChatGPT 成功: 8 (80%)
   降級到 Google: 2 (20%)
3. 建議：如果成功率低，可能需要檢查網路或 Playwright 設定
```

### 範例 6: Playwright 故障排除
```
用戶: "一直出現『我不是機器人』驗證"

Claude:
1. 診斷：這是 CAPTCHA 問題
2. 說明：Playwright Stealth 模式已大幅改善此問題
3. 解決方案：
   a) 確認使用最新版本：
      pip install --upgrade playwright playwright-stealth
   b) 嘗試有頭模式手動驗證：
      ./translate.sh --mode=auto --no-headless docs/en/API.md
   c) 或直接降級到 Google：
      ./translate.sh --mode=google docs/en/API.md
4. 預防：批量翻譯時加入延遲
```

### 範例 7: Playwright 環境設定
```
用戶: "如何安裝 Playwright？"

Claude:
1. 安裝 Python 套件：
   pip install playwright playwright-stealth
2. 安裝瀏覽器（重要！）：
   playwright install chromium
3. 驗證安裝：
   playwright --version
4. 測試翻譯：
   ./translate.sh --mode=auto --no-headless docs/en/test.md
```

---

## 進階功能

### 自訂校稿提示詞
用戶可以修改 `translation/config/proofreading_prompt.txt` 來自訂校稿規則。

Claude 應該協助：
1. 理解現有提示詞結構
2. 根據需求修改
3. 測試修改效果

### 多語言支援
雖然目前只支援英文→繁體中文，但架構允許擴展。

Claude 應該：
1. 解釋如何新增其他語言對
2. 指導修改配置檔案
3. 協助測試新語言

### Playwright 進階配置 ⭐

#### 調整反偵測強度
用戶可以修改 `chatgpt_translator.py` 中的反偵測設定：

```python
# 更嚴格的反偵測
await page.add_init_script("""
    // 更多反偵測腳本
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });
""")
```

#### 使用持久化瀏覽器會話
避免重複登入或驗證：

```python
# 儲存瀏覽器狀態
await context.storage_state(path="auth.json")

# 下次使用
context = await browser.new_context(storage_state="auth.json")
```

#### 自訂 User Agent
針對特定需求調整：

```python
context = await browser.new_context(
    user_agent='自訂的 User Agent 字串'
)
```

### 效能優化

#### 批量處理優化
```bash
# 平行處理（小心 CAPTCHA）
./translate.sh --mode=auto docs/en/file1.md &
./translate.sh --mode=auto docs/en/file2.md &
wait

# 序列處理（更安全）
for file in docs/en/*.md; do
    ./translate.sh --mode=auto "$file"
    sleep 5  # 避免觸發頻率限制
done
```

---

## 特別注意事項

### 網路環境
- ChatGPT 後端需要穩定的網路連線
- 可能需要處理防火牆或代理設定
- **Playwright 需要下載瀏覽器（~100MB）** ⭐

### Playwright 環境
- **首次使用必須執行**: `playwright install chromium` ⭐
- 需要 Python 3.7+ 以支援 async/await
- 無頭模式在某些環境可能不穩定（如 Docker）
- macOS 可能需要授予終端機「螢幕錄製」權限（System Preferences）

### CAPTCHA 處理
- **Stealth 模式大幅降低 CAPTCHA 觸發率**（<10%）
- 如果遇到 CAPTCHA，使用 `--no-headless` 模式
- 批量翻譯時建議加入延遲（避免觸發頻率限制）
- 某些 IP（如 VPN、資料中心 IP）更容易觸發 CAPTCHA

### 檔案權限
- 確保翻譯腳本有執行權限
- 確保輸出目錄可寫入

### 版本控制
- 英文文檔是權威來源
- 中文譯文自動生成，不應手動編輯
- 所有修改應在英文版進行

### CI/CD 環境注意事項 ⭐
```yaml
# GitLab CI 需要額外設定
before_script:
  - apt-get update
  - apt-get install -y libnss3 libatk-bridge2.0-0 libdrm2 libgbm1
  - pip install playwright playwright-stealth
  - playwright install chromium --with-deps
```

---

請根據以上資訊創建 document-translator skill 的 SKILL.md 檔案。

要求：
1. 結構清晰，易於 Claude 理解
2. 包含所有重要資訊
3. **重點強調智慧降級翻譯策略**（ChatGPT 優先，Google 備案）⭐
4. **重點強調 Playwright + Stealth 模式的優勢**（相對於 Selenium）⭐
5. **詳細說明 CAPTCHA 問題的改善**（觸發率從 50%+ 降至 <10%）⭐
6. **清楚說明三種翻譯模式的差異和使用場景**（chatgpt, auto, google）⭐
7. **詳細解釋降級機制的運作方式**⭐
8. **包含 Playwright 環境設定的完整步驟**（pip install, playwright install）⭐
9. 提供足夠的範例，特別是 CAPTCHA 處理和降級場景
10. 考慮實際使用場景
11. 使用 Markdown 格式
12. 加入適當的章節和目錄
13. **包含 Mermaid 圖表來解釋智慧降級流程和反偵測機制**⭐
14. 提供完整的命令參考（包含降級相關參數）
15. **包含完整的故障排除指南**（特別是 Playwright 和 CAPTCHA 相關）⭐
16. 加入最佳實踐建議（何時用哪種模式、如何避免 CAPTCHA）
17. 包含翻譯統計的解讀說明
18. **對比 Selenium vs Playwright 的差異**（技術對比表）⭐

謝謝！
```

---

## 使用步驟

### 步驟 1: 複製提示詞

將上面「提示詞內容」區塊中的所有文字（從「請使用 skill-creator...」到「謝謝！」）複製。

### 步驟 2: 與 Claude 對話

在 Claude Desktop 或 Claude.ai 中：

```
[貼上完整提示詞]
```

### 步驟 3: 等待生成

Claude 會使用 skill-creator skill 生成 document-translator skill 的 SKILL.md。

### 步驟 4: 下載檔案

Claude 會使用 `present_files` 工具呈現生成的 SKILL.md，點擊下載即可。

### 步驟 5: 放置檔案

將下載的 SKILL.md 放到：

```
/mnt/skills/user/document-translator/SKILL.md
```

或專案中的：

```
skills/user/document-translator/SKILL.md
```

---

## 驗證 Skill

創建完成後，測試 skill 是否正確工作：

### 測試 1: 基本理解

```
用戶: "使用 document-translator skill 解釋智慧降級翻譯流程"

預期: Claude 能清楚解釋 ChatGPT 優先、失敗降級到 Google + 校稿的策略
```

### 測試 2: 執行翻譯

```
用戶: "使用 document-translator skill 幫我翻譯 docs/en/test.md"

預期: Claude 執行 auto 模式翻譯命令並報告使用的方法
```

### 測試 3: 模式比較

```
用戶: "使用 document-translator skill 比較不同翻譯模式的差異"

預期: Claude 能解釋 chatgpt, auto, google 三種模式的區別和使用場景
```

### 測試 4: 故障排除

```
用戶: "使用 document-translator skill 幫我解決 ChatGPT 翻譯失敗的問題"

預期: Claude 能說明降級機制並建議使用 auto 模式
```

### 測試 5: 統計理解

```
用戶: "使用 document-translator skill 解釋翻譯統計資訊"

預期: Claude 能解釋 ChatGPT 成功率、降級次數等統計指標
```

---

## 進階調整

如果生成的 SKILL.md 需要調整，可以追加要求：

### 補充內容

```
"請在 document-translator skill 中補充：
1. 更詳細的智慧降級機制說明
2. **Playwright + Stealth 模式的反偵測原理** ⭐
3. **CAPTCHA 處理的完整流程** ⭐
4. ChatGPT Translate 失敗的常見原因
5. 降級統計的解讀方法
6. **Playwright 環境設定的詳細步驟** ⭐
7. **Async/Await 程式設計模式說明** ⭐
8. 更多實際使用範例"
```

### 調整格式

```
"請調整 document-translator skill 的格式：
1. 加入智慧降級的 Mermaid 流程圖
2. **加入 Playwright 反偵測機制的流程圖** ⭐
3. **加入 CAPTCHA 處理決策樹** ⭐
4. 使用表格呈現翻譯模式對比
5. 使用表格呈現 Selenium vs Playwright 對比
6. 增加降級決策樹圖表
7. 加入翻譯統計的視覺化說明"
```

### 簡化內容

```
"請簡化 document-translator skill：
1. 聚焦在智慧降級策略
2. 移除過於技術性的細節
3. 簡化範例
4. 使用更簡潔的語言"
```

---

## 預期輸出結構

Claude 生成的 SKILL.md 應該包含以下主要章節：

```markdown
# Document Translator Skill

## 📋 Table of Contents

## Overview
- Skill purpose
- Key features (智慧降級策略 + Playwright)
- System requirements

## System Architecture
- Directory structure
- Component diagram
- Data flow

## Technology Stack ⭐
- Playwright + Stealth 模式
- 反機器人偵測技術
- Async/Await 架構
- Python 3.7+ 要求

## Translation Strategy (重點)⭐
- 智慧降級機制
- ChatGPT 優先策略（Playwright）
- Google 備案機制
- 成功率統計

## Translation Modes
- chatgpt mode
- auto mode (推薦)
- google mode
- Mode comparison

## Translators & Proofreaders
- ChatGPT Translate (Playwright + Stealth) ⭐
- Google Translate (備案)
- Proofreading backends (降級時使用)
- Backend selection logic

## Anti-Detection Mechanisms ⭐
- Playwright Stealth 原理
- 反偵測技術細節
- CAPTCHA 觸發率對比（Selenium vs Playwright）
- 最佳實踐

## Usage Guide
- Installation (Playwright 設定)
- Basic commands
- Mode selection guide
- Fallback behavior
- Advanced options

## CAPTCHA Handling ⭐
- 偵測機制
- 自動處理（Stealth）
- 手動處理流程
- 預防策略

## Glossary Management
- Structure
- Update procedures
- Best practices

## Quality Validation
- Automatic checks
- Translation validation
- Manual review

## Troubleshooting
- CAPTCHA 問題（最常見）⭐
- Playwright 安裝問題 ⭐
- Async 錯誤處理 ⭐
- ChatGPT failures
- Fallback not triggered
- Quality problems
- Debug tips

## Examples
- Basic translation with Playwright
- CAPTCHA 處理範例 ⭐
- Batch processing
- Glossary updates
- Fallback statistics

## CI/CD Integration
- GitLab setup (Playwright in CI)
- Docker 環境配置 ⭐
- Fallback in CI
- Automation tips

## Performance Metrics
- Success rates (Playwright vs Selenium)
- CAPTCHA 觸發率對比 ⭐
- Quality comparison
- Speed comparison

## Best Practices
- When to use which mode
- Fallback configuration
- Monitoring statistics
- CAPTCHA 預防 ⭐
- 批量處理策略

## Advanced Topics ⭐
- Playwright 進階配置
- 持久化瀏覽器會話
- 自訂反偵測腳本
- Async 程式設計模式
- 效能調優

## Reference
- File paths
- Command reference
- Configuration options
- Playwright API 參考 ⭐
```

---

## 附錄

### A. 相關檔案

- 翻譯系統主程式：`translation/translate.py`
- Shell 入口點：`translation/translate.sh`
- 術語表：`translation/config/glossary.json`

### B. 參考資源

- Anthropic Skills 官方文檔
- skill-creator 使用指南
- **Playwright 官方文檔**: https://playwright.dev/python/ ⭐
- **Playwright Stealth**: https://github.com/AtuboDad/playwright_stealth ⭐
- **反機器人偵測技術**: https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth
- Python Async/Await 教學

### C. 版本歷史

- **v2.0.0 (2025-01-18): Playwright 升級版** ⭐
  - **從 Selenium 遷移到 Playwright + Stealth**
  - **CAPTCHA 觸發率降低 85%（50%+ → <10%）**
  - **新增 Async/Await 支援**
  - 改進反機器人偵測能力
  - 更穩定的自動化體驗
  - 更簡單的安裝流程

- v1.0.0 (2025-01-16): 初始版本
  - 智慧降級翻譯策略
  - ChatGPT Translate 優先（Selenium）
  - Google Translate 備案機制
  - 支援 3 種翻譯模式（chatgpt, auto, google）
  - 支援 4 種校稿後端（desktop, cli, manual, auto）
  - 完整的術語表管理
  - 翻譯統計與成功率追蹤

---

## 授權

本提示詞文檔採用 MIT License。

---

**文檔結束**
