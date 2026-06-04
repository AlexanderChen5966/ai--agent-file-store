# Cross Platform Archive Agent Skill 規格文件

## 1. Skill Meta

``` yaml
meta:
  name: cross-platform-archive-agent
  description: >
    Generate optimal compression commands based on target extraction platform.
    Automatically excludes OS-specific metadata and system junk files.
    Supports macOS, Windows, and Linux as both build and target platforms.
  version: 1.0.0
  author: internal
  license: MIT
  tags:
    - archive
    - zip
    - tar
    - cross-platform
    - packaging
  triggers:
    - 壓縮
    - 打包
    - archive
    - zip
    - tar
```

------------------------------------------------------------------------

## 2. Skill 目的

此 Skill 負責：

1.  接收壓縮需求（自然語言）
2.  自動偵測 build platform（優先順序：使用者明確指定 → 從對話上下文推斷 → 主動詢問使用者）
3.  接收 target extraction platform（使用者指定）
4.  根據 target 平台決定最佳壓縮格式
5.  套用跨平台 ignore 規則
6.  產生最安全的 CLI 壓縮指令
7.  支援 dry-run 模式

------------------------------------------------------------------------

## 3. 壓縮格式決策規則

  Target Platform   推薦格式
  ----------------- ----------
  windows           zip
  macos             tar.gz
  linux             tar.gz

### 輸出檔名規則

    輸出檔名 = basename(path) + 對應副檔名

範例：`./project` → `project.zip`，`./src/` → `src.tar.gz`

------------------------------------------------------------------------

## 4. Ignore 規則

``` yaml
ignore_rules:
  macos:
    - .DS_Store
    - __MACOSX
    - ._*
  windows:
    - Thumbs.db
    - Desktop.ini
  linux:
    - .directory
    - .Trash-*
  common:
    - .git
    - .gitignore
    - .env
```

### Ignore 組合邏輯

    excludes =
      common
    + 所有「非 target_platform」的 OS 垃圾檔

### Pattern 語法說明

| 工具 | 寫法 | 說明 |
|------|------|------|
| zip  | `-x "**/pattern"` | 需加 `**/` 前綴以遞迴比對子目錄 |
| tar  | `--exclude='pattern'` | 預設比對任意深度的檔名，無需路徑前綴 |

目錄排除：zip 用 `**/.git/**`（含內容），tar 用 `--exclude='.git'`（整個目錄）

------------------------------------------------------------------------

## 5. 自然語言指令設計

    壓縮 <路徑>
    壓縮 <路徑> 成 zip
    壓縮 <路徑> 成 tar.gz
    壓縮 <路徑>，解壓平台是 windows
    壓縮 <路徑>，給 linux 用
    模擬壓縮 <路徑>

------------------------------------------------------------------------

## 6. Examples

### 範例 1

使用者輸入：

    壓縮 ./project，解壓平台是 windows

輸出指令：

``` bash
zip -r project.zip project \
  -x "**/.DS_Store" \
  -x "**/__MACOSX/**" \
  -x "**/._*" \
  -x "**/.directory" \
  -x "**/.Trash-*" \
  -x "**/.git/**" \
  -x "**/.gitignore" \
  -x "**/.env"
```

------------------------------------------------------------------------

### 範例 2

使用者輸入：

    壓縮 ./src，給 linux 用

輸出指令：

``` bash
tar \
  --exclude='.DS_Store' \
  --exclude='__MACOSX' \
  --exclude='._*' \
  --exclude='Thumbs.db' \
  --exclude='Desktop.ini' \
  --exclude='.git' \
  --exclude='.gitignore' \
  --exclude='.env' \
  -czf src.tar.gz src
```

------------------------------------------------------------------------

## 7. Dry Run 設計

若偵測到以下關鍵字：

-   模擬
-   dry-run
-   不要真的壓縮

則僅輸出排除清單，不產生壓縮指令。

------------------------------------------------------------------------

## 8. 核心邏輯範例

``` python
def resolve_strategy(build_os, target_os):
    format_map = {
        "windows": "zip",
        "macos": "tar.gz",
        "linux": "tar.gz"
    }

    ignore_rules = {
        "macos": [".DS_Store", "__MACOSX", "._*"],
        "windows": ["Thumbs.db", "Desktop.ini"],
        "linux": [".directory", ".Trash-*"],
        "common": [".git", ".gitignore", ".env"]
    }

    archive_format = format_map[target_os]

    excludes = set(ignore_rules["common"])

    for os_name, rules in ignore_rules.items():
        if os_name != target_os:
            excludes.update(rules)

    return archive_format, list(excludes)
```

------------------------------------------------------------------------

## 9. 未來版本規劃

  版本    功能
  ------- -------------------------
  1.1.0   支援 .compressignore
  1.2.0   支援 7z auto-detect
  2.0.0   支援 CI/CD release mode

------------------------------------------------------------------------

## 10. 結論

此 Agent Skill 透過 target-based 策略：

-   自動選擇最佳壓縮格式
-   自動排除跨平台垃圾檔
-   支援乾淨發佈流程
-   可整合至 CI/CD pipeline

版本：1.0.0
