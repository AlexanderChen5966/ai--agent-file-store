"""各腳本共用的小工具：碼號解析、JSON 讀寫、ffmpeg 呼叫。"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SEGMENTS_JSON = "segments.json"
REVIEW_JSON = "review.json"


def die(msg):
    print(f"錯誤：{msg}", file=sys.stderr)
    sys.exit(1)


def require(cmd):
    if not shutil.which(cmd):
        die(f"找不到 {cmd}，請先安裝（brew install {cmd}）")


def run(args, **kw):
    kw.setdefault("text", True)
    return subprocess.run(args, capture_output=True, **kw)


def probe_duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)])
    if r.returncode != 0:
        die(f"無法讀取音檔長度：{path}\n{r.stderr}")
    return float(r.stdout.strip())


def parse_codes(spec):
    """'461-470,480,500-502' → [461, ..., 470, 480, 500, 501, 502]"""
    codes = []
    for part in re.split(r"[,\s]+", spec.strip()):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a), int(b)
            step = 1 if b >= a else -1
            codes.extend(range(a, b + step, step))
        else:
            codes.append(int(part))
    for c in codes:
        if not 0 <= c <= 65535:
            die(f"碼號 {c} 超出範圍（0–65535）")
    return codes


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_segments(work_dir):
    p = Path(work_dir) / SEGMENTS_JSON
    if not p.exists():
        die(f"找不到 {p}，請先執行 split.py")
    return load_json(p)


def save_segments(work_dir, data):
    save_json(Path(work_dir) / SEGMENTS_JSON, data)


def load_review(work_dir):
    """讀審核結果；沒有就回傳空 dict。key 為片段 index（字串）。"""
    p = Path(work_dir) / REVIEW_JSON
    if not p.exists():
        return {}
    return load_json(p).get("segments", {})


def to_traditional(text):
    """國語辨識結果轉台灣繁體；沒裝 OpenCC 就原樣回傳。"""
    try:
        from opencc import OpenCC
    except ImportError:
        return text
    return OpenCC("s2twp").convert(text)
