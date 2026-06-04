"""
Claude Desktop Proofreader - 使用 Claude Desktop 應用程式進行校稿
透過檔案交換方式與使用者互動
"""

import os
import tempfile
import time
from pathlib import Path
from typing import Optional

from .base_proofreader import BaseProofreader


class ClaudeDesktopProofreader(BaseProofreader):
    """Claude Desktop 校稿器（半自動）"""

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self._exchange_dir = None

    @property
    def name(self) -> str:
        return "desktop"

    @property
    def priority(self) -> int:
        return 30  # 第三優先順序

    def is_available(self) -> bool:
        """檢查 Claude Desktop 是否已安裝"""
        # macOS
        mac_path = "/Applications/Claude.app"
        if os.path.exists(mac_path):
            self._log("找到 Claude Desktop (macOS)")
            return True

        # Windows
        win_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Claude\Claude.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Claude\Claude.exe"),
        ]
        for path in win_paths:
            if os.path.exists(path):
                self._log(f"找到 Claude Desktop (Windows): {path}")
                return True

        # Linux (如果有的話)
        linux_path = os.path.expanduser("~/.local/share/applications/claude.desktop")
        if os.path.exists(linux_path):
            self._log("找到 Claude Desktop (Linux)")
            return True

        self._log("Claude Desktop 未安裝")
        return False

    def _create_exchange_files(self, text: str, prompt: str) -> tuple[Path, Path]:
        """建立檔案交換目錄和檔案"""
        # 建立交換目錄
        self._exchange_dir = Path(tempfile.mkdtemp(prefix="claude_desktop_"))

        # 輸入檔案（給使用者複製到 Claude Desktop）
        input_file = self._exchange_dir / "input.md"
        full_content = f"""# 校稿請求

{prompt}

---

## 待校稿內容

{text}

---

**請將校稿後的內容複製到 output.md 檔案中**
"""
        input_file.write_text(full_content, encoding="utf-8")

        # 輸出檔案（使用者將校稿結果存入此處）
        output_file = self._exchange_dir / "output.md"
        output_file.write_text("", encoding="utf-8")

        return input_file, output_file

    def _wait_for_output(self, output_file: Path, timeout: int = 600) -> Optional[str]:
        """等待使用者完成校稿並寫入輸出檔案"""
        start_time = time.time()
        last_size = 0

        while time.time() - start_time < timeout:
            if output_file.exists():
                current_size = output_file.stat().st_size
                if current_size > 0:
                    # 等待檔案寫入完成（大小不再變化）
                    time.sleep(2)
                    new_size = output_file.stat().st_size
                    if new_size == current_size and new_size > last_size:
                        return output_file.read_text(encoding="utf-8").strip()
                    last_size = current_size

            time.sleep(1)

        return None

    def _cleanup(self):
        """清理交換目錄"""
        if self._exchange_dir and self._exchange_dir.exists():
            import shutil

            shutil.rmtree(self._exchange_dir, ignore_errors=True)

    def proofread(self, text: str, prompt: str) -> Optional[str]:
        """
        使用 Claude Desktop 進行校稿

        這是一個半自動流程，需要使用者手動操作：
        1. 開啟 Claude Desktop
        2. 複製輸入檔案內容
        3. 將校稿結果存入輸出檔案

        Args:
            text: 待校稿的文本
            prompt: 校稿提示詞

        Returns:
            校稿後的文本，失敗時返回 None
        """
        if not self.is_available():
            self._log("Claude Desktop 不可用")
            return None

        try:
            # 建立交換檔案
            input_file, output_file = self._create_exchange_files(text, prompt)

            # 顯示指示
            print("\n" + "=" * 60)
            print("Claude Desktop 校稿模式")
            print("=" * 60)
            print(f"\n輸入檔案: {input_file}")
            print(f"輸出檔案: {output_file}")
            print("\n請執行以下步驟:")
            print("1. 開啟 Claude Desktop")
            print(f"2. 複製 {input_file} 的內容到 Claude Desktop")
            print("3. 等待 Claude 完成校稿")
            print(f"4. 將校稿結果複製到 {output_file}")
            print("5. 儲存檔案")
            print("\n等待校稿完成...")
            print("(按 Ctrl+C 取消)")
            print("=" * 60 + "\n")

            # 嘗試開啟檔案管理器到交換目錄
            self._open_exchange_dir()

            # 等待輸出
            result = self._wait_for_output(output_file)

            if result:
                self._log("校稿完成")
                return result
            else:
                self._log("校稿逾時或被取消")
                return None

        except KeyboardInterrupt:
            self._log("使用者取消校稿")
            return None
        except Exception as e:
            self._log(f"校稿錯誤: {e}")
            return None
        finally:
            # 詢問是否清理
            try:
                cleanup = input("\n是否清理暫存檔案? (y/n): ").lower().strip()
                if cleanup == "y":
                    self._cleanup()
            except Exception:
                pass

    def _open_exchange_dir(self):
        """開啟檔案管理器到交換目錄"""
        import platform
        import subprocess

        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.Popen(["open", str(self._exchange_dir)])
            elif system == "Windows":
                subprocess.Popen(["explorer", str(self._exchange_dir)])
            elif system == "Linux":
                subprocess.Popen(["xdg-open", str(self._exchange_dir)])
        except Exception as e:
            self._log(f"無法開啟檔案管理器: {e}")
