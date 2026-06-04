import os
import markdown
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# === 基本路徑設定 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE_DIR, "API_DOCUMENT.md")
PDF_FILE = os.path.join(BASE_DIR, "delivery_doc/washcar_api.pdf")
TEMPLATE_FILE = "template.html"

# === 讀取 Markdown 內容 ===
if not os.path.exists(MD_FILE):
    print(f"錯誤：找不到 {MD_FILE}")
    exit(1)

with open(MD_FILE, "r", encoding="utf-8") as f:
    md_text = f.read()

# 把 Markdown 轉成 HTML
html_body = markdown.markdown(
    md_text,
    extensions=[
        "extra",
        "tables",
        "fenced_code",
    ],
)

# === 使用 Jinja2 渲染 HTML 模板 ===
env = Environment(loader=FileSystemLoader(BASE_DIR))
template = env.get_template(TEMPLATE_FILE)
full_html = template.render(title="洗車 API 接口文件", content=html_body)

# === 產出 PDF ===
HTML(string=full_html, base_url=BASE_DIR).write_pdf(PDF_FILE)

print(f"已產生 PDF：{PDF_FILE}")
