"""
Claude CLI Proofreader - 使用 Claude CLI 命令列工具進行校稿
"""

import shutil
import subprocess
import tempfile
from typing import Optional

from .base_proofreader import BaseProofreader


class ClaudeCLIProofreader(BaseProofreader):
    """Claude CLI 校稿器"""

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)

    @property
    def name(self) -> str:
        return "cli"

    @property
    def priority(self) -> int:
        return 20  # 第二優先順序

    def is_available(self) -> bool:
        """檢查 Claude CLI 是否可用"""
        claude_path = shutil.which("claude")
        if claude_path:
            self._log(f"找到 Claude CLI: {claude_path}")
            return True
        else:
            self._log("Claude CLI 未安裝")
            return False

    def proofread(self, text: str, prompt: str) -> Optional[str]:
        """
        使用 Claude CLI 進行校稿

        Args:
            text: 待校稿的文本
            prompt: 校稿提示詞

        Returns:
            校稿後的文本，失敗時返回 None
        """
        if not self.is_available():
            self._log("Claude CLI 不可用")
            return None

        try:
            # 組合完整提示
            full_prompt = f"{prompt}\n\n---\n\n{text}"

            # 寫入暫存檔案（避免命令列長度限制）
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, encoding="utf-8"
            ) as f:
                f.write(full_prompt)
                temp_path = f.name

            self._log("呼叫 Claude CLI...")

            # 執行 Claude CLI
            # 使用 --print 模式直接輸出結果
            result = subprocess.run(
                ["claude", "--print", "-f", temp_path],
                capture_output=True,
                text=True,
                timeout=300,  # 5 分鐘超時
            )

            # 清理暫存檔案
            import os

            os.unlink(temp_path)

            if result.returncode == 0:
                response = result.stdout.strip()
                if response:
                    self._log("校稿完成")
                    return response
                else:
                    self._log("CLI 回應為空")
                    return None
            else:
                self._log(f"CLI 執行失敗: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            self._log("CLI 執行逾時")
            return None
        except Exception as e:
            self._log(f"校稿錯誤: {e}")
            return None
