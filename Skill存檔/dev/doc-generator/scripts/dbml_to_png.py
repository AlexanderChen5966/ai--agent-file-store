import re
import os
import subprocess

def check_graphviz_installed():
    """檢查是否已安裝 graphviz"""
    try:
        subprocess.run(["dot", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def parse_dbml(dbml_content):
    """解析 DBML 內容，提取表和關係信息"""
    tables = {}
    relationships = []

    # Regex patterns
    table_regex = re.compile(r"Table\s+(\w+)\s+\{([^}]+)\}", re.MULTILINE | re.DOTALL)
    column_regex = re.compile(r"^\s*(\w+)\s+([\w\(\)]+)(\s+\[(.*?)\])?", re.MULTILINE)
    ref_regex = re.compile(r"Ref:\s*(\w+)\.(\w+)\s*>\s*(\w+)\.(\w+)")

    # Parse Tables
    for match in table_regex.finditer(dbml_content):
        table_name = match.group(1)
        columns_block = match.group(2)
        columns = []
        for col_match in column_regex.finditer(columns_block):
            col_name = col_match.group(1)
            col_type = col_match.group(2)
            col_props = col_match.group(4) if col_match.group(4) else ""

            is_pk = "pk" in col_props
            columns.append({
                "name": col_name,
                "type": col_type,
                "pk": is_pk
            })
        tables[table_name] = columns

    # Parse Relationships
    for match in ref_regex.finditer(dbml_content):
        relationships.append({
            "from_table": match.group(1),
            "from_col": match.group(2),
            "to_table": match.group(3),
            "to_col": match.group(4)
        })

    return tables, relationships

def generate_dot(tables, relationships):
    """生成 Graphviz DOT 格式的內容"""
    dot = "digraph DB {\n"
    dot += "    rankdir=LR;\n"
    dot += "    node [shape=none, fontname=\"Arial\"];\n"
    dot += "    edge [fontname=\"Arial\"];\n\n"

    # Generate tables
    for table_name, columns in tables.items():
        label = f'<<table border="0" cellborder="1" cellspacing="0" cellpadding="4">'
        label += f'<tr><td bgcolor="#1f4e79" align="center"><font color="white"><b>{table_name}</b></font></td></tr>'

        for col in columns:
            col_txt = f"{col['name']} : {col['type']}"
            if col['pk']:
                col_txt = f"* {col_txt}"  # Mark PK

            bg_color = "#eef4fa" if col['pk'] else "white"
            port = f' port="{col["name"]}"'
            label += f'<tr><td bgcolor="{bg_color}" align="left"{port}>{col_txt}</td></tr>'

        label += "</table>>"
        dot += f'    {table_name} [label={label}];\n'

    dot += "\n"

    # Generate relationships
    colors = ["#d9534f", "#f0ad4e", "#5bc0de", "#0275d8", "#5cb85c"]
    color_idx = 0

    for rel in relationships:
        color = colors[color_idx % len(colors)]
        # Connect specific ports
        dot += f'    {rel["from_table"]}:{rel["from_col"]} -> {rel["to_table"]}:{rel["to_col"]} [color="{color}"];\n'
        color_idx += 1

    dot += "}\n"
    return dot

def main():
    if not check_graphviz_installed():
        print("錯誤: 系統未安裝 Graphviz (dot 指令)。")
        print("請安裝 Graphviz:")
        print("  - macOS: brew install graphviz")
        print("  - Linux: sudo apt-get install graphviz")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    dbml_file = os.path.join(script_dir, "ORDER_TRADE_INVOICE_DB_DBML.md")
    output_png = os.path.join(script_dir, "delivery_doc/Table_scheme.png")

    if not os.path.exists(dbml_file):
        print(f"錯誤: 找不到 DBML 文件: {dbml_file}")
        return

    try:
        with open(dbml_file, "r", encoding="utf-8") as f:
            dbml_content = f.read()

        print("正在解析 DBML...")
        tables, relationships = parse_dbml(dbml_content)

        print("正在生成 DOT 腳本...")
        dot_content = generate_dot(tables, relationships)

        # Generate PNG using dot command
        print(f"正在生成 PNG: {output_png} ...")
        process = subprocess.Popen(
            ["dot", "-Tpng", "-o", output_png],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=dot_content.encode('utf-8'))

        if process.returncode != 0:
            print("生成 PNG 失敗:")
            print(stderr.decode('utf-8'))
        else:
            print("成功!")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
