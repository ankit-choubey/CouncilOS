import asyncio
from automation.selectors import CHATGPT_SELECTORS


class ChatGPTClient:
    def __init__(self, page):
        self.page = page

    async def send_prompt(self, prompt: str):
        prompt_box = self.page.get_by_placeholder("Ask anything")

        print(await prompt_box.is_visible())
        await self.page.pause()

        await prompt_box.wait_for(state="visible")
        await prompt_box.click()
        await prompt_box.fill(prompt)

        send_button = self.page.locator(
            CHATGPT_SELECTORS["send_button"]
        )

        await send_button.click()

    async def wait_for_response(self):
        previous_text = ""

        while True:
            messages = self.page.locator('[data-message-author-role="assistant"]')

            count = await messages.count()

            if count == 0:
                await asyncio.sleep(2)
                continue

            latest = messages.nth(count - 1)

            current_text = await latest.inner_text()

            if current_text == previous_text and current_text.strip() != "":
                break

            previous_text = current_text

            await asyncio.sleep(2)

        return current_text

    async def get_latest_response(self):
        messages = self.page.locator(
            '[data-message-author-role="assistant"]'
        )

        count = await messages.count()

        if count == 0:
            return ""

        latest = messages.nth(count - 1)

        return await latest.inner_text()