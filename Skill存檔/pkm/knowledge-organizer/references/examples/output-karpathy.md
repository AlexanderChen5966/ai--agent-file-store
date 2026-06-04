# 範例：處理後的 wiki 條目

> 這是 knowledge-organizer Skill 處理後的輸出，存入 `wiki/`

---

```yaml
---
title: Karpathy AI 知識庫方法
date: 2026-05-13
tags: [pkm/workflow, pkm/obsidian]
source: https://www.anduril.tw/karpathy-knowledge-base/
type: article
status: processed
asset_value: 75
---
```

## T（核心論點）
把 AI 從「用完即忘的問答工具」升級為「會自己長大的個人圖書館」——人只負責
丟資料，AI 全權負責整理與維護 wiki。

## B（適用場景）
**適用：** 有大量碎片素材需要整理、長期研究某個主題、希望 AI 越用越精準的場景
**不適用：** 一次性查詢、素材量少（< 10 篇）時效益不明顯

## R（操作步驟）
1. 建立 `raw/` `wiki/` `outputs/` 三個資料夾
2. 所有素材丟入 `raw/`（不分類，用 Web Clipper）
3. 對 Claude Code 下指令：「讀取 raw/ 編譯成 wiki/」
4. 每次查詢的結果回存到 `outputs/`（知識複利）
5. 每月執行健康檢查：找矛盾、補缺漏、發現關聯

## C（關鍵行動）
- [ ] raw/ 和 wiki/ 必須分開存放（避免 AI 內容淹沒個人筆記）
- [ ] wiki 建立後先確認 INDEX.md 是否更新
- [ ] 每次查詢結果記得回存 outputs/

## 原始摘要
Karpathy 比喻：大多數人用 AI 像去便利商店（用完即忘），他的做法是讓 AI
建一座圖書館（越用越厚）。六步驟流程的關鍵是第二步：AI 自動編譯 raw/ 為 wiki，
人幾乎不手動整理。Lex Fridman 延伸做法：跑步時用語音模式對 wiki 提問。

## 相關連結
- [[obsidian-web-clipper]] — 配合使用的擷取工具
```

---

**Skill 判斷說明：**

| 判斷 | 結果 |
|------|------|
| 資產化價值 | 頻率(5) × 耗時(3) × 複雜度(5) = 75 → 完整 TBRC 處理 |
| Tag | `pkm/workflow`（方法論） + `pkm/obsidian`（工具） |
| 歸屬 | `wiki/`（長期參考的方法論） |
| Wikilink | 連結到 `obsidian-web-clipper`（同一工作流的工具） |
