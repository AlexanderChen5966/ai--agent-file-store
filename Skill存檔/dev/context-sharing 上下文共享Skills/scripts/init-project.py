#!/usr/bin/env python3
"""
Context Sharing - 專案初始化腳本
自動生成標準化的專案文檔檔案
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


def create_file(filepath, content):
    """創建文件並寫入內容"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ 已創建: {filepath}")


def init_claude_md(project_name, tech_stack):
    """生成 CLAUDE.md"""
    return f"""# CLAUDE.md - 專案配置

> 這是專案的 AI 工具配置檔案

## 📋 專案資訊

**專案名稱：** {project_name}
**專案描述：** [請填寫專案描述]
**技術棧：** {tech_stack}
**開發階段：** MVP
**創建日期：** {datetime.now().strftime('%Y-%m-%d')}

## 🤖 AI 工具分工

### Claude Code
- 架構設計
- 代碼審查
- 技術決策

### GitHub Copilot CLI
- 快速代碼生成
- 測試撰寫
- Shell 腳本

## 🔄 標準工作流程

1. **規劃：** Claude 設計架構 → 更新 ARCHITECTURE.md
2. **實作：** Copilot 生成代碼
3. **審查：** Claude 審查品質
4. **記錄：** 更新 TASKS.md 和 DECISIONS.md

## 📚 文檔維護

- **TASKS.md：** 每日更新
- **ARCHITECTURE.md：** 架構變更時
- **DECISIONS.md：** 重要決策時

---

**維護者：** [你的名字]
**最後更新：** {datetime.now().strftime('%Y-%m-%d')}
"""


def init_tasks_md():
    """生成 TASKS.md"""
    return f"""# TASKS.md - 任務追蹤

> 追蹤專案任務和進度

## 📊 專案概覽

**當前 Sprint：** Sprint 1
**開始日期：** {datetime.now().strftime('%Y-%m-%d')}

**進度統計：**
- 總任務：0
- 已完成：0
- 進行中：0

---

## 🚧 進行中

_目前沒有進行中的任務_

---

## 📋 待辦

### #1 專案初始化

**優先級：** 🔴 高
**預估：** 1 天

**檢查清單：**
- [x] 創建專案文檔檔案
- [ ] 設定開發環境
- [ ] 建立專案結構

---

## ✅ 已完成

_目前沒有已完成的任務_

---

**最後更新：** {datetime.now().strftime('%Y-%m-%d')}
"""


def init_architecture_md(tech_stack):
    """生成 ARCHITECTURE.md"""
    return f"""# ARCHITECTURE.md - 系統架構

> 記錄系統架構和設計

## 🏗️ 系統架構概覽

### 技術棧

{tech_stack}

### 系統架構

```
[待設計]
```

---

## 📦 模組架構

### 目錄結構

```
project/
├── src/           # 源代碼
├── tests/         # 測試
└── docs/          # 文檔
```

---

## 🗄️ 資料庫設計

_待設計_

---

## 🔌 API 設計

_待設計_

---

**最後更新：** {datetime.now().strftime('%Y-%m-%d')}
"""


def init_decisions_md():
    """生成 DECISIONS.md"""
    return f"""# DECISIONS.md - 技術決策記錄

> 記錄重要的技術決策

## 📋 決策索引

| ID | 標題 | 日期 | 狀態 |
|----|------|------|------|
| #1 | [專案初始化決策](#決策-1-專案初始化決策) | {datetime.now().strftime('%Y-%m-%d')} | ✅ 已採用 |

---

## 決策 #1: 專案初始化決策

**日期：** {datetime.now().strftime('%Y-%m-%d')}
**狀態：** ✅ 已採用

### 背景

開始新專案，需要建立標準化的文檔系統。

### 決策

使用 Context Sharing Skill 建立專案文檔。

### 理由

1. 標準化文檔格式
2. 便於 AI 工具協作
3. 知識沉澱和傳承

---

**最後更新：** {datetime.now().strftime('%Y-%m-%d')}
"""


def main():
    parser = argparse.ArgumentParser(
        description='Context Sharing - 專案初始化工具'
    )
    parser.add_argument(
        '--project-name',
        required=True,
        help='專案名稱'
    )
    parser.add_argument(
        '--tech-stack',
        default='Node.js, TypeScript, PostgreSQL',
        help='技術棧 (預設: Node.js, TypeScript, PostgreSQL)'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='輸出目錄 (預設: 當前目錄)'
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 50)
    print("Context Sharing - 專案初始化")
    print("=" * 50)
    print(f"\n專案名稱: {args.project_name}")
    print(f"技術棧: {args.tech_stack}")
    print(f"輸出目錄: {output_dir.absolute()}\n")

    # 創建文件
    files = {
        'CLAUDE.md': init_claude_md(args.project_name, args.tech_stack),
        'TASKS.md': init_tasks_md(),
        'ARCHITECTURE.md': init_architecture_md(args.tech_stack),
        'DECISIONS.md': init_decisions_md()
    }

    for filename, content in files.items():
        filepath = output_dir / filename
        if filepath.exists():
            print(f"⚠ 檔案已存在，跳過: {filename}")
        else:
            create_file(filepath, content)

    print("\n" + "=" * 50)
    print("✅ 初始化完成！")
    print("=" * 50)
    print("\n下一步：")
    print("1. 編輯 CLAUDE.md 填寫專案資訊")
    print("2. 在 TASKS.md 新增你的第一個任務")
    print("3. 開始使用 AI 工具協作開發")
    print("\n使用範例：")
    print('  $ claude')
    print('  > "在 TASKS.md 新增任務：設定開發環境"')
    print()


if __name__ == '__main__':
    main()
