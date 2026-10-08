---
name: sanlong-pay-onboarding
metadata:
  version: 1.0.0
description: sanlong（山隆 PAY，iOS + Android Flutter APP）專案的新人快速上手導覽。回答「環境怎麼建、APP 怎麼跑起來、某功能的程式碼在哪、我的第一個任務怎麼下手、這裡有哪些不能踩的規則」。觸發時機：/sanlong-pay-onboarding、我是新人、剛接手 sanlong、剛接手這專案、怎麼開始、APP 怎麼跑、程式碼在哪、幫我導覽專案、第一次改這個專案、新增畫面/API 該從哪開始。僅適用於 app01-double 這個 repo；在其他專案請用該專案自己的 onboarding skill。
---

# 山隆 PAY 新人上手導覽

**這個 skill 是路由器，不是教科書。** 專案已有 `AGENTS.md`（含必讀路由表）、`DESIGN.md`、
`.claude/rules/` 四份規則、`docs/` 46 篇——問題是新人不知道**該讀哪一份、什麼順序**。

⚠️ **絕不憑記憶回答專案細節。** 每個答案都要落地到具體檔案路徑與行號；
不確定就先 `Read` / `Grep` 驗證，再回答。這個專案有多處**文件與程式碼有落差**（見路徑 B、D）。

📌 **本 skill 的所有行號與檔案規模以 `main` 分支為基準**（撰寫時為 `190038a9`）。
feature 分支上數字會位移，**對不上時一律以原始碼為準**——先 `git branch --show-current`
確認對方在哪支分支上，再決定要不要提醒他數字會有出入。

## 📄 先確認對方知道有 `docs/onboarding.html`

專案已有一份**給人自己讀**的一頁式導覽（含色票色塊、mermaid 架構圖、可勾選進度）。
純自學讓對方直接開那個檔；**本 skill 負責的是對話式問答**——他問一個具體問題、你給落地答案。

⚠️ `docs/` 在 `.gitignore:57`，**新人 clone 拿不到那份 HTML**，得請人直接傳給他。
反之 `.claude/` 沒有被 ignore，所以**這支 skill 會隨 repo 進版控**，clone 就有。

---

## Step 0：先判斷「他是誰、卡在哪」

若使用者沒說清楚，先用一句話問，不要一次問五題：

- 環境還沒跑起來（Xcode / CocoaPods / flavor） → **路徑 A**
- 環境好了，在找程式碼 → **路徑 B**
- 已接到任務，要動手 → **路徑 C**
- 剛被 review 打槍 / 想先知道地雷 → **路徑 D**
- 看不懂業務名詞（儲值金、快速加油、B2C QR…） → **路徑 E**

---

## 決策樹（路由表）

| 使用者的問題長這樣 | 走哪條 | 載入 |
|---|---|---|
| 「怎麼跑起來」「要跑哪個 main」「flavor 是什麼」「pod install 失敗」 | A · Day 1 | `references/day1-setup.md` |
| 「XX 功能在哪」「controller 為什麼這麼大」「路由怎麼運作」「provider 在哪定義」 | B · 地圖 | `references/codebase-map.md` |
| 「我要加一個畫面／一支 API／一個顏色／一句文案／一個 Bottom Sheet」 | C · 食譜 | `references/first-task-recipes.md` |
| 「有什麼不能做」「為什麼畫面從底部彈出」「改了設定別頁沒更新」 | D · 地雷 | `references/conventions-gotchas.md` |
| 「儲值金和點數差在哪」「快速加油是什麼」「Screen enum 這些名字什麼意思」 | E · 名詞 | `references/glossary-domain.md` |

多條同時命中時，**依 A → B → C → D 的順序**帶，不要一次倒完五份。

---

## 給「完全零基礎、要一條龍」的人：四小時上手路線

只有在使用者明確說「我第一天，帶我走一遍」時才整套跑。

1. **跑起來（~60 min，iOS 要 pod install 會比較久）** — `references/day1-setup.md`
   驗收：模擬器或實機跑起 dev flavor，能進到首頁
2. **看懂一條資料流（~40 min）** — `references/codebase-map.md` 的「垂直切片」段
   驗收：能講出「按下儲值」從 UI 到 controller 到 repository 經過哪幾行
3. **改一句文案（~30 min）** — `references/first-task-recipes.md` 食譜 4
   驗收：改 `assets/zh-tw.csv` 一個 key，畫面看到變化（**不要 commit**）
4. **讀紅線（~50 min）** — `references/conventions-gotchas.md`
   驗收：能答對下方自我測試全 10 題
5. **認名詞（~20 min）** — `references/glossary-domain.md`
6. **接第一個真任務** — 建議「調整某個輸入欄位長度限制」這類題型：
   會同時碰 UI、controller、i18n，但風險極低、驗收明確（近期 commit `5a651658`、`09f92fb5` 就是這型）

---

## 十分鐘版（老手接手，只要重點）

一次講完這六句，不要展開：

1. **Flutter 手機 APP（iOS + Android，直式）**，加油站服務／儲值金／會員點數；**沒有 Web**
2. 分層固定：**UI（ConsumerStatefulWidget）→ SLController → Repository → Dio / SharedPreferences**，
   ❌ UI 層不可直接打 API
3. **`controller.dart` 3418 行是刻意的單一大型 controller**，不是技術債，別自己開始拆
4. **路由是自製的 SLRouter + NavStack**（`lib/app/router/`），不是 go_router，官方文件查不到
5. **本專案沒有 screenutil**——`.w/.h/.sp` 照抄 b2b-manager 會破壞版面
6. 狀態管理 Riverpod，最大宗 bug 是**狀態不同步**（A 頁改了 B 頁顯示舊值），
   動 provider 前先讀 `.claude/rules/riverpod-state-sync.md`

---

## 回答時的規矩

- **先給檔案路徑與行號，再給說明。**
- **每條路徑都給驗收動作**，別停在「大概是這樣」。
- **遇到高風險區直接標紅**：修改共用元件（先 `grep` 使用範圍）、引入新套件、
  改原生 iOS/Android 設定、拆 SLController、改資料模型核心結構
  → 一律提醒「需先取得使用者同意」（見 `AGENTS.md` >「修改範圍原則」）。
- **文件可能與程式碼有落差**，引用前開檔案抽驗一眼，對不上就以原始碼為準並回報。
- 一律**繁體中文台灣用語**；技術術語與識別符保留英文。

---

## 新人自我測試（帶完後請對方作答）

1. 這個 APP 支援哪些平台？有 Web 版嗎？
2. 要跑起來該執行哪個 main 檔？flavor 怎麼指定？
3. UI 想拿一筆 API 資料，正確的呼叫鏈是什麼？
4. `controller.dart` 三千多行，該不該順手拆掉？
5. 這個專案可以用 `.w` / `.h` / `.sp` 嗎？
6. 想讓新畫面「側滑進入」，`pushMain` 的 `isDraggable` 要怎麼帶？
7. 防止使用者連點兩次送出，該擋在哪一層？
8. 上傳設定成功後，為什麼別的畫面還顯示舊值？該補什麼？
9. 要加一句中文文案，寫在哪個檔案？可以用中文當 key 嗎？
10. 準備上架時，`pubspec.yaml` 的版本代碼基底該設成多少？

> 標準答案散在各 reference 與 `.claude/rules/`；批改時請引用出處，不要憑印象給分。

---

## 相關資產索引

| 位置 | 內容 |
|---|---|
| `AGENTS.md` | 共用規則 + **必讀檔案路由表**（跨 agent 單一維護點）、NEVER 清單、命名慣例 |
| `CLAUDE.md` | Claude Code 專屬補充，含「模型不易自行發現的專案慣例」三條 |
| `DESIGN.md` | 設計系統 SoT（色彩／字級／間距／元件／反模式） |
| `.claude/rules/flutter-ui-pitfalls.md` | Bottom Sheet、固定高度排版、共用元件五個實際踩過的坑 |
| `.claude/rules/riverpod-state-sync.md` | 狀態同步四坑（源自 SSGS-13122，來回修三輪） |
| `.claude/rules/dev-resources.md` | `lib/app/utils/` 既有工具清單，動手前先查 |
| `.claude/rules/release-checklist.md` | 版本代碼計算規則（dev+1／stage+2／release+3） |
| `docs/onboarding.html` | 給人自學的一頁式導覽（⚠️ gitignore，clone 拿不到） |
| `docs/page_architecture/PROJECT_ARCHITECTURE.md` | 架構正本 |
| `docs/shared/*.md` | 任務文件；`docs/bug_record/`、`docs/issue/` 為歷史復盤 |