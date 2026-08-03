# v5.0 CLI 實測紀錄（E1–E8）

## 目錄

- [E1. agy 模型名稱與無效名稱處理](#e1-agy-模型名稱與無效名稱處理)
  - [E1-a 有效 slug（`gemini-3.5-flash-low`）](#e1-a-有效-sluggemini-35-flash-low)
  - [E1-b 舊「顯示名」格式（`"Gemini 3.1 Pro (High)"`，skill 現行寫法）](#e1-b-舊顯示名格式gemini-31-pro-highskill-現行寫法)
  - [E1-c 真正無效的名稱（`definitely-not-a-model`）](#e1-c-真正無效的名稱definitely-not-a-model)
  - [🔴 E1 結論：agy 接受兩種命名格式](#-e1-結論agy-接受兩種命名格式)
  - [被推翻的三項主張（v5.0 初稿 §1.1）](#被推翻的三項主張v50-初稿-11)
  - [⚠️ 對 §4.2 白名單提案的影響：原設計會引入 bug](#-對-42-白名單提案的影響原設計會引入-bug)
- [E2. copilot 能否自行讀取路徑 ✅ 成立](#e2-copilot-能否自行讀取路徑--成立)
- [E3. copilot 有效模型清單](#e3-copilot-有效模型清單)
  - [E3 補測（依使用者提供的 copilot `/model` 完整清單）](#e3-補測依使用者提供的-copilot-model-完整清單)
  - [🔴 E3 補測的架構含義：copilot 單一 CLI 已涵蓋五個模型家族](#-e3-補測的架構含義copilot-單一-cli-已涵蓋五個模型家族)
  - [E3 原始結論](#e3-原始結論)
- [E4. agy `--json-schema` 是否被遵守 ✅ 成立（但暴露一個關鍵問題）](#e4-agy---json-schema-是否被遵守--成立但暴露一個關鍵問題)
  - [✅ schema 遵守情況：完全符合](#-schema-遵守情況完全符合)
  - [🔴 但 findings 的 `file` 路徑是錯的](#-但-findings-的-file-路徑是錯的)
  - [✅ 延伸驗證：加 `--add-dir` 後路徑正確](#-延伸驗證加---add-dir-後路徑正確)
  - [🔴 E4 的核心結論：捏造路徑是「嵌 payload」的直接後果，不是模型缺陷](#-e4-的核心結論捏造路徑是嵌-payload的直接後果不是模型缺陷)
- [E5. Copilot 計費模式與各模型費率（網路查證，非 CLI 實測）](#e5-copilot-計費模式與各模型費率網路查證非-cli-實測)
  - [🔴 計費模式已變更：multiplier 制廢除](#-計費模式已變更multiplier-制廢除)
  - [各模型費率（USD / 每百萬 token）](#各模型費率usd--每百萬-token)
  - [五項對 v5.0 有直接影響的發現](#五項對-v50-有直接影響的發現)
- [E6. copilot 輸出格式陷阱（v5.0 實作驗證時發現）](#e6-copilot-輸出格式陷阱v50-實作驗證時發現)
  - [🔴 `--output-format json` 是 JSONL 事件串流，不是單一 JSON](#---output-format-json-是-jsonl-事件串流不是單一-json)
  - [⚠️ E6 原結論已修正（見下方 E6-bis）](#-e6-原結論已修正見下方-e6-bis)
  - [原結論：只用 `-s`，不加 `--output-format`](#原結論只用--s不加---output-format)
  - [附帶：v5.0 manifest 協定端到端驗證通過](#附帶v50-manifest-協定端到端驗證通過)
- [E6-bis. `-s` 的 stdout 不保證乾淨（E6 結論修正）](#e6-bis--s-的-stdout-不保證乾淨e6-結論修正)
  - [修正後的規則](#修正後的規則)
- [E7. 🔴 agy headless 需 `--dangerously-skip-permissions`](#e7--agy-headless-需---dangerously-skip-permissions)
  - [🔴 兩個關鍵事實](#-兩個關鍵事實)
  - [修正](#修正)
- [E8. 回歸測試：文件寫的解析配方本身有 bug（零成本測出）](#e8-回歸測試文件寫的解析配方本身有-bug零成本測出)
  - [測試對象（三份真實產物，皆來自 `phase4-v5-first-run/`）](#測試對象三份真實產物皆來自-phase4-v5-first-run)
  - [結果：抓到三個文件層 bug](#結果抓到三個文件層-bug)
  - [修正後的統一配方（三條鐵則）](#修正後的統一配方三條鐵則)
  - [回歸測試結果（`/tmp/v5-parse-test.sh`，以 zsh 執行）](#回歸測試結果tmpv5-parse-testsh以-zsh-執行)
  - [📌 方法論結論](#-方法論結論)
- [附帶實測發現（影響實作寫法）](#附帶實測發現影響實作寫法)
- [對 v5.0 提案的總體影響](#對-v50-提案的總體影響)

---

**執行日期：** 2026-07-30
**環境：** macOS（Darwin 25.5.0）／copilot CLI v1.0.75／agy CLI v1.1.8
**目的：** 驗證 `重構建議-v5.0.md` §7 的假設，作為實作依據與日後回歸基準
**範圍：** E1–E4 實測、E5 費率查證、E6 實作驗證（+E6-bis 修正）、E7 v5.0 首跑發現、E8 修正的回歸測試

> 🔴 **重要：E1 推翻了 v5.0 初稿 §1.1 的核心主張**（agy 模型名稱並未失效）。
> 🔴 **E4 反過來為 §5.1 提供了最強實證**：捏造路徑是「嵌 payload」的後果，改傳路徑即消失。
> 詳見各節結論與文末「對提案的影響」。

---

## E1. agy 模型名稱與無效名稱處理

### E1-a 有效 slug（`gemini-3.5-flash-low`）

```bash
agy --model gemini-3.5-flash-low --output-format json -p "Reply with exactly: SLUG_OK"
```

```json
{"conversation_id":"0251e09f-...","status":"SUCCESS","response":"SLUG_OK\n",
 "duration_seconds":1.805512,"num_turns":1,
 "usage":{"input_tokens":16858,"output_tokens":32,"thinking_tokens":24,
          "cache_read_tokens":0,"total_tokens":16890}}
```

✅ slug 格式可用。
📌 **JSON 無 `model` 欄位**——無法從輸出回推實際使用的模型。

### E1-b 舊「顯示名」格式（`"Gemini 3.1 Pro (High)"`，skill 現行寫法）

```json
{"conversation_id":"d96234c7-...","status":"SUCCESS","response":"OLD_OK\n",
 "duration_seconds":5.223264,"num_turns":1,
 "usage":{"input_tokens":17542,"output_tokens":293,"thinking_tokens":285,
          "cache_read_tokens":0,"total_tokens":17835}}
```

✅ **成功。此格式是有效的模型名稱，不是靜默降級。**

### E1-c 真正無效的名稱（`definitely-not-a-model`）

```json
{"conversation_id":"","status":"ERROR","response":"",
 "error":"invalid model selection (--model \"definitely-not-a-model\" --effort \"\"):
          model definitely-not-a-model is not recognized as a known model or custom model in settings
          Available models:
            Gemini 3.6 Flash (High) / (Medium) / (Low)
            Gemini 3.5 Flash (High) / (Medium) / (Low)
            Gemini 3.1 Pro (High) / (Low)
            Claude Sonnet 4.6 (Thinking)
            Claude Opus 4.6 (Thinking)
            GPT-OSS 120B (Medium)",
 "duration_seconds":0,"num_turns":0,
 "usage":{"input_tokens":0,"output_tokens":0,"total_tokens":0}}
```

✅ **agy 對無效模型明確報錯**：`status: "ERROR"`、附可用清單、**零 token 消耗**（不會空跑燒額度）。

### 🔴 E1 結論：agy 接受兩種命名格式

| 格式 | 範例 | 來源 | 有效 |
|---|---|---|---|
| slug | `gemini-3.1-pro-high` | `agy models` 的輸出 | ✅ |
| 顯示名 | `Gemini 3.1 Pro (High)` | 錯誤訊息的 "Available models" 清單、skill 現行寫法 | ✅ |

**兩種都有效，指向同一組模型。** 對照（slug ⇄ 顯示名）：

```
gemini-3.6-flash-{high,medium,low} ⇄ Gemini 3.6 Flash ({High},{Medium},{Low})
gemini-3.5-flash-{high,medium,low} ⇄ Gemini 3.5 Flash ({High},{Medium},{Low})
gemini-3.1-pro-{high,low}          ⇄ Gemini 3.1 Pro ({High},{Low})
claude-sonnet-4-6                  ⇄ Claude Sonnet 4.6 (Thinking)
claude-opus-4-6-thinking           ⇄ Claude Opus 4.6 (Thinking)
gpt-oss-120b-medium                ⇄ GPT-OSS 120B (Medium)
```

### 被推翻的三項主張（v5.0 初稿 §1.1）

| 初稿主張 | 實測結果 |
|---|---|
| skill 的 `"Gemini 3.1 Pro (High)"` 格式已失效 | ❌ **錯**——有效 |
| agy 對無效模型名靜默降級，`ERR:MODEL` 偵測不可靠 | ❌ **錯**（於 v1.1.8）——明確報錯且零消耗 |
| gemini-reviewer 一直跑在預設模型而非 Pro (High) | ❌ **錯**——無此問題 |

> v4.3（2026-06-22）記載的「靜默降級」Known Limitation 在 agy v1.1.8 **已不成立**。屬**過期的限制描述**，非當時記載錯誤。

### ⚠️ 對 §4.2 白名單提案的影響：原設計會引入 bug

```bash
# 提案原文（❌ 不可實作）
agy models | grep -qx "$MODEL" || exit 1
```

`agy models` 只輸出 **slug**，因此此檢查會把**有效的顯示名全部擋掉**——包含 skill 現行所有 agy 模型設定。這是引入故障，不是修復。

**修正方向**：agy 本身已能可靠驗證，無需自建白名單。改為判讀回傳：

```bash
# ⚠️ 初版寫法，已被 E8 推翻，保留供對照
status=$(agy --model "$MODEL" --output-format json -p "$PROMPT" | jq -r '.status')
[ "$status" = "ERROR" ] && { echo "ERR:MODEL"; }
```

> ⚠️ **上方程式碼為當時的初版，已被 E8 回歸測試推翻**（`status` 撞 zsh 唯讀保留字、agy 失敗輸出不乾淨、輸出穿過變數會壞）。**不可照抄**——正式配方見 E8 的三條鐵則。

若仍要前置驗證，白名單須**同時**接受兩種格式（slug 取自 `agy models`，顯示名取自錯誤訊息的 Available models 清單）。

---

## E2. copilot 能否自行讀取路徑 ✅ 成立

```bash
printf 'The secret token is MAGIC_7X9Q.\n' > aipair-probe.txt
copilot --model gpt-5.4-mini --allow-all-tools --add-dir "$PWD" \
        --max-ai-credits 30 -s --no-custom-instructions \
        -p "Read the file aipair-probe.txt in the current directory and reply with only the token it contains."
```

輸出：`MAGIC_7X9Q`

✅ **§5.1「傳路徑取代嵌 payload」可行。** copilot 能以自身檔案工具讀取指定目錄的檔案。

---

## E3. copilot 有效模型清單

以 `copilot --model X --max-ai-credits 30 -s -p "Reply with exactly: OK"` 逐一探測：

| 模型 | 結果 |
|---|---|
| `gpt-5.4-mini` | ✅ 可用 |
| `gpt-5-mini` | ✅ 可用 |
| `gpt-5.3-codex` | ✅ 可用 |
| `claude-sonnet-4.6` | ✅ 可用 |
| `claude-sonnet-5` | ✅ 可用（`~/.copilot/settings.json` 的**使用者選用值**；系統預設另有其人，見補測） |
| `claude-haiku-4.5` | ✅ 可用 |
| `mai-code-1-flash-picker` | ✅ 可用（但依 §4.5 品質篩選**不採用**） |
| ~~`claude-haiku-4-5`~~ | ❌ 不可用——**此為探測時的拼寫錯誤**，正確拼法見上（`4.5` 非 `4-5`） |

### E3 補測（依使用者提供的 copilot `/model` 完整清單）

初次探測只涵蓋 skill 提及的模型，遺漏了大半catalog。使用者提供互動模式的實際清單後補測：

| 模型（顯示名） | context | slug | 結果 |
|---|---|---|---|
| GPT-5.6 Terra **(系統預設)** | 400K | `gpt-5.6-terra` | ✅ |
| GPT-5.6 Luna | 328K | `gpt-5.6-luna` | ✅ |
| GPT-5.4 | 400K | `gpt-5.4` | ✅ |
| GPT-5.3-Codex | — | `gpt-5.3-codex` | ✅ |
| GPT-5.4 mini | — | `gpt-5.4-mini` | ✅ |
| GPT-5 mini | — | `gpt-5-mini` | ✅ |
| Claude Sonnet 5 **(使用者目前選用 ✓)** | 264K | `claude-sonnet-5` | ✅ |
| Claude Sonnet 4.6 | 264K | `claude-sonnet-4.6` | ✅ |
| Claude Sonnet 4.5 | — | `claude-sonnet-4.5` | ✅ |
| Claude Haiku 4.5 | — | `claude-haiku-4.5` | ✅ |
| Gemini 3.1 Pro (Preview) | 264K | `gemini-3.1-pro-preview` | ✅（`gemini-3.1-pro` ❌） |
| Gemini 3.6 Flash | 264K | `gemini-3.6-flash` | ✅ |
| Gemini 3.5 Flash | 264K | `gemini-3.5-flash` | ✅ |
| Grok 4.5 | 328K | `grok-4.5` | ✅ |
| Kimi K2.7 Code | — | `kimi-k2.7-code` | ✅ |
| MAI-Code-1-Flash | — | `mai-code-1-flash-picker` | ✅（`mai-code-1-flash` ❌，`-picker` 後綴必要） |

📌 **系統預設是 GPT-5.6 Terra**；`~/.copilot/settings.json` 的 `"model": "claude-sonnet-5"` 是**使用者選用值**，兩者不同（先前誤記為「預設是 claude-sonnet-5」）。

### 🔴 E3 補測的架構含義：copilot 單一 CLI 已涵蓋五個模型家族

```
GPT (5.6 Terra/Luna, 5.4, 5.3-Codex, mini) │ Claude (Sonnet 5/4.6/4.5, Haiku 4.5)
Gemini (3.1 Pro Preview, 3.6/3.5 Flash)    │ Grok 4.5 │ Kimi K2.7 Code │ MAI
```

這**削弱了「保留 agy 是為了模型家族多樣性」的理由**——三個 reviewer 全走 copilot、各指定不同家族，同樣能取得異質視角。

**但 agy 仍有兩項不可取代的價值：**

1. **跨供應商分散額度**——三個 reviewer 若全走 copilot，就共用同一個 Credit 池，失去 `重構建議-v5.0.md` §2 明列要保留的優勢
2. **免費額度**——agy 不消耗 Copilot Credits

**結論：保留 agy 的理由從「模型多樣性」改為「成本與額度分散」。** 多樣性現在是 copilot 內部就能滿足的次要理由。

### E3 原始結論

✅ **skill 現行指定的 copilot 模型名稱全部有效**，無過期問題。

📌 **copilot 的命名慣例與 agy 相反**：copilot 用 `claude-haiku-4.5`（點），agy 用 `claude-sonnet-4-6`（連字號）。跨 CLI 套用同一拼法會失敗。

✅ copilot 對無效模型明確報錯：`Error: Model "X" from --model flag is not available.`（與 agy 同樣安全）

---

## E4. agy `--json-schema` 是否被遵守 ✅ 成立（但暴露一個關鍵問題）

```bash
agy --model gemini-3.5-flash-low --output-format json --json-schema findings-schema.json \
    -p "Review this Dart code ... <程式碼直接貼在 prompt 裡>"
```

### ✅ schema 遵守情況：完全符合

回傳新增 **`structured_output`** 欄位，內容嚴格符合 schema（`findings[]` 含 `file`/`line`/`severity`/`issue`/`fix`，加頂層 `verdict`），另附 `json_schema` 欄位回述所用 schema。

findings 品質也正確：抓到 `name!` 的 null assertion 風險（`W`）與字串串接的 style 問題（`S`），verdict `WARN`。

📌 **解析必須取 `structured_output`，不可取 `response`**——`response` 欄位混入了 agent 的敘述（"I will start by checking the current permissions..."），只有 `structured_output` 是乾淨的結構化資料。

📌 `cache_read_tokens: 32534 / total 46884` — **prompt cache 有效運作**，重複呼叫成本可觀地降低。

### 🔴 但 findings 的 `file` 路徑是錯的

回報路徑為 `/Users/alexander/.gemini/antigravity-cli/scratch/probe.dart`。

原因在 `response` 的敘述裡露出來了：**agy 沒有我的 cwd 存取權，於是在自己的 sandbox scratch 目錄「建立」了一份 probe.dart，再回報那個路徑。**

### ✅ 延伸驗證：加 `--add-dir` 後路徑正確

```bash
printf 'The secret token is AGY_TOKEN_4B2.\n' > agy-probe.txt
agy --model gemini-3.5-flash-low --add-dir "$PWD" --output-format json \
    -p "Read the file $PWD/agy-probe.txt and reply with only the token it contains."
→ status: SUCCESS   response: 'AGY_TOKEN_4B2\n'
```

### 🔴 E4 的核心結論：捏造路徑是「嵌 payload」的直接後果，不是模型缺陷

同一個模型：

| 做法 | 結果 |
|---|---|
| 程式碼**貼進 prompt**（現行 ai-pair 做法） | ❌ 在 sandbox 自建檔案，回報**捏造的路徑** |
| 給**路徑** + `--add-dir`（v5.0 §5.1 提案） | ✅ 讀到真實檔案，路徑正確 |

**這是對 §1.2／§5.1 最直接的實證**：把 agentic CLI 當 text pipe 用，會誘發它「為了有東西可指」而自建工作檔——先前歸因於「模型幻覺」的路徑問題，根因其實是傳遞方式。

同時證明 §6.2 的機械攔阻（`file` 不在審查範圍內就整份棄用）**必要且有效**——它正好能攔下這次的 `.gemini/antigravity-cli/scratch/` 路徑。

---

## E5. Copilot 計費模式與各模型費率（網路查證，非 CLI 實測）

### 🔴 計費模式已變更：multiplier 制廢除

**2026-06-01 起 Copilot 改為 usage-based billing**，依供應商 list price 按 token 計費，`1 AI credit = $0.01 USD`。

- 舊的 model multiplier（Claude Opus 27×、Sonnet 9× 等）**僅對 2026-06-01 前既有年約、且留在 legacy request-based billing 的 Pro/Pro+ 用戶適用**
- 計費涵蓋 **input + output + cached tokens**
- **無任何免費模型**

> 這使 skill Tier 表的「Output Credits/M」欄位在概念上仍有效（本來就是按 token），但**數值全部需要更新**，且必須改為引用官方費率而非自行維護。

### 各模型費率（USD / 每百萬 token）

| 模型 | Input | Cached in | Cache write | Output |
|---|---|---|---|---|
| GPT-5.6 Terra（系統預設） | 2.50 | 0.25 | — | 15.00 |
| GPT-5.6 Terra（long context） | 5.00 | 0.50 | — | 22.50 |
| **GPT-5.6 Luna** | **1.00** | 0.10 | — | **6.00** |
| GPT-5.6 Luna（long context） | 2.00 | 0.20 | — | 9.00 |
| GPT-5.4 | 2.50 | 0.25 | — | 15.00 |
| GPT-5.3-Codex | 1.75 | 0.175 | — | 14.00 |
| GPT-5.4 mini | 0.75 | 0.075 | — | 4.50 |
| GPT-5 mini | 0.25 | 0.025 | — | 2.00 |
| **Claude Sonnet 5**（促銷至 2026-08-31） | **2.00** | 0.20 | 2.50 | **10.00** |
| Claude Sonnet 4.6 | 3.00 | 0.30 | 3.75 | 15.00 |
| Claude Sonnet 4.5 | 3.00 | 0.30 | 3.75 | 15.00 |
| Claude Haiku 4.5 | 1.00 | 0.10 | 1.25 | 5.00 |
| Gemini 3.1 Pro | 2.00 | 0.20 | — | 12.00 |
| Gemini 3.6 Flash | 1.50 | 0.15 | — | 7.50 |
| Gemini 3.5 Flash | 1.50 | 0.15 | — | 9.00 |
| Grok 4.5 | 2.00 | 0.50 | — | 6.00 |
| **Kimi K2.7 Code** | **0.95** | 0.19 | — | **4.00** |
| MAI-Code-1-Flash | 0.75 | 0.075 | — | 4.50 |

### 五項對 v5.0 有直接影響的發現

**① skill 現行指定的 `claude-sonnet-4.6` 已被 `claude-sonnet-5` 全面優於**
Sonnet 5 是 $2.00/$10.00，Sonnet 4.6 是 $3.00/$15.00——**更新的模型反而更便宜 33%**。developer 預設應改 Sonnet 5。
⚠️ 但 Sonnet 5 是**促銷價，2026-08-31 到期**，屆時須重新評估。

**② 🔴 Anthropic 模型獨有 cache write 成本，在 ai-pair 的使用模式下是實質劣勢**
只有 Claude 系列有 cache write 費用（Sonnet 5 為 $2.50/M）。而 ai-pair **每個任務都重新啟動 CLI**（cold start），cache write 付了卻難以在後續讀取中攤提——E4 雖觀察到 `cache_read_tokens: 32534`，那是**單一 conversation 內**的效果。
→ 跨任務的冷啟動模式下，GPT／Gemini／Grok／Kimi 在成本上優於 Claude 系列。

**③ GPT-5.6 Luna 與 Kimi K2.7 Code 是成本異常值**
Luna $1.00/$6.00 只有 Terra 的 40% output 成本；Kimi $0.95/$4.00 更低。若品質達標，這兩者是 developer 的強力候選（Kimi 名稱即標示為 code 取向）。
⚠️ 兩者皆**未經 §4.5.5 的 A/B 准入程序**，不得直接設為預設。

**④ MAI-Code-1-Flash 從來沒有成本優勢**
費率與 GPT-5.4 mini **完全相同**（$0.75/$4.50）。而既有 A/B 實測顯示它多用 49% token → 同費率下即**多花 49% 成本**。
→ 「不採用 MAI」的決定不只是品質問題，**成本上也全面劣於 GPT-5.4 mini**。第三方評測宣稱的「省 60% token」在費率層面也無從實現。

**⑤ 🔴 long context 費率約為 2×，為 §5.1 的 manifest 設計提供了成本論證**
Terra 從 $2.50/$15.00 跳到 $5.00/$22.50。**把 diff 全文塞進 prompt 會推高 context 進入 long-context 計費級距；改傳 manifest 路徑則讓 prompt 保持精簡。**
→ §5.1「傳路徑不傳 payload」原本的理由是「查證能力」與「避免傳遞失敗」，現在多一條：**直接的成本理由**。

> 📌 費率會變動（Sonnet 5 促銷即為例）。**skill 不應自行維護費率表**，而應引用官方頁面並標註查證日期。

---

## E6. copilot 輸出格式陷阱（v5.0 實作驗證時發現）

以 v5.0 的 manifest 協定實跑 copilot-reviewer 時發現規格 bug。

### 🔴 `--output-format json` 是 JSONL 事件串流，不是單一 JSON

```bash
copilot --model gpt-5.4-mini ... -s --output-format json -p "... Output ONLY JSON: {...}"
```

stdout 是大量 `assistant.message_delta` 逐字事件，最終答案埋在 `assistant.message` 事件的 `.data.content`：

```
{"type":"assistant.message_delta","data":{"deltaContent":"BLOCK"},...}
{"type":"assistant.message","data":{"content":"{\"findings\":[...],\"verdict\":\"BLOCK\"}"},...}
{"type":"result","exitCode":0,"usage":{...}}
```

→ 直接 `jq '.verdict'` **會失敗**。

### ⚠️ E6 原結論已修正（見下方 E6-bis）

初次驗證時的結論是「只用 `-s` → stdout 直接是乾淨 JSON」。**該結論只在單輪短任務成立**，v5.0 首跑（E7 同一輪）證明多步驟工具呼叫時不成立。修正見 E6-bis。

### 原結論：只用 `-s`，不加 `--output-format`

```bash
copilot --model gpt-5.4-mini --allow-all-tools --add-dir /tmp --add-dir "$PWD" \
  --max-ai-credits 30 -s --effort low -p "... Output ONLY JSON: {...}"
```

stdout 直接是乾淨 JSON，`jq -e '.verdict'` 通過：

```json
{"findings":[{"file":"run-luna/output/plate_validator_test.dart","line":1,"severity":"S",
"issue":"測試檔直接依賴 `package:test/test.dart`，這是第三方套件，違反 D2…","fix":"…"}],
"verdict":"BLOCK"}
```

若確實需要 token/usage 統計，才加 `--output-format json`，並用：

```bash
jq -r 'select(.type=="assistant.message") | .data.content'
```

**agy 不受此影響**——`--output-format json` 回單一 JSON 物件，取 `.structured_output` 即可。

### 附帶：v5.0 manifest 協定端到端驗證通過

同一次測試也驗證了 v5.0 的核心設計：

| 驗證項 | 結果 |
|---|---|
| copilot 依 manifest **路徑**自行讀取 | ✅ 正確讀到 manifest 與 scope 內三個檔案 |
| reviewer 讀原始碼做查證 | ✅ 找到 `plate_validator_test.dart:1` 的 `package:test` import |
| findings 路徑在審查範圍內 | ✅ 回報 `run-luna/output/plate_validator_test.dart`，無捏造路徑 |
| 依 manifest 的裁決清單判定 | ✅ 正確引用 D2 並回 `BLOCK` |

---

## E6-bis. `-s` 的 stdout 不保證乾淨（E6 結論修正）

**發現時機：** v5.0 首跑，以 manifest 協定派 copilot-reviewer 審 SSGS-12853（40 檔、`--allow-all-tools` 多步驟工具呼叫）。

stdout 前段是大量過程敘述：

```
我先讀 manifest 和變更範圍，接著只針對指定內容做審查。
我在核對 enum/DTO wire contract；接著比對後端原始碼與產生的序列化結果。
...（約 15 行）
{"findings":[{"file":"lib/page/setting/report_auto_send_page.dart","line":157,...}],"verdict":"WARN"}
```

`jq` 直接讀 → `parse error: Invalid numeric literal at line 1, column 10`。

### 修正後的規則

| 情境 | stdout |
|---|---|
| 單輪短任務（如 E2/E3 的 `Reply with exactly: OK`） | 純結果，可直接 `jq` |
| 🔴 多步驟工具呼叫（`--allow-all-tools` + 讀多檔） | **混有過程敘述**，JSON 在**尾端** |

**一律抽取，不可假設乾淨：**

```bash
raw=$(copilot ... --allow-all-tools -s -p "...")
json=$(printf '%s' "$raw" | grep -o '{"findings".*}' | tail -1)
```

> 📌 教訓與 §1.1 同型：**單一情境驗證出的結論，不可外推成通則。** E6 在短任務上驗證通過就寫成規格，遇到真實負載即失效。

---

## E7. 🔴 agy headless 需 `--dangerously-skip-permissions`

**發現時機：** v5.0 首跑，派 gemini-reviewer 做 spec compliance review。

依 v5.0 原協定（`--add-dir` + `--output-format json` + `--json-schema`）執行，結果：

```
jetski: no output produced — a tool required the "command" permission that
headless mode cannot prompt for, so it was auto-denied. Add an allow-rule under
permissions.allow in settings.json (e.g. command(<target>)). Alternatively,
re-run with --dangerously-skip-permissions to auto-approve all tools.

{"conversation_id":"...","status":"SUCCESS","response":"","duration_seconds":19.9,
 "num_turns":1,"json_schema":{...}}
```

### 🔴 兩個關鍵事實

1. **`--add-dir` 只授予檔案讀取權**，不含 shell 工具（grep／glob）的 `command` 權限。headless 無法提示 → **自動拒絕**。
2. **失敗時仍回 `status:"SUCCESS"`**，只是 `response` 為空且**無 `structured_output`**。→ **只判 `status` 會把空跑誤判為「review 通過」**。

### 修正

```bash
agy --model "$M" --dangerously-skip-permissions \
  --add-dir "$PROJECT_DIR" --add-dir "$BACKEND_REPO" \
  --output-format json --json-schema "$SCHEMA" --effort high -p "..."
```

並在判定端補上空手偵測：

```bash
if [ "$status" = "SUCCESS" ] && [ "$(echo "$result" | jq -r '.structured_output // empty')" = "" ]; then
  echo "ERR:MODEL|agy returned SUCCESS with no output — check --dangerously-skip-permissions"
fi
```

加旗標後重跑成功：`status=SUCCESS`、134s、`in=356356 cached=3558852 out=18929`、`verdict=PASS`。

> 📌 這是**假成功**（false PASS）類型的故障，比明確失敗危險——與 §1.1 初稿誤判的「靜默降級」同一族。差別在這次是真的，且已實測確認。
> 原始證據留存於 `phase4-v5-first-run/gemini-reviewer.attempt1-permission-denied.json`。

---

## E8. 回歸測試：文件寫的解析配方本身有 bug（零成本測出）

**動機：** E6-bis／E7 修正後，被問「要不要再測一次」。判斷是**不需重跑整輪**——兩個修正動的是 CLI 呼叫管線而非 review 邏輯，而**兩次失敗的原始輸出都已留存**，可直接對它們跑「文件裡寫的那條指令」。

> 📌 這一步的價值在於一個尷尬的事實：**E6-bis 的修正我文件裡寫的是 `grep -o ... | tail -1`，但當時實際用的是 python 正則——文件裡那條指令從沒跑過。**

### 測試對象（三份真實產物，皆來自 `phase4-v5-first-run/`）

| 產物 | 特徵 |
|---|---|
| `copilot-reviewer.json` | 15 行過程敘述 + 尾端 JSON |
| `gemini-reviewer.raw.json` | 成功：單行乾淨 JSON |
| `gemini-reviewer.attempt1-permission-denied.json` | 失敗：診斷文字 + JSON 共 2 行 |

### 結果：抓到三個文件層 bug

| # | Bug | 症狀 |
|---|---|---|
| 1 | 🔴 **`status=$(...)` 在 zsh 直接失敗** | `(eval):14: read-only variable: status`——zsh 的 `$status` 是 `$?` 的唯讀別名。**使用者環境正是 zsh**，文件那段程式碼在他機器上跑不起來 |
| 2 | 🔴 **agy 失敗時 stdout 也不是乾淨 JSON** | 前面多一行 `jetski: no output produced — a tool required the "command" permission...`，`jq` 報 `Invalid numeric literal at line 1, column 7`。E7 的偵測邏輯假設 `$result` 可直接 parse → **偵測不到它本要偵測的東西** |
| 3 | 🔴 **輸出穿過 shell 變數會壞掉** | `result=$(cat f)` 後 `echo "$result" \| jq` 報 `control characters from U+0000 through U+001F must be escaped`；直接 `jq file` 則正常 |

> Bug 2 特別諷刺：**E7 是為了偵測「假成功」而寫的，但它自己在真實的假成功輸入上解析失敗。** 若不做這次回歸測試，v5.0 會帶著一個「偵測不到目標」的偵測器上線。

### 修正後的統一配方（三條鐵則）

```
① 一律先落檔，不讓 CLI 輸出穿過 shell 變數
② 一律抽取 JSON 物件行——兩個 CLI 的 stdout 都可能夾雜非 JSON 文字
③ ❌ 不可用變數名 status（zsh 唯讀保留字）
```

### 回歸測試結果（`/tmp/v5-parse-test.sh`，以 zsh 執行）

```
R2a agy 權限被拒 : ERR:MODEL|SUCCESS with no structured_output — check --dangerously-skip-permissions
R2b agy 正常     : OK|verdict=PASS|findings=0
R1  copilot 混合 : OK|verdict=WARN|findings=1
```

三項全過：失敗被正確判為 `ERR:MODEL`、成功不被誤判（無 false positive）、混合輸出能取出 findings。

### 📌 方法論結論

**「留存失敗產物」讓修正可以零成本回歸測試。** 本次三個 bug 全部在不花任何 Credit、不呼叫任何模型的情況下測出——因為 `phase4-v5-first-run/` 保留了原始輸出。

這條應寫進協定：**reviewer 的原始輸出一律落檔留存，包含失敗的那次。** 它同時是稽核證據與回歸測試資料。

---

## 附帶實測發現（影響實作寫法）

| # | 發現 | 影響 |
|---|---|---|
| 1 | `--max-ai-credits` **最小值為 30**（傳 1 會被拒） | 成本上限無法設得比 30 credits 更低 |
| 2 | 🔴 `agy models > file` **會 hang**；`agy models \| ...` 正常 | 任何取用 `agy models` 之處**必須用管線**，不可重導向到檔案 |
| 3 | macOS 無 `timeout` 指令 | 探測腳本不可用 `timeout`；需 `gtimeout`（coreutils）或改用其他機制 |
| 4 | agy `-p` 單次呼叫約需數秒至數十秒；`--print-timeout` 預設 5m | 批次探測需預留時間 |

---

## 對 v5.0 提案的總體影響

| 提案項 | 狀態 |
|---|---|
| §1.1 模型名稱格式全錯 | 🔴 **推翻，須改寫** |
| §4.2 白名單硬失敗 | 🔴 **原設計會引入 bug，須改為判讀 `status`** |
| §1.4 agy/copilot 新能力可用 | ✅ 成立（`--output-format json`、`--add-dir`、`--max-ai-credits` 皆實測可用） |
| §5.1 傳 manifest 路徑 | ✅ **成立**（E2 驗證） |
| §4.1 執行期發現取代硬編碼 | ⚠️ **理由減弱**——現行模型名稱並未過期，此項從「修 bug」降為「降低維護負擔」的預防性改善 |
| §4.5 developer 模型篩選 | ✅ 不受影響（品質判定與名稱有效性無關）；候選池大幅擴充（見 E3 補測） |
| §6.1 `--json-schema` 結構化輸出 | ✅ **成立**（E4；解析須取 `structured_output` 非 `response`） |
| §6.2 幻覺路徑機械攔阻 | ✅ **必要且有效**（E4 實際產生了 sandbox 捏造路徑，此機制可攔下） |
| §3.2 保留 agy 的理由 | ⚠️ **須改寫**——copilot 已涵蓋五個模型家族，agy 的價值從「模型多樣性」改為「成本與額度分散」 |
| §3 架構決策（copilot-first／explorer／reviewer 保留） | ✅ 不受影響（依據是資源稀缺性，與本次實測無關） |

---

*2026-07-30 | E1–E4 實測 + E5 費率查證 + E6 輸出格式（E6-bis 修正其外推錯誤）+ E7 agy headless 權限（v5.0 首跑發現）+ E8 回歸測試（測出文件配方三個 bug，零成本）*

*待補：各模型的 Copilot Credit 費率（skill 現行 Tier 表為 2026-06 資料，未含 GPT-5.6 Terra/Luna、Grok 4.5、Kimi K2.7 Code），影響 §4.5.2「同 tier 內按成本排序」的實作*
