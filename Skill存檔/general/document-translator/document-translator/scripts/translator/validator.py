"""
Translation Validator - 翻譯品質驗證器
"""

import re
from typing import Optional


class TranslationValidator:
    """翻譯品質驗證器"""

    # 簡體中文字元對照
    SIMPLIFIED_CHARS = {
        "账": "帳",
        "数据": "資料",
        "软件": "軟體",
        "网络": "網路",
        "服务器": "伺服器",
        "内存": "記憶體",
        "硬盘": "硬碟",
        "文件夹": "資料夾",
        "窗口": "視窗",
        "默认": "預設",
        "支持": "支援",
        "视频": "影片",
        "链接": "連結",
        "程序": "程式",
        "信息": "訊息",
    }

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def _log(self, message: str):
        """輸出詳細日誌"""
        if self.verbose:
            print(f"  [Validator] {message}")

    def _count_code_blocks(self, text: str) -> int:
        """計算程式碼區塊數量"""
        return len(re.findall(r"```", text)) // 2

    def _count_headings(self, text: str) -> int:
        """計算標題數量"""
        return len(re.findall(r"^#+\s", text, re.MULTILINE))

    def _count_links(self, text: str) -> int:
        """計算連結數量"""
        return len(re.findall(r"\[([^\]]+)\]\([^)]+\)", text))

    def _count_images(self, text: str) -> int:
        """計算圖片數量"""
        return len(re.findall(r"!\[([^\]]*)\]\([^)]+\)", text))

    def _find_simplified_chinese(self, text: str) -> list:
        """找出簡體中文字元"""
        found = []
        for simplified, traditional in self.SIMPLIFIED_CHARS.items():
            if simplified in text:
                found.append((simplified, traditional))
        return found

    def _check_markdown_syntax(self, text: str) -> list:
        """檢查 Markdown 語法問題"""
        issues = []

        # 檢查未閉合的程式碼區塊
        backtick_count = text.count("```")
        if backtick_count % 2 != 0:
            issues.append("程式碼區塊未正確閉合")

        # 檢查未閉合的粗體/斜體
        # (簡單檢查，可能有誤報)
        asterisk_pairs = len(re.findall(r"\*\*[^*]+\*\*", text))
        underscore_pairs = len(re.findall(r"__[^_]+__", text))

        # 檢查連結格式
        broken_links = re.findall(r"\[[^\]]+\]\([^)]*$", text, re.MULTILINE)
        if broken_links:
            issues.append(f"發現 {len(broken_links)} 個可能損壞的連結")

        return issues

    def validate(self, source: str, translation: str) -> dict:
        """
        驗證翻譯品質

        Args:
            source: 原文
            translation: 譯文

        Returns:
            驗證結果字典，包含 valid, warnings, errors
        """
        result = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "stats": {},
        }

        self._log("開始驗證翻譯品質...")

        # 統計比較
        source_stats = {
            "code_blocks": self._count_code_blocks(source),
            "headings": self._count_headings(source),
            "links": self._count_links(source),
            "images": self._count_images(source),
            "length": len(source),
        }

        trans_stats = {
            "code_blocks": self._count_code_blocks(translation),
            "headings": self._count_headings(translation),
            "links": self._count_links(translation),
            "images": self._count_images(translation),
            "length": len(translation),
        }

        result["stats"] = {
            "source": source_stats,
            "translation": trans_stats,
        }

        # 檢查程式碼區塊數量
        if source_stats["code_blocks"] != trans_stats["code_blocks"]:
            result["warnings"].append(
                f"程式碼區塊數量不一致: 原文 {source_stats['code_blocks']}, "
                f"譯文 {trans_stats['code_blocks']}"
            )

        # 檢查標題數量
        if source_stats["headings"] != trans_stats["headings"]:
            result["warnings"].append(
                f"標題數量不一致: 原文 {source_stats['headings']}, "
                f"譯文 {trans_stats['headings']}"
            )

        # 檢查連結數量
        if source_stats["links"] != trans_stats["links"]:
            result["warnings"].append(
                f"連結數量不一致: 原文 {source_stats['links']}, "
                f"譯文 {trans_stats['links']}"
            )

        # 檢查圖片數量
        if source_stats["images"] != trans_stats["images"]:
            result["warnings"].append(
                f"圖片數量不一致: 原文 {source_stats['images']}, "
                f"譯文 {trans_stats['images']}"
            )

        # 檢查簡體中文
        simplified_found = self._find_simplified_chinese(translation)
        if simplified_found:
            for simplified, traditional in simplified_found:
                result["warnings"].append(
                    f"發現簡體中文詞彙: '{simplified}' (建議改為 '{traditional}')"
                )

        # 檢查 Markdown 語法
        markdown_issues = self._check_markdown_syntax(translation)
        for issue in markdown_issues:
            result["warnings"].append(f"Markdown 語法問題: {issue}")

        # 檢查譯文是否為空或過短
        if not translation or len(translation.strip()) < 10:
            result["errors"].append("譯文為空或過短")
            result["valid"] = False

        # 檢查譯文長度比例（中文通常比英文短）
        if source_stats["length"] > 0:
            ratio = trans_stats["length"] / source_stats["length"]
            if ratio < 0.3:
                result["warnings"].append(
                    f"譯文長度異常偏短 (原文的 {ratio:.1%})"
                )
            elif ratio > 2.0:
                result["warnings"].append(
                    f"譯文長度異常偏長 (原文的 {ratio:.1%})"
                )

        # 如果有錯誤，標記為無效
        if result["errors"]:
            result["valid"] = False

        # 輸出日誌
        self._log(f"驗證完成: {'通過' if result['valid'] else '失敗'}")
        self._log(f"警告數量: {len(result['warnings'])}")
        self._log(f"錯誤數量: {len(result['errors'])}")

        return result

    def get_quality_score(self, validation_result: dict) -> int:
        """
        計算品質分數 (0-100)

        Args:
            validation_result: validate() 的回傳結果

        Returns:
            品質分數
        """
        score = 100

        # 每個警告扣 5 分
        score -= len(validation_result["warnings"]) * 5

        # 每個錯誤扣 20 分
        score -= len(validation_result["errors"]) * 20

        return max(0, min(100, score))
