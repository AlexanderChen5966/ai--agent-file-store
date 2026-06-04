import sys
import os

# Ensure the module path is correct
sys.path.append('/Users/alexander/Desktop/紀錄文件資料夾/實驗用文件/Skill存檔/document-translator/document-translator/scripts/translator')

from chatgpt_translator import ChatGPTTranslator

def test_translate():
    input_file = '/Users/alexander/Desktop/紀錄文件資料夾/實驗用文件/Skill存檔/document-translator/TEST_GENERATION_TEMPLATE.md'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return

    # Read the file content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Reading file: {input_file}")
    print(f"Content length: {len(content)} characters")

    # Initialize translator (headless=True for testing in background, False if you want to see browser)
    # Using headless=False to handle CAPTCHA manually
    translator = ChatGPTTranslator(verbose=True, headless=False)

    if not translator.is_available():
        print("Error: Chrome or Selenium not available.")
        return

    print("Starting translation to zh-TW (Traditional Chinese)...")
    # This should trigger the new URL: https://chatgpt.com/zh-Hant/translate/
    result = translator.translate(content, target_lang='zh-TW')

    if result:
        print("\nTranslation successful!")
        print("-" * 20)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("-" * 20)
        
        # Optionally save to a file
        output_file = input_file.replace('.md', '_zh.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Translation saved to: {output_file}")
    else:
        print("\nTranslation failed.")

if __name__ == "__main__":
    test_translate()
