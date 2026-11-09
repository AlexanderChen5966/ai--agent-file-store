#!/usr/bin/env python3
"""
pack.py -- 把「內容貼號碼.mp3」打包成卡米點讀筆可讀的 DAB（步驟 ⑤）

用法：
  python3 scripts/pack.py work/out --book-sticker 1 --title "Dear Zoo"
    → 產生 work/001-1-Dear_Zoo.dab（普通書名貼 001，內容貼 0001～ 對應碼 25001～）

  python3 scripts/pack.py work/out --prefix 001 --title "Dear Zoo"
    → 智能書名貼 001 用 --prefix 001（檔名 001-…）

輸入：資料夾內以「內容貼印刷號碼」命名的 MP3，例如 0001.mp3、0002.mp3（assign.py 的輸出）
規則（2026-10-10 實測）：
  內容貼實際碼號 = 25000 + 印刷號碼
  普通書名貼 N → 碼 56000+N → 檔名 NNN-1-書名.dab
  智能書名貼 N → 檔名 NNN-書名.dab
"""
import os, re, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dab_tool import read_dab, write_dab


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp3dir", help="內含 0001.mp3、0002.mp3… 的資料夾")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--book-sticker", type=int, help="普通書名貼印刷號碼（檔名會是 NNN-1-）")
    g.add_argument("--prefix", help="直接指定檔名前綴，例如智能書名貼 001")
    ap.add_argument("--title", required=True, help="書名（寫進檔頭，也用於檔名）")
    ap.add_argument("--code-base", type=int, default=25000, help="內容貼碼號 = 此值 + 印刷號碼")
    ap.add_argument("--template", default=os.path.join(HERE, "template_header.dab"))
    ap.add_argument("--intro", help="選書時的提示音 MP3（可省略；預設用最小號碼那一段）")
    ap.add_argument("-o", "--outdir", help="輸出資料夾（預設為 mp3dir 的上一層）")
    a = ap.parse_args()

    files = {}
    for f in sorted(os.listdir(a.mp3dir)):
        m = re.fullmatch(r"(\d+)\.mp3", f, re.I)
        if m:
            files[int(m.group(1))] = os.path.join(a.mp3dir, f)
    if not files:
        sys.exit(f"{a.mp3dir} 裡沒有「數字.mp3」檔案")
    base = a.code_base
    if min(files) > a.code_base:          # 檔名已經是實際碼號（例如 25001.mp3）
        base = 0
        print(f"檔名已是實際碼號（{min(files)} 起），不再加 {a.code_base}")
    clips = {base + n: {"mp3": open(p, "rb").read()} for n, p in files.items()}

    tpl = read_dab(a.template)
    hdr = bytearray(tpl["header"])
    t = a.title.encode("gbk", "replace")[:0xC4]
    hdr[4:0xC8] = t + b"\xff" * (0xC4 - len(t))
    intro = {"mp3": open(a.intro, "rb").read()} if a.intro else clips[min(clips)]

    prefix = f"{a.book_sticker:03d}-1" if a.book_sticker is not None else a.prefix
    safe = re.sub(r"[^\w一-鿿]+", "_", a.title).strip("_")
    outdir = a.outdir or os.path.dirname(os.path.abspath(a.mp3dir))
    out = os.path.join(outdir, f"{prefix}-{safe}.dab")
    write_dab(out, {"header": bytes(hdr), "start": min(clips), "clips": clips, "intro": intro})

    back = read_dab(out)
    ok = sorted(back["clips"]) == sorted(clips) and all(back["clips"][c]["mp3"] == clips[c]["mp3"] for c in clips)
    print(f"{'✅' if ok else '❌'} {out}")
    print(f"   {len(clips)} 段，碼 {min(clips)}–{max(clips)}，{os.path.getsize(out) / 1e6:.2f} MB，讀回驗證{'通過' if ok else '失敗'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
