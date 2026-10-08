#!/usr/bin/env python3
"""① 依靜音切檔。

用 ffmpeg silencedetect 找出靜音區間，把中間有聲的部分切成 seg_001.mp3、seg_002.mp3……
並寫出 segments.json（時間點清單），供後續步驟使用。

用法：
  python3 split.py 錄音.mp3 --out work/            # 正式切
  python3 split.py 錄音.mp3 --out work/ --dry-run  # 只看會切成幾段，不輸出檔案
  python3 split.py 錄音.mp3 --out work/ --noise -40 --min-silence 0.6 --expect 20
"""
import argparse
import re
import statistics
from pathlib import Path

from _common import (die, probe_duration, require, run, save_segments)


def detect_silences(src, noise_db, min_silence):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src),
             "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}",
             "-f", "null", "-"])
    if r.returncode != 0:
        die(f"ffmpeg 執行失敗：\n{r.stderr[-2000:]}")
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    # 結尾仍在靜音中時 ffmpeg 不會印 silence_end
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def speech_intervals(silences, total):
    intervals, cursor = [], 0.0
    for s, e in silences:
        s = max(s, 0.0)
        if s > cursor:
            intervals.append((cursor, s))
        cursor = total if e is None else e
    if cursor < total:
        intervals.append((cursor, total))
    return intervals


def main():
    ap = argparse.ArgumentParser(description="依靜音切檔")
    ap.add_argument("input", help="原始音檔")
    ap.add_argument("--out", required=True, help="工作資料夾（片段與 segments.json 存這裡）")
    ap.add_argument("--noise", type=float, default=-35,
                    help="靜音門檻 dB，越低越嚴格（預設 -35）")
    ap.add_argument("--min-silence", type=float, default=0.5,
                    help="最短靜音秒數，短於此不算斷點（預設 0.5）")
    ap.add_argument("--min-segment", type=float, default=0.25,
                    help="短於此秒數的片段視為雜音丟棄（預設 0.25）")
    ap.add_argument("--pad", type=float, default=0.15,
                    help="每段前後保留的靜音秒數，避免切到字頭字尾（預設 0.15）")
    ap.add_argument("--expect", type=int, help="預期段數（內容貼張數），用來比對結果")
    ap.add_argument("--dry-run", action="store_true", help="只回報段數與長度，不輸出檔案")
    a = ap.parse_args()

    require("ffmpeg")
    src = Path(a.input).resolve()
    if not src.exists():
        die(f"找不到音檔：{src}")

    total = probe_duration(src)
    raw = speech_intervals(detect_silences(src, a.noise, a.min_silence), total)
    kept = [(s, e) for s, e in raw if e - s >= a.min_segment]
    dropped = len(raw) - len(kept)

    segments = []
    for i, (s, e) in enumerate(kept, 1):
        start, end = max(0.0, s - a.pad), min(total, e + a.pad)
        segments.append({"index": i, "file": f"seg_{i:03d}.mp3",
                         "start": round(start, 3), "end": round(end, 3),
                         "duration": round(end - start, 3)})

    # ── 報告：讓 agent 判斷參數是否要調 ──
    durs = [x["duration"] for x in segments]
    print(f"音檔長度 {total:.1f}s｜門檻 {a.noise}dB｜最短靜音 {a.min_silence}s")
    print(f"切出 {len(segments)} 段（丟棄 {dropped} 段過短雜音）")
    if durs:
        med = statistics.median(durs)
        print(f"片段長度：最短 {min(durs):.2f}s／中位數 {med:.2f}s／最長 {max(durs):.2f}s")
        long_ones = [x["index"] for x in segments if x["duration"] > med * 2.5 and x["duration"] > 2]
        if long_ones:
            print(f"⚠ 可能黏在一起（長度超過中位數 2.5 倍）：{long_ones}")
    if a.expect:
        diff = len(segments) - a.expect
        if diff == 0:
            print(f"✓ 段數與預期 {a.expect} 相符")
        elif diff < 0:
            print(f"⚠ 比預期少 {-diff} 段 → 可能有沒切開的，試試提高 --noise（如 -30）或降低 --min-silence")
        else:
            print(f"⚠ 比預期多 {diff} 段 → 可能切太碎或有雜音，試試降低 --noise（如 -40）或提高 --min-silence")

    if a.dry_run:
        return

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("seg_*.mp3"):
        old.unlink()
    for x in segments:
        r = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                 "-ss", str(x["start"]), "-to", str(x["end"]), "-i", str(src),
                 "-ac", "1", "-c:a", "libmp3lame", "-q:a", "2", str(out / x["file"])])
        if r.returncode != 0:
            die(f"輸出 {x['file']} 失敗：\n{r.stderr}")

    save_segments(out, {
        "source": str(src),
        "params": {"noise": a.noise, "min_silence": a.min_silence,
                   "min_segment": a.min_segment, "pad": a.pad},
        "segments": segments,
    })
    print(f"已輸出到 {out}/（segments.json + {len(segments)} 個 mp3）")


if __name__ == "__main__":
    main()
