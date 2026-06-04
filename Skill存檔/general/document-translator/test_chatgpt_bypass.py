#!/usr/bin/env python3
"""
測試 ChatGPTTranslator 的繞過驗證機制
"""
import sys
from pathlib import Path

# 加入模組路徑
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "document-translator/scripts"))

from translator.chatgpt_translator import ChatGPTTranslator

def test_bypass():
    print("=== ChatGPT 繞過驗證測試 ===")
    print("提示: 將啟動有介面的瀏覽器，以便在必要時手動點擊驗證。")
    
    # 建立翻譯器，設為非 headless 以便調試
    translator = ChatGPTTranslator(verbose=True, headless=False)
    
    test_text = "Hello, this is a test of the automated translation system using ChatGPT."
    
    print(f"\n測試原文: {test_text}")
    print("正在啟動瀏覽器並前往 ChatGPT...")
    
    result = translator.translate(test_text)
    
    if result:
        print("\n✅ 測試成功！")
        print(f"翻譯結果: {result}")
    else:
        print("\n❌ 測試失敗。")

if __name__ == "__main__":
    test_bypass()
