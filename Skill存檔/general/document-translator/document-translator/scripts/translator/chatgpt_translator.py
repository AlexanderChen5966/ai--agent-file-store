"""
ChatGPT Translator - 使用 nodriver 自動化操作 ChatGPT 進行翻譯
Version: 2.1.0

技術特點：
- nodriver: undetected-chromedriver 作者的新一代反偵測瀏覽器自動化
- 自動下載並管理 Chrome，不依賴系統 Chrome 版本
- 內建反偵測，無需額外 stealth 設定
- Async/Await 非同步設計
- CAPTCHA 觸發率極低
"""

import asyncio
import time
from pathlib import Path
from typing import Optional

CHATGPT_URL = "https://chatgpt.com/"
CHATGPT_TW_TRANSLATE_URL = "https://chatgpt.com/zh-Hant/translate/"


class ChatGPTTranslator:
    """ChatGPT 翻譯器（nodriver 模式）- 主要翻譯器"""

    MAX_RETRIES = 3
    WAIT_TIMEOUT = 120
    CAPTCHA_WAIT_TIMEOUT = 120

    def __init__(self, verbose: bool = False, headless: bool = True):
        self.verbose = verbose
        self.headless = headless
        self._browser = None
        self._page = None

    def _log(self, message: str):
        """輸出日誌"""
        if self.verbose:
            print(f"  [ChatGPTTranslator] {message}")

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

        # nodriver 設定
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
                    self._log("建議: 使用 --no-headless 參數手動驗證一次")
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

    async def _wait_for_element(self, selector: str, timeout: int = None) -> Optional[any]:
        """等待元素出現並返回元素"""
        timeout = timeout or self.WAIT_TIMEOUT
        try:
            element = await self._page.select(selector, timeout=timeout)
            return element
        except Exception:
            return None

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
        """等待 ChatGPT 回應完成"""
        start_time = time.time()
        self._log("等待 ChatGPT 回應...")

        while time.time() - start_time < self.WAIT_TIMEOUT:
            try:
                # 檢查是否還在生成回應（查找 stop 按鈕）
                stop_button = await self._page.select(
                    'button[aria-label="Stop generating"]',
                    timeout=1
                )
                if not stop_button:
                    # 沒有 stop 按鈕表示回應完成
                    await asyncio.sleep(2)
                    self._log("回應完成")
                    return True
            except Exception:
                # 找不到 stop 按鈕，可能回應已完成
                await asyncio.sleep(2)
                return True
            await asyncio.sleep(0.5)

        return False

    async def _get_last_response(self) -> Optional[str]:
        """取得最後一個 ChatGPT 回應"""
        try:
            responses = await self._page.select_all(
                '[data-message-author-role="assistant"]'
            )
            if responses:
                last_response = responses[-1]
                text = await last_response.text
                return text
        except Exception as e:
            self._log(f"取得回應失敗: {e}")

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

    def _build_translation_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        """構建翻譯提示詞"""
        return f"""Translate the following text to Traditional Chinese (Taiwan).
Keep technical terms and Markdown format intact.
Do not add any extra explanation.
Use Taiwan terminology (帳號, 資料, 軟體, 網路).

---
{text}
---"""

    async def _is_translation_page(self) -> bool:
        """檢查是否在專用的翻譯頁面"""
        url = self._page.url or ""
        return "/translate" in url

    async def _translate_on_special_page(self, text: str) -> Optional[str]:
        """在專用翻譯頁面執行翻譯"""
        try:
            self._log("在專用翻譯頁面執行翻譯...")

            # ===== 步驟 1: 選擇目標語言為「中文 (繁體，臺灣)」=====
            self._log("步驟 1: 選擇目標語言...")

            # 使用 JavaScript 直接設定 <select> 元素的值
            # 語言選擇器是 <select> 元素，目標語言選擇器是第二個 select
            try:
                # 方式 1: 使用 JavaScript 設定第二個 select 的值為 zh-TW
                result = await self._page.evaluate("""
                    (() => {
                        const selects = document.querySelectorAll('select');
                        if (selects.length >= 2) {
                            const targetSelect = selects[1];  // 第二個 select 是目標語言
                            targetSelect.value = 'zh-TW';
                            // 觸發 change 事件，讓網頁知道值已改變
                            targetSelect.dispatchEvent(new Event('change', { bubbles: true }));
                            return targetSelect.value;
                        } else if (selects.length === 1) {
                            // 只有一個 select，可能是目標語言
                            const targetSelect = selects[0];
                            targetSelect.value = 'zh-TW';
                            targetSelect.dispatchEvent(new Event('change', { bubbles: true }));
                            return targetSelect.value;
                        }
                        return null;
                    })()
                """)

                if result == 'zh-TW':
                    self._log("✅ 已選擇「中文 (繁體，臺灣)」(value=zh-TW)")
                else:
                    self._log(f"⚠️ 語言設定結果: {result}")

                    # 方式 2: 備用 - 遍歷所有 select 找到包含 zh-TW 選項的
                    backup_result = await self._page.evaluate("""
                        (() => {
                            const selects = document.querySelectorAll('select');
                            for (let i = 0; i < selects.length; i++) {
                                const select = selects[i];
                                const options = select.querySelectorAll('option');
                                for (let opt of options) {
                                    if (opt.value === 'zh-TW') {
                                        select.value = 'zh-TW';
                                        select.dispatchEvent(new Event('change', { bubbles: true }));
                                        return 'zh-TW set on select ' + i;
                                    }
                                }
                            }
                            return 'zh-TW option not found';
                        })()
                    """)
                    self._log(f"備用方式結果: {backup_result}")

            except Exception as e:
                self._log(f"選擇語言時發生錯誤: {e}，嘗試繼續...")

            await asyncio.sleep(1)

            # ===== 步驟 2: 找到左側輸入框並輸入文字 =====
            self._log("步驟 2: 尋找輸入框...")

            input_textarea = None
            selectors = [
                'textarea[placeholder*="輸入"]',
                'textarea[placeholder*="貼上"]',
                'textarea',
            ]

            for selector in selectors:
                try:
                    input_textarea = await self._page.select(selector, timeout=5)
                    if input_textarea:
                        self._log(f"找到輸入框: {selector}")
                        break
                except Exception:
                    continue

            if not input_textarea:
                self._log("找不到輸入框")
                return None

            # 點擊並輸入
            await input_textarea.click()
            await asyncio.sleep(0.5)

            # 清空現有內容
            try:
                await input_textarea.clear_input()
            except Exception:
                # 如果 clear_input 不存在，用其他方式清空
                await input_textarea.send_keys("")
            await asyncio.sleep(0.3)

            # 輸入翻譯文字
            self._log(f"開始輸入文字 ({len(text)} 字元)...")
            await self._human_like_type(input_textarea, text)
            self._log("文字輸入完成")

            # ===== 步驟 3: 等待翻譯完成 =====
            self._log("步驟 3: 等待翻譯完成...")

            # 計算最大等待時間：根據文字長度動態調整（長文檔需要更多時間）
            max_wait_time = max(60, min(180, len(text) // 200 * 5 + 30))
            self._log(f"最大等待時間: {max_wait_time} 秒")

            # 等待翻譯完成的策略：檢測輸出內容是否穩定（不再變化）
            start_time = time.time()
            last_output_length = 0
            stable_count = 0  # 連續幾次內容長度相同
            required_stable_count = 3  # 需要連續穩定 3 次（約 9 秒）才認為完成

            while time.time() - start_time < max_wait_time:
                await asyncio.sleep(3)

                try:
                    # 取得輸出 textarea 的內容長度
                    current_output = await self._page.evaluate("""
                        (() => {
                            const textareas = document.querySelectorAll('textarea');
                            if (textareas.length >= 2) {
                                return textareas[1].value || '';
                            }
                            return '';
                        })()
                    """)

                    current_length = len(current_output) if current_output else 0
                    elapsed = int(time.time() - start_time)

                    if current_length > 0:
                        if current_length == last_output_length:
                            stable_count += 1
                            self._log(f"輸出穩定中... ({stable_count}/{required_stable_count}) - {current_length} 字元 ({elapsed}秒)")

                            if stable_count >= required_stable_count:
                                self._log(f"✅ 翻譯內容已穩定，共 {current_length} 字元")
                                break
                        else:
                            stable_count = 0  # 重置穩定計數
                            self._log(f"翻譯進行中... {last_output_length} → {current_length} 字元 ({elapsed}秒)")

                        last_output_length = current_length
                    else:
                        self._log(f"等待翻譯開始... ({elapsed}/{max_wait_time} 秒)")

                except Exception as e:
                    self._log(f"檢查輸出時發生錯誤: {e}")

            # 額外等待確保完全完成
            await asyncio.sleep(3)

            # ===== 步驟 4: 點擊複製按鈕取得結果 =====
            self._log("步驟 4: 點擊複製按鈕...")

            result = None

            try:
                # 找到複製按鈕（根據截圖是右側翻譯結果區域的複製圖示）
                # 複製按鈕通常有 copy 相關的 aria-label 或 class
                copy_button = None

                # 方式 1: 找 SVG 圖示按鈕（複製圖示）
                buttons = await self._page.select_all('button')
                for btn in buttons:
                    try:
                        # 檢查按鈕的 aria-label 或內部內容
                        btn_html = await btn.get_html()
                        if btn_html and ('copy' in str(btn_html).lower() or 'clipboard' in str(btn_html).lower()):
                            copy_button = btn
                            break
                    except Exception:
                        continue

                # 方式 2: 找右側區域的按鈕（根據截圖位置）
                if not copy_button:
                    # 複製按鈕在右側翻譯結果下方
                    all_buttons = await self._page.select_all('button, div[role="button"]')
                    # 通常複製按鈕是較小的圖示按鈕
                    for btn in all_buttons:
                        try:
                            btn_text = btn.text if hasattr(btn, 'text') else ""
                            # 複製按鈕通常沒有文字，只有圖示
                            if not btn_text or len(str(btn_text).strip()) == 0:
                                copy_button = btn
                                # 不要立即 break，繼續找更合適的
                        except Exception:
                            continue

                if copy_button:
                    await copy_button.click()
                    self._log("已點擊複製按鈕")
                    await asyncio.sleep(1)

                    # 從剪貼簿取得結果
                    try:
                        # 使用 JavaScript 讀取剪貼簿
                        result = await self._page.evaluate("navigator.clipboard.readText()")
                        if result:
                            self._log(f"從剪貼簿取得結果 ({len(result)} 字元)")
                    except Exception as e:
                        self._log(f"無法讀取剪貼簿: {e}")

            except Exception as e:
                self._log(f"點擊複製按鈕失敗: {e}")

            # ===== 步驟 5: 備用方式取得結果 =====
            if not result:
                self._log("步驟 5: 嘗試備用方式取得結果...")

                # 方式 A: 直接從第二個 textarea 取得內容
                try:
                    textareas = await self._page.select_all('textarea')
                    if len(textareas) >= 2:
                        output_textarea = textareas[1]
                        # 使用 JavaScript 取得 value
                        result = await self._page.evaluate(
                            "document.querySelectorAll('textarea')[1].value"
                        )
                        if result:
                            self._log(f"從 textarea 取得結果 ({len(result)} 字元)")
                except Exception as e:
                    self._log(f"備用方式 A 失敗: {e}")

                # 方式 B: 從頁面 DOM 取得
                if not result:
                    try:
                        # 取得右側區域的所有文字
                        result = await self._page.evaluate("""
                            (() => {
                                const textareas = document.querySelectorAll('textarea');
                                if (textareas.length >= 2) {
                                    return textareas[1].value || textareas[1].textContent;
                                }
                                return null;
                            })()
                        """)
                        if result:
                            self._log(f"從 DOM 取得結果 ({len(result)} 字元)")
                    except Exception as e:
                        self._log(f"備用方式 B 失敗: {e}")

            if result and result.strip():
                self._log(f"✅ 翻譯成功！結果長度: {len(result)} 字元")
                return result.strip()
            else:
                self._log("❌ 無法取得翻譯結果（剪貼簿為空或點擊失敗）")
                return None

        except Exception as e:
            self._log(f"專用頁面錯誤: {e}")
            import traceback
            self._log(traceback.format_exc())
            return None

    async def _translate_async(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "zh-TW",
    ) -> Optional[str]:
        """非同步翻譯實作"""
        if not text or not text.strip():
            return text

        self._log(f"嘗試翻譯 ({len(text)} 字元)")

        try:
            await self._init_browser()

            # 導航到 ChatGPT
            url = CHATGPT_TW_TRANSLATE_URL if target_lang == "zh-TW" else CHATGPT_URL
            self._log(f"導航到: {url}")

            self._page = await self._browser.get(url)
            await asyncio.sleep(5)  # 等待頁面載入

            self._log(f"當前 URL: {self._page.url}")

            # 檢查 CAPTCHA
            if not await self._check_for_captcha():
                return None

            # 額外等待頁面穩定
            await asyncio.sleep(2)

            # 檢查是否在專用翻譯頁面
            if await self._is_translation_page():
                return await self._translate_on_special_page(text)

            # 一般對話模式
            prompt = self._build_translation_prompt(text, source_lang, target_lang)

            if not await self._send_message(prompt):
                return None

            if not await self._wait_for_response():
                self._log("等待回應逾時")
                return None

            result = await self._get_last_response()

            if result:
                self._log(f"翻譯成功 ({len(result)} 字元)")

            return result

        except Exception as e:
            self._log(f"翻譯錯誤: {e}")
            import traceback
            self._log(traceback.format_exc())
            return None

        finally:
            if self.headless:
                await self._close_browser()

    def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "zh-TW",
    ) -> Optional[str]:
        """
        使用 ChatGPT 進行翻譯（同步包裝器）
        """
        try:
            import nodriver as uc
            # 使用 nodriver 的事件循環
            loop = uc.loop()
            result = loop.run_until_complete(
                self._translate_async(text, source_lang, target_lang)
            )
            return result
        except Exception as e:
            self._log(f"翻譯失敗: {e}")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return None
        finally:
            # 確保瀏覽器在翻譯完成後關閉
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
