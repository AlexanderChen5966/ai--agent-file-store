"""
ChatGPT Proofreader - 使用 nodriver 自動化操作 ChatGPT 網頁進行校稿
Version: 3.0.0

技術特點：
- nodriver: undetected-chromedriver 作者的新一代反偵測瀏覽器自動化
- 自動下載並管理 Chrome，不依賴系統 Chrome 版本
- 內建反偵測，無需額外 stealth 設定
- Async/Await 非同步設計
- CAPTCHA 觸發率極低
- 使用 ChatGPT 對話頁面（https://chatgpt.com/）進行校稿
"""

import asyncio
import time
from pathlib import Path
from typing import Optional

from .base_proofreader import BaseProofreader

CHATGPT_URL = "https://chatgpt.com/"


class ChatGPTProofreader(BaseProofreader):
    """ChatGPT 校稿器（nodriver 模式）- 使用對話頁面校稿"""

    MAX_RETRIES = 3
    WAIT_TIMEOUT = 120
    CAPTCHA_WAIT_TIMEOUT = 120

    def __init__(self, verbose: bool = False, headless: bool = False):
        super().__init__(verbose)
        self.headless = headless
        self._browser = None
        self._page = None

    @property
    def name(self) -> str:
        return "chatgpt"

    @property
    def priority(self) -> int:
        return 5  # 最高優先順序（比 desktop 的 10 更高）

    def is_available(self) -> bool:
        """檢查 nodriver 是否可用"""
        try:
            import nodriver
            return True
        except ImportError:
            self._log("nodriver 未安裝，請執行: pip install nodriver")
            return False

    def _get_user_data_dir(self) -> Path:
        """取得瀏覽器資料目錄（用於保存登入狀態）"""
        # 使用版本化的資料夾名稱，避免舊資料導致問題
        path = Path.home() / ".chatgpt-translator" / "chrome-profile-v3"
        path.mkdir(parents=True, exist_ok=True)
        return path

    async def _init_browser(self):
        """初始化 nodriver 瀏覽器"""
        if self._browser is not None:
            return

        try:
            import nodriver as uc
        except ImportError:
            raise ImportError(
                "缺少必要套件: nodriver\n"
                "請執行: pip install nodriver"
            )

        self._log("初始化 nodriver 瀏覽器...")

        # nodriver 設定 - 使用與翻譯器相同的 profile
        user_data_dir = self._get_user_data_dir()

        # macOS 可能需要 sandbox=False
        import platform
        browser_args = []
        if platform.system() == "Darwin":  # macOS
            browser_args.append("--no-sandbox")
            browser_args.append("--disable-setuid-sandbox")

        self._browser = await uc.start(
            headless=self.headless,
            user_data_dir=str(user_data_dir),
            lang="zh-TW",
            sandbox=False,  # macOS 安全性設定
            browser_args=browser_args
        )

        self._log(f"瀏覽器已啟動 (headless={self.headless})")
        self._log(f"使用者資料目錄: {user_data_dir}")

    async def _close_browser(self):
        """關閉瀏覽器"""
        if self._browser:
            try:
                self._browser.stop()
                self._log("瀏覽器已關閉")
            except Exception as e:
                self._log(f"關閉瀏覽器時發生錯誤: {e}")
            self._browser = None
            self._page = None

    async def _check_for_captcha(self) -> bool:
        """檢查並處理 CAPTCHA"""
        captcha_keywords = [
            "Verify you are human",
            "Checking if the site connection is secure",
            "cloudflare",
            "請確認您是真人",
            "Just a moment",
            "checking your browser",
            "cf-turnstile",
            "challenge-running"
        ]

        page_content = await self._page.get_content()

        for keyword in captcha_keywords:
            if keyword.lower() in page_content.lower():
                self._log("⚠️ 偵測到人類驗證 (CAPTCHA)...")

                if self.headless:
                    self._log("警告: Headless 模式下無法手動完成驗證")
                    self._log("建議: 使用非 headless 模式手動驗證一次")
                    return False
                else:
                    self._log("⏳ 請在瀏覽器視窗中手動完成驗證...")
                    self._log(f"⏳ 等待時間上限: {self.CAPTCHA_WAIT_TIMEOUT} 秒")

                    start_time = time.time()
                    while time.time() - start_time < self.CAPTCHA_WAIT_TIMEOUT:
                        await asyncio.sleep(2)

                        # 檢查 URL 是否已經變更
                        current_url = self._page.url
                        if "chatgpt.com" in current_url and "challenge" not in current_url:
                            await asyncio.sleep(3)
                            self._log(f"✅ CAPTCHA 驗證完成，已跳轉到: {current_url}")
                            return True

                        page_content = await self._page.get_content()

                        still_has_captcha = any(
                            kw.lower() in page_content.lower()
                            for kw in captcha_keywords
                        )

                        if not still_has_captcha:
                            await asyncio.sleep(3)
                            self._log("✅ CAPTCHA 驗證完成")
                            return True

                        elapsed = int(time.time() - start_time)
                        self._log(f"⏳ 等待中... ({elapsed}/{self.CAPTCHA_WAIT_TIMEOUT} 秒)")

                    self._log("❌ CAPTCHA 驗證逾時")
                    return False

        return True  # 沒有 CAPTCHA

    async def _human_like_type(self, element, text: str):
        """模擬人類打字 - nodriver 使用 send_keys"""
        import random

        # 分段輸入
        chunk_size = 500
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            await element.send_keys(chunk)
            await asyncio.sleep(random.uniform(0.1, 0.3))

    async def _wait_for_response(self) -> bool:
        """等待 ChatGPT 回應完成（使用內容穩定偵測）"""
        start_time = time.time()
        self._log("等待 ChatGPT 回應...")

        last_content_length = 0
        stable_count = 0
        required_stable_count = 3  # 連續穩定 3 次才認為完成

        # 先等待幾秒讓回應開始
        await asyncio.sleep(5)

        while time.time() - start_time < self.WAIT_TIMEOUT:
            try:
                # 使用 JavaScript 取得最後一則回應的長度
                current_length = await self._page.evaluate("""
                    (() => {
                        const messages = document.querySelectorAll('[data-message-author-role="assistant"]');
                        if (messages.length > 0) {
                            const lastMessage = messages[messages.length - 1];
                            const text = lastMessage.innerText || lastMessage.textContent || '';
                            return text.length;
                        }
                        return 0;
                    })()
                """)

                elapsed = int(time.time() - start_time)

                if current_length > 0:
                    if current_length == last_content_length:
                        stable_count += 1
                        self._log(f"回應穩定中... ({stable_count}/{required_stable_count}) - {current_length} 字元 ({elapsed}秒)")

                        if stable_count >= required_stable_count:
                            self._log(f"回應完成，共 {current_length} 字元")
                            await asyncio.sleep(2)  # 額外等待確保完全完成
                            return True
                    else:
                        stable_count = 0
                        self._log(f"回應生成中... {last_content_length} → {current_length} 字元 ({elapsed}秒)")

                    last_content_length = current_length
                else:
                    self._log(f"等待回應開始... ({elapsed}/{self.WAIT_TIMEOUT} 秒)")

            except Exception as e:
                self._log(f"檢查回應時發生錯誤: {e}")

            await asyncio.sleep(3)

        self._log("等待回應逾時")
        return False

    async def _get_last_response(self) -> Optional[str]:
        """取得最後一個 ChatGPT 回應 - 透過點擊「複製程式碼」按鈕並從剪貼簿讀取"""
        try:
            self._log("尋找並點擊「複製程式碼」按鈕...")
            
            # 等待一下，確保「複製程式碼」按鈕已經出現
            await asyncio.sleep(2)
            
            # 方式 1: 使用 JavaScript 精確定位並點擊「複製程式碼」按鈕
            copy_code_button_found = await self._page.evaluate("""
                (() => {
                    // 策略 1: 找 aria-label="複製" 且文字包含"複製程式碼"的按鈕
                    const buttons = document.querySelectorAll('button[aria-label="複製"]');
                    for (let btn of buttons) {
                        const text = btn.innerText || btn.textContent || '';
                        if (text.includes('複製程式碼') || 
                            text.includes('Copy code') || 
                            text.includes('复制代码')) {
                            console.log('[ChatGPT Proofreader] 找到按鈕 (aria-label):', text);
                            btn.click();
                            return true;
                        }
                    }
                    
                    // 策略 2: 找所有按鈕中包含「複製程式碼」文字的
                    const allButtons = document.querySelectorAll('button');
                    for (let btn of allButtons) {
                        const text = btn.innerText || btn.textContent || '';
                        if (text.includes('複製程式碼') || 
                            text.includes('Copy code') || 
                            text.includes('复制代码')) {
                            console.log('[ChatGPT Proofreader] 找到按鈕 (text match):', text);
                            btn.click();
                            return true;
                        }
                    }
                    
                    console.log('[ChatGPT Proofreader] 未找到「複製程式碼」按鈕');
                    return false;
                })()
            """)
            
            if copy_code_button_found:
                self._log("✅ 已透過 JavaScript 點擊「複製程式碼」按鈕")
                await asyncio.sleep(2)  # 等待剪貼簿操作完成
                
                # 從剪貼簿讀取結果
                try:
                    result = await self._page.evaluate("navigator.clipboard.readText()")
                    if result:
                        # 移除開頭的語言標記和「複製程式碼」標記（如果存在）
                        lines = result.split('\n')
                        if len(lines) >= 2:
                            # 檢查第一行是否為語言標記
                            first_line = lines[0].strip().lower()
                            if first_line in ['markdown', 'typescript', 'python', 'java', 'javascript', 'html', 'css']:
                                # 檢查第二行是否為「複製程式碼」
                                if '複製程式碼' in lines[1] or 'Copy code' in lines[1] or '复制代码' in lines[1]:
                                    # 移除前兩行
                                    result = '\n'.join(lines[2:])
                                    self._log("✅ 已移除語言標記和「複製程式碼」標記")
                        
                        self._log(f"✅ 從剪貼簿取得校稿結果: {len(result)} 字元")
                        return result.strip()
                    else:
                        self._log("⚠️ 剪貼簿是空的")
                except Exception as e:
                    self._log(f"⚠️ 無法讀取剪貼簿: {e}")
            else:
                self._log("⚠️ 未找到「複製程式碼」按鈕，使用備用方式（DOM）...")
            
            # 備用方式：從 DOM 直接讀取（如果沒有找到「複製程式碼」按鈕）
            result = await self._page.evaluate("""
                (() => {
                    const messages = document.querySelectorAll('[data-message-author-role="assistant"]');
                    if (messages.length > 0) {
                        const lastMessage = messages[messages.length - 1];
                        return lastMessage.innerText || lastMessage.textContent || '';
                    }
                    return '';
                })()
            """)

            if result:
                self._log(f"使用 DOM 取得回應: {len(result)} 字元")
                return result

            self._log("❌ 找不到任何 assistant 回應")
        except Exception as e:
            self._log(f"❌ 取得回應失敗: {e}")

        return None

    async def _send_message(self, message: str) -> bool:
        """發送訊息到 ChatGPT"""
        try:
            self._log("尋找輸入框...")

            # 找到輸入框
            textarea = await self._page.select(
                'textarea[id="prompt-textarea"]',
                timeout=30
            )

            if not textarea:
                # 嘗試其他選擇器
                textarea = await self._page.select('textarea', timeout=10)

            if not textarea:
                self._log("找不到輸入框")
                return False

            self._log("找到輸入框，開始輸入...")

            # 點擊輸入框以確保焦點
            await textarea.click()
            await asyncio.sleep(0.3)

            # 輸入訊息
            await self._human_like_type(textarea, message)

            await asyncio.sleep(0.5)

            self._log("尋找發送按鈕...")

            # 點擊發送按鈕
            try:
                send_button = await self._page.select(
                    'button[data-testid="send-button"]',
                    timeout=5
                )
                if send_button:
                    await send_button.click()
                    self._log("已點擊發送按鈕")
                else:
                    # 備用方案：按 Enter
                    await textarea.send_keys("\n")
                    self._log("使用 Enter 發送")
            except Exception:
                await textarea.send_keys("\n")
                self._log("使用 Enter 發送 (fallback)")

            return True

        except Exception as e:
            self._log(f"發送訊息失敗: {e}")
            return False

    async def _proofread_async(self, text: str, prompt: str) -> Optional[str]:
        """非同步校稿實作"""
        if not text or not text.strip():
            return text

        self._log(f"開始校稿 ({len(text)} 字元)")

        try:
            await self._init_browser()

            # 導航到 ChatGPT
            self._log(f"導航到: {CHATGPT_URL}")
            self._page = await self._browser.get(CHATGPT_URL)
            await asyncio.sleep(5)  # 等待頁面載入

            self._log(f"當前 URL: {self._page.url}")

            # 檢查 CAPTCHA
            if not await self._check_for_captcha():
                return None

            # 額外等待頁面穩定
            await asyncio.sleep(2)

            # 組合校稿訊息（新格式：提示詞 + 文件 + 結束標記）
            full_message = f"{prompt}\n\n{text}\n\n【文件結束】"

            # 發送訊息
            self._log("發送校稿請求...")
            if not await self._send_message(full_message):
                return None

            # 等待回應
            if not await self._wait_for_response():
                self._log("等待回應逾時")
                return None

            # 取得回應
            result = await self._get_last_response()

            if result:
                self._log(f"校稿成功 ({len(result)} 字元)")

            return result

        except Exception as e:
            self._log(f"校稿錯誤: {e}")
            import traceback
            self._log(traceback.format_exc())
            return None

        finally:
            if self.headless:
                await self._close_browser()

    def proofread(self, text: str, prompt: str) -> Optional[str]:
        """
        使用 ChatGPT 進行校稿（同步包裝器）

        Args:
            text: 待校稿的文本
            prompt: 校稿提示詞

        Returns:
            校稿後的文本，失敗時返回 None
        """
        if not self.is_available():
            self._log("ChatGPT 校稿器不可用")
            return None

        try:
            import nodriver as uc
            # 使用 nodriver 的事件循環
            loop = uc.loop()
            result = loop.run_until_complete(
                self._proofread_async(text, prompt)
            )
            return result
        except Exception as e:
            self._log(f"校稿失敗: {e}")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return None
        finally:
            # 確保瀏覽器在校稿完成後關閉
            if self._browser:
                try:
                    import asyncio
                    loop = asyncio.get_event_loop()
                    if loop and not loop.is_closed():
                        loop.run_until_complete(self._close_browser())
                except Exception:
                    pass

    def __del__(self):
        """清理資源 - 安全地處理事件循環關閉的情況"""
        if self._browser:
            try:
                import asyncio
                # 檢查事件循環是否存在且未關閉
                try:
                    loop = asyncio.get_event_loop()
                    if loop and not loop.is_closed():
                        # 嘗試同步關閉
                        if hasattr(self._browser, 'stop'):
                            self._browser.stop()
                except RuntimeError:
                    # 事件循環已關閉，忽略錯誤
                    pass
            except Exception:
                # 忽略所有清理錯誤
                pass
