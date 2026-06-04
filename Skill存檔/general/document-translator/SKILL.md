---
name: document-translator
version: "1.0.0"
description: Technical documentation translation system for English to Traditional Chinese. Use when users request document translation, ask to translate files in docs/en/, need help with translation modes (google/auto), want to configure proofreading backends (chatgpt/desktop/cli/manual), or need to manage glossary terms. Triggers on phrases like "translate", "翻譯", "translation", or mentions of docs/en/ files.
---

# Translator

A two-stage translation system: Google Translate for initial draft, followed by intelligent proofreading.

## Translation Flow

```
docs/en/*.md  →  Google Translate  →  Proofreader  →  docs/zh-TW/*.md
```

## Quick Reference

| Mode | Command | Use Case |
|------|---------|----------|
| Auto (recommended) | `./translation/translate.sh --mode=auto FILE` | Production docs |
| Google only | `./translation/translate.sh --mode=google FILE` | Quick drafts |

| Proofreader | Flag | Best For |
|-------------|------|----------|
| Auto-detect | (default) | General use |
| ChatGPT | `--proofreader=chatgpt` | Free, automated |
| Claude Desktop | `--proofreader=desktop` | Highest quality |
| Claude CLI | `--proofreader=cli` | CI/CD pipelines |
| Manual | `--proofreader=manual` | Full control |

## Workflow Decision Tree

```
User requests translation
    │
    ├─ Single file? ─────────────► Use --mode=auto
    │
    ├─ Multiple files? ──────────► Use --mode=auto docs/en/*.md
    │
    ├─ Quick draft needed? ──────► Use --mode=google
    │
    ├─ Important document? ──────► Use --proofreader=desktop
    │
    └─ CI/CD automation? ────────► Use --proofreader=cli
```

## Standard Workflow

### 1. Translate a File

```bash
# Recommended: auto mode with intelligent proofreading
./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md

# Fast draft: Google Translate only
./translation/translate.sh --mode=google docs/en/DRAFT.md

# High quality: Claude Desktop proofreading
./translation/translate.sh --mode=auto --proofreader=desktop docs/en/IMPORTANT.md
```

### 2. Batch Translation

```bash
# All markdown files
./translation/translate.sh --mode=auto docs/en/*.md

# Force overwrite existing translations
./translation/translate.sh --mode=auto --force docs/en/*.md

# With verbose logging
./translation/translate.sh --mode=auto --verbose docs/en/*.md
```

### 3. Verify Output

After translation, check:
- Output exists: `docs/zh-TW/<filename>.md`
- File not empty or too small
- No simplified Chinese characters (賬、數據、軟件、網絯)

## Command Reference

```
./translation/translate.sh [OPTIONS] FILE(s)

Options:
  --mode=MODE        Translation mode: google | auto (default: auto)
  --proofreader=BE   Proofreading backend: auto | chatgpt | desktop | cli | manual
  --force            Overwrite existing translations
  --verbose          Show detailed progress
  --help             Show help message
```

## Glossary Management

Location: `translation/config/glossary.json`

### Structure

```json
{
  "technical_terms": {
    "API": "API",
    "endpoint": "端點",
    "request": "請求"
  },
  "taiwan_terms": {
    "account": "帳號",
    "data": "資料",
    "software": "軟體"
  },
  "preserve": ["Claude", "GitHub", "Docker"]
}
```

### Adding Terms

1. Read current glossary: `view translation/config/glossary.json`
2. Add term to appropriate section using `str_replace`
3. Verify update

## Troubleshooting

### Translation Failed

```bash
# Reset Python environment
cd translation && rm -rf venv
./translate.sh --mode=auto docs/en/test.md
```

### Proofreader Not Found

```bash
# Use manual proofreader as fallback
./translate.sh --mode=auto --proofreader=manual docs/en/API.md
```

### ChatGPT Backend Error

```bash
# Switch to desktop or CLI
./translate.sh --mode=auto --proofreader=desktop docs/en/API.md
```

### Poor Translation Quality

1. Update glossary with correct terms
2. Use `--proofreader=desktop` for critical docs
3. Adjust `translation/config/proofreading_prompt.txt`

## Key Paths

| Resource | Path |
|----------|------|
| Translation script | `./translation/translate.sh` |
| Python main | `./translation/translate.py` |
| Glossary | `./translation/config/glossary.json` |
| Proofreading prompt | `./translation/config/proofreading_prompt.txt` |
| English source | `./docs/en/` |
| Chinese output | `./docs/zh-TW/` |

## Example Interactions

**User**: "翻譯 API 文檔"
```bash
# Execute
./translation/translate.sh --mode=auto docs/en/API_DOCUMENTATION.md
# Then present: docs/zh-TW/API_DOCUMENTATION.md
```

**User**: "翻譯所有文檔"
```bash
# List files first
ls docs/en/*.md
# Execute batch
./translation/translate.sh --mode=auto docs/en/*.md
```

**User**: "新增術語 container = 容器"
```bash
# Read, update, verify glossary.json
```

## Quality Checklist

After translation, verify:
- [ ] Output file exists in docs/zh-TW/
- [ ] File size is reasonable (not empty)
- [ ] Code blocks preserved
- [ ] Headers count matches
- [ ] Links preserved
- [ ] No simplified Chinese (賬/數據/軟件/網絡)

## References

- **Proofreader details**: See [references/proofreaders.md](references/proofreaders.md) for backend comparison, requirements, and troubleshooting
- **Configuration guide**: See [references/configuration.md](references/configuration.md) for glossary structure, prompt customization, and config options
