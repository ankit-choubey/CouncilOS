# browser_manager.py
from playwright.async_api import async_playwright


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir="profiles/chatgpt",
            headless=False
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()

        await self.page.goto("https://chatgpt.com")

    async def stop(self):
        await self.context.close()
        await self.playwright.stop()