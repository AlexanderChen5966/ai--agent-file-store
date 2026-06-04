# API 開發完整範例

## 任務：建立用戶認證系統

### 需求
- 用戶註冊（email + password）
- 用戶登入（返回 JWT）
- Token 刷新
- 密碼加密（bcrypt）
- 完整驗證

### 工具分工
- **Claude：** 架構設計、安全審查
- **Copilot：** 代碼生成、測試
- **驗證：** Claude

---

## 階段 1：架構設計（Claude）

```bash
$ claude
> "設計用戶認證系統的完整架構"
```

### Claude 輸出重點

```
資料庫 Schema：
- users 表（id, email, password_hash）
- refresh_tokens 表（id, user_id, token, expires_at）

API 端點：
- POST /auth/register
- POST /auth/login
- POST /auth/refresh

安全考量：
- bcrypt cost factor: 10
- JWT 有效期：15 分鐘
- Refresh token：7 天
- Rate limiting
```

---

## 階段 2：實作（Copilot）

```bash
$ gh copilot --prompt "實作 Express.js 註冊端點，
  使用 bcrypt 和 joi 驗證"
```

Copilot 生成基礎代碼...

---

## 階段 3：審查（Claude）

```bash
$ claude
> "審查這個認證實作的安全性"
```

### Claude 發現的問題

1. ❌ 缺少密碼強度驗證
2. ❌ 沒有 rate limiting
3. ❌ 錯誤訊息太詳細（洩漏資訊）
4. ❌ 缺少 SQL 注入防護
5. ❌ 沒有 CSRF token

### Claude 建議改進

```javascript
// 1. 加強密碼驗證
const passwordSchema = Joi.string()
  .min(8)
  .pattern(/[A-Z]/)  // 至少一個大寫
  .pattern(/[a-z]/)  // 至少一個小寫
  .pattern(/[0-9]/)  // 至少一個數字
  .required();

// 2. 加入 rate limiting
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts'
});

// 3. 統一錯誤訊息
// ❌ 不要這樣
if (!user) return res.status(404).json({ error: 'User not found' });
if (!validPassword) return res.status(401).json({ error: 'Wrong password' });

// ✅ 應該這樣
if (!user || !validPassword) {
  return res.status(401).json({ error: 'Invalid credentials' });
}
```

---

## 階段 4：測試（Copilot）

```bash
$ gh copilot --prompt "為認證端點撰寫 Jest 測試"
```

生成完整測試套件...

---

## 完整流程總結

```
1. Claude 設計架構（10 分鐘）
   ↓
2. Copilot 生成代碼（5 分鐘）
   ↓
3. Claude 審查安全性（10 分鐘）
   ↓
4. Copilot 生成測試（5 分鐘）
   ↓
5. Claude 最終驗證（5 分鐘）

總時間：35 分鐘
節省 Claude 額度：~40%
```

## 學到的教訓

### ✅ 有效的做法
- Claude 先規劃再實作
- Copilot 處理重複性代碼
- 分階段驗證每個輸出
- 使用共享文檔記錄決策

### ❌ 避免的錯誤
- 不要跳過設計階段
- 不要盲目接受 AI 代碼
- 不要忘記安全審查
- 不要省略測試

## 相關資源
- [最佳實踐](../references/best-practices.md)
- [安全檢查清單](../references/security-checklist.md)
