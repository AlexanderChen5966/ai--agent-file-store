# Obsidian 個人知識庫規劃：從知識整理到資產化的完整路線圖

---

## 第一部分：五篇文章的共通方法拆解

### 核心共識：AI + Obsidian = 活的知識系統

五篇文章來自不同作者、不同角度，但都指向同一個結論：**Obsidian 的本地 Markdown 檔案結構，天然適合讓 AI 直接讀寫，因此能從「被動筆記」升級為「主動知識系統」**。

以下是從五篇內容提煉出的六項共通方法：

---

### 共通方法 1：以 Markdown 為基礎設施

所有文章都強調一件事：不用資料庫、不用私有格式，用純文字 Markdown。

理由很簡單——Markdown 是 AI 最能理解的格式。Claude Code 可以直接進入你的資料夾讀取、寫入、更新，不需要複製貼上。NxCode 指南提到 Obsidian 截至 2026 年 2 月已超過 150 萬用戶，22% 年增長，正是因為本地優先的 Markdown 架構讓任何 AI 模型都能接入。

WenHao Yu 在他的個人 AI 工作流文章中，把這稱為「可程式化的基礎設施」——所有文件用 Markdown，純文字、跨平台、AI 可以直接讀寫。

**落地做法：** 在 Obsidian 中建立 Vault，所有筆記一律用 `.md` 格式，frontmatter 統一使用 YAML 標記 tags、日期、來源。

---

### 共通方法 2：資料夾結構採用 PARA 或類似分層

多篇文章都使用或建議 PARA 方法（Projects, Areas, Resources, Archive）作為資料夾骨架：

```
My Vault/
├── 00 Inbox/          # 未分類的原始輸入
├── 01 Projects/       # 進行中的專案
├── 02 Areas/          # 持續關注的領域
├── 03 Resources/      # 參考資料
├── 04 Archive/        # 完成或停用的內容
├── Templates/         # 筆記模板
└── Scripts/           # 自動化腳本
```

Karpathy 的方法更極簡，只用三個資料夾加一份設定檔。但核心邏輯相同：**收集和整理分離，讓 AI 負責整理，人只負責丟進去**。

---

### 共通方法 3：讓 AI 代替你做整理工作

這是五篇文章最大的共通主張。

經理人的文章引述 Karpathy 的做法：你只需要把資料丟進去，摘要、分類、交叉連結、維護全部交給 AI。他用這個方法在某個研究主題上累積了將近 100 篇筆記、40 萬字，而且查得動。

數位時代兩篇文章拆解了具體流程：用 Obsidian Web Clipper 一鍵擷取網頁 → Claude Code 自動讀取 Inbox → 生成摘要、加標籤、建立 wikilink → 更新目錄索引。

WenHao Yu 更進一步建立了完整的自動化循環：每日 AI 自動生成 Brief，涵蓋目標追蹤、信箱摘要、會議紀錄。

**共通原則：人負責輸入（capture）和思考，AI 負責整理（organize）和連結（link）。**

---

### 共通方法 4：用 Claude Code + MCP 做深度整合

NxCode 指南稱之為「power combo」——透過 MCP（Model Context Protocol）讓 Claude Code 直接存取 Obsidian Vault，實現讀取、搜尋、建立、修改筆記。

這不是在聊天框裡交換文字，而是 AI 真正進入你的檔案系統操作。五篇文章中有四篇都提到 Claude Code 是這套系統的核心引擎。

**關鍵差異：** 一般的 ChatGPT 或 Claude 網頁版只能在對話框裡互動；Claude Code 則可以直接操作你的資料夾，像一個能用你電腦的 AI 助理。

---

### 共通方法 5：Context Engineering（情境工程）

NxCode 文章特別提出「Context Engineering」的概念：你的筆記結構越一致（統一 tags、links、metadata），AI 就越能檢索到正確的上下文。

這呼應了所有文章的隱含訊息：**知識庫不只是「存資料」，而是「為 AI 做好情境準備」**。每一篇筆記都是未來 AI 互動的上下文素材。

WenHao Yu 的三大設計原則中也強調「讓 AI 成為唯一的介面」——不應該需要記得在哪裡找什麼，讓 AI 幫你跨系統整合。

---

### 共通方法 6：漸進式建設，不追求完美

所有文章都不約而同地警告「完美主義」的陷阱：

- NxCode：先亂輸入，之後再整理（Embrace messy initial capture）
- Karpathy：極簡結構，三個資料夾就夠
- WenHao Yu：花三個月從空資料夾長成完整系統
- 經理人文章：用最快方式建起來，先跑再說

---

### 共通方法對照表

| 方法 | NxCode 指南 | 經理人 | 數位時代(Karpathy) | 數位時代(Obsidian+CC) | WenHao Yu |
|------|:-----------:|:------:|:------------------:|:---------------------:|:---------:|
| Markdown 為基礎 | ✅ | ✅ | ✅ | ✅ | ✅ |
| PARA/分層結構 | ✅ | — | ✅(極簡版) | ✅ | ✅(LYT) |
| AI 負責整理 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Code + MCP | ✅ | ✅ | ✅ | ✅ | ✅ |
| Context Engineering | ✅ | — | — | — | ✅ |
| 漸進式建設 | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 第二部分：知識資產化——用 MAPS 框架讓知識庫產生複利

### Axton Liu 的核心主張

Axton Liu 的 MAPS 方法論和 Claude Skills 實測文章，提供了一個關鍵的思維升級：

> **從「知識整理」到「知識資產化」**
> 知識庫不只是「查得到」，而是要變成「可復用、可傳承、可規模化」的資產。

---

### MAPS 框架應用於知識庫

MAPS 是乘法關係（M × A × P × S），任何一項為零，整體歸零。

**M（Mindset 心智模式）— 資產化思維**

關鍵轉變：從「我把筆記存好了」→「我把判斷邏輯封裝成可復用的模組」。

每次你在 Obsidian 中整理資料時，問自己：
- 這個整理動作會重複嗎？（頻率）
- 每次花多長時間？（耗時）
- 需要專業判斷嗎？（複雜度）

用 5A+ 的「資產化價值 = 頻率 × 耗時 × 複雜度」公式計算，≥50 分就值得資產化。

**A（Architecture 架構設計）— 模組化知識結構**

把知識庫設計成可組合的模組：
- 每個「知識模組」只負責一個主題（單一職責）
- 輸入輸出明確（接口清晰）
- 模組之間透過 wikilink 和 tag 連結（可組合性）

**P（Prompt 提示工程）— 將整理邏輯寫成指令**

把你的「整理筆記」習慣轉化為 Claude 可執行的 Skill。例如：
- 判斷一篇筆記的核心論點是什麼（T 層）
- 判斷適用場景和限制（B 層）
- 提取可執行的步驟（R 層）
- 生成行動清單（C 層）

**S（Systems 系統化落地）— 用 5A+ 循環迭代**

不需要一次做完，用 5A+ 循環：
1. AIM：定義你的知識庫要解決什麼問題
2. ACQUIRE：收集必要的模板和工具
3. ATTEMPT：先建一個最小可用版本
4. ADJUST：用了兩週後根據實際體驗優化
5. APPLY：穩定後擴展到更多領域
6. PLUS：持續沉澱最佳實踐

---

### Claude Skills 如何讓知識庫資產化

Axton 的 Claude Skills 實測揭示了兩種核心用法：

**能力包型（Capability Package）**

把你的判斷邏輯封裝進一個 SKILL.md。例如他的 discussion-organizer Skill 內含四層判斷邏輯（價值判斷 → 可信度判斷 → 提取粒度 → 措辭規範化），5 分鐘完成原本需要 3-4 小時的筆記整理。

對應到你的 Obsidian 知識庫：你可以建立一個「知識整理 Skill」，定義你自己的判斷標準，讓 Claude 每次按同樣邏輯處理新輸入。

**軟編排型（Soft Orchestration）**

多個獨立 Agent 協作完成複雜流程。例如 srt-workflow Skill 通過 Task 工具調度多個子 Agent，數分鐘將字幕轉為結構化文章。

對應到你的知識庫：可以設計一個流程——Agent A 負責擷取和摘要 → Agent B 負責分類和打標 → Agent C 負責更新索引和建立連結。

---

## 第三部分：整合規劃——Obsidian 知識庫 × MAPS 資產化的實戰路線圖

### 整體架構

```
┌─────────────────────────────────────────────────────┐
│               你的 Obsidian Vault                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  輸入層 (Capture)                                    │
│  ├─ Web Clipper 擷取文章                             │
│  ├─ 手動筆記                                        │
│  └─ 檔案/PDF/影片字幕 丟入 Inbox                     │
│                                                     │
│  處理層 (Process) ← Claude Code + Skills             │
│  ├─ 知識整理 Skill (能力包型)                        │
│  │   ├─ T: 提煉核心論點                              │
│  │   ├─ B: 標記適用場景與限制                         │
│  │   ├─ R: 提取可執行步驟                            │
│  │   └─ C: 生成行動清單                              │
│  ├─ 自動分類 + 打標                                  │
│  ├─ Wikilink 交叉連結                                │
│  └─ 索引/MOC 更新                                   │
│                                                     │
│  資產層 (Asset) ← MAPS 資產化                        │
│  ├─ Skills 庫：封裝的判斷邏輯                         │
│  ├─ 模板庫：標準化的筆記格式                          │
│  ├─ SOP 庫：可復用的工作流程                          │
│  └─ 知識索引：可查詢的結構化知識                      │
│                                                     │
│  輸出層 (Output)                                     │
│  ├─ 每日 Brief：AI 生成的每日摘要                     │
│  ├─ 專案報告：基於知識庫生成                          │
│  ├─ 內容創作：文章/教程/分享素材                      │
│  └─ 決策支持：基於歷史資料的分析                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 分階段實施計劃（用 5A+ 循環）

#### 第一階段：AIM + ACQUIRE（第 1-2 週）

**目標：** 建立基礎 Vault 結構，完成工具安裝

行動清單：
- 安裝 Obsidian，建立 Vault
- 設定 PARA 資料夾結構（或你偏好的分層方式）
- 安裝 Obsidian Web Clipper
- 安裝 Claude Code（需 Anthropic 帳號）
- 建立第一份筆記模板（包含 YAML frontmatter）
- 蒐集 3-5 篇你最常參考的文章，用 Web Clipper 存入 Inbox

**模板建議：**

```yaml
---
title: 
date: {{date}}
tags: []
source: 
type: [article/note/idea/reference]
status: [inbox/processed/reviewed]
tbrc_layer: [T/B/R/C]
asset_value: 
---
```

#### 第二階段：ATTEMPT（第 3-4 週）

**目標：** 建立 MVP 版的知識整理流程

行動清單：
- 用 Claude Code 指向你的 Vault 資料夾
- 建立第一版「知識整理 Prompt」（先不做成 Skill，先手動測試）
- 處理 Inbox 中的 10 篇筆記，觀察 Claude 的判斷品質
- 記錄你希望 Claude 做但還沒做好的地方
- 建立第一份 MOC（Map of Content）索引筆記

**測試指令範例：**

```
請讀取 00 Inbox/ 中的所有筆記，對每一篇：
1. 用一句話總結核心論點
2. 給出 1-3 個 tag
3. 判斷它屬於 Projects/Areas/Resources 哪一類
4. 如果和 Vault 中已有筆記有關聯，建立 [[wikilink]]
5. 移動到對應資料夾
```

#### 第三階段：ADJUST（第 5-6 週）

**目標：** 根據實際使用優化流程，開始資產化

行動清單：
- 回顧前兩週的處理結果，評估品質（準確率、分類一致性）
- 優化 Prompt，加入 TBRC 判斷框架
- 建立第一個 Claude Skill（能力包型）：`knowledge-organizer`
- 設計 SKILL.md，封裝你的判斷邏輯
- 建立 references/ 資料夾，放入 TBRC 模板

**Skill 結構：**

```
/skills/knowledge-organizer/
├── SKILL.md           # 核心指令：TBRC 判斷邏輯
├── references/
│   ├── tbrc-template.md   # TBRC 格式模板
│   ├── tag-taxonomy.md    # 標籤分類表
│   └── examples/          # 輸入輸出範例
└── scripts/               # 自動化腳本（可選）
```

#### 第四階段：APPLY（第 7-8 週）

**目標：** 擴展知識庫到更多領域，建立穩定的日常工作流

行動清單：
- 將 Skill 應用到不同類型的內容（技術文章、會議紀錄、學習筆記）
- 建立「每日 Brief」流程（參考 WenHao Yu 的做法）
- 設計第二個 Skill：`daily-brief-generator`
- 開始使用 SCQA 框架做階段性回顧
- 考慮是否需要軟編排型 Skill（多 Agent 協作）

#### 第五階段：PLUS（持續）

**目標：** 持續優化，沉澱最佳實踐

行動清單：
- 每週 15 分鐘回顧：知識庫新增了多少筆記？查詢效率如何？
- 每月 1 小時深度回顧：哪些 Skill 最常用？哪些需要調整？
- 記錄踩坑經驗和高級技巧
- 持續優化 tag 體系和 MOC 結構

---

### 四大框架在知識庫中的定位

```
┌────────────────────────────────────────────────────┐
│                  你的知識庫工作流                     │
├────────────────────────────────────────────────────┤
│                                                    │
│  MAPS 提供全局思維                                   │
│  → M: 每次存筆記前問「這值得資產化嗎？」               │
│  → A: 知識庫的模組化架構設計                          │
│  → P: 寫出 Claude 能精確執行的 Skill                  │
│  → S: 5A+ 循環持續迭代                               │
│                                                    │
│  TBRC 負責單篇知識的結構化                            │
│  → T: 這篇的核心論點是什麼？                          │
│  → B: 適用於什麼場景？不適用於什麼？                   │
│  → R: 具體怎麼操作？                                  │
│  → C: 關鍵行動是什麼？                                │
│                                                    │
│  SCQA 用於階段性回顧和決策溝通                        │
│  → S: 知識庫現在什麼狀態？                            │
│  → C: 遇到什麼問題？                                  │
│  → Q: 下一步要解決什麼？                              │
│  → A: 具體怎麼調整？                                  │
│                                                    │
│  5A+ 驅動每一輪迭代                                   │
│  → AIM → ACQUIRE → ATTEMPT → ADJUST → APPLY → PLUS │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

### 立即行動清單

**今天就能開始（< 30 分鐘）：**
- 安裝 Obsidian，建立一個新 Vault
- 建立 5 個 PARA 資料夾
- 用 Web Clipper 存入你收藏的第一篇文章

**本週完成（< 3 小時）：**
- 安裝 Claude Code 並指向你的 Vault
- 手動測試「讀取 Inbox → 分類 → 打標」流程
- 建立第一份筆記模板

**本月目標：**
- Vault 中累計 30+ 篇經過處理的筆記
- 建立第一個知識整理 Skill
- 初步形成每日或每週的知識整理習慣

---

## 附錄：資源連結

**知識庫建設參考：**
- NxCode Obsidian AI 完整指南 (2026)
- 經理人：一個指令打造 AI 知識庫
- 數位時代：Karpathy LLM 知識庫方法
- 數位時代：Claude Code 整理 Obsidian 筆記
- WenHao Yu：Claude Code + Obsidian 個人 AI 助理系統

**資產化框架參考：**
- Axton Liu：MAPS 四維羅盤方法論
- Axton Liu：Claude Skills 能力包與軟編排指南
- Axton Liu：Claude Skills 從指令到資產的系統化構建指南
- 四大框架參考文件：SCQA、TBRC、MAPS、5A+

---

*文件版本：v1.0*
*建立日期：2026-05-13*
*適用平台：Obsidian + Claude Code*
