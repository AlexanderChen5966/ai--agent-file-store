#!/usr/bin/env python3
"""
dab_tool.py -- DAB 點讀包讀寫工具（逆向所得，樣本：535-高频词32.dab）

檔案結構（little-endian）
  0x0000  "deb3" + GBK 書名 (0xFF 填充)
  0x00C8  GUID 字串           0x012C  作者字串
  0x014A  01 00 | 20 00 00 00 | 不透明 32+ bytes（用途未明，原樣保留）
  0x017B  u32 起始 OID 碼      0x017F  u32 音訊區結尾位移
  0x0183  u32 介紹音檔長度     0x0187  "Create by Builder <時間>"
  0x01AF  u32 有效碼數量       0x01B3  589 bytes 不透明加密區（原樣保留）
  0x0400  指標表：第 i 格 = OID (起始碼+i)；u32 位移 + u32 長度；空格 ff×8
  音訊段  [0x52 標記][MP3]，交替金鑰 (k, k^0x52) XOR；段間無間隙
  結尾    介紹音檔段（同樣遮蔽）→ "BOID" + 8192 bytes OID 點陣圖(MSB first) + "EOID"
"""
import os, random, argparse, json

def le(d, o): return int.from_bytes(d[o:o+4], 'little')
def u32(v):   return v.to_bytes(4, 'little')

_XT = [bytes(i ^ k for i in range(256)) for k in range(256)]   # XOR 對照表

def xor2(buf, k0):
    """交替金鑰 (k0, k0^0x52) XOR，C 速度"""
    out = bytearray(len(buf))
    out[0::2] = buf[0::2].translate(_XT[k0])
    out[1::2] = buf[1::2].translate(_XT[k0 ^ 0x52])
    return bytes(out)

def _dec(d, off, ln):
    k0 = d[off] ^ 0x52
    return xor2(d[off:off+ln+1], k0)[1:], k0

def _enc(mp3, k0):
    return xor2(b'\x52' + mp3, k0)

def read_dab(path):
    d = open(path, 'rb').read()
    start, audio_end, intro_len = le(d, 0x17B), le(d, 0x17F), le(d, 0x183)
    T0 = 0x400
    first, o = len(d), T0
    while o < first:                       # 表格止於最前面那段音訊
        if d[o:o+8] != b'\xff'*8:
            first = min(first, le(d, o))
        o += 8
    clips = {}
    for i in range((first - T0) // 8):
        o = T0 + 8*i
        if d[o:o+8] == b'\xff'*8: continue
        mp3, k = _dec(d, le(d, o), le(d, o+4))
        clips[start + i] = {"mp3": mp3, "key": k}
    intro = None
    if intro_len:
        mp3, k = _dec(d, audio_end, intro_len)
        intro = {"mp3": mp3, "key": k}
    tail = d[audio_end + (intro_len + 1 if intro_len else 0):]
    return {"header": d[:T0], "start": start, "clips": clips,
            "intro": intro, "tail_pad": tail}

def write_dab(path, book, keep_keys=False, rng=None, dedup=False):
    rng = rng or random.Random()
    key_of = lambda c: c["key"] if keep_keys and "key" in c else rng.randrange(256)
    clips = book["clips"]
    start = book.get("start", min(clips))
    end = max(clips)
    nslot = end - start + 1
    T0 = 0x400
    table, body = bytearray(), bytearray()
    cursor = T0 + 8*nslot
    seen = {}
    for code in range(start, end + 1):
        c = clips.get(code)
        if not c:
            table += b'\xff'*8; continue
        if dedup and c["mp3"] in seen:           # 多個碼共用同一段（實驗性）
            table += u32(seen[c["mp3"]]) + u32(len(c["mp3"])); continue
        if dedup: seen[c["mp3"]] = cursor
        seg = _enc(c["mp3"], key_of(c))
        table += u32(cursor) + u32(len(c["mp3"]))
        body += seg; cursor += len(seg)
    audio_end = cursor
    intro = book.get("intro")
    if intro:
        body += _enc(intro["mp3"], key_of(intro))
    # BOID bitmap
    bm = bytearray(8192)
    for code in clips:
        bm[code >> 3] |= 0x80 >> (code & 7)
    tail = book.get("tail_pad")
    if tail and len(tail) >= 8200 and tail[:4] == b'BOID' and tail[-4:] == b'EOID' and keep_keys:
        tailb = tail                                  # 原樣（回環測試用）
    else:
        tailb = b'BOID' + bytes(bm) + b'EOID'
    hdr = bytearray(book["header"])
    hdr[0x17B:0x17F] = u32(start)
    hdr[0x17F:0x183] = u32(audio_end)
    hdr[0x183:0x187] = u32(len(intro["mp3"]) if intro else 0)
    hdr[0x1AF:0x1B3] = u32(len(clips))
    open(path, 'wb').write(bytes(hdr) + bytes(table) + bytes(body) + tailb)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("extract");   x.add_argument("dab"); x.add_argument("-o", default="dab_out")
    r = sub.add_parser("roundtrip"); r.add_argument("dab"); r.add_argument("out")
    t = sub.add_parser("swaptest", help="產生實測檔：相鄰兩碼音訊互換、金鑰全換，檔頭不透明區原樣保留")
    t.add_argument("dab"); t.add_argument("out")
    a = ap.parse_args()
    if a.cmd == "extract":
        b = read_dab(a.dab); os.makedirs(a.o, exist_ok=True)
        for code, c in b["clips"].items():
            open(os.path.join(a.o, f"{code:05d}.mp3"), 'wb').write(c["mp3"])
        if b["intro"]: open(os.path.join(a.o, "intro.mp3"), 'wb').write(b["intro"]["mp3"])
        print(f"起始碼 {b['start']}，{len(b['clips'])} 段 + intro={'有' if b['intro'] else '無'}")
    elif a.cmd == "roundtrip":
        write_dab(a.out, read_dab(a.dab), keep_keys=True)
    elif a.cmd == "swaptest":
        b = read_dab(a.dab); codes = sorted(b["clips"]); sw = {}
        for i in range(0, len(codes) - 1, 2):
            x, y = codes[i], codes[i+1]
            sw[x] = {"mp3": b["clips"][y]["mp3"]}; sw[y] = {"mp3": b["clips"][x]["mp3"]}
        if len(codes) % 2: sw[codes[-1]] = {"mp3": b["clips"][codes[-1]]["mp3"]}
        b["clips"] = sw; b["tail_pad"] = None
        if b["intro"]: b["intro"] = {"mp3": b["intro"]["mp3"]}
        write_dab(a.out, b, rng=random.Random(42))
        print(f"已產生 {a.out}：{len(codes)//2} 對相鄰碼互換，例如 {codes[0]}↔{codes[1]}")
