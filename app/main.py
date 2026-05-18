import asyncio
from automation.browser_manager import BrowserManager


async def main():
    manager = BrowserManager()
    await manager.start()

    input("Browser launched. Press Enter to close...")

    await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())