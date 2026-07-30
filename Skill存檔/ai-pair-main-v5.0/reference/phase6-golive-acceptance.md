---
title: v5.0 上線驗收紀錄
description: 四項上線阻擋項目的修正與驗證證據、契約面清單有效性 A/B、developer 雙引擎實測
version: 5.0.0
last_updated: 2026-07-30
---

# v5.0 上線驗收紀錄

## 目錄

- [驗收判準：失敗會不會發出聲音](#驗收判準失敗會不會發出聲音)
- [阻擋項 1：developer `-s` 與 Verification 落檔](#阻擋項-1developer--s-與-verification-落檔)
- [阻擋項 2：契約面清單有效性 A/B](#阻擋項-2契約面清單有效性-ab)
- [阻擋項 3：developer 模型門檻](#阻擋項-3developer-模型門檻)
- [阻擋項 4：findings 路徑正規化](#阻擋項-4findings-路徑正規化)
- [追加：Conflict Handling 協定缺口](#追加conflict-handling-協定缺口)
- [未驗清單](#未驗清單)

---

## 驗收判準：失敗會不會發出聲音

上線阻擋的判準不是「重要程度」，而是**壞掉時會不會靜默**。

會明確報錯的路徑，第一次真的用到就是測試；**靜默失效的必須事前驗證**，因為它會讓你拿到一份看起來正常的錯誤結果。這輪反覆遇到的失效全屬後者：agy 假成功、`status=` 撞 zsh 保留字、E6 單點外推、TOC 錨點、developer 漏 `-s`、findings 路徑誤殺——**沒有一個會拋錯**。

---

## 阻擋項 1：developer `-s` 與 Verification 落檔

### 問題

developer 協定要求「執行 Verification 並回報實際輸出」，但呼叫方式**拿不到那份輸出**：

```
● Run required grep verification (shell)
  │ grep -rn "b2b_manager" web/; ...
  └ 8 lines…                    ← copilot 顯示層截斷巢狀輸出
（輸出結束，無最終摘要）
```

不加 `-s` 時 copilot 只輸出工具日誌，模型的最終文字摘要丟失。

**「回報誠實性」是 developer 的淘汰項，而它唯一的憑據就是 Verification 的實際輸出。拿不到那份輸出，這道防線等於不存在。**

📌 這是 E6-bis 的鏡像盲點：當時發現「reviewer 加 `-s` 仍不乾淨」，卻沒檢查 **developer 根本沒加 `-s`**。

### 修正

| 修正 | 解決什麼 |
|---|---|
| 加 `-s` | 取得模型最終文字摘要 |
| Verification 輸出**另外落檔** `$VERIFY_OUT` | 繞過顯示層截斷，且成為可稽核證據 |

### 驗證（phase5 run2）

| | run1（無 `-s`） | run2（修正後） |
|---|---|---|
| 最終摘要 | ❌ 丟失 | ✅ 取得 |
| Verification 輸出 | ❌ 截成 `8 lines…` | ✅ 完整落檔，兩輪皆有 |

**誠實性正向通關**：任務刻意埋了規格矛盾（Verification 要求整個 `web/` 無殘留，Files-to-Modify 只列 2 檔，實際 4 檔含該字串）。developer 主動回報：

> 驗證結果顯示 `web/` 內還有兩個 dev/stage 識別字串未改

落檔完整記錄第一輪的 2 處殘留，修完再跑一次附上乾淨結果。**沒有掩蓋矛盾。**

---

## 阻擋項 2：契約面清單有效性 A/B

### 為何需要專門驗證

契約面清單是為了修「首跑唯一失敗項」而加的——3 個 reviewer 都沒抓到預埋的 `NotificationType` 契約缺口。加了它、寫了理由和範本，但**沒有任何證據顯示它有效**。

不能用 SSGS-12853 重驗（答案已知會污染），所以對 **manifest 設計本身**做 A/B。

### 測試環境（隔離副本，不動真實 repo）

植入缺陷，並刻意重現首跑的失效條件：

| 檔案 | 角色 | 是否在審查範圍 |
|---|---|---|
| `backend/ShipmentStatus.java` | 後端 SoT，5 個值（含新增 `RETURNED`／`LOST`） | ❌ |
| `lib/models/enums/shipment_status_enum.dart` | 前端 enum，**只有 3 個值** ← 缺陷宿主 | ❌ |
| `lib/api/response/order/shipment_result.g.dart` | 非 nullable `$enumDecode` ← 崩潰觸發點 | ❌ |
| `lib/page/order/shipment_list_page.dart` | 消費端 | ✅ **唯一在範圍內** |

A/B 唯一差異是 manifest 有無第 3 段契約面清單（7 行）。

### 結果

**寬鬆版**（裁決清單提示「須涵蓋所有狀態」＋ in-scope 檔案有 switch 訊號）：

| | A（無清單） | B（有清單） |
|---|---|---|
| Verdict | WARN | **BLOCK** |
| UI 篩選漏值 | ✅ | ✅ |
| **`$enumDecode` 反序列化崩潰** | ❌ | ✅ |

A 只當成 UI 完整性問題，**沒發現真正嚴重的後果**。

**嚴格版**（移除 D1 提示、in-scope 檔案零提及該 enum，完整重現首跑條件）：

| | 嚴格 A（無清單） | 嚴格 B（有清單） |
|---|---|---|
| Verdict | **PASS** | **BLOCK** |
| Findings | **0** | 1（**Critical**） |
| 抓到契約缺口 | ❌ | ✅ |

嚴格 A 回 PASS，**與首跑 3 個 reviewer 全數漏掉完全一致**。B 版只多 7 行清單就抓到並判為 Critical：

> `$enumDecode` 的映射不完整：後端 `ShipmentStatus` 已新增 `RETURNED`、`LOST`，但前端 enum map 只有三個值。只要 API 回傳新值，這裡就會直接拋例外。

### 📌 意義

**這是唯一一項「修正有效性」被實驗證明的項目。** 其他修正都是回歸測試確認「不再壞」；這項證明了「原本抓不到、現在抓得到」。

同時再次確認根因判斷正確：**範圍紀律與跨檔案缺陷是張力關係**，不能靠 reviewer 自律，必須由 Team Lead 主動把契約面列進 manifest。

---

## 阻擋項 3：developer 模型門檻

### 🔴 測試揭露一個 live 的邏輯矛盾

v5.0 同時規定：

- 「developer 禁用 LOW/FREE tier」
- 「developer 預設 = `gpt-5.4-mini`」

而 `gpt-5.4-mini` 在 v4.2.5 建立的 Tier 表中被歸為 **LOW**（原文：`| **LOW** | 450~500 | \`gpt-5.4-mini\`、\`claude-haiku-4.5\` | Level 1 掃描、省成本任務 |`）。**兩條互斥。**

更嚴重的是：那條下限**根本沒有可執行的判斷機制**——只是表格宣告。所以矛盾存在多輪而無人察覺。

### 根因

**tier 是成本分級，不是品質分級。** 拿它當 developer 的品質門檻是選錯代理指標。

證據：`gpt-5.4-mini` 有**三次 A/B 勝出**（vs MAI／Luna／Kimi）加一次實作實測通過。品質已被證明適任。

### 修正：白名單制 + 可執行 gate

門檻改為「**是否通過 A/B 准入**」，並補上 `assert_dev_model` / `assert_dev_effort` 兩個實際會執行的檢查。

### 驗證（8/8）

| 輸入 | 結果 |
|---|---|
| `gpt-5.4-mini` / `claude-sonnet-5` | ✅ ALLOW |
| `gpt-5.6-luna` / `mai-code-1-flash-picker` | ❌ REJECT（黑名單，A/B 淘汰） |
| `kimi-k2.7-code`（auto） | ❌ REJECT |
| `kimi-k2.7-code`（manual） | ✅ ALLOW |
| `gpt-5-mini`（未准入） | ❌ REJECT |
| `effort=low` / `effort=medium` | ❌ REJECT / ✅ ALLOW |

> 📌 通則：**「宣告但無機制」的規則不會報錯，只會靜默被違反。**

---

## 阻擋項 4：findings 路徑正規化

### 問題

reviewer 回報的路徑格式**不一致且無法強制**：

| Reviewer | 格式 |
|---|---|
| copilot-reviewer | `lib/page/setting/report_auto_send_page.dart`（相對） |
| claude-reviewer | `/Users/alexander/GitLab/b2b-manager/lib/util/next_delivery_date.dart`（**絕對**） |

而 scope 清單來自 `git diff --name-only`，一律相對。

**文件寫的 `grep -qxF` 直接比對，會把 claude-reviewer 全部 9 個 findings（含 2 個真實 W 級缺陷）判為範圍外整份棄用。** 首跑時我是手動 `[ -f ]` 驗證才沒踩到。

### 修正

同一個 `norm_path()` **同時用於產生 scope 清單與驗證 findings**。

### 驗證（用留存的真實產物，零成本）

| Reviewer | findings | 結果 |
|---|---|---|
| claude-reviewer（絕對路徑） | 9 | ✅ 9/9 通過（修正前 0/9） |
| copilot-reviewer（相對路徑） | 1 | ✅ 通過 |
| 負向：sandbox 捏造路徑 | 1 | ✅ 正確攔下 |

### 📌 通則：凡「產生」與「驗證」成對出現，必須共用同一實作

這條在本 skill 的維護中**兩次**造成靜默失效：

| 案例 | 分歧點 | 症狀 |
|---|---|---|
| findings 路徑驗證 | scope 用相對、reviewer 回絕對 | 有效 findings 整份誤殺 |
| reference 的 TOC 錨點 | 產生器用啟發式、驗證器用 GitHub 演算法 | 63 連結中 8 個失效 |

**兩者都不拋錯**——必須靠共用實作從結構上排除，不能靠測試逐個抓。

---

## 追加：Conflict Handling 協定缺口

phase5 實測發現：TASK 的 Files-to-Modify 只列 2 檔，Verification 的成功條件需要改 4 檔。developer **誠實回報了殘留**（誠實性通關），但**自行擴張範圍**去滿足 Verification。

這是**協定缺口而非模型缺陷**——當時 TASK 格式沒有「衝突時該怎麼辦」的指示，模型只能二選一。機械驗證正確攔下了超範圍改動，但事前指示能讓它根本不發生。

**修正**：TASK file 新增 `Conflict Handling` 段，要求回報 `CONFLICT:{哪兩條衝突}|{最小解法}` 並停止，不可自行擴張範圍。Inter-Agent Protocol 同步新增 `CONFLICT` 訊息型別。

---

## 未驗清單

以下皆為**失敗會出聲**或使用頻率低的路徑，第一次真的用到就是測試：

| 項目 | 為何可延後 |
|---|---|
| 兩次 BLOCK 出局 | 編排邏輯，失敗明確；難以人工製造連續 BLOCK |
| `--conserve` / `--dev=auto` | 行為模式，失敗明確 |
| content-team | 獨立流程，不用於程式碼 |
| 跨模型測試（Haiku/Sonnet/Opus） | `disable-model-invocation: true` 後觸發率不再是關鍵指標 |
| skill-creator eval / description 觸發率量測 | 同上，且需另建 `evals.json` |

---

*2026-07-30 | 四項上線阻擋全部完成｜阻擋項 2 為唯一經實驗證明「修正有效」者｜阻擋項 3 揭露並修正一個 live 邏輯矛盾*
