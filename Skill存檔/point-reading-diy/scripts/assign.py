#!/usr/bin/env python3
"""④ 對應內容貼：決定哪個片段對哪張內容貼，複製並改名為 <碼號>.mp3。

兩種模式：
  照順序（預設）：第 1 段 → 第 1 個碼號、第 2 段 → 第 2 個碼號……任何語言都適用
  單字表比對（--wordlist）：用辨識文字與單字表模糊比對，依序對齊，可容忍多一段或少一段

review.json 中標為「刪除」的片段會跳過；仍有「問題」未處理的片段預設會停下來。

用法：
  python3 assign.py work/ --codes 461-480                       # 照順序
  python3 assign.py work/ --wordlist words.txt --codes 461-480  # 單字表（每行一個詞）
  python3 assign.py work/ --wordlist words.tsv                  # 單字表自帶碼號（碼號<Tab>文字）
  python3 assign.py work/ --codes 461-480 --dry-run             # 只看對應表
  python3 assign.py work/ --codes 1-18 --width 4                # 輸出 0001.mp3～0018.mp3
  python3 assign.py work/ --apply                               # 依手動修改過的 assignment.json 重新輸出

單字表格式：每行「文字」或「碼號<Tab或逗號>文字」，# 開頭為註解。
"""
import argparse
import difflib
import re
import shutil
import unicodedata
from pathlib import Path

from _common import (die, load_json, load_review, load_segments, parse_codes,
                     save_json, to_traditional)

LOW_CONFIDENCE = 0.6
MATCH_BONUS = 0.35  # 相似度低於此值時寧可當作「沒對上」而不硬配


def read_wordlist(path):
    entries = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(\d+)\s*[\t,]\s*(.+)$", line)
        entries.append((int(m.group(1)), m.group(2).strip()) if m else (None, line))
    return entries


def norm(text):
    text = to_traditional(unicodedata.normalize("NFKC", text or "")).lower()
    return "".join(ch for ch in text if ch.isalnum())


def similarity(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def align(seg_texts, word_texts):
    """依序對齊（類似 Needleman-Wunsch）：允許跳過片段或單字，回傳 [(seg_i, word_j, sim)]。"""
    n, m = len(seg_texts), len(word_texts)
    sim = [[similarity(s, w) for w in word_texts] for s in seg_texts]
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        back[i][0] = "s"
    for j in range(1, m + 1):
        back[0][j] = "w"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opts = [(dp[i - 1][j - 1] + sim[i - 1][j - 1] - MATCH_BONUS, "m"),
                    (dp[i - 1][j], "s"), (dp[i][j - 1], "w")]
            dp[i][j], back[i][j] = max(opts, key=lambda x: x[0])
    pairs, i, j = [], n, m
    while i > 0 or j > 0:
        step = back[i][j]
        if step == "m":
            pairs.append((i - 1, j - 1, sim[i - 1][j - 1]))
            i, j = i - 1, j - 1
        elif step == "s":
            i -= 1
        else:
            j -= 1
    return pairs[::-1]


def build_rows(segs, codes, words):
    if words is None:  # 照順序
        return [{"index": s["index"], "file": s["file"], "code": c,
                 "text": s.get("text", ""), "expected": "", "score": None}
                for s, c in zip(segs, codes)]
    pairs = align([s.get("text", "") for s in segs], [w for _, w in words])
    return [{"index": segs[i]["index"], "file": segs[i]["file"], "code": codes[j],
             "text": segs[i].get("text", ""), "expected": words[j][1], "score": round(sc, 2)}
            for i, j, sc in pairs]


def report(rows, segs, codes):
    print(f"{'片段':>4}  {'碼號':>5}  {'分數':>4}  辨識文字 → 單字表")
    for r in rows:
        sc = "" if r["score"] is None else f"{r['score']:.2f}"
        flag = " ⚠" if r["score"] is not None and r["score"] < LOW_CONFIDENCE else ""
        arrow = f" → {r['expected']}" if r["expected"] else ""
        print(f"{r['index']:>4}  {r['code']:>5}  {sc:>4}  {r['text'] or '—'}{arrow}{flag}")
    used_seg = {r["index"] for r in rows}
    used_code = {r["code"] for r in rows}
    left_seg = [s["index"] for s in segs if s["index"] not in used_seg]
    left_code = [c for c in codes if c not in used_code]
    low = [r["index"] for r in rows if r["score"] is not None and r["score"] < LOW_CONFIDENCE]
    print(f"\n對上 {len(rows)} 組｜片段 {len(segs)}｜碼號 {len(codes)}")
    if left_seg:
        print(f"⚠ 沒對到碼號的片段：{left_seg}")
    if left_code:
        print(f"⚠ 沒有音檔的碼號：{left_code}")
    if low:
        print(f"⚠ 低信心（< {LOW_CONFIDENCE}），請人工確認：片段 {low}")
    return left_seg, left_code


def write_out(work, rows, out, width=0):
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.mp3"):
        old.unlink()
    seen = set()
    for r in rows:
        if r["code"] in seen:
            die(f"碼號 {r['code']} 重複指派，請檢查 assignment.json")
        seen.add(r["code"])
        shutil.copy2(work / r["file"], out / f"{r['code']:0{width}d}.mp3")
    print(f"已輸出 {len(rows)} 個檔案到 {out}/")


def main():
    ap = argparse.ArgumentParser(description="片段對應內容貼碼號")
    ap.add_argument("work", help="split.py 的輸出資料夾")
    ap.add_argument("--codes", help="內容貼碼號，如 461-480 或 461-470,480-489")
    ap.add_argument("--wordlist", help="單字表檔案（啟用模糊比對）")
    ap.add_argument("--out", help="輸出資料夾（預設 <work>/out）")
    ap.add_argument("--width", type=int, default=0, help="檔名碼號補零位數，如 4 → 0001.mp3（預設不補）")
    ap.add_argument("--allow-problem", action="store_true", help="有未處理的「問題」段也繼續")
    ap.add_argument("--dry-run", action="store_true", help="只印對應表，不輸出")
    ap.add_argument("--apply", action="store_true", help="直接依 assignment.json 輸出")
    a = ap.parse_args()

    work = Path(a.work)
    out = Path(a.out) if a.out else work / "out"

    if a.apply:
        p = work / "assignment.json"
        if not p.exists():
            die("找不到 assignment.json，請先不加 --apply 執行一次")
        write_out(work, load_json(p)["rows"], out, a.width)
        return

    data = load_segments(work)
    review = load_review(work, data)
    if not review:
        print("⚠ 尚未有 review.json（未經人工審核）。正式打包前一定要審核。")

    segs = []
    for s in data["segments"]:
        rv = review.get(str(s["index"]), {})
        if rv.get("status") == "drop":
            continue
        if rv.get("status") == "problem" and not a.allow_problem:
            die(f"片段 {s['index']} 標為問題（{rv.get('note') or '無備註'}），"
                "請先處理（重切、刪除或改成 OK），或加 --allow-problem")
        segs.append({**s, "text": rv.get("text") or s.get("text", "")})

    words = read_wordlist(a.wordlist) if a.wordlist else None
    if words and all(c is not None for c, _ in words):
        codes = [c for c, _ in words]
        if a.codes:
            print("（單字表已帶碼號，忽略 --codes）")
    elif a.codes:
        codes = parse_codes(a.codes)
        if words:
            if len(codes) != len(words):
                die(f"碼號 {len(codes)} 個，單字表 {len(words)} 行，數量要一致")
            words = [(c, w) for c, (_, w) in zip(codes, words)]
    else:
        die("請用 --codes 指定碼號，或在單字表中帶碼號")
    if len(set(codes)) != len(codes):
        die("碼號有重複")
    if words and not any(s.get("text") for s in segs):
        die("片段都沒有辨識文字，無法用單字表比對。請先跑 transcribe.py，或改用照順序（拿掉 --wordlist）")

    rows = build_rows(segs, codes, words)
    report(rows, segs, codes)
    if a.dry_run:
        return
    save_json(work / "assignment.json",
              {"mode": "wordlist" if words else "order", "rows": rows})
    print(f"對應表已存 {work / 'assignment.json'}（可手動修改後用 --apply 重新輸出）")
    write_out(work, rows, out, a.width)


if __name__ == "__main__":
    main()
