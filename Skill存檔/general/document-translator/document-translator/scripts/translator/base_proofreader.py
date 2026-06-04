"""
Base Proofreader - 校稿器基礎類別
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseProofreader(ABC):
    """校稿器抽象基礎類別"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def _log(self, message: str):
        """輸出詳細日誌"""
        if self.verbose:
            print(f"  [{self.__class__.__name__}] {message}")

    @abstractmethod
    def is_available(self) -> bool:
        """檢查此校稿器是否可用"""
        pass

    @abstractmethod
    def proofread(self, text: str, prompt: str) -> Optional[str]:
        """
        執行校稿

        Args:
            text: 待校稿的文本
            prompt: 校稿提示詞

        Returns:
            校稿後的文本，失敗時返回 None
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """校稿器名稱"""
        pass

    @property
    def priority(self) -> int:
        """自動偵測優先順序（數字越小優先順序越高）"""
        return 100
