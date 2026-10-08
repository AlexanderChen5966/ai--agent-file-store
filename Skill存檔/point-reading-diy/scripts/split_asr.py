#!/usr/bin/env python3
"""①' 依語音辨識的時間點切檔（取代 split.py，用於有背景音樂、找不到靜音的錄音）。

第一次執行會用 mlx-whisper 辨識整段錄音（含逐字時間點），結果快取在 <work>/transcript.json，
並列出編號句子清單。再用 --groups 指定「哪幾句合成一段」，未列入的句子（片頭、片尾宣傳）會被丟掉。
輸出與 split.py 相同：seg_XXX.mp3 + segments.json（已帶 text，可跳過 transcribe.py）。

用法：
  python3 split_asr.py 錄音.mp3 --out work/ --lang en              # 辨識並列出句子
  python3 split_asr.py 錄音.mp3 --out work/ --groups "1,2-5,6-8"   # 一段 = 一組句子
  python3 split_asr.py 錄音.mp3 --out work/ --groups all           # 一句一段
"""
import argparse
import array
import math
from pathlib import Path

from _common import (die, load_json, probe_duration, require, run, save_json,
                     save_segments, to_traditional)

DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
TRANSCRIPT_JSON = "transcript.json"
FRAME = 0.05  # 音量分析的時間解析度（秒）


def transcribe(src, lang, model):
    try:
        import mlx_whisper
    except ImportError:
        die("需要 mlx-whisper：pip install mlx-whisper（Homebrew Python 請在 venv 中安裝）")
    res = mlx_whisper.transcribe(str(src), path_or_hf_repo=model, language=lang,
                                 word_timestamps=True)
    sentences = []
    for s in res["segments"]:
        words = [w for w in s.get("words", []) if w["end"] > w["start"]]
        text = " ".join(s["text"].split())
        if not words or not text:
            continue  # Whisper 在音檔尾端常產生空白或零長度的幻覺句
        # 與上一句文字相同且緊接著 → 視為幻覺重複，併入上一句
        if sentences and text == sentences[-1]["text"] and words[0]["start"] - sentences[-1]["end"] < 0.5:
            sentences[-1]["end"] = round(words[-1]["end"], 3)
            continue
        if lang in (None, "zh"):
            text = to_traditional(text)
        sentences.append({"start": round(words[0]["start"], 3),
                          "end": round(words[-1]["end"], 3),
                          "last_word_start": round(words[-1]["start"], 3), "text": text})
    for i, s in enumerate(sentences, 1):
        s["n"] = i
    return sentences


def loudness(src):
    """整段音檔每 FRAME 秒的音量（dB），前後各平滑一格，避免挑到單一瞬間的低點。"""
    rate = 8000
    raw = run(["ffmpeg", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(rate),
               "-f", "s16le", "-"], text=False).stdout
    pcm = array.array("h", raw[: len(raw) // 2 * 2])
    w = int(rate * FRAME)
    db = []
    for i in range(0, len(pcm) - w + 1, w):
        rms = math.sqrt(sum(x * x for x in pcm[i:i + w]) / w)
        db.append(20 * math.log10(max(rms, 1) / 32768))
    return [sum(db[max(0, i - 1):i + 2]) / len(db[max(0, i - 1):i + 2]) for i in range(len(db))]


def quietest(db, t0, t1):
    """t0–t1 之間音量最低的時間點。"""
    i0, i1 = int(t0 / FRAME), max(int(t0 / FRAME) + 1, int(t1 / FRAME))
    i = min(range(i0, min(i1, len(db))), key=db.__getitem__, default=i0)
    return (i + 0.5) * FRAME


def boundary(db, prev, nxt):
    """兩句之間的切點。

    Whisper 常把句尾的拖長音或停頓（"a..."）整段算進最後一個字，下一個字的開始時間也因此不準，
    所以不用時間中點，而是從上一句最後一個字開始後、到下一句開頭稍後，找音量最低處下刀。
    句間的音效（翻開、動物叫聲）也會因此完整留在其中一段，不會被切成兩半。
    """
    lws = prev.get("last_word_start", prev["end"] - 0.5)
    t0 = max(prev["start"], lws + 0.25)
    t1 = min(nxt["start"] + 0.4, nxt["end"] - 0.1)
    if t1 <= t0:
        return (prev["end"] + nxt["start"]) / 2
    return quietest(db, t0, t1)


def parse_groups(spec, count):
    if spec == "all":
        return [[i] for i in range(1, count + 1)]
    groups = []
    for part in spec.replace(" ", "").split(","):
        if "-" in part:
            a, b = map(int, part.split("-", 1))
            groups.append(list(range(a, b + 1)))
        else:
            groups.append([int(part)])
    flat = [n for g in groups for n in g]
    if any(not 1 <= n <= count for n in flat):
        die(f"--groups 有超出範圍的句子編號（共 {count} 句）")
    if flat != sorted(flat) or len(set(flat)) != len(flat):
        die("--groups 需依序且不可重複")
    return groups


def main():
    ap = argparse.ArgumentParser(description="依語音辨識時間點切檔")
    ap.add_argument("input", help="原始音檔")
    ap.add_argument("--out", required=True, help="工作資料夾")
    ap.add_argument("--lang", help="語言代碼：en、zh、ja……")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="mlx-whisper 模型")
    ap.add_argument("--groups", help="句子分組，如 1,2-5,6-8；all＝一句一段；不給則只列出句子")
    ap.add_argument("--pre", type=float, default=0.3, help="每段開頭提前秒數（預設 0.3）")
    ap.add_argument("--post", type=float, default=0.6, help="每段結尾延後秒數（預設 0.6）")
    ap.add_argument("--fade", type=float, default=0.15, help="頭尾淡入淡出秒數，避免背景音樂突然出現（預設 0.15）")
    ap.add_argument("--retranscribe", action="store_true", help="忽略快取，重新辨識")
    a = ap.parse_args()

    require("ffmpeg")
    src = Path(a.input).resolve()
    if not src.exists():
        die(f"找不到音檔：{src}")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cache = out / TRANSCRIPT_JSON

    if cache.exists() and not a.retranscribe and load_json(cache).get("source") == str(src):
        sentences = load_json(cache)["sentences"]
    else:
        print("辨識中（第一次使用會下載模型）……")
        sentences = transcribe(src, a.lang, a.model)
        save_json(cache, {"source": str(src), "lang": a.lang, "model": a.model,
                          "sentences": sentences})

    if not a.groups:
        for s in sentences:
            print(f"{s['n']:>3}  {s['start']:7.2f}–{s['end']:7.2f}  {s['text']}")
        print(f"\n共 {len(sentences)} 句。用 --groups 指定分段後再執行一次。")
        return

    total = probe_duration(src)
    by_n = {s["n"]: s for s in sentences}
    groups = parse_groups(a.groups, len(sentences))
    db = loudness(src)
    segments = []
    for i, g in enumerate(groups, 1):
        first, last = by_n[g[0]], by_n[g[-1]]
        prev = by_n.get(g[0] - 1)
        nxt = by_n.get(g[-1] + 1)
        # 往前／往後延伸，但不越過與相鄰句子之間的最安靜點，避免切進別人的聲音
        lo = boundary(db, prev, first) if prev else 0.0
        hi = boundary(db, last, nxt) if nxt else total
        start = max(lo, first["start"] - a.pre, 0.0)
        end = min(hi, last["end"] + a.post, total)
        segments.append({"index": i, "file": f"seg_{i:03d}.mp3",
                         "start": round(start, 3), "end": round(end, 3),
                         "duration": round(end - start, 3), "sentences": g,
                         "text": " ".join(by_n[n]["text"] for n in g)})

    for old in out.glob("seg_*.mp3"):
        old.unlink()
    for x in segments:
        fade = min(a.fade, x["duration"] / 4)
        af = f"afade=t=in:d={fade},afade=t=out:st={x['duration'] - fade:.3f}:d={fade}"
        r = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                 "-ss", str(x["start"]), "-to", str(x["end"]), "-i", str(src),
                 "-af", af, "-ac", "1", "-c:a", "libmp3lame", "-q:a", "2", str(out / x["file"])])
        if r.returncode != 0:
            die(f"輸出 {x['file']} 失敗：\n{r.stderr}")
        print(f"{x['index']:>3}  {x['start']:7.2f}–{x['end']:7.2f}  {x['duration']:5.1f}s  {x['text']}")

    dropped = [s["n"] for s in sentences if s["n"] not in {n for g in groups for n in g}]
    save_segments(out, {
        "source": str(src),
        "method": "asr",
        "params": {"groups": a.groups, "pre": a.pre, "post": a.post, "fade": a.fade},
        "segments": segments,
    })
    print(f"\n已輸出 {len(segments)} 段到 {out}/" + (f"｜未使用的句子：{dropped}" if dropped else ""))


if __name__ == "__main__":
    main()
