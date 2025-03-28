import asyncio
import random


class HumanBrowser:

    def __init__(
        self,
        typing_speed: float = 1.0,
        typing_p_skip: float = 0.01,
        typing_p_duplication: float = 0.01,
        typing_p_fixed_typo: float = 0.05,
    ):
        self.typing_speed = typing_speed
        self.typing_p_skip = typing_p_skip
        self.typing_p_duplication = typing_p_duplication
        self.typing_p_fixed_typo = typing_p_fixed_typo

    async def type(
        self, page, selector: str, text: str, delete_existing: bool = True
    ) -> None:
        """Type text with variations in typing speed and occasional errors."""
        # Click the entry box
        await page.wait_for_selector(selector, state="visible", timeout=100)
        await page.click(selector)

        async def press(char):
            delay = random.uniform(50, 200) / self.typing_speed
            await page.keyboard.press(char, delay=delay)

        # Delete existing text if any
        current_value = await page.evaluate(
            f'document.querySelector("{selector}").value || ""'
        )
        if current_value and delete_existing:
            if len(current_value) < 5:
                for _ in range(len(current_value)):
                    await press("Backspace")
                    await asyncio.sleep(random.uniform(0.05, 0.15) / self.typing_speed)
            else:
                await press("Control+A")
                await asyncio.sleep(random.uniform(0.1, 0.2) / self.typing_speed)
                await press("Backspace")
                await asyncio.sleep(random.uniform(0.1, 0.2) / self.typing_speed)

        # Type in query
        for char in text:
            if random.random() > self.typing_p_skip:
                await press(char)
            if random.random() < self.typing_p_duplication:
                await press(char)
            if random.random() < self.typing_p_fixed_typo:
                typo_keys = "qwertyuiopasdfghjklzxcvbnm"
                typo_char = random.choice(typo_keys)
                await press(typo_char)
                await asyncio.sleep(random.uniform(0.3, 0.5) / self.typing_speed)
                await press("Backspace")
                await asyncio.sleep(random.uniform(0.1, 0.2) / self.typing_speed)
            if random.random() < 0.1:  # extra pauses between some keystrokes
                await asyncio.sleep(random.uniform(0.1, 0.4) / self.typing_speed)
