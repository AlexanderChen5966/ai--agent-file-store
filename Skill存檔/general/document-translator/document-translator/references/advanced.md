# 進階功能指南

## 目錄

- [自訂校稿提示詞](#自訂校稿提示詞)
- [術語表管理](#術語表管理)
- [多語言支援](#多語言支援)
- [效能調校](#效能調校)
- [擴展開發](#擴展開發)

---

## 自訂校稿提示詞

### 提示詞位置

`scripts/config/proofreading_prompt.txt`

### 提示詞結構

```
[角色定義]
[品質要求]
[格式要求]
[輸出要求]
```

### 針對不同文檔類型的提示詞

#### API 文檔專用

```
你是 API 文檔翻譯專家。請確保：

1. HTTP 方法（GET, POST, PUT, DELETE）保持原文
2. 狀態碼（200, 404, 500）保持原文
3. 請求/回應範例中的 JSON 結構不變
4. endpoint 路徑保持原文
5. 參數名稱保持原文，說明翻譯為中文
```

#### 使用者指南專用

```
你是使用者體驗文案專家。請確保：

1. 使用親切、易懂的語氣
2. 步驟說明清晰明確
3. 按鈕名稱與實際 UI 一致
4. 避免技術術語，或加上解釋
```

### 動態載入提示詞

可以根據檔案類型載入不同提示詞：

```python
def get_prompt_for_file(file_path: str) -> str:
    if 'api' in file_path.lower():
        return load_prompt('api_prompt.txt')
    elif 'guide' in file_path.lower():
        return load_prompt('guide_prompt.txt')
    else:
        return load_prompt('default_prompt.txt')
```

---

## 術語表管理

### 術語表結構

```json
{
  "technical_terms": {},    // 技術術語（英文→中文）
  "taiwan_terms": {},       // 臺灣用語偏好
  "preserve": []            // 保持原文的詞彙
}
```

### 批量新增術語

```python
import json

def add_terms(glossary_path: str, terms: dict, category: str):
    with open(glossary_path, 'r') as f:
        glossary = json.load(f)

    glossary[category].update(terms)

    with open(glossary_path, 'w') as f:
        json.dump(glossary, f, ensure_ascii=False, indent=2)

# 使用範例
add_terms('config/glossary.json', {
    'microservice': '微服務',
    'serverless': '無伺服器',
    'containerization': '容器化'
}, 'technical_terms')
```

### 從現有翻譯提取術語

```python
import re
from collections import Counter

def extract_potential_terms(en_file: str, zh_file: str) -> list:
    """從已翻譯的文檔中提取潛在術語"""
    with open(en_file) as f:
        en_text = f.read()
    with open(zh_file) as f:
        zh_text = f.read()

    # 找出英文中的技術術語（首字母大寫或全大寫）
    en_terms = re.findall(r'\b[A-Z][a-zA-Z]+\b|\b[A-Z]{2,}\b', en_text)
    term_counts = Counter(en_terms)

    # 返回出現次數 > 2 的術語
    return [(term, count) for term, count in term_counts.most_common() if count > 2]
```

### 術語表版本控制

建議將術語表納入版本控制：

```bash
# 術語表變更時
git add scripts/config/glossary.json
git commit -m "chore: 更新術語表 - 新增 Kubernetes 相關術語"
```

---

## 多語言支援

### 目前支援

- 英文 (en) → 繁體中文 (zh-TW)

### 擴展到其他語言

#### 1. 修改配置

```json
{
  "language_pairs": [
    {"source": "en", "target": "zh-TW"},
    {"source": "en", "target": "ja"},
    {"source": "en", "target": "ko"}
  ]
}
```

#### 2. 建立語言專用術語表

```
config/
├── glossary_zh-TW.json
├── glossary_ja.json
└── glossary_ko.json
```

#### 3. 建立語言專用校稿提示詞

```
config/
├── proofreading_prompt_zh-TW.txt
├── proofreading_prompt_ja.txt
└── proofreading_prompt_ko.txt
```

#### 4. 修改目錄結構

```
docs/
├── en/           # 英文（來源）
├── zh-TW/        # 繁體中文
├── ja/           # 日文
└── ko/           # 韓文
```

---

## 效能調校

### Google Translate 優化

#### 分段策略

```python
# config/translation_config.json
{
  "google_translate": {
    "chunk_size": 5000,           # 每段最大字元數
    "delay_between_chunks_ms": 100, # 段落間延遲
    "max_concurrent_requests": 3   # 最大並行請求
  }
}
```

#### 快取策略

```python
import hashlib
import json
from pathlib import Path

CACHE_DIR = Path('.translation_cache')

def get_cached_translation(text: str, target_lang: str) -> str | None:
    """從快取取得翻譯"""
    cache_key = hashlib.md5(f"{text}{target_lang}".encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)['translation']
    return None

def cache_translation(text: str, target_lang: str, translation: str):
    """儲存翻譯到快取"""
    CACHE_DIR.mkdir(exist_ok=True)
    cache_key = hashlib.md5(f"{text}{target_lang}".encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.json"

    with open(cache_file, 'w') as f:
        json.dump({
            'source': text,
            'target_lang': target_lang,
            'translation': translation
        }, f, ensure_ascii=False)
```

### 批量處理優化

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def translate_files_parallel(files: list, max_workers: int = 3):
    """並行翻譯多個檔案"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, translate_file, f)
            for f in files
        ]
        results = await asyncio.gather(*tasks)
    return results
```

---

## 擴展開發

### 新增校稿後端

1. **建立新的 Proofreader 類別**

```python
# translator/my_proofreader.py
from .base_proofreader import BaseProofreader

class MyProofreader(BaseProofreader):

    @property
    def name(self) -> str:
        return "my_proofreader"

    @property
    def priority(self) -> int:
        return 25  # 設定優先順序

    def is_available(self) -> bool:
        # 檢查是否可用
        return True

    def proofread(self, text: str, prompt: str) -> str | None:
        # 實作校稿邏輯
        pass
```

2. **註冊到工廠**

```python
# translator/proofreader_factory.py
from .my_proofreader import MyProofreader

# 在 _init_proofreaders 中加入
cls._proofreaders.append(MyProofreader(verbose=verbose))
```

### 新增驗證規則

```python
# translator/validator.py

class TranslationValidator:
    def _check_custom_rule(self, translation: str) -> list:
        """自訂驗證規則"""
        issues = []

        # 範例：檢查是否有未翻譯的英文句子
        import re
        english_sentences = re.findall(r'[A-Z][a-z]+ [a-z]+ [a-z]+', translation)
        if len(english_sentences) > 5:
            issues.append(f"發現 {len(english_sentences)} 個可能未翻譯的英文句子")

        return issues
```

### 新增輸出格式

```python
# 支援輸出為其他格式

def export_translation(source: str, translation: str, format: str) -> str:
    if format == 'json':
        return json.dumps({
            'source': source,
            'translation': translation
        }, ensure_ascii=False)
    elif format == 'xliff':
        return generate_xliff(source, translation)
    else:
        return translation
```
