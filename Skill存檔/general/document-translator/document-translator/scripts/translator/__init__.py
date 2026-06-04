"""
Document Translator - 翻譯器模組
Version: 3.0.0

使用 nodriver 自動化（undetected-chromedriver 作者的新一代工具）
- CAPTCHA 觸發率 <5%
- 自動下載 Chrome
- 內建反偵測
"""

from .google_translator import GoogleTranslator
from .chatgpt_translator import ChatGPTTranslator
from .proofreader_factory import ProofreaderFactory
from .validator import TranslationValidator

__all__ = [
    "GoogleTranslator",
    "ChatGPTTranslator",
    "ProofreaderFactory",
    "TranslationValidator"
]