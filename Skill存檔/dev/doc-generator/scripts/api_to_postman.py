#!/usr/bin/env python3
# md_to_postman_with_body.py

import re
import json
import uuid
from pathlib import Path
from collections import defaultdict

# ============================
# 可以在這裡改預設檔名 & 參數
# ============================
INPUT_MD_FILE = "API_DOCUMENT.md"                  # 你的 markdown 檔
OUTPUT_POSTMAN_FILE = "delivery_doc/washcar_api.json"  # 輸出的 collection
COLLECTION_NAME = "山隆洗車機API"                   # Postman 顯示的名稱
BASE_URL_VAR = "baseUrl"
BASE_URL_DEFAULT = "http://localhost:8080"
# ============================


def parse_markdown_to_endpoints(md_text: str):
    """
    從 Markdown 中解析出 endpoint 資訊：
      - Group = 每個 "## ..." heading
      - Title = 每個 "### ..." heading
      - URL   = 行內的 **URL**: `/path`
      - Method= 行內的 **方法**: `POST`
      - Request Body = 緊接在「##### 請求 JSON 結構」或「##### 請求 JSON 範例」
                       之後的第一個 ```json ... ``` 區塊
    """
    endpoints = []

    current_group = None
    current_section = None
    last_endpoint = None

    expect_request_code_block = False
    in_request_code_block = False
    request_json_lines = []

    lines = md_text.splitlines()

    for line in lines:
        # ====== Group: "## 2. 用戶身份查詢 API ..." ======
        m2 = re.match(r'^##\s+(.*)', line)
        if m2:
            current_group = m2.group(1).strip()
            current_section = None
            last_endpoint = None
            continue

        # ====== Endpoint title: "### 2.1 綜合車牌檢查" ======
        m3 = re.match(r'^###\s+(.*)', line)
        if m3:
            current_section = m3.group(1).strip()
            last_endpoint = None
            continue

        # ====== 找到「##### 請求 JSON 結構 / 範例」 → 準備讀 code block ======
        if re.match(r'^#####\s*請求 JSON\s*(結構|範例)', line):
            expect_request_code_block = True
            in_request_code_block = False
            request_json_lines = []
            continue

        # ====== 處理請求的 JSON code block ======
        if expect_request_code_block and line.strip().startswith("```"):
            # 看到 ```json 或 ``` 就開始收集
            in_request_code_block = True
            expect_request_code_block = False
            continue

        if in_request_code_block:
            # 結束 ``` -> 把 body 存入 endpoint
            if line.strip().startswith("```"):
                in_request_code_block = False
                if last_endpoint is not None:
                    body_str = "\n".join(request_json_lines).strip()
                    last_endpoint["request_body"] = body_str
                request_json_lines = []
            else:
                request_json_lines.append(line)
            continue

        # 其他地方的 ``` (例如響應 JSON) 一律略過
        if line.strip().startswith("```"):
            continue

        # ====== URL 行 ======
        # 例如：*   **URL**: `/api/v1/washcar/account/checkPlateStatus`
        m_url = re.search(r'\*\s*\*\*URL\*\*:\s*`([^`]+)`', line)
        if m_url and current_section:
            url_path = m_url.group(1).strip()
            ep = {
                "group": current_group or "Default",
                "title": current_section,
                "url": url_path,
                "method": None,
                "request_body": None,
            }
            endpoints.append(ep)
            last_endpoint = ep
            continue

        # ====== 方法 行 ======
        # 例如：*   **方法**: `POST`
        m_method = re.search(r'\*\s*\*\*方法\*\*:\s*`?([A-Z]+)`?', line)
        if m_method:
            method = m_method.group(1).strip().upper()
            if last_endpoint is not None and last_endpoint["method"] is None:
                last_endpoint["method"] = method
            continue

    return endpoints


def build_postman_collection(
    endpoints,
    collection_name=COLLECTION_NAME,
    base_url_var=BASE_URL_VAR,
    base_url_default=BASE_URL_DEFAULT,
):
    """
    建立 Postman Collection v2.1 JSON 結構
    """
    collection = {
        "info": {
            "name": collection_name,
            "_postman_id": str(uuid.uuid4()),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [],
        "variable": [
            {"key": base_url_var, "value": base_url_default}
        ],
    }

    grouped = defaultdict(list)
    for ep in endpoints:
        grouped[ep["group"]].append(ep)

    for group_name, eps in grouped.items():
        folder = {
            "name": group_name,
            "item": [],
        }

        for ep in eps:
            # 拆 URL 變成 path segments
            path = ep["url"].lstrip("/")
            path_segments = [seg for seg in path.split("/") if seg]

            request = {
                "method": ep["method"] or "POST",
                "header": [
                    {"key": "Content-Type", "value": "application/json"}
                ],
                "url": {
                    "raw": "{{%s}}%s" % (base_url_var, ep["url"]),
                    "host": ["{{%s}}" % base_url_var],
                    "path": path_segments,
                },
            }

            # 如果有解析到請求 JSON 結構，就塞到 raw body
            if ep.get("request_body"):
                request["body"] = {
                    "mode": "raw",
                    "raw": ep["request_body"],
                    "options": {"raw": {"language": "json"}},
                }

            item = {
                "name": ep["title"],
                "request": request,
                "response": [],
            }
            folder["item"].append(item)

        collection["item"].append(folder)

    return collection


def md_to_postman(
    input_md: str = INPUT_MD_FILE,
    output_json: str = OUTPUT_POSTMAN_FILE,
    base_url_var: str = BASE_URL_VAR,
    base_url_default: str = BASE_URL_DEFAULT,
):
    md_path = Path(input_md)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    md_text = md_path.read_text(encoding="utf-8")
    endpoints = parse_markdown_to_endpoints(md_text)

    if not endpoints:
        raise RuntimeError("No endpoints found in markdown (no **URL** / **方法** blocks detected).")

    collection = build_postman_collection(
        endpoints,
        collection_name=COLLECTION_NAME,
        base_url_var=base_url_var,
        base_url_default=base_url_default,
    )

    out_path = Path(output_json)
    out_path.write_text(
        json.dumps(collection, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("✅ Generated Postman collection:")
    print(f"   File          : {out_path}")
    print(f"   Collection    : {COLLECTION_NAME}")
    print(f"   Endpoints     : {len(endpoints)}")


if __name__ == "__main__":
    # 直接用上面的預設變數
    md_to_postman()
