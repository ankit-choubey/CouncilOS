# browser_manager.py
from playwright.async_api import async_playwright


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir="profiles/chatgpt",
            headless=False
        )

    async def stop(self):
        await self.context.close()
        await self.playwright.stop()