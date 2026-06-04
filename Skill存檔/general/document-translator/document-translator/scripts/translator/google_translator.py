"""
Google Translator - 使用 Google Translate 進行粗翻
"""

import re
from typing import Optional


class GoogleTranslator:
    """Google Translate 翻譯器"""

    def __init__(self, glossary: dict = None, verbose: bool = False):
        self.glossary = glossary or {}
        self.verbose = verbose
        self._translator = None

    def _get_translator(self):
        """延遲載入翻譯器（優先使用 deep-translator，備案 googletrans）"""
        if self._translator is None:
            # 優先嘗試 deep-translator（支援 Python 3.13+）
            try:
                from deep_translator import GoogleTranslator as DeepGoogleTranslator
                self._translator = DeepGoogleTranslator(source='auto', target='zh-TW')
                self._translator_type = 'deep'
                return self._translator
            except ImportError:
                pass

            # 備案：googletrans（可能在舊版 Python 上工作）
            try:
                from googletrans import Translator
                self._translator = Translator()
                self._translator_type = 'googletrans'
            except ImportError:
                raise ImportError(
                    "請安裝翻譯套件: pip install deep-translator\n"
                    "或: pip install googletrans==4.0.0-rc1"
                )
        return self._translator

    def _log(self, message: str):
        """輸出詳細日誌"""
        if self.verbose:
            print(f"  [GoogleTranslator] {message}")

    def _protect_code_blocks(self, text: str) -> tuple[str, dict]:
        """保護程式碼區塊不被翻譯"""
        placeholders = {}
        counter = 0

        # 保護程式碼區塊 ```...```
        def replace_code_block(match):
            nonlocal counter
            placeholder = f"__CODE_BLOCK_{counter}__"
            placeholders[placeholder] = match.group(0)
            counter += 1
            return placeholder

        text = re.sub(r"```[\s\S]*?```", replace_code_block, text)

        # 保護行內程式碼 `...`
        def replace_inline_code(match):
            nonlocal counter
            placeholder = f"__INLINE_CODE_{counter}__"
            placeholders[placeholder] = match.group(0)
            counter += 1
            return placeholder

        text = re.sub(r"`[^`]+`", replace_inline_code, text)

        # 保護連結 [text](url)
        def replace_link(match):
            nonlocal counter
            placeholder = f"__LINK_{counter}__"
            placeholders[placeholder] = match.group(0)
            counter += 1
            return placeholder

        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", replace_link, text)

        # 保護需要保持原文的詞彙
        preserve_terms = self.glossary.get("preserve", [])
        for term in preserve_terms:
            if term in text:
                placeholder = f"__PRESERVE_{term}__"
                placeholders[placeholder] = term
                text = text.replace(term, placeholder)

        return text, placeholders

    def _restore_protected(self, text: str, placeholders: dict) -> str:
        """還原被保護的內容"""
        for placeholder, original in placeholders.items():
            text = text.replace(placeholder, original)
        return text

    def _apply_glossary(self, text: str) -> str:
        """套用術語表替換"""
        # 技術術語
        for en, zh in self.glossary.get("technical_terms", {}).items():
            # 只替換獨立的詞（避免部分匹配）
            pattern = rf"\b{re.escape(en)}\b"
            text = re.sub(pattern, zh, text, flags=re.IGNORECASE)

        # 臺灣用語（修正簡體→繁體）
        taiwan_corrections = {
            "数据": "資料",
            "软件": "軟體",
            "网络": "網路",
            "账号": "帳號",
            "账户": "帳戶",
            "视频": "影片",
            "信息": "訊息",
            "服务器": "伺服器",
            "内存": "記憶體",
            "硬盘": "硬碟",
            "文件夹": "資料夾",
            "窗口": "視窗",
            "默认": "預設",
            "支持": "支援",
        }

        for simplified, traditional in taiwan_corrections.items():
            text = text.replace(simplified, traditional)

        # 使用者自訂的臺灣用語
        for en, zh in self.glossary.get("taiwan_terms", {}).items():
            text = text.replace(en, zh)

        return text

    def translate(self, text: str, source_lang: str = "en", target_lang: str = "zh-TW") -> Optional[str]:
        """
        翻譯文本

        Args:
            text: 要翻譯的文本
            source_lang: 來源語言 (預設: en)
            target_lang: 目標語言 (預設: zh-TW)

        Returns:
            翻譯後的文本，失敗時返回 None
        """
        if not text or not text.strip():
            return text

        self._log(f"開始翻譯 ({len(text)} 字元)")

        try:
            # 保護特殊內容
            protected_text, placeholders = self._protect_code_blocks(text)
            self._log(f"保護了 {len(placeholders)} 個區塊")

            # 分段翻譯（避免超過 API 限制）
            translator = self._get_translator()

            # 按段落分割
            paragraphs = protected_text.split("\n\n")
            translated_paragraphs = []

            for i, para in enumerate(paragraphs):
                if para.strip():
                    # 跳過只有佔位符的段落
                    if re.match(r"^__[A-Z_]+_\d+__$", para.strip()):
                        translated_paragraphs.append(para)
                        continue

                    try:
                        # 根據翻譯器類型使用不同的 API
                        if getattr(self, '_translator_type', 'googletrans') == 'deep':
                            # deep-translator API
                            result = translator.translate(para)
                            translated_paragraphs.append(result)
                        else:
                            # googletrans API
                            result = translator.translate(para, src=source_lang, dest=target_lang)
                            translated_paragraphs.append(result.text)
                        self._log(f"段落 {i + 1}/{len(paragraphs)} 完成")
                    except Exception as e:
                        self._log(f"段落 {i + 1} 翻譯失敗: {e}")
                        translated_paragraphs.append(para)
                else:
                    translated_paragraphs.append(para)

            translated_text = "\n\n".join(translated_paragraphs)

            # 還原被保護的內容
            translated_text = self._restore_protected(translated_text, placeholders)

            # 套用術語表
            translated_text = self._apply_glossary(translated_text)

            self._log("翻譯完成")
            return translated_text

        except Exception as e:
            self._log(f"翻譯錯誤: {e}")
            return None
