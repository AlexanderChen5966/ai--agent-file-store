---
name: daily-brief-generator
description: |
  Daily knowledge base briefing generator.
  Scans the vault and produces a structured daily brief covering:
  new raw materials pending processing, wiki updates, task status changes,
  and vault statistics. Inspired by WenHao Yu's daily AI brief system.

  Trigger: daily-brief, 每日摘要, 今日簡報, brief, 知識庫狀況, vault status
metadata:
  version: 1.2.0
---

# daily-brief-generator

掃描整個 Vault，產出每日結構化簡報。
讓你不需要手動檢查就能掌握知識庫狀態。

## 使用方式

```
daily-brief
今日簡報
知識庫狀況
```

---

## 輸出結構

### 每日 Brief 格式

```markdown
# 知識庫每日 Brief — YYYY-MM-DD

## 📥 待處理（raw/ 積壓）
- 共 N 篇未處理素材（.md：N / .pdf：N）
- [清單：檔名、格式、來源、建立日期]
- 建議：[是否需要立即處理]

## 📚 最近更新（wiki/）
- 過去 7 天新增：N 篇
- 過去 7 天修改：N 篇
- [清單：標題、更新日期]

## 📋 任務狀態（projects/ + shared tasks）
- 進行中：N 個
- 待實作：N 個
- [清單：任務名稱、狀態、最後更新]

## 🔗 孤立筆記
- 沒有 wikilink 的 wiki 條目：N 篇
- [清單：建議可連結的筆記]

## 📊 Vault 統計
| 項目 | 數量 |
|------|------|
| wiki/ 條目 | N |
| raw/ 待處理（.md） | N |
| raw/ 待處理（.pdf） | N |
| research/ 筆記 | N |
| ideas/ 筆記 | N |
| projects/ 專案 | N |

## 💡 今日建議行動（SCQA）

**S（現況）**：[一句話描述知識庫目前狀態，例：raw/ 積壓 N 篇，本週 wiki 新增 N 篇]

**C（衝突）**：[最突出的問題，例：raw/ 積壓超過 15 篇 / 有 N 個孤立筆記 / 任務逾期]

**Q（核心問題）**：[因此，現在最需要優先解決的是什麼？]

**A（行動）**：
1. [最優先]
2. [次優先]
```

---

## 執行流程

1. **掃描 `raw/`** — 列出所有未處理素材：`.md`（`status: inbox` 或無 frontmatter）與 `.pdf`（wiki/ 中無對應 `source_format: pdf` 條目者）
2. **掃描 `wiki/`** — 找出過去 7 天建立或修改的條目
3. **掃描 `projects/`** — 列出進行中的專案與待實作任務
4. **掃描 `tasks`** — 讀取 `wiki/b2b-manager/tasks.md` 的待實作項目
5. **找孤立筆記** — wiki/ 中沒有被任何其他筆記 wikilink 指向的條目
6. **統計** — 計算各資料夾的 `.md` 檔案數量
7. **產出 Brief** — 依上方格式產出，存入 `outputs/brief-YYYY-MM-DD.md`

---

## 判斷規則

### raw/ 積壓警示等級

| 積壓數量 | 警示 |
|----------|------|
| 0-5 篇 | 正常，無需特別處理 |
| 6-15 篇 | 建議本週批次處理 |
| > 15 篇 | 需要立即用 knowledge-organizer 處理 |

### 今日建議行動優先順序（SCQA 填寫邏輯）

**S（現況）** — 用統計數字說明，不加評論：
- 例：「raw/ 積壓 12 篇（.md：8 / .pdf：4），本週 wiki 新增 3 篇」

**C（衝突）** — 選最突出的一個問題：
1. raw/ 積壓 > 15 篇 → 衝突是「素材消化速度跟不上輸入速度」
2. 有未完成 projects/ 任務逾期 → 衝突是「任務停滯」
3. 有孤立筆記 > 3 篇 → 衝突是「知識島嶼，無法被引用」
4. wiki 本週零更新 → 衝突是「知識庫停止生長」

**Q（核心問題）** — 從 C 直接推導，一句話：
- 例：「如何在本週內清完 raw/ 積壓？」

**A（行動）** — 最多 2 個，具體可執行：
- 例：「1. 今天跑 raw-pipeline 批次處理 / 2. 完成 sort_data_tables 任務」

---

## 參考資源

- `references/brief-template.md` — Brief 空白模板
- WenHao Yu 每日 Brief 方法：涵蓋目標追蹤、信箱摘要、會議紀錄

---

## Changelog

### v1.2.0（2026-05-14）
- 「今日建議行動」改用 SCQA 框架結構化輸出（S 現況 / C 衝突 / Q 核心問題 / A 行動）
- 新增 SCQA 各層填寫邏輯說明

### v1.1.0（2026-05-14）
- 待處理積壓分開顯示 .md / .pdf 數量
- 統計表拆分 raw/ .md 與 .pdf 兩列
- 執行流程步驟 1 加入 PDF 未處理判斷邏輯

### v1.0.0（2026-05-13）
- 初始版本
- 五區塊 Brief 格式（待處理 / 最近更新 / 任務狀態 / 孤立筆記 / 統計）
- raw/ 積壓警示等級
- 自動存入 outputs/brief-YYYY-MM-DD.md
