"""
Proofreader Factory - 校稿器工廠
Version: 3.0.0

校稿器用於 Google Translate 降級時的校稿工作。
優先順序：chatgpt > desktop > cli > manual

新增：ChatGPT 校稿器（使用 nodriver 自動化 chatgpt.com 對話頁面）
"""

from typing import Optional, List
from .base_proofreader import BaseProofreader


class ProofreaderFactory:
    """校稿器工廠類別"""

    _proofreaders: List[BaseProofreader] = []
    _initialized = False

    @classmethod
    def _init_proofreaders(cls, verbose: bool = False):
        """初始化所有校稿器"""
        if cls._initialized:
            return

        # 延遲載入各校稿器
        from .chatgpt_proofreader import ChatGPTProofreader
        from .claude_desktop_proofreader import ClaudeDesktopProofreader
        from .claude_cli_proofreader import ClaudeCLIProofreader
        from .manual_proofreader import ManualProofreader

        cls._proofreaders = [
            ChatGPTProofreader(verbose=verbose),        # 最高優先（priority=5）
            ClaudeDesktopProofreader(verbose=verbose),  # 第二（priority=10）
            ClaudeCLIProofreader(verbose=verbose),      # 第三
            ManualProofreader(verbose=verbose),         # 備案
        ]

        # 按優先順序排序
        cls._proofreaders.sort(key=lambda p: p.priority)
        cls._initialized = True

    @classmethod
    def create(cls, proofreader_type: str, verbose: bool = False) -> Optional[BaseProofreader]:
        """
        建立校稿器實例

        Args:
            proofreader_type: 校稿器類型 (auto, desktop, cli, manual)
            verbose: 是否顯示詳細日誌

        Returns:
            校稿器實例，無法建立時返回 None
        """
        cls._init_proofreaders(verbose)

        if proofreader_type == "auto":
            return cls._auto_detect(verbose)

        # 建立指定類型的校稿器
        from .chatgpt_proofreader import ChatGPTProofreader
        from .claude_cli_proofreader import ClaudeCLIProofreader
        from .claude_desktop_proofreader import ClaudeDesktopProofreader
        from .manual_proofreader import ManualProofreader

        proofreader_map = {
            "chatgpt": ChatGPTProofreader,
            "cli": ClaudeCLIProofreader,
            "desktop": ClaudeDesktopProofreader,
            "manual": ManualProofreader,
        }

        proofreader_class = proofreader_map.get(proofreader_type)
        if proofreader_class:
            proofreader = proofreader_class(verbose=verbose)
            if proofreader.is_available():
                return proofreader
            else:
                if verbose:
                    print(f"  [ProofreaderFactory] {proofreader_type} 不可用")
                return None

        if verbose:
            print(f"  [ProofreaderFactory] 未知的校稿器類型: {proofreader_type}")
        return None

    @classmethod
    def _auto_detect(cls, verbose: bool = False) -> Optional[BaseProofreader]:
        """
        自動偵測可用的校稿器

        優先順序：desktop > cli > manual
        """
        if verbose:
            print("  [ProofreaderFactory] 自動偵測校稿器...")

        for proofreader in cls._proofreaders:
            if proofreader.is_available():
                if verbose:
                    print(f"  [ProofreaderFactory] 偵測到: {proofreader.name}")
                # 建立新實例以確保 verbose 設定正確
                return cls.create(proofreader.name, verbose)

        if verbose:
            print("  [ProofreaderFactory] 沒有可用的校稿器")
        return None

    @classmethod
    def list_available(cls, verbose: bool = False) -> List[str]:
        """列出所有可用的校稿器"""
        cls._init_proofreaders(verbose)
        return [p.name for p in cls._proofreaders if p.is_available()]

    @classmethod
    def list_all(cls, verbose: bool = False) -> List[dict]:
        """列出所有校稿器及其狀態"""
        cls._init_proofreaders(verbose)
        return [
            {
                "name": p.name,
                "available": p.is_available(),
                "priority": p.priority,
            }
            for p in cls._proofreaders
        ]
