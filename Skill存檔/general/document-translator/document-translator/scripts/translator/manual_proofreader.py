"""
Manual Proofreader - 開啟文字編輯器讓使用者手動校稿
"""

import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from .base_proofreader import BaseProofreader


class ManualProofreader(BaseProofreader):
    """手動校稿器（開啟編輯器）"""

    # 編輯器優先順序
    EDITORS = [
        ("code", ["code", "--wait"]),  # VS Code
        ("subl", ["subl", "--wait"]),  # Sublime Text
        ("nano", ["nano"]),  # Nano
        ("vi", ["vi"]),  # Vi
        ("vim", ["vim"]),  # Vim
        ("notepad", ["notepad"]),  # Windows Notepad
    ]

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self._editor = None
        self._editor_cmd = None

    @property
    def name(self) -> str:
        return "manual"

    @property
    def priority(self) -> int:
        return 100  # 最低優先順序（fallback）

    def is_available(self) -> bool:
        """檢查是否有可用的文字編輯器"""
        for editor_name, editor_cmd in self.EDITORS:
            if shutil.which(editor_name):
                self._editor = editor_name
                self._editor_cmd = editor_cmd
                self._log(f"找到編輯器: {editor_name}")
                return True

        # macOS 特殊處理：使用 open -e 開啟 TextEdit
        if platform.system() == "Darwin":
            self._editor = "TextEdit"
            self._editor_cmd = ["open", "-e", "-W"]  # -W 等待應用程式關閉
            self._log("使用 macOS TextEdit")
            return True

        self._log("沒有找到可用的文字編輯器")
        return False

    def _get_editor_command(self) -> list:
        """取得編輯器命令"""
        # 優先使用環境變數指定的編輯器
        env_editor = os.environ.get("EDITOR") or os.environ.get("VISUAL")
        if env_editor:
            self._log(f"使用環境變數指定的編輯器: {env_editor}")
            return [env_editor]

        if self._editor_cmd:
            return self._editor_cmd

        # 重新偵測
        self.is_available()
        return self._editor_cmd or ["vi"]

    def proofread(self, text: str, prompt: str) -> Optional[str]:
        """
        開啟編輯器讓使用者手動校稿

        Args:
            text: 待校稿的文本
            prompt: 校稿提示詞

        Returns:
            校稿後的文本，失敗時返回 None
        """
        if not self.is_available():
            self._log("沒有可用的文字編輯器")
            return None

        try:
            # 建立暫存檔案
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".md",
                delete=False,
                encoding="utf-8",
                prefix="proofread_",
            ) as f:
                # 寫入提示和待校稿內容
                f.write(f"# 校稿提示\n\n")
                f.write(f"<!-- \n{prompt}\n-->\n\n")
                f.write(f"# 請在下方編輯校稿內容\n\n")
                f.write(f"<!-- 刪除此行以上的所有內容，只保留校稿後的譯文 -->\n\n")
                f.write(text)
                temp_path = f.name

            # 顯示指示
            print("\n" + "=" * 60)
            print("手動校稿模式")
            print("=" * 60)
            print(f"\n編輯器: {self._editor}")
            print(f"檔案: {temp_path}")
            print("\n請執行以下步驟:")
            print("1. 在編輯器中修改翻譯內容")
            print("2. 刪除檔案開頭的提示區塊")
            print("3. 儲存並關閉編輯器")
            print("=" * 60 + "\n")

            # 取得編輯器命令
            editor_cmd = self._get_editor_command()

            # 開啟編輯器
            self._log(f"開啟編輯器: {' '.join(editor_cmd)} {temp_path}")
            process = subprocess.run(
                editor_cmd + [temp_path],
                check=True,
            )

            # 讀取編輯後的內容
            with open(temp_path, "r", encoding="utf-8") as f:
                result = f.read()

            # 清理暫存檔案
            os.unlink(temp_path)

            # 移除提示區塊
            result = self._remove_prompt_header(result)

            if result.strip():
                self._log("校稿完成")
                return result.strip()
            else:
                self._log("校稿結果為空")
                return None

        except subprocess.CalledProcessError as e:
            self._log(f"編輯器執行失敗: {e}")
            return None
        except Exception as e:
            self._log(f"校稿錯誤: {e}")
            return None

    def _remove_prompt_header(self, text: str) -> str:
        """移除提示標頭"""
        lines = text.split("\n")
        result_lines = []
        skip_header = True

        for line in lines:
            # 找到分隔標記後開始保留內容
            if skip_header and "刪除此行以上的所有內容" in line:
                skip_header = False
                continue

            if not skip_header:
                result_lines.append(line)

        # 如果沒有找到分隔標記，返回原始文本（使用者可能已經清理了）
        if skip_header:
            return text

        return "\n".join(result_lines)
