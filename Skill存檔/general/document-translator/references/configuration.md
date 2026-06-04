# Configuration Reference

Detailed configuration options for the translation system.

## Table of Contents

1. [Glossary Configuration](#glossary-configuration)
2. [Proofreading Prompt](#proofreading-prompt)
3. [Translation Config](#translation-config)

## Glossary Configuration

Location: `translation/config/glossary.json`

### Full Structure

```json
{
  "technical_terms": {
    "API": "API",
    "endpoint": "端點",
    "request": "請求",
    "response": "回應",
    "authentication": "身份驗證",
    "authorization": "授權",
    "token": "權杖",
    "header": "標頭",
    "payload": "酬載",
    "schema": "綱要",
    "query": "查詢",
    "mutation": "變更",
    "callback": "回呼",
    "middleware": "中介軟體",
    "framework": "框架",
    "library": "函式庫",
    "module": "模組",
    "package": "套件",
    "dependency": "相依套件",
    "runtime": "執行環境",
    "container": "容器",
    "instance": "實例",
    "cluster": "叢集"
  },
  
  "taiwan_terms": {
    "account": "帳號",
    "data": "資料",
    "software": "軟體",
    "network": "網路",
    "information": "資訊",
    "video": "影片",
    "file": "檔案",
    "memory": "記憶體",
    "printer": "印表機",
    "mouse": "滑鼠",
    "default": "預設"
  },
  
  "preserve": [
    "Claude",
    "Anthropic",
    "GitHub",
    "GitLab",
    "Docker",
    "Kubernetes",
    "AWS",
    "GCP",
    "Azure",
    "Linux",
    "macOS",
    "Windows",
    "Python",
    "JavaScript",
    "TypeScript",
    "JSON",
    "YAML",
    "Markdown",
    "API",
    "URL",
    "HTTP",
    "HTTPS",
    "REST",
    "GraphQL"
  ]
}
```

### Section Descriptions

| Section | Purpose | Example |
|---------|---------|---------|
| `technical_terms` | Tech vocabulary translations | endpoint → 端點 |
| `taiwan_terms` | Taiwan vs China differences | 資料 vs 數據 |
| `preserve` | Keep original, don't translate | Claude, GitHub |

### Adding New Terms

**Via Claude:**
1. User: "新增術語 webhook = 網頁鉤子"
2. Claude reads glossary
3. Claude adds to appropriate section
4. Claude verifies update

**Manual:**
```bash
# Edit directly
vim translation/config/glossary.json
```

### Taiwan vs Simplified Chinese

Always use Taiwan Traditional Chinese terms:

| Taiwan (✓) | Simplified (✗) | English |
|------------|----------------|---------|
| 帳號 | 賬號 | account |
| 資料 | 數據 | data |
| 軟體 | 軟件 | software |
| 網路 | 網絡 | network |
| 資訊 | 信息 | information |
| 影片 | 視頻 | video |
| 檔案 | 文件 | file |
| 記憶體 | 內存 | memory |
| 印表機 | 打印機 | printer |
| 滑鼠 | 鼠標 | mouse |
| 預設 | 默認 | default |

## Proofreading Prompt

Location: `translation/config/proofreading_prompt.txt`

### Default Prompt Structure

```
你是一位專業的技術文檔翻譯校稿員。請校對以下由 Google 翻譯產生的繁體中文譯文。

校稿規則：
1. 使用台灣繁體中文用語（帳號、資料、軟體、網路）
2. 保持技術術語一致性
3. 保留所有程式碼區塊不變
4. 保留所有 Markdown 格式
5. 保留所有連結
6. 確保句子通順自然

術語表：
{glossary}

原文摘要：
{summary}

請校對以下譯文：
{translated_text}
```

### Customization Tips

**Adjust tone:**
```
# More formal
風格：正式技術文檔

# More casual
風格：開發者部落格
```

**Add domain-specific rules:**
```
領域特定規則：
- "deployment" 一律翻譯為「部署」
- "pipeline" 一律翻譯為「管線」
```

## Translation Config

Location: `translation/config/translation_config.json`

### Structure

```json
{
  "source_language": "en",
  "target_language": "zh-TW",
  "source_dir": "docs/en",
  "target_dir": "docs/zh-TW",
  
  "google_translate": {
    "enabled": true,
    "timeout": 30
  },
  
  "proofreading": {
    "enabled": true,
    "default_backend": "auto"
  },
  
  "validation": {
    "check_code_blocks": true,
    "check_headers": true,
    "check_links": true,
    "check_simplified_chinese": true
  },
  
  "file_patterns": {
    "include": ["*.md"],
    "exclude": ["README.md", "CHANGELOG.md"]
  }
}
```

### Options Explained

| Option | Description | Default |
|--------|-------------|---------|
| `source_language` | Source language code | "en" |
| `target_language` | Target language code | "zh-TW" |
| `source_dir` | Source documents directory | "docs/en" |
| `target_dir` | Output directory | "docs/zh-TW" |
| `google_translate.timeout` | API timeout in seconds | 30 |
| `proofreading.default_backend` | Default proofreader | "auto" |
| `validation.check_simplified_chinese` | Check for wrong characters | true |
