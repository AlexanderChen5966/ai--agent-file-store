#!/usr/bin/env python3
"""③ 產生審核網頁 review.html（單一檔案，雙擊即可在瀏覽器開啟）。

每段可播放、顯示波形與辨識文字（可直接修改），並標記：
  OK／問題（黏在一起、念錯、切到字……）／刪除（雜音、多餘段）
審核完按「匯出審核結果」，把下載的 review.json 放回工作資料夾，assign.py 會讀取。

用法：
  python3 review.py work/
  python3 review.py work/ --title "Max & Mousy 第 1 冊"
"""
import argparse
import array
import json
from pathlib import Path

from _common import (REVIEW_JSON, load_json, load_review, load_segments, require, run)

PEAKS = 160


def peaks(path):
    """把音檔降成 8kHz 單聲道 PCM，取 PEAKS 個區間的最大振幅（0–1）。"""
    r = run(["ffmpeg", "-loglevel", "error", "-i", str(path),
             "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], text=False)
    samples = array.array("h", r.stdout[: len(r.stdout) // 2 * 2])
    if not samples:
        return [0] * PEAKS
    step = max(1, len(samples) // PEAKS)
    out = [max(abs(v) for v in samples[i:i + step]) / 32768
           for i in range(0, step * PEAKS, step) if samples[i:i + step]]
    top = max(out) or 1
    return [round(v / top, 3) for v in out]


def main():
    ap = argparse.ArgumentParser(description="產生審核網頁")
    ap.add_argument("work", help="split.py 的輸出資料夾")
    ap.add_argument("--title", default="點讀音檔審核")
    a = ap.parse_args()

    require("ffmpeg")
    work = Path(a.work)
    data = load_segments(work)
    review = load_review(work)
    assigned = {}
    if (work / "assignment.json").exists():
        for row in load_json(work / "assignment.json")["rows"]:
            assigned[str(row["index"])] = row["code"]

    rows = []
    for s in data["segments"]:
        prev = review.get(str(s["index"]), {})
        rows.append({
            "index": s["index"], "file": s["file"], "start": s["start"],
            "duration": s["duration"], "text": prev.get("text", s.get("text", "")),
            "status": prev.get("status", ""), "note": prev.get("note", ""),
            "code": assigned.get(str(s["index"])), "peaks": peaks(work / s["file"]),
        })

    html = TEMPLATE.replace("__TITLE__", a.title).replace(
        "__DATA__", json.dumps({"title": a.title, "source": data.get("source", ""),
                                "review_file": REVIEW_JSON, "rows": rows},
                               ensure_ascii=False).replace("</", "<\\/"))
    out = work / "review.html"
    out.write_text(html, encoding="utf-8")
    print(f"已產生 {out}（{len(rows)} 段）")
    print(f"開啟：open '{out}'")


TEMPLATE = r"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#f7f6f3;--card:#fff;--ink:#222;--mute:#777;--line:#e2e0da;--accent:#2f6fde;
--ok:#2e9d5b;--warn:#d98a00;--bad:#c94040;--wave:#b9c6dd;--wave-on:#2f6fde}
@media (prefers-color-scheme:dark){:root{--bg:#18191b;--card:#222326;--ink:#e8e8e8;--mute:#999;
--line:#34363a;--accent:#6e9cff;--wave:#46536b;--wave-on:#6e9cff}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,"PingFang TC","Noto Sans TC",sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 16px}
h1{font-size:18px;margin:0 0 4px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:13px;color:var(--mute)}
.bar .stat b{color:var(--ink)}
button{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:6px;padding:4px 10px;cursor:pointer}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff}
main{max-width:980px;margin:0 auto;padding:12px 16px 80px}
.row{display:grid;grid-template-columns:52px 1fr;gap:10px;background:var(--card);border:1px solid var(--line);
border-left:4px solid var(--line);border-radius:8px;padding:10px;margin-bottom:8px}
.row.cur{outline:2px solid var(--accent)}
.row[data-status=ok]{border-left-color:var(--ok)}
.row[data-status=problem]{border-left-color:var(--warn)}
.row[data-status=drop]{border-left-color:var(--bad);opacity:.55}
.idx{font-weight:600;font-size:18px;text-align:center}
.idx small{display:block;font-weight:400;font-size:12px;color:var(--mute)}
.idx .code{display:block;font-size:12px;color:var(--accent)}
canvas{width:100%;height:40px;display:block;cursor:pointer}
.ctl{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:6px}
.ctl input[type=text]{flex:1 1 220px;min-width:0;font:inherit;padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:transparent;color:var(--ink)}
.ctl .note{flex:1 1 160px}
.st button[aria-pressed=true][data-v=ok]{background:var(--ok);border-color:var(--ok);color:#fff}
.st button[aria-pressed=true][data-v=problem]{background:var(--warn);border-color:var(--warn);color:#fff}
.st button[aria-pressed=true][data-v=drop]{background:var(--bad);border-color:var(--bad);color:#fff}
.keys{font-size:12px;color:var(--mute)}
kbd{border:1px solid var(--line);border-radius:3px;padding:0 4px;font-size:11px}
</style>
</head>
<body>
<header>
  <h1 id="title"></h1>
  <div class="bar">
    <span class="stat">共 <b id="n"></b> 段｜OK <b id="nok"></b>｜問題 <b id="npb"></b>｜刪除 <b id="ndp"></b>｜未審 <b id="nun"></b></span>
    <button id="playall">▶ 從目前段連續播放</button>
    <button class="primary" id="export">匯出審核結果（review.json）</button>
  </div>
  <div class="keys">快捷鍵：<kbd>空白</kbd> 播放目前段　<kbd>↑</kbd><kbd>↓</kbd> 換段　<kbd>1</kbd> OK　<kbd>2</kbd> 問題　<kbd>3</kbd> 刪除（標記後自動跳下一段）</div>
</header>
<main id="list"></main>
<audio id="player" preload="none"></audio>
<script>
const D = __DATA__;
const KEY = "pr-review:" + D.source;
let saved = {};
try { saved = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
for (const r of D.rows) Object.assign(r, saved[r.index] || {});

const $ = s => document.querySelector(s);
const player = $("#player");
let cur = 0, chain = false;
$("#title").textContent = D.title;

function persist() {
  const o = {};
  for (const r of D.rows) o[r.index] = {status: r.status, note: r.note, text: r.text};
  try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  const c = s => D.rows.filter(r => r.status === s).length;
  $("#n").textContent = D.rows.length; $("#nok").textContent = c("ok");
  $("#npb").textContent = c("problem"); $("#ndp").textContent = c("drop"); $("#nun").textContent = c("");
}

function css(v) { return getComputedStyle(document.documentElement).getPropertyValue(v).trim(); }

function draw(cv, peaks, frac) {
  const w = cv.width = cv.clientWidth * devicePixelRatio, h = cv.height = 40 * devicePixelRatio;
  const g = cv.getContext("2d"), bw = w / peaks.length;
  peaks.forEach((p, i) => {
    g.fillStyle = i / peaks.length < frac ? css("--wave-on") : css("--wave");
    const ph = Math.max(1, p * h * .9);
    g.fillRect(i * bw, (h - ph) / 2, Math.max(1, bw - 1), ph);
  });
}

const els = D.rows.map((r, i) => {
  const el = document.createElement("div");
  el.className = "row"; el.dataset.status = r.status;
  el.innerHTML = `<div class="idx">${r.index}<small>${r.duration.toFixed(2)}s</small>${r.code != null ? `<span class="code">→ ${r.code}</span>` : ""}</div>
  <div><canvas></canvas>
  <div class="ctl">
    <button class="play">▶</button>
    <input type="text" class="text" placeholder="辨識文字（可修改）">
    <span class="st"><button data-v="ok">OK</button> <button data-v="problem">問題</button> <button data-v="drop">刪除</button></span>
    <input type="text" class="note" placeholder="備註：黏在一起、念錯、切到字…">
  </div></div>`;
  const cv = el.querySelector("canvas");
  el.querySelector(".text").value = r.text || "";
  el.querySelector(".note").value = r.note || "";
  el.querySelector(".text").oninput = e => { r.text = e.target.value; persist(); };
  el.querySelector(".note").oninput = e => { r.note = e.target.value; persist(); };
  el.querySelector(".play").onclick = () => { chain = false; play(i); };
  cv.onclick = () => { chain = false; play(i); };
  el.querySelectorAll(".st button").forEach(b => b.onclick = () => setStatus(i, b.dataset.v, false));
  el.onclick = e => { if (e.target === el) select(i); };
  $("#list").appendChild(el);
  return {el, cv};
});

function paintStatus(i) {
  const r = D.rows[i];
  els[i].el.dataset.status = r.status;
  els[i].el.querySelectorAll(".st button").forEach(b => b.setAttribute("aria-pressed", b.dataset.v === r.status));
}

function setStatus(i, v, advance) {
  const r = D.rows[i];
  r.status = r.status === v && !advance ? "" : v;
  paintStatus(i); persist();
  if (advance && i < D.rows.length - 1) select(i + 1, true);
}

function select(i, scroll) {
  els[cur].el.classList.remove("cur");
  cur = i; els[i].el.classList.add("cur");
  if (scroll) els[i].el.scrollIntoView({block: "center", behavior: "smooth"});
}

function play(i) {
  select(i, chain);
  player.src = D.rows[i].file;
  player.play();
}

player.ontimeupdate = () => draw(els[cur].cv, D.rows[cur].peaks, player.currentTime / (player.duration || 1));
player.onended = () => {
  draw(els[cur].cv, D.rows[cur].peaks, 0);
  if (chain && cur < D.rows.length - 1) setTimeout(() => play(cur + 1), 400); else chain = false;
};

$("#playall").onclick = () => { chain = true; play(cur); };

document.addEventListener("keydown", e => {
  if (e.target.tagName === "INPUT") return;
  if (e.key === " ") { e.preventDefault(); if (!player.paused) player.pause(); else { chain = false; play(cur); } }
  else if (e.key === "ArrowDown") { e.preventDefault(); if (cur < D.rows.length - 1) select(cur + 1, true); }
  else if (e.key === "ArrowUp") { e.preventDefault(); if (cur > 0) select(cur - 1, true); }
  else if (e.key === "1") setStatus(cur, "ok", true);
  else if (e.key === "2") setStatus(cur, "problem", true);
  else if (e.key === "3") setStatus(cur, "drop", true);
});

$("#export").onclick = () => {
  const segments = {};
  for (const r of D.rows) segments[r.index] = {status: r.status, note: r.note, text: r.text};
  const blob = new Blob([JSON.stringify({source: D.source, exported: new Date().toISOString(), segments}, null, 2)],
                        {type: "application/json"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = D.review_file; a.click();
};

window.onresize = () => D.rows.forEach((r, i) => draw(els[i].cv, r.peaks, 0));
D.rows.forEach((r, i) => { draw(els[i].cv, r.peaks, 0); paintStatus(i); });
select(0); persist();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
