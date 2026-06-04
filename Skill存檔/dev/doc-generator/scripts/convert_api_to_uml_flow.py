#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

# ========= Input / Output =========
MD_FILE = Path("API_DOCUMENT.md")  # ✅ 唯一資料來源

OUT_DIR = Path("delivery_doc")
UML_FILE = OUT_DIR / "Wash_Car_API_Flow.puml"
PNG_FILE = OUT_DIR / "Wash_Car_API_Flow.png"

# ========= PNG 固定尺寸 =========
TARGET_W = 1024
TARGET_H = 768
RESIZE_MODE = "contain"   # "contain"(不裁切補白) / "cover"(填滿裁切)
ALLOW_UPSCALE = True      # contain 時允許放大（字更大，但可能略糊）


# ========= Markdown 解析 =========
URL_PAT = re.compile(r"\*\s*\*\*URL\*\*:\s*`([^`]+)`")
METHOD_PAT = re.compile(r"\*\s*\*\*(方法|Method)\*\*:\s*`?([A-Z]+)`?", re.I)
CODE_FENCE_PAT = re.compile(r"^\s*```")

# 兼容常見的「請求/響應」標題寫法
REQ_HDR_PAT = re.compile(r"^#{3,6}\s*(請求|Request)\s*(JSON)?\s*(結構|範例|示例|Example|Body)?", re.I)
RESP_HDR_PAT = re.compile(r"^#{3,6}\s*(響應|回應|Response)\s*(JSON)?\s*(結構|範例|示例|Example|Body)?", re.I)


def parse_markdown_to_endpoints(md_text: str) -> List[Dict]:
    """
    解析 md，抓 endpoints（依 md 出現順序）：
    - group: ## ...
    - title: ### ...
    - url/method: **URL** / **方法**
    - request_body/response_body: 對應標題下的 code block（若有）
    """
    endpoints: List[Dict] = []
    current_group: Optional[str] = None
    current_section: Optional[str] = None
    last_endpoint: Optional[Dict] = None

    expect_code: Optional[str] = None  # None / "request" / "response"
    in_code = False
    code_lines: List[str] = []

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip("\n")

        m2 = re.match(r"^##\s+(.*)", line)
        if m2:
            current_group = m2.group(1).strip()
            current_section = None
            last_endpoint = None
            continue

        m3 = re.match(r"^###\s+(.*)", line)
        if m3:
            current_section = m3.group(1).strip()
            last_endpoint = None
            continue

        if REQ_HDR_PAT.match(line.strip()):
            expect_code = "request"
            continue
        if RESP_HDR_PAT.match(line.strip()):
            expect_code = "response"
            continue

        if expect_code and CODE_FENCE_PAT.match(line.strip()) and not in_code:
            in_code = True
            code_lines = []
            continue

        if in_code:
            if CODE_FENCE_PAT.match(line.strip()):
                in_code = False
                body = "\n".join(code_lines).strip()
                if last_endpoint is not None and expect_code:
                    if expect_code == "request":
                        last_endpoint["request_body"] = body
                    else:
                        last_endpoint["response_body"] = body
                expect_code = None
                code_lines = []
            else:
                code_lines.append(line)
            continue

        # 其他 code fence 不處理
        if CODE_FENCE_PAT.match(line.strip()):
            continue

        m_url = URL_PAT.search(line)
        if m_url and current_section:
            url_path = m_url.group(1).strip()
            ep = {
                "group": current_group or "Default",
                "title": current_section,
                "url": url_path,
                "method": None,
                "request_body": None,
                "response_body": None,
            }
            endpoints.append(ep)
            last_endpoint = ep
            continue

        m_method = METHOD_PAT.search(line)
        if m_method and last_endpoint is not None and last_endpoint["method"] is None:
            last_endpoint["method"] = m_method.group(2).strip().upper()
            continue

    return endpoints


def _escape_for_plantuml(text: str) -> str:
    """
    避免 PlantUML 因為特殊字元（尤其反斜線）炸掉。
    """
    if text is None:
        return ""
    # PlantUML/Java 解析上，反斜線最容易造成問題
    text = text.replace("\\", "\\\\")
    # 去掉不可見控制字元
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)
    return text


def json_one_line(text: Optional[str], max_len: int = 240) -> str:
    """
    將 md 裡的 request/response JSON 壓成單行 + 截斷（避免圖太大 or PlantUML 爆掉）。
    """
    if not text:
        return "{ }"
    s = text.strip()

    try:
        obj = json.loads(s)
        s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        s = re.sub(r"\s+", " ", s).strip()
        if not s:
            s = "{ }"

    s = _escape_for_plantuml(s)
    if len(s) > max_len:
        s = s[: max_len - 3] + "..."
    return s


# ========= 產生「所有 API 都在同一張」PUML =========
def build_all_apis_puml(endpoints: List[Dict]) -> str:
    if not endpoints:
        raise ValueError("Markdown 沒解析到任何 endpoint（請確認有 **URL** 與 **方法**）。")

    lines: List[str] = []
    lines.append("@startuml")
    lines.append("title 洗車 API - 全端點調用列表（由 API_DOCUMENT.md 自動產生）")
    lines.append("")
    lines.append('actor Client as "客戶端 (洗車機/POS)"')
    lines.append('participant Server as "SmartApp 伺服器"')
    lines.append("")
    lines.append('box "通用流程 / 全端點"')
    lines.append("autonumber")
    lines.append("")

    current_group = None

    for ep in endpoints:
        group = ep.get("group") or "Default"
        title = (ep.get("title") or "").replace('"', "'")
        method = (ep.get("method") or "POST").upper()
        url = ep.get("url") or ""

        req = json_one_line(ep.get("request_body"), max_len=260)
        resp = json_one_line(ep.get("response_body"), max_len=260) if ep.get("response_body") else "{ ... }"

        if group != current_group:
            current_group = group
            lines.append(f"== {current_group} ==")

        lines.append(f"note right of Client: {title}")
        lines.append(f"Client -> Server: {method} {url}\\n{req}")
        lines.append("activate Server")
        lines.append(f"Server --> Client: Result \\n{resp}")
        lines.append("deactivate Server")
        lines.append("")

    lines.append("end box")
    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


# ========= PlantUML 產 PNG + 固定 1024x768 =========
def run_plantuml_to_png(puml_path: Path) -> Path:
    """
    產生 puml 同名 png，失敗時把 stderr 印出來。
    """
    cmd = ["plantuml", "-charset", "UTF-8", "-tpng", str(puml_path)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            "plantuml 執行失敗\n"
            f"cmd: {cmd}\n"
            f"returncode: {p.returncode}\n"
            f"stdout:\n{p.stdout}\n"
            f"stderr:\n{p.stderr}\n"
        )
    raw_png = puml_path.with_suffix(".png")
    if not raw_png.exists():
        raise FileNotFoundError(f"PlantUML 未產生 png：{raw_png}")
    return raw_png


def to_fixed_png(src_png: Path, dst_png: Path, w: int, h: int, mode: str, allow_upscale: bool):
    from PIL import Image

    img = Image.open(src_png).convert("RGBA")
    iw, ih = img.size

    if mode == "contain":
        scale = min(w / iw, h / ih)
        if not allow_upscale:
            scale = min(scale, 1.0)
        nw, nh = max(1, int(round(iw * scale))), max(1, int(round(ih * scale)))
        img2 = img.resize((nw, nh), Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        x = (w - nw) // 2
        y = (h - nh) // 2
        canvas.paste(img2, (x, y), img2)

    elif mode == "cover":
        scale = max(w / iw, h / ih)
        nw, nh = max(1, int(round(iw * scale))), max(1, int(round(ih * scale)))
        img2 = img.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - w) // 2
        top = (nh - h) // 2
        canvas = img2.crop((left, top, left + w, top + h))
    else:
        raise ValueError("mode must be 'contain' or 'cover'")

    dst_png.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(dst_png, "PNG")


def main():
    if not MD_FILE.exists():
        print(f"❌ 找不到 Markdown：{MD_FILE.resolve()}")
        return

    md_text = MD_FILE.read_text(encoding="utf-8")
    endpoints = parse_markdown_to_endpoints(md_text)

    if not endpoints:
        print("❌ 沒解析到 endpoint，請確認 md 內有 '**URL**: `...`' 與 '**方法**: `POST`'")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) 產生單一 puml（全部 API）
    puml_text = build_all_apis_puml(endpoints)
    UML_FILE.write_text(puml_text, encoding="utf-8")
    print(f"✅ 已輸出 PUML：{UML_FILE.resolve()}")

    # 2) PlantUML 產 raw png
    raw_png = run_plantuml_to_png(UML_FILE)

    # 保留 raw
    raw_keep = raw_png.with_name(f"{raw_png.stem}_raw.png")
    shutil.copy2(raw_png, raw_keep)

    # 3) 轉固定 1024x768
    to_fixed_png(raw_png, PNG_FILE, TARGET_W, TARGET_H, RESIZE_MODE, ALLOW_UPSCALE)
    print(f"✅ 已輸出 PNG：{PNG_FILE.resolve()} ({TARGET_W}x{TARGET_H})")
    print(f"🗂️  原始 PNG：{raw_keep.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ 缺少 Pillow：python -m pip install pillow")
    except Exception as e:
        print("❌ 錯誤：")
        print(e)
