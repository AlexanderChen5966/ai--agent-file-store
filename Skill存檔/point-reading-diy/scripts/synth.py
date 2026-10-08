#!/usr/bin/env python3
"""Mac 語音合成：給單字清單，用 `say` 批次產生 <碼號>.mp3（跳過切檔與辨識）。

適合單字卡、簡單句子。台語沒有內建語音，無法使用。

用法：
  python3 synth.py words.txt --codes 461-480 --voice Meijia --out out/
  python3 synth.py words.tsv --voice Samantha --rate 150 --out out/   # 單字表自帶碼號
  python3 synth.py --list-voices zh                                   # 列出可用語音

常用語音：Meijia（國語・台灣）、Samantha（英文）、Sinji（粵語）、Kyoko（日文）
單字表格式同 assign.py：每行「文字」或「碼號<Tab或逗號>文字」。
"""
import argparse
import sys
import tempfile
from pathlib import Path

from _common import die, parse_codes, require, run
from assign import read_wordlist


def main():
    ap = argparse.ArgumentParser(description="用 Mac say 批次合成點讀音檔")
    ap.add_argument("wordlist", nargs="?", help="單字表檔案")
    ap.add_argument("--codes", help="碼號，如 461-480（單字表沒帶碼號時必填）")
    ap.add_argument("--voice", default="Meijia", help="say 的語音名稱（預設 Meijia）")
    ap.add_argument("--rate", type=int, help="語速（每分鐘字數），兒童用可調慢如 140")
    ap.add_argument("--out", default="out", help="輸出資料夾（預設 out/）")
    ap.add_argument("--list-voices", metavar="LANG", help="列出某語言的語音，如 zh、en、ja")
    a = ap.parse_args()

    require("say")
    if a.list_voices is not None:
        r = run(["say", "-v", "?"])
        for line in r.stdout.splitlines():
            if a.list_voices.lower() in line.lower():
                print(line)
        return
    if not a.wordlist:
        die("請指定單字表檔案")
    require("ffmpeg")

    words = read_wordlist(a.wordlist)
    if all(c is not None for c, _ in words):
        codes = [c for c, _ in words]
    elif a.codes:
        codes = parse_codes(a.codes)
        if len(codes) != len(words):
            die(f"碼號 {len(codes)} 個，單字表 {len(words)} 行，數量要一致")
    else:
        die("請用 --codes 指定碼號，或在單字表中帶碼號")

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        aiff = Path(tmp) / "t.aiff"
        for code, (_, text) in zip(codes, words):
            args = ["say", "-v", a.voice, "-o", str(aiff)]
            if a.rate:
                args += ["-r", str(a.rate)]
            r = run(args + [text])
            if r.returncode != 0:
                die(f"say 失敗（語音 {a.voice} 是否存在？用 --list-voices 查）：{r.stderr}")
            # 前後各補 0.15 秒靜音，筆上播放比較不會吃字
            r = run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(aiff),
                     "-af", "adelay=150,apad=pad_dur=0.15", "-ac", "1",
                     "-c:a", "libmp3lame", "-q:a", "2", str(out / f"{code}.mp3")])
            if r.returncode != 0:
                die(f"轉 mp3 失敗：{r.stderr}")
            print(f"  {code}.mp3  {text}")
    print(f"已產生 {len(codes)} 個檔案到 {out}/", file=sys.stderr)


if __name__ == "__main__":
    main()
