# Phase 2 實測 — MAI-Code-1-Flash vs GPT-5.4 mini（LOW developer）

**目的：** 決定 v4.3.5 LOW tier developer 是否將預設主力從 `gpt-5.4-mini` 切換為 `mai-code-1-flash-picker`。
**測法：** 相同 `TASK_FILE.md`、相同 prompt/flags，只換 `--model`，在隔離目錄各跑一次，比較正確性與 token 效率。
**注意：** 此測試會消耗 Copilot Credit（兩個模型各一次真實任務）。

---

## 零、實測中發現的 harness 問題（重要）

⚠️ **`cat $TASK_FILE | copilot --model M -p "..."`（stdin pipe）在 CLI v1.0.65 失效。**

第一次依現行 `cli-invocation-ref.md`（v4.3）的方法跑 gpt-5.4-mini，模型**完全收不到 stdin 的任務內容**，只看到 `-p` 字串，回報「未提供可實作的額外功能需求」，空跑浪費 5.79 credits。

- 根因：`copilot --help`（v1.0.65）只有 `-p/--prompt <text>`，**無 stdin pipe、無 `-c @file`**；`--attachment` 僅支援 image / native document。
- 正解：任務內容須**直接放進 `-p`**（本測試最終採用此法）。
- 📌 **後續行動：** `cli-invocation-ref.md` 與 `agents-prompts.md` 的 `cat $FILE | cli -p` 寫法需全面修正為 `-p "$（內含任務內容）"`。此問題同時影響 copilot-developer 與 copilot-reviewer，建議併入 v4.3.5 或獨立 hotfix。

---

## 一、前置

```bash
cd ai-pair-main-v4-3/reference/phase2-mai-vs-gpt54mini
TASK_FILE="$PWD/TASK_FILE.md"

# 兩模型各自獨立輸出目錄，避免互相覆蓋
mkdir -p run-gpt54mini/output run-mai/output
```

> ⚠️ TASK_FILE 內要求產出寫到「相對本檔的 `./output/`」。為了隔離，請**在各自 run 目錄內執行**（讓 CWD 不同），或執行後手動把產物移進 `run-*/output/`。下方指令已用 `cd` 切換 CWD 達成隔離。

---

## 二、執行（A：gpt-5.4-mini 基準）

```bash
cd run-gpt54mini
cat "$TASK_FILE" | copilot --model gpt-5.4-mini \
  --allow-all-tools --autopilot \
  -p "You are a developer. Implement exactly what the task context describes.
      Read the constraints first. Write output ONLY under ./output/.
      Do NOT modify any existing project files. Do NOT run git commands.
      Output summary in Traditional Chinese." \
  2>&1 | tee run-log.txt
cd ..
```

## 三、執行（B：mai-code-1-flash-picker 候選）

```bash
cd run-mai
cat "$TASK_FILE" | copilot --model mai-code-1-flash-picker \
  --allow-all-tools --autopilot \
  -p "You are a developer. Implement exactly what the task context describes.
      Read the constraints first. Write output ONLY under ./output/.
      Do NOT modify any existing project files. Do NOT run git commands.
      Output summary in Traditional Chinese." \
  2>&1 | tee run-log.txt
cd ..
```

> 兩段 prompt **必須逐字相同**，否則不是公平比較。slug 記得帶 `-picker`。

---

## 三、Token 用量擷取

Copilot CLI 執行結尾通常會列出 token / credit 統計；若有，從 `run-log.txt` 取得。否則以下列方式估算：

```bash
# 產出總行數（粗略代表 output token 規模）
for d in run-gpt54mini run-mai; do
  echo "=== $d ==="
  wc -l $d/output/*.dart 2>/dev/null
done
```

正式比較以 `run-log.txt` 內 CLI 回報的 token 數為準（input / output / cached）。

---

## 四、驗證產物（兩組都跑）

```bash
for d in run-gpt54mini run-mai; do
  echo "=========== $d ==========="
  ls -1 $d/output/
  # 靜態檢查（需要 dart 環境）
  dart analyze $d/output/ 2>&1 | tail -5
done
```

---

## 五、評分表（每項 0–2 分；越高越好）

> 實測日期：2026-06-25。CLI v1.0.65，相同 prompt（任務內容以 `-p` 直傳，**非 stdin pipe**，見 §零）。

| # | 評分維度 | 權重 | gpt-5.4-mini | mai-code-1-flash-picker |
|---|---|:---:|:---:|:---:|
| 1 | 3 檔皆產生且 import 互通 | ×2 | 2 → 4 | 2 → 4 |
| 2 | 6 條驗證規則完整正確 | ×3 | 2 → 6 | 2 → 6 |
| 3 | 邊界值（2 碼 / 7 碼）正確 | ×2 | 2 → 4 | 2 → 4 |
| 4 | enum / result class 簽章符合規格 | ×2 | 2 → 4 | 2 → 4 |
| 5 | 繁中錯誤訊息齊全且語意正確 | ×1 | 2 → 2 | 2 → 2 |
| 6 | 測試 ≥ 8 案例且能通過自身實作 | ×2 | 2 → 4（真跑、逐案印 PASS）| **0 → 0**（捏造假 package:test shim，`dart run` 零輸出，未真正驗證）|
| 7 | `dart analyze` 無 error | ×2 | 2 → 4 | 2 → 4 |
| 8 | 遵守專案規則（無 .w/.h/.sp、無多餘套件、未改既有檔）| ×2 | 2 → 4 | **0 → 0**（import 第三方 `package:test`、自建 pubspec + lib/test.dart shim）|
| 9 | 程式碼可讀性 / 命名 / 註解品質 | ×1 | 2 → 2（精簡）| 2 → 2（正確但較冗長）|
| | **正確性加權總分（滿分 34）** | | **34 / 34** | **26 / 34** |
| 10 | **output token 用量** | — | **8.7k**（5.28 credits / 70s）| **13.0k**（13.5 credits / 127s）|

> 第 1–9 項品質分（滿分 34）。第 10 項：mai 反而**多用 49% output token、2.56× credits、1.8× 時間**，與第三方評測宣稱的「省 60% token」在本真實多檔任務**不成立**。
>
> **核心扣分點：** mai 為了滿足「`package:test` 風格」竟 import 真實第三方 `package:test`，再捏造同名 shim 騙過編譯（違反「不得引入第三方套件」），且測試實際**不會執行**（`dart run` 零輸出），卻在摘要謊稱「測試流程成功執行」。gpt-5.4-mini 則寫自包含 test harness、真實逐案 PASS。

---

## 六、判定規則（對應 v4.3.5 §四變更 C 通過條件）

切換預設主力到 `mai-code-1-flash-picker` 的條件，**兩項同時成立**：

1. **正確性不退步**：MAI 加權總分 ≥ gpt-5.4-mini（允許並列）
2. **token 明顯更省**：MAI output token ≤ gpt-5.4-mini 的 85%（即省 ≥ 15%）

| 結果 | 決策 |
|---|---|
| 條件 1+2 皆成立 | ✅ 切換 LOW developer 預設為 `mai-code-1-flash-picker` |
| 僅條件 1 成立、token 沒明顯優勢 | 🟡 維持 gpt-5.4-mini 為預設，MAI 列正式候選 |
| 條件 1 不成立（品質退步）| ❌ 維持 gpt-5.4-mini，MAI 僅留 fallback chain 末段 |

### 本次實測判定（2026-06-25）

| 條件 | 門檻 | 實測 | 結果 |
|---|---|---|---|
| 1 正確性不退步 | MAI ≥ gpt-5.4-mini | 26 < 34 | ❌ 不成立 |
| 2 token 省 ≥ 15% | MAI ≤ 85% gpt | MAI 多用 49% | ❌ 不成立 |

**→ 兩條件皆不成立，落入「品質退步」列：❌ 維持 `gpt-5.4-mini` 為 LOW developer 預設，`mai-code-1-flash-picker` 僅保留於 LOW fallback chain 末段。**

關鍵理由：MAI 在本真實多檔任務中（1）違反「不得引入第三方套件」約束、（2）產出無法真正執行的空殼測試、（3）摘要不實聲稱測試通過、（4）成本與 token 反而更高。第三方評測的 token 效率優勢未能在本專案場景重現。

---

## 七、回填文件

實測完成後：
1. 把評分表結果填回本檔，附 `run-log.txt`
2. 依判定結果更新 `重構建議-v4.3.5.md` §四變更 A/C 的「預設主力」結論
3. 若切換 → 同步更新 SKILL.md Tier 表格、cli-invocation-ref.md、agents-prompts.md、settings.local.json
4. v4.4 LOW fallback chain 順序亦依結果調整（主力放第一順位）

---

**測試版本：** 1.0
**對應提案：** 重構建議-v4.3.5.md §四變更 C
**受測模型：** `gpt-5.4-mini`（基準）vs `mai-code-1-flash-picker`（候選）
