#!/usr/bin/env python3
"""
Document Translator - 技術文檔翻譯系統
Version: 3.0.0

使用智慧降級翻譯策略 + nodriver：
1. 優先使用 ChatGPT Translate（nodriver，CAPTCHA 觸發率 <5%）
2. 失敗時自動降級到 Google Translate + 校稿

技術升級：
- Playwright → nodriver（undetected-chromedriver 作者的新一代工具）
- CAPTCHA 觸發率降至 <5%
- 自動下載 Chrome，安裝更簡單
- 瀏覽器資料持久化（保存驗證狀態）
- 智慧等待機制（偵測輸出穩定）

已移除功能：
- TranslateGemma/HuggingFace 本機翻譯（效率太慢不實際）
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, field

# 加入模組路徑
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from translator.chatgpt_translator import ChatGPTTranslator
from translator.google_translator import GoogleTranslator
from translator.proofreader_factory import ProofreaderFactory
from translator.validator import TranslationValidator


@dataclass
class TranslationStats:
    """翻譯統計"""
    total: int = 0
    success: int = 0
    failed: int = 0
    chatgpt_success: int = 0
    chatgpt_failed: int = 0
    fallback_used: int = 0
    captcha_encountered: int = 0  # CAPTCHA 遭遇次數
    files_success: List[str] = field(default_factory=list)
    files_failed: List[str] = field(default_factory=list)

    def chatgpt_success_rate(self) -> float:
        """計算 ChatGPT 成功率"""
        total_attempts = self.chatgpt_success + self.chatgpt_failed
        if total_attempts == 0:
            return 0.0
        return (self.chatgpt_success / total_attempts) * 100

    def captcha_rate(self) -> float:
        """計算 CAPTCHA 觸發率"""
        total_attempts = self.chatgpt_success + self.chatgpt_failed
        if total_attempts == 0:
            return 0.0
        return (self.captcha_encountered / total_attempts) * 100


class DocumentTranslator:
    """文檔翻譯器主類別 - 支援智慧降級策略"""

    # 文件類型對應的描述
    DOC_TYPE_DESCRIPTIONS = {
        "api": "API 技術文檔",
        "srs": "軟體需求規格書 (Software Requirements Specification)",
        "design": "軟體設計文檔",
        "user-guide": "使用者手冊",
        "tutorial": "教學文件",
        "readme": "README 專案說明",
        "changelog": "變更日誌",
        "general": "一般技術文檔",
    }

    def __init__(
        self,
        mode: str = "auto",
        proofreader: str = "auto",
        verbose: bool = False,
        force: bool = False,
        dry_run: bool = False,
        no_fallback: bool = False,
        headless: bool = True,
        doc_type: str = "general",
    ):
        self.mode = mode
        self.proofreader_type = proofreader
        self.verbose = verbose
        self.force = force
        self.dry_run = dry_run
        self.no_fallback = no_fallback
        self.headless = headless
        self.doc_type = doc_type

        # 載入配置
        self.config_dir = SCRIPT_DIR / "config"
        self.glossary = self._load_glossary()
        self.proofreading_prompt = self._load_proofreading_prompt()

        # 初始化翻譯器
        self.chatgpt_translator = ChatGPTTranslator(
            verbose=verbose, headless=headless
        )
        self.google_translator = GoogleTranslator(
            glossary=self.glossary, verbose=verbose
        )

        self.validator = TranslationValidator(verbose=verbose)

        # 統計
        self.stats = TranslationStats()

    def _load_glossary(self) -> dict:
        """載入術語表"""
        glossary_path = self.config_dir / "glossary.json"
        if glossary_path.exists():
            with open(glossary_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"technical_terms": {}, "taiwan_terms": {}, "preserve": []}

    def _load_proofreading_prompt(self) -> str:
        """載入校稿提示詞"""
        prompt_path = self.config_dir / "proofreading_prompt.txt"
        if prompt_path.exists():
            with open(prompt_path, "r", encoding="utf-8") as f:
                base_prompt = f.read()
        else:
            base_prompt = self._get_default_proofreading_prompt()

        # 加入文件類型上下文
        return self._build_proofreading_prompt(base_prompt)

    def _build_proofreading_prompt(self, base_prompt: str) -> str:
        """根據文件類型建構完整的校稿提示詞"""
        doc_type_desc = self.DOC_TYPE_DESCRIPTIONS.get(self.doc_type, "一般技術文檔")

        context_header = f"""## 文件背景資訊

- **文件類型**：{doc_type_desc}
- **翻譯來源**：Google Translate 機器翻譯
- **校稿重點**：請特別注意機器翻譯常見的問題，如詞彙選擇不當、語句不通順、專業術語翻譯錯誤等

---

"""
        return context_header + base_prompt

    def _get_default_proofreading_prompt(self) -> str:
        """預設校稿提示詞"""
        return """請校對以下繁體中文翻譯，確保：
1. 使用臺灣慣用詞彙（帳號而非賬號、資料而非數據、軟體而非軟件、網路而非網絡）
2. 技術術語翻譯正確且一致
3. 句子通順，符合中文語法
4. 保持原文的 Markdown 格式
5. 程式碼區塊保持不變

請直接輸出校對後的內容，不要加入任何說明。"""

    def _log(self, level: str, message: str):
        """輸出日誌"""
        colors = {
            "INFO": "\033[0;34m",
            "OK": "\033[0;32m",
            "WARN": "\033[1;33m",
            "ERROR": "\033[0;31m",
            "FALLBACK": "\033[1;35m",
        }
        nc = "\033[0m"
        color = colors.get(level, "")
        print(f"{color}[{level}]{nc} {message}")

    def _get_output_path(self, input_path: Path) -> Path:
        """計算輸出路徑（docs/en/ -> docs/zh-TW/）"""
        path_str = str(input_path)
        if "/docs/en/" in path_str:
            return Path(path_str.replace("/docs/en/", "/docs/zh-TW/"))
        elif "\\docs\\en\\" in path_str:
            return Path(path_str.replace("\\docs\\en\\", "\\docs\\zh-TW\\"))
        else:
            return input_path.with_suffix(f".zh-TW{input_path.suffix}")

    def _translate_with_chatgpt(self, source_text: str) -> Optional[str]:
        """使用 ChatGPT 翻譯"""
        self._log("INFO", "嘗試 ChatGPT Translate...")

        if not self.chatgpt_translator.is_available():
            self._log("WARN", "ChatGPT Translator 不可用")
            return None

        result = self.chatgpt_translator.translate(source_text)
        if result:
            self._log("OK", "ChatGPT Translate 成功")
            self.stats.chatgpt_success += 1
            return result
        else:
            self._log("WARN", "ChatGPT Translate 失敗")
            self.stats.chatgpt_failed += 1
            return None

    def _translate_with_google_and_proofread(self, source_text: str) -> Optional[str]:
        """使用 Google Translate + 校稿"""
        self._log("FALLBACK", "降級到 Google Translate + 校稿")
        self.stats.fallback_used += 1

        # 步驟 1: Google Translate
        self._log("INFO", "步驟 1/2: Google Translate 粗翻...")
        rough_translation = self.google_translator.translate(source_text)

        if not rough_translation:
            self._log("ERROR", "Google Translate 失敗")
            return None

        # 步驟 2: 校稿
        self._log("INFO", f"步驟 2/2: 智慧校稿 (後端: {self.proofreader_type})...")
        proofreader = ProofreaderFactory.create(
            self.proofreader_type, verbose=self.verbose
        )

        if proofreader:
            proofread_result = proofreader.proofread(
                rough_translation, self.proofreading_prompt
            )
            if proofread_result:
                self._log("OK", "Google + 校稿完成")
                return proofread_result
            else:
                self._log("WARN", "校稿失敗，使用粗翻結果")
                return rough_translation
        else:
            self._log("WARN", f"無法建立校稿器，使用粗翻結果")
            return rough_translation

    def translate_file(self, input_path: Path) -> bool:
        """翻譯單一檔案"""
        if not input_path.exists():
            self._log("ERROR", f"檔案不存在: {input_path}")
            return False

        output_path = self._get_output_path(input_path)

        # 檢查是否需要翻譯
        if output_path.exists() and not self.force:
            self._log("WARN", f"譯文已存在，跳過: {output_path}")
            self._log("INFO", "使用 --force 強制覆蓋")
            return True

        if self.dry_run:
            self._log("INFO", f"[DRY-RUN] 將翻譯: {input_path} -> {output_path}")
            return True

        self._log("INFO", f"翻譯: {input_path}")

        # 讀取原文
        with open(input_path, "r", encoding="utf-8") as f:
            source_text = f.read()

        final_translation = None
        translation_method = None

        # 根據模式選擇翻譯策略
        if self.mode == "chatgpt":
            # 僅使用 ChatGPT（不降級）
            final_translation = self._translate_with_chatgpt(source_text)
            translation_method = "ChatGPT"

        elif self.mode == "auto":
            # 智慧降級：先 ChatGPT，失敗降級到 Google + 校稿
            final_translation = self._translate_with_chatgpt(source_text)
            translation_method = "ChatGPT"

            if not final_translation and not self.no_fallback:
                # 降級到 Google + 校稿
                final_translation = self._translate_with_google_and_proofread(source_text)
                translation_method = "Google + 校稿（降級）"

        elif self.mode == "google+proofread":
            # Google Translate + 校稿（用於測試校稿流程）
            final_translation = self._translate_with_google_and_proofread(source_text)
            translation_method = "Google + 校稿"

        elif self.mode == "google":
            # 僅使用 Google Translate（無校稿）
            self._log("INFO", "Google Translate...")
            final_translation = self.google_translator.translate(source_text)
            translation_method = "Google"

        # 檢查翻譯結果
        if not final_translation:
            self._log("ERROR", "翻譯失敗")
            return False

        # 驗證翻譯品質
        self._log("INFO", "驗證翻譯品質...")
        validation_result = self.validator.validate(source_text, final_translation)
        if not validation_result["valid"]:
            for warning in validation_result["warnings"]:
                self._log("WARN", warning)

        # 確保輸出目錄存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 寫入譯文
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_translation)

        self._log("OK", f"翻譯完成: {output_path}")
        self._log("INFO", f"使用方法: {translation_method}")
        return True

    def translate_files(self, input_paths: List[Path]) -> TranslationStats:
        """批量翻譯檔案"""
        self.stats = TranslationStats(total=len(input_paths))

        for path in input_paths:
            try:
                if self.translate_file(path):
                    self.stats.success += 1
                    self.stats.files_success.append(str(path))
                else:
                    self.stats.failed += 1
                    self.stats.files_failed.append(str(path))
            except Exception as e:
                self._log("ERROR", f"翻譯失敗 {path}: {e}")
                self.stats.failed += 1
                self.stats.files_failed.append(str(path))

        return self.stats

    def print_stats(self):
        """輸出統計資訊"""
        print("\n" + "=" * 60)
        print("翻譯完成")
        print("=" * 60)
        print(f"總計: {self.stats.total} 個檔案")
        print(f"✅ 成功: {self.stats.success}")
        print(f"❌ 失敗: {self.stats.failed}")

        if self.mode in ["auto", "chatgpt"]:
            print("\n" + "=" * 60)
            print("翻譯統計 (nodriver 模式)")
            print("=" * 60)
            total_chatgpt = self.stats.chatgpt_success + self.stats.chatgpt_failed
            if total_chatgpt > 0:
                print(f"ChatGPT 成功: {self.stats.chatgpt_success} ({self.stats.chatgpt_success / total_chatgpt * 100:.0f}%)")
                print(f"ChatGPT 失敗: {self.stats.chatgpt_failed} ({self.stats.chatgpt_failed / total_chatgpt * 100:.0f}%)")
                print(f"降級到 Google: {self.stats.fallback_used}")
                print(f"ChatGPT 成功率: {self.stats.chatgpt_success_rate():.1f}%")
                print(f"CAPTCHA 遭遇: {self.stats.captcha_encountered} 次 ({self.stats.captcha_rate():.1f}%)")

        print("=" * 60)

        if self.stats.files_failed:
            print("\n失敗的檔案:")
            for f in self.stats.files_failed:
                print(f"  - {f}")


def main():
    parser = argparse.ArgumentParser(
        description="Document Translator - 技術文檔翻譯系統（智慧降級策略 + nodriver）"
    )
    parser.add_argument("files", nargs="+", help="要翻譯的檔案路徑")
    parser.add_argument(
        "--mode",
        choices=["chatgpt", "auto", "google+proofread", "google"],
        default="chatgpt",
        help="翻譯模式: chatgpt, auto, google+proofread, google (預設: chatgpt)",
    )
    parser.add_argument(
        "--proofreader",
        choices=["auto", "chatgpt", "desktop", "cli", "manual"],
        default="auto",
        help="降級時的校稿後端 (預設: auto)。chatgpt 使用 ChatGPT 對話頁面校稿",
    )
    parser.add_argument("--force", action="store_true", help="強制覆蓋已存在的譯文")
    parser.add_argument("--verbose", action="store_true", help="顯示詳細日誌")
    parser.add_argument(
        "--dry-run", action="store_true", help="僅顯示將執行的操作，不實際執行"
    )
    parser.add_argument(
        "--no-fallback", action="store_true", help="禁用降級機制（ChatGPT 失敗就報錯）"
    )
    parser.add_argument(
        "--no-headless", action="store_true", help="顯示瀏覽器視窗（調試用）"
    )
    parser.add_argument(
        "--doc-type",
        choices=["api", "srs", "design", "user-guide", "tutorial", "readme", "changelog", "general"],
        default="general",
        help="文件類型，用於校稿時提供上下文 (預設: general)",
    )

    args = parser.parse_args()

    translator = DocumentTranslator(
        mode=args.mode,
        proofreader=args.proofreader,
        verbose=args.verbose,
        force=args.force,
        dry_run=args.dry_run,
        no_fallback=args.no_fallback,
        headless=not args.no_headless,
        doc_type=args.doc_type,
    )

    # 轉換檔案路徑
    input_paths = [Path(f) for f in args.files]

    # 執行翻譯
    stats = translator.translate_files(input_paths)

    # 輸出統計
    translator.print_stats()

    # 設定退出碼
    sys.exit(0 if stats.failed == 0 else 1)


if __name__ == "__main__":
    main()
