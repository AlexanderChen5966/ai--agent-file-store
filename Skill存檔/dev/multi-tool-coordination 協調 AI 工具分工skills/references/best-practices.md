# Multi-Tool Coordination 最佳實踐

## 工具選擇原則

### 決策樹

```
任務複雜度？
├─ 低（< 50 行代碼）
│  └─ 使用 Copilot
│
├─ 中（50-200 行）
│  ├─ 標準模式？
│  │  └─ 使用 Copilot
│  └─ 需要設計？
│     └─ Claude 設計 → Copilot 實作
│
└─ 高（> 200 行）
   └─ Claude 規劃 → 分段實作 → Claude 整合
```

### 工具強度對照

| 任務類型 | Claude | Copilot | Codex | Gemini |
|---------|--------|---------|-------|--------|
| 架構設計 | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| 快速編碼 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 代碼審查 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| 演算法 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 技術研究 | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## 上下文傳遞模式

### 模式 1：摘要傳遞（推薦）

**適用：** 中小型任務

```bash
# ❌ 不好
$ gh copilot --prompt "優化這 500 行代碼：[完整代碼]"

# ✅ 好
$ gh copilot --prompt "優化認證中間件：
  問題：每次請求查詢資料庫驗證 JWT
  目標：加入記憶體快取（Redis）
  要求：保持原有錯誤處理邏輯"
```

**優點：**
- 節省 tokens
- 聚焦問題
- 回應更精準

### 模式 2：文件橋接（推薦）

**適用：** 團隊協作、長期專案

```bash
# 步驟 1: 記錄到文件
$ claude
> "更新 ARCHITECTURE.md：記錄新的快取策略"

# 步驟 2: 參考文件
$ gh copilot --prompt "根據 ARCHITECTURE.md 的快取策略，
  實作 Redis 快取層"

# 步驟 3: 更新進度
$ claude
> "更新 TASKS.md：標記快取實作完成"
```

**優點：**
- 可追蹤
- 可審查
- 可重用

### 模式 3：迭代精煉

**適用：** 複雜任務

```bash
# 迭代 1: 粗略實作
$ gh copilot --prompt "快速實作用戶認證 API"

# 迭代 2: Claude 審查
$ claude
> "審查這個認證實作，列出需要改進的地方"

# 迭代 3: 針對性改進
$ gh copilot --prompt "改進：[Claude 列出的具體問題]"

# 迭代 4: 最終驗證
$ claude
> "最終檢查，確認所有問題都已解決"
```

**優點：**
- 逐步提升品質
- 及時發現問題
- 學習最佳實踐

## 常見場景最佳策略

### 場景 1：新功能開發

```
1. Claude：需求分析 + 架構設計（15 分鐘）
2. Copilot：實作核心邏輯（20 分鐘）
3. Claude：代碼審查 + 重構（15 分鐘）
4. Copilot：撰寫測試（10 分鐘）
5. Claude：整合驗證（10 分鐘）

總時間：70 分鐘
品質：高
```

### 場景 2：Bug 修復

```
1. Copilot：快速查詢常見原因（2 分鐘）
2. Claude：深度分析根本原因（10 分鐘）
3. Claude/Copilot：實作修復（15 分鐘）
4. Claude：驗證 + 測試（10 分鐘）

總時間：37 分鐘
準確度：高
```

### 場景 3：技術調研

```
1. Gemini：廣泛調研（15 分鐘）
2. Claude：分析適用性（10 分鐘）
3. Copilot：實作 PoC（20 分鐘）
4. Claude：評估結果（10 分鐘）

總時間：55 分鐘
全面性：高
```

### 場景 4：重構優化

```
1. Claude：分析重構範圍（20 分鐘）
2. Claude：制定重構計劃（10 分鐘）
3. Copilot：實作簡單重構（15 分鐘）
4. Claude：處理複雜部分（25 分鐘）
5. Claude：驗證 + 測試（15 分鐘）

總時間：85 分鐘
風險：低
```

## 效率提升技巧

### 技巧 1：批次處理

```bash
# 準備任務清單
tasks=(
  "實作用戶 CRUD"
  "實作權限中間件"
  "實作錯誤處理"
)

# Claude 規劃
$ claude
> "為這些任務制定實作順序和架構"

# Copilot 批次實作
for task in "${tasks[@]}"; do
  gh copilot --prompt "實作：$task"
done

# Claude 批次審查
$ claude
> "審查所有新增代碼的一致性"
```

### 技巧 2：模板化

建立常用模板：

```bash
# templates/api-endpoint.md
POST /api/{resource}
請求：{schema}
回應：{schema}
驗證：{rules}
錯誤：{error_codes}
```

使用時：

```bash
$ gh copilot --prompt "根據 templates/api-endpoint.md，
  實作 POST /api/users 端點"
```

### 技巧 3：快速切換

使用 alias 簡化命令：

```bash
# .bashrc 或 .zshrc
alias copilot='gh copilot --prompt'
alias ask-claude='claude'

# 使用
$ copilot "如何排序陣列"
$ ask-claude "審查這段代碼"
```

### 技巧 4：結果快取

記錄常見問題的答案：

```markdown
# FAQ.md

## Q: 如何處理 async/await 錯誤？
Copilot 建議：try-catch
Claude 補充：使用 Promise.catch + 全域錯誤處理器

## Q: PostgreSQL 連線池設定？
Copilot 建議：[代碼]
Claude 優化：[改進版]
```

## 品質保證檢查清單

### 每次實作後檢查

- [ ] 代碼符合專案風格
- [ ] 所有邊界條件都處理
- [ ] 錯誤處理完整
- [ ] 有適當的日誌記錄
- [ ] 敏感資訊已保護
- [ ] 效能考量已處理
- [ ] 文檔已更新
- [ ] 測試已撰寫

### 安全性檢查

- [ ] SQL 注入防護
- [ ] XSS 防護
- [ ] CSRF 防護
- [ ] 認證正確實作
- [ ] 授權檢查完整
- [ ] 敏感資料加密
- [ ] Rate limiting
- [ ] 輸入驗證

### 效能檢查

- [ ] N+1 查詢問題
- [ ] 快取策略
- [ ] 索引優化
- [ ] 連線池設定
- [ ] 記憶體洩漏
- [ ] 並發處理

## 團隊協作建議

### 規範化工作流程

```markdown
# WORKFLOW.md

## 團隊標準流程

### 新功能
1. 建立 feature branch
2. Claude 設計架構 → 更新 ARCHITECTURE.md
3. 實作（Claude/Copilot）
4. 程式碼審查（Claude）
5. PR 前最終檢查
6. 合併到 main

### 工具分工
- Senior：主要用 Claude（設計、審查）
- Junior：多用 Copilot（實作、學習）
- All：Claude 最終審查
```

### Code Review 重點

```markdown
## Review Checklist

### AI 生成代碼特別注意
- [ ] 檢查安全性（AI 可能忽略）
- [ ] 驗證邏輯正確性
- [ ] 確認邊界條件處理
- [ ] 檢查效能影響
- [ ] 確保符合專案規範
```

## 成本優化策略

### 策略 1：選擇性使用 Claude

```
只在以下情況用 Claude：
✅ 架構設計
✅ 代碼審查
✅ 複雜問題分析
✅ 技術決策

用 Copilot 處理：
✅ 樣板代碼
✅ 簡單查詢
✅ 測試生成
✅ 文檔撰寫
```

預估節省：**50-60% Claude 額度**

### 策略 2：批次處理

```bash
# ❌ 不好（多次調用）
$ claude "實作 A"
$ claude "實作 B"
$ claude "實作 C"

# ✅ 好（一次調用）
$ claude "實作 A、B、C 三個功能，
  共用以下架構：[架構說明]"
```

預估節省：**30-40% 調用次數**

### 策略 3：使用 Copilot 訂閱

```
個人：$10/月
學生/教師：免費

相比單獨用 Claude API：
月省約 $20-50（依使用量）
```

## 進階模式

### 模式：平行協作

```
任務：全端應用開發

並行軌道：
Track 1 (Claude)  : 後端 API 設計
Track 2 (Copilot) : 前端元件開發
Track 3 (Codex)   : 資料處理腳本

最後 (Claude)     : 整合審查
```

### 模式：專家系統

```
Gemini  : 研究最新實踐
Claude  : 評估適用性
Copilot : 生成實作代碼
Claude  : 優化整合
```

## 疑難排解

### 問題：上下文丟失

**症狀：** AI 不了解之前的決策

**解決：**
```bash
# 使用文件記錄
$ claude
> "更新 DECISIONS.md：為何選擇 Redis"

# 後續參考
$ gh copilot --prompt "根據 DECISIONS.md，
  實作 Redis 快取"
```

### 問題：代碼品質不一致

**症狀：** 不同工具生成的代碼風格差異大

**解決：**
```bash
# 建立風格指南
$ claude
> "根據我們的代碼，建立風格指南"

# 要求遵循
$ gh copilot --prompt "遵循 STYLE.md，實作..."
```

### 問題：效率未提升

**症狀：** 使用多工具反而更慢

**診斷：**
- 切換太頻繁？→ 完成單元再切換
- 工具選擇錯誤？→ 參考決策樹
- 上下文傳遞低效？→ 使用摘要模式

## 持續改進

### 每週回顧

```markdown
## 本週回顧

### 工具使用統計
- Claude: 20 次（節省 45%）
- Copilot: 50 次
- 效率提升: 2.5x

### 學到的經驗
1. [經驗 1]
2. [經驗 2]

### 下週改進
1. [改進計劃]
```

### 技能提升

定期練習：
- 每週嘗試 1 個新協作模式
- 記錄效果最好的策略
- 分享給團隊

---

**版本：** 1.0  
**最後更新：** 2025-01-28
