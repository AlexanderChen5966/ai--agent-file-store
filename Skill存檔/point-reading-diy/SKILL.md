---
name: point-reading-diy
description: |
  把整段錄音切成一句一檔，對應到卡米點讀筆的「內容貼」碼號，最後打包成 DAB 點讀包。
  流程：靜音切檔 → Whisper 語音辨識 → 人工審核網頁 → 依單字表或順序對應碼號 → dab_tool 打包。
  也支援用 Mac `say` 從單字清單直接合成音檔。

  Trigger: 點讀筆, 卡米, 內容貼, 書名貼, 點讀包, DAB, 切音檔, 一句一檔, DIY 點讀, point reading
metadata:
  version: 0.3.2
---

# point-reading-diy

協助使用者把沒有點讀碼的一般書，用「書名貼 + 內容貼」做成卡米點讀筆可用的點讀書。
本 Skill 負責最花時間的部分：**把錄音切成一段段、對到內容貼號碼、打包成 DAB**。

設計背景與決策見 `規劃文件.md`。

---

## 前置需求

| 工具 | 用途 | 安裝 |
|---|---|---|
| ffmpeg / ffprobe | 切檔、轉檔、波形 | `brew install ffmpeg` |
| mlx-whisper **或** whisper.cpp | 語音辨識（擇一） | `pip install mlx-whisper`／`brew install whisper-cpp` + 下載 ggml 模型 |
| OpenCC（選用） | 國語辨識結果轉台灣繁體 | `pip install opencc` |
| `dab_tool.py` + 範本 DAB | 打包 DAB | `dab_tool.py` 已在 `scripts/`；範本 DAB 由使用者提供（見步驟 ⑤） |

Homebrew 的 Python 不允許直接 `pip install`，請用專用 venv（本機已建立）：

```bash
python3 -m venv ~/.venvs/point-reading-diy
~/.venvs/point-reading-diy/bin/pip install mlx-whisper opencc
```

之後**所有腳本都用 `~/.venvs/point-reading-diy/bin/python` 執行**（以下範例寫 `python3` 時請自行替換）。

開始前先檢查：`which ffmpeg`、`~/.venvs/point-reading-diy/bin/python -c "import mlx_whisper"`、`ls scripts/dab_tool.py`。
缺什麼先告訴使用者，不要默默略過步驟。

---

## 開始前要向使用者確認

1. **音檔來源**：現成音檔／自己錄的一整段／只有單字清單（→ 走「語音合成」）
2. **內容貼碼號**：要用哪幾張（如 461–480）。碼號必須是「實際碼號」，見下方〈卡米規則〉
3. **有沒有單字表**：有 → 用比對模式；沒有或語言辨識弱（台語、客語、注音、兒歌）→ 照順序模式
4. **錄音順序是否與貼紙順序一致**：照順序模式的前提
5. **書名貼種類**：決定 DAB 檔名前綴

---

## 流程

所有腳本都在 `scripts/`，以「工作資料夾」串接（以下用 `work/` 表示）。
每一步的中間結果都存在 `work/segments.json`，可隨時中斷再接續。

### ① 切檔 — `split.py`

```bash
python3 scripts/split.py 錄音.mp3 --out work/ --expect 20 --dry-run   # 先試切，只看段數
python3 scripts/split.py 錄音.mp3 --out work/ --expect 20             # 參數 OK 後正式切
```

**調參原則**（每份錄音都不同，一定要試切）：

| 現象 | 調整 |
|---|---|
| 段數比預期**少**、出現「可能黏在一起」 | `--noise` 調高（-35 → -30 → -25），或 `--min-silence` 調低（0.5 → 0.3） |
| 段數比預期**多**、很多極短片段 | `--noise` 調低（-35 → -40 → -45），或 `--min-silence` 調高、`--min-segment` 調高 |
| 句子內部停頓也被切開（如長句、慢速朗讀） | `--min-silence` 調高（0.8～1.2） |
| 字頭字尾被切掉 | `--pad` 調高（0.15 → 0.25） |

- 用 `--dry-run` 反覆試，通常 2～4 次可收斂；**不要一次改兩個參數**，否則看不出是哪個有效
- 段數剛好相符不代表切點都對（可能一處黏住、另一處多切）——長度分布也要看
- **有背景音樂的錄音切不開** → 改用下方 ①' `split_asr.py`
- 判斷方式：各種門檻試切都只切出 1～3 段，或 `ffmpeg -af volumedetect` 看到整段最低音量都在 -30～-45 dB（沒有真正的靜音）
- 個別片段要手動修：用 ffmpeg 直接切 `work/seg_XXX.mp3`，並同步改 `segments.json`（index 重新連號、file 對應）

### ①' 依辨識時間點切檔 — `split_asr.py`（有背景音樂時）

用 Whisper 逐字時間點找切點，不依賴靜音。也適合「一頁一張貼」這種要把好幾句合成一段的情況。

```bash
python3 scripts/split_asr.py 錄音.mp3 --out work/ --lang en                    # 辨識並列出編號句子
python3 scripts/split_asr.py 錄音.mp3 --out work/ --groups "1,2-5,6-8,9-11"   # 依分組切
```

- 第一次執行會辨識並快取到 `work/transcript.json`，改分組重切不必重新辨識
- `--groups`：每個逗號一段，`2-5` 表示第 2～5 句合成一段；**沒列到的句子會被捨棄**（片頭片尾、YouTube 訂閱宣傳等）
- 分組由 agent 依內容判斷後**先向使用者說明**：重複句型（如 "So they sent me a… X! He was too Y."）是很好的分段線索
- **翻翻書（lift-the-flap）要把「翻開前的懸念句」和「翻開後的揭曉」分成兩段**：
  例如 "So they sent me a…" 一張貼、"Giraffe! He was too tall…" 一張貼，因為兩句印在翻蓋的不同側。
  不確定版面時，預設一句一段比一頁一段好——拆過頭只要重新分組，不必重新辨識
- 兩句之間的切點取**音量最低處**（不是時間中點）：Whisper 常把拖長的 "a…" 和後面的停頓整段算進同一個字，
  下一句的開始時間也跟著不準。句間的音效（翻開、動物叫聲）會完整留在其中一段
- 頭尾會加淡入淡出（`--fade`），避免背景音樂突然出現；字頭字尾被吃掉時調大 `--pre`／`--post`
- 輸出的 `segments.json` 已帶文字，**可跳過步驟 ②**
- 驗證：把每段再辨識一次，比對開頭結尾是否完整
- Whisper 在音檔結尾常產生幻覺句（重複的 "Bye."、"Oop!"），不要放進分組

### ② 語音辨識 — `transcribe.py`

```bash
python3 scripts/transcribe.py work/ --lang en
python3 scripts/transcribe.py work/ --lang zh --backend cpp --model ~/models/ggml-large-v3-turbo.bin
```

- **一定要指定 `--lang`**，短片段自動偵測語言很容易錯
- 只想重跑某幾段：`--only 3,7,12`
- 照順序模式下這步可省略，但建議仍跑一次，審核時有文字可以對照
- 空白結果通常代表雜音或片段太短，審核時特別留意

### ③ 人工審核 — `review.py`（不可省略）

```bash
python3 scripts/review.py work/ --title "Max & Mousy 第 1 冊"
open work/review.html
```

審核網頁功能：波形、播放、連續播放、修改辨識文字、標記 OK／問題／刪除、快捷鍵（空白、↑↓、1/2/3）。
審核進度會暫存在瀏覽器。

請使用者審核完按「**匯出審核結果**」，把下載的 `review.json` **移到 `work/`**。
拿到 review.json 後：

- **刪除**：assign 自動跳過
- **問題**：讀備註判斷——黏在一起 → 手動切開或整體重切；切到字 → 加大 `--pad` 重切；念錯 → 請使用者重錄該句
- 處理完重新產生審核頁讓使用者確認修過的段落
- **重切前先把上一版保存起來**（`seg_*.mp3`、`segments.json`、`review.html`、`review.json` 移到 `work/v1_<說明>/`），
  重切會刪掉舊的 `seg_*.mp3`。保存後舊的審核頁在新資料夾裡仍可播放
- review.json 帶有切檔版本識別碼（`build`）：重切後舊的 review.json 會被 `assign.py` 拒絕，必須用新審核頁重新審核。
  沒有 `build` 的 review.json（舊版審核頁匯出）只會警告，此時要自行核對文字欄位是否對得上目前片段
- `split_asr.py` 重切只要改 `--groups`；使用者的備註（「A 和 B 再切成兩句」）直接對照 `transcript.json` 的句子編號換算

**切點準不準、念的對不對，最後一定要有人聽過。不要因為辨識文字看起來都對就跳過審核。**

### ④ 對應內容貼 — `assign.py`

```bash
# 照順序：第 1 段 → 461、第 2 段 → 462……
python3 scripts/assign.py work/ --codes 461-480 --dry-run

# 單字表比對（words.txt 每行一個詞，順序與碼號對應）
python3 scripts/assign.py work/ --wordlist words.txt --codes 461-480 --dry-run

# 確認後去掉 --dry-run 正式輸出到 work/out/<碼號>.mp3
```

- 碼號格式：`461-480`、`461-470,480-489`
- 檔名要補零（如 `0001.mp3`）時加 `--width 4`
- 單字表也可自帶碼號：每行 `461<Tab>apple`
- 比對採「依序對齊」，能容忍少一段（念漏）或多一段（雜音），不會整串錯位
- 分數 < 0.6 會標 ⚠，要逐一確認；國語同音字、單一個字特別容易低分或錯配
- 結果存在 `work/assignment.json`，可直接修改後 `--apply` 重新輸出
- **有沒對到的片段或碼號時，先問使用者再繼續**，不要自行猜測補上

### ⑤ 打包 DAB — `dab_tool.py`

> `dab_tool.py` 沿用 AP4 → DAB 專案逆向並實測的版本，**不要修改它的格式邏輯**，也不要自行撰寫 DAB 格式。

`dab_tool.py` 目前只有 `extract`／`roundtrip`／`swaptest` 指令，**沒有「從 MP3 打包」的 CLI**，要用它的 `write_dab()`：

- `write_dab(path, book)` 的 `book` 需要 `header`（現成 DAB 的前 0x400 bytes，含不透明區）→ **必須有一個範本 DAB**，用 `read_dab()` 取得
- `book["clips"] = {碼號: {"mp3": bytes}}`，碼號是**實際 OID**（報碼念出的數字），不是印刷號碼
- `book["intro"]` 選用：選書時播放的介紹音檔
- `start` 不給時取最小碼號；中間沒用到的碼號會自動填空格
- 書名（0x0000 起的 GBK 字串）不會被 `write_dab` 改寫，沿用範本的

打包前確認：範本 DAB 路徑、內容貼實際碼號、書名貼對應的檔名前綴（見〈卡米規則〉）。三者任一未確認就停下來問使用者。
打包流程尚未包裝成腳本，第一次實作時請寫成 `scripts/pack.py` 並更新本節。

---

## 語音合成（無錄音時）— `synth.py`

適合單字卡、簡單句子，跳過 ①②③ 的切檔與辨識，直接產生 `<碼號>.mp3`：

```bash
python3 scripts/synth.py --list-voices zh                                    # 查語音
python3 scripts/synth.py words.txt --codes 461-480 --voice Meijia --out work/out/
python3 scripts/synth.py words.txt --codes 461-480 --voice Samantha --rate 140 --out work/out/
```

常用語音：Meijia（國語・台灣）、Samantha（英文）、Sinji（粵語）、Kyoko（日文）。台語無內建語音。
合成結果仍建議讓使用者試聽幾個（多音字、專有名詞容易念錯）。

---

## 卡米規則（AP4 → DAB 專案實測）

- 先點書名貼（入口碼）選書，再點內容貼；未選書直接點內容會說「不對應的文件」
- 入口碼 60001–65000：檔名前綴取末四碼（60309 → `0309-…dab`）
- 智能書名貼 001 → 檔名前綴 `001-`（已實測）
- 普通書名貼用 `001-` 前綴**沒有反應**，命名規則**尚未確認**
- 內容貼「印刷號碼 → 實際碼號」換算**尚未確認**
- DAB 支援任意碼號（上限 65535）

**未確認的規則不要用猜的。** 使用者要用普通書名貼或不確定內容貼碼號時，請他用筆的報碼功能點一下貼紙，
記下印刷號碼與念出的數字（內容貼請點兩張號碼相差較遠的），再依結果決定前綴與碼號。
確認後更新本節與 `規劃文件.md` 第 8 節。

---

## 語言與內容注意事項

| 情況 | 建議 |
|---|---|
| 英文、國語、日文 | 單字表比對可用 |
| 台語、客語 | 辨識弱 → 照順序模式，辨識結果只當參考 |
| 注音、自然發音 | 太短辨不出 → 照順序模式；切檔時 `--min-segment` 調低（0.1） |
| 中英混念 | `--lang` 選主要語言，低分段落人工確認 |
| 兒歌、唱的內容 | 靜音少，常切不開 → 考慮整首對一張貼，或手動指定切點 |

---

## 腳本一覽

| 腳本 | 步驟 | 輸入 → 輸出 |
|---|---|---|
| `split.py` | ① | 原始音檔 → `seg_XXX.mp3` + `segments.json` |
| `split_asr.py` | ①' | 原始音檔 → `transcript.json`；加 `--groups` 後 → `seg_XXX.mp3` + `segments.json`（含文字） |
| `transcribe.py` | ② | `segments.json` → 填入 `text` |
| `review.py` | ③ | `segments.json` → `review.html`；使用者匯出 `review.json` |
| `assign.py` | ④ | `segments.json` + `review.json` (+ 單字表) → `out/<碼號>.mp3` + `assignment.json` |
| `synth.py` | 合成 | 單字表 → `out/<碼號>.mp3` |
| `dab_tool.py` | ⑤ | DAB 讀寫函式庫（`read_dab`／`write_dab`），打包需搭配範本 DAB |
| `_common.py` | — | 共用函式 |
