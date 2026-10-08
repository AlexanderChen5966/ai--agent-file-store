#!/usr/bin/env python3
"""② 語音辨識：替每個片段配上文字，寫回 segments.json 的 "text" 欄位。

支援兩種本機後端（自動偵測，先 mlx-whisper 再 whisper.cpp）：
  - mlx-whisper：pip install mlx-whisper（Apple Silicon）
  - whisper.cpp：brew install whisper-cpp，並用 --model 指定 ggml 模型檔

國語結果若有安裝 OpenCC（pip install opencc）會自動轉台灣繁體。

用法：
  python3 transcribe.py work/ --lang en
  python3 transcribe.py work/ --lang zh --backend cpp --model ~/models/ggml-large-v3-turbo.bin
"""
import argparse
import shutil
import tempfile
from pathlib import Path

from _common import (die, load_segments, require, run, save_segments, to_traditional)

DEFAULT_MLX_MODEL = "mlx-community/whisper-large-v3-turbo"


def pick_backend(choice):
    if choice in ("mlx", "auto"):
        try:
            import mlx_whisper  # noqa: F401
            return "mlx"
        except ImportError:
            if choice == "mlx":
                die("未安裝 mlx-whisper：pip install mlx-whisper")
    if shutil.which("whisper-cli"):
        return "cpp"
    die("找不到語音辨識工具。請安裝 mlx-whisper（pip install mlx-whisper）"
        "或 whisper.cpp（brew install whisper-cpp）")


def transcribe_mlx(path, lang, model):
    import mlx_whisper
    res = mlx_whisper.transcribe(str(path), path_or_hf_repo=model or DEFAULT_MLX_MODEL,
                                 language=lang)
    return res.get("text", "")


def transcribe_cpp(path, lang, model, tmp):
    if not model:
        die("whisper.cpp 需要用 --model 指定 ggml 模型檔")
    wav = Path(tmp) / "in.wav"
    require("ffmpeg")
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(path),
         "-ar", "16000", "-ac", "1", str(wav)])
    args = ["whisper-cli", "-m", str(Path(model).expanduser()), "-f", str(wav), "-nt", "-np"]
    if lang:
        args += ["-l", lang]
    r = run(args)
    if r.returncode != 0:
        die(f"whisper-cli 失敗：\n{r.stderr[-1500:]}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser(description="替片段做語音辨識")
    ap.add_argument("work", help="split.py 的輸出資料夾")
    ap.add_argument("--lang", help="語言代碼：en、zh、ja……（不給則自動偵測，短片段容易誤判）")
    ap.add_argument("--backend", choices=["auto", "mlx", "cpp"], default="auto")
    ap.add_argument("--model", help="mlx：HF repo 名稱；cpp：ggml 模型檔路徑")
    ap.add_argument("--only", help="只辨識指定片段，如 3,7,12")
    a = ap.parse_args()

    data = load_segments(a.work)
    backend = pick_backend(a.backend)
    only = {int(x) for x in a.only.split(",")} if a.only else None
    print(f"後端：{backend}｜語言：{a.lang or '自動'}")

    with tempfile.TemporaryDirectory() as tmp:
        for seg in data["segments"]:
            if only and seg["index"] not in only:
                continue
            path = Path(a.work) / seg["file"]
            text = (transcribe_mlx(path, a.lang, a.model) if backend == "mlx"
                    else transcribe_cpp(path, a.lang, a.model, tmp))
            text = " ".join(text.split())
            if a.lang in (None, "zh"):
                text = to_traditional(text)
            seg["text"] = text
            print(f"  {seg['index']:>3}  {seg['duration']:5.2f}s  {text or '（空白）'}")
            save_segments(a.work, data)  # 每段存一次，中斷也不會全丟

    empty = [s["index"] for s in data["segments"] if not s.get("text")]
    if empty:
        print(f"⚠ 沒辨識出文字的片段（可能是雜音或太短）：{empty}")


if __name__ == "__main__":
    main()
