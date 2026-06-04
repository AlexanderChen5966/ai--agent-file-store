import argparse
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

def translate_text(text, model, tokenizer, device):
    """
    使用 TranslateGemma 模型進行翻譯。
    """
    # 根據 TranslateGemma 的提示格式調整
    prompt = f"Translate English to Traditional Chinese:\n{text}"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # 使用 Streamer 顯示生成進度，讓使用者知道程式沒卡住
    # skip_prompt=True 讓它只印出翻譯結果，不會重複印 prompt
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    # 於終端機顯示區隔線，方便閱讀
    print("-" * 20 + " Translation Stream " + "-" * 20)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=2048,
            do_sample=False, # 翻譯通常使用 Greedy Search 以求穩定
            streamer=streamer
        )
    
    print("-" * 60)

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 移除提示部分，僅保留翻譯結果
    if decoded.startswith(prompt):
        translation = decoded[len(prompt):].strip()
    else:
        # 如果格式不如預期，嘗試尋找翻譯後的內容
        translation = decoded.replace(prompt, "").strip()
        
    return translation

def process_file(input_path, output_path, model, tokenizer, device):
    """
    讀取檔案並分段翻譯，以避免超出 token 限制。
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 簡單的分段邏輯：依段落分段（可根據需求優化，如保留 Markdown 區塊）
    paragraphs = content.split('\n\n')
    translated_paragraphs = []

    print(f"Processing {len(paragraphs)} segments...")
    for i, para in enumerate(paragraphs):
        if not para.strip():
            translated_paragraphs.append("")
            continue
            
        print(f"Translating segment {i+1}/{len(paragraphs)}...")
        translated_para = translate_text(para, model, tokenizer, device)
        translated_paragraphs.append(translated_para)

    translated_content = '\n\n'.join(translated_paragraphs)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"Translation saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Translate English Markdown to Traditional Chinese using TranslateGemma.")
    parser.add_argument("--input", required=True, help="Path to the input English Markdown file.")
    parser.add_argument("--output", help="Path to the output Traditional Chinese Markdown file.")
    parser.add_argument("--model_name", default="google/translategemma-4b-it", help="Hugging Face model name.")
    parser.add_argument("--device", help="Device to use (cuda/cpu/mps). Automatically detected if not specified.")
    parser.add_argument("--token", help="Hugging Face Access Token (required for gated models like Gemma).")

    args = parser.parse_args()

    # 自動偵測設備
    if args.device:
        device = args.device
    elif torch.cuda.is_available():
        device = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    
    print(f"Using device: {device}")

    # 預設輸出路徑
    if not args.output:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}_zh-TW{ext}"

    # 決定資料型態
    if device == "cuda":
        torch_dtype = torch.bfloat16
    elif device == "mps":
        # macOS MPS 目前對 float16 支援較佳，bfloat16 可能導致效能問題或卡住
        torch_dtype = torch.float16
    else:
        torch_dtype = torch.float32

    print(f"Loading model {args.model_name} with {torch_dtype}...")
    
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, token=args.token)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=torch_dtype,
        device_map="auto" if device != "cpu" else None,
        token=args.token
    )
    
    if device == "cpu":
        model = model.to(device)

    process_file(args.input, args.output, model, tokenizer, device)

if __name__ == "__main__":
    main()
