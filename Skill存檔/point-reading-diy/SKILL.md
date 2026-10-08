---
name: point-reading-diy
description: |
  把整段錄音切成一句一檔，對應到卡米點讀筆的「內容貼」碼號，最後打包成 DAB 點讀包。
  流程：靜音切檔 → Whisper 語音辨識 → 人工審核網頁 → 依單字表或順序對應碼號 → dab_tool 打包。
  也支援用 Mac `say` 從單字清單直接合成音檔。

  Trigger: 點讀筆, 卡米, 內容貼, 書名貼, 點讀包, DAB, 切音檔, 一句一檔, DIY 點讀, point reading
metadata:
  version: 0.1.0
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
| `dab_tool.py` | 打包 DAB | 從 AP4 → DAB 專案複製到 `scripts/`（見步驟 ⑤） |

開始前先檢查：`which ffmpeg`、`python3 -c "import mlx_whisper"`、`ls scripts/dab_tool.py`。
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
- **有背景音樂的錄音切不開**，直接告訴使用者，建議改成自己錄或手動指定切點
- 個別片段要手動修：用 ffmpeg 直接切 `work/seg_XXX.mp3`，並同步改 `segments.json`（index 重新連號、file 對應）

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
- 單字表也可自帶碼號：每行 `461<Tab>apple`
- 比對採「依序對齊」，能容忍少一段（念漏）或多一段（雜音），不會整串錯位
- 分數 < 0.6 會標 ⚠，要逐一確認；國語同音字、單一個字特別容易低分或錯配
- 結果存在 `work/assignment.json`，可直接修改後 `--apply` 重新輸出
- **有沒對到的片段或碼號時，先問使用者再繼續**，不要自行猜測補上

### ⑤ 打包 DAB — `dab_tool.py`

> `dab_tool.py` 沿用 AP4 → DAB 專案已實測的版本，**本資料夾尚未放入**。
> 若 `scripts/dab_tool.py` 不存在，請使用者提供該檔案；**不要自行撰寫 DAB 格式**。

拿到後先讀 `dab_tool.py` 的說明／參數，再以 `work/out/` 為輸入打包。檔名前綴依〈卡米規則〉。

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
| `transcribe.py` | ② | `segments.json` → 填入 `text` |
| `review.py` | ③ | `segments.json` → `review.html`；使用者匯出 `review.json` |
| `assign.py` | ④ | `segments.json` + `review.json` (+ 單字表) → `out/<碼號>.mp3` + `assignment.json` |
| `synth.py` | 合成 | 單字表 → `out/<碼號>.mp3` |
| `dab_tool.py` | ⑤ | `out/` → `.dab`（待放入） |
| `_common.py` | — | 共用函式 |
