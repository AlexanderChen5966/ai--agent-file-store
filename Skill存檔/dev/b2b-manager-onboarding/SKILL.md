---
name: b2b-manager-onboarding
metadata:
  version: 1.1.0
description: B2B Manager（山隆 B2B 智慧平台，Flutter Web）專案的新人快速上手導覽。回答「環境怎麼建、專案怎麼跑起來、某功能的程式碼在哪、我的第一個任務怎麼下手、這裡有哪些不能踩的規則」。觸發時機：/b2b-manager-onboarding、我是新人、剛接手 b2b-manager、剛接手這專案、怎麼開始、專案怎麼跑、程式碼在哪、幫我導覽專案、第一次改這個專案、新增頁面/API 該從哪開始。僅適用於 b2b-manager 這個 repo；其他專案請用該專案自己的 onboarding skill。
---

# B2B Manager 新人上手導覽

**這個 skill 是路由器，不是教科書。** 專案已有大量文件（`CLAUDE.md` / `AGENTS.md` / `DESIGN.md` /
`docs/`），問題出在新人不知道**該讀哪一份、讀多少、什麼順序**。
本 skill 的工作是：判斷來者要什麼 → 給出最短路徑 → 只載入必要的 reference。

⚠️ **絕不憑記憶回答專案細節。** 每個答案都要落地到具體檔案路徑或指令；
不確定就先 `Read` / `Grep` 驗證，再回答。

---

## Step 0：先判斷「他是誰、卡在哪」

若使用者沒說清楚，先用一句話問，不要一次問五題：

- 環境還沒跑起來 → **路徑 A**
- 環境好了，在找程式碼 → **路徑 B**
- 已接到任務，要動手 → **路徑 C**
- 剛被 review 打槍 / 想先知道地雷 → **路徑 D**
- 看不懂業務名詞（群組、儲值、標籤、報表排程…） → **路徑 E**

---

## 決策樹（路由表）

| 使用者的問題長這樣 | 走哪條 | 載入 |
|---|---|---|
| 「怎麼跑起來」「flutter run 要帶什麼」「登入轉不進去」「build_runner 是什麼」 | A · Day 1 | `references/day1-setup.md` |
| 「XX 功能在哪個檔案」「列表頁怎麼組起來的」「API 從哪打出去」「狀態放哪」 | B · 地圖 | `references/codebase-map.md` |
| 「我要新增一支 API／一個頁面／一個列表／一個欄位／一個顏色／一句文案」 | C · 食譜 | `references/first-task-recipes.md` |
| 「有什麼不能做」「為什麼不能用 `.w`」「排序怎麼又壞了」「權限要隱藏還是 disable」 | D · 地雷 | `references/conventions-gotchas.md` |
| 「群組是什麼」「Authorities 有哪些」「dev/staging 差在哪」 | E · 名詞 | `references/glossary-domain.md` |

多條同時命中時，**依 A → B → C → D 的順序**帶，不要一次倒完五份。

---

## 給「完全零基礎、要一條龍」的人：四小時上手路線

只有在使用者明確說「我第一天，帶我走一遍」時才整套跑。

1. **跑起來（~40 min）** — `references/day1-setup.md`
   驗收：`http://localhost:9001` 能登入進到首頁儀表板
2. **看懂一條資料流（~40 min）** — `references/codebase-map.md` 的「垂直切片」段
   驗收：能講出「車輛列表」從按鈕點下去到畫面更新，經過哪 5 個檔案
3. **改一個字（~30 min）** — `references/first-task-recipes.md` 的「食譜 5：i18n」
   驗收：改一句文案並看到畫面變化（**不要 commit**）
4. **讀硬規則（~40 min）** — `references/conventions-gotchas.md`
   驗收：能答對下方「自我測試」全 10 題
5. **認名詞（~30 min）** — `references/glossary-domain.md`
6. **接第一個真任務** — 到 `docs/shared/readme.md` 找 ⏳ 待實作 的小票

---

## 十分鐘版（老手接手，只要重點）

一次講完這五句，不要展開：

1. **Flutter Web only**，基準 1920×1024，不支援 iOS/Android；部署走 Docker/Nginx → AWS ECS
2. **狀態 Riverpod**（`lib/api/notifier/**`）、**路由 GoRouter**（`lib/page/page_route.dart`）、
   **API Retrofit + Dio**（`lib/api/restclient/rest_client.dart`），改 API 後**必跑 build_runner**
3. **認證 OAuth2 PKCE，一律經 TaskManager**（`lib/api/connector/task_manager.dart`），禁止直呼
4. **UI token 化**：色 `SLColor`、字 `SLText`、間距 `SpacerWidget`、圓角 `kAppRadius`；
   **新程式碼禁用 `.w/.h/.sp`**，改固定 px
5. **表格是本專案最大地雷區**（`ApiPaginatedDataTable` / `DataTable2` / `VirtualDataTable`），
   動之前先讀 `.claude/rules/datatable-safety.md`

---

## 回答時的規矩

- **先給檔案路徑，再給說明。** 新人要的是「打開哪一個檔案」，不是概念複述。
- **每條路徑都給驗收動作**（跑什麼指令、畫面上看到什麼），別停在「大概是這樣」。
- **遇到高風險區直接標紅**：`page_route.dart`、`external_libs/`、TaskManager／OAuth2、
  DataTable 欄寬與排序 → 一律提醒「需先取得使用者確認」（見 `.claude/rules/change-policy.md`）。
- **文件可能過期。** `docs/` 是描述性文件，會與程式碼漂移；引用前先開檔案抽驗一眼，
  對不上就以原始碼為準並回報落差。
- 一律**繁體中文台灣用語**；技術術語與識別符保留英文。

---

## 新人自我測試（帶完後請對方作答）

答不出來的題目，回頭補對應的 reference：

1. 這專案支援哪些平台？基準解析度多少？
2. 本機要用哪個 port 跑？為什麼不能隨便換？
3. 改了 `lib/api/request/` 之後要下什麼指令？
4. `ref.watch` / `ref.read` / `ref.listen` 分別什麼時候用？build phase 能改 provider 嗎？
5. 新程式碼可以寫 `SizedBox(height: 40.h)` 嗎？表格容器高度呢？
6. 列表頁 search request 的 `size` 該填多少？為什麼不能填 10？
7. 新增／刪除後重抓列表，`isClear` 要傳 true 還 false？為什麼？
8. 使用者沒有刪除權限時，刪除按鈕該隱藏還是 disable？表單欄位呢？
9. `external_libs/` 底下的套件可以 `flutter pub upgrade` 嗎？
10. 想改 `lib/page/page_route.dart` 之前要先做什麼？

> 標準答案散在各 reference 與 `.claude/rules/`；批改時請引用出處，不要憑印象給分。

---

## 相關資產索引

| 位置 | 內容 |
|---|---|
| `CLAUDE.md` / `AGENTS.md` | AI agent 共用硬規則（開場自動載入） |
| `.claude/rules/*.md` | P0 規則集：scope／change-policy／auth-taskmanager／datatable-safety／permission-gating／list-page-header／external-libs／api-build-runner／output-style |
| `DESIGN.md` | 設計系統 SoT，改 UI 前必讀 |
| `PROGRAM_STRUCTURE.md` | 1400 行完整結構圖（太長，只在需要全景時查目錄） |
| `docs/claude/*.md` | overview／architecture／development-workflows／datatable-rules／external-libs／troubleshooting／cicd |
| `docs/api/api_documentation_v16.md` | 後端 API 契約副本（注意版本與 `source-commit`） |
| `docs/shared/readme.md` | 任務文件索引（找第一個練手任務的地方） |
| `docs/bug_record/*.md` | 歷史 bug 復盤，踩到怪事先搜這裡 |