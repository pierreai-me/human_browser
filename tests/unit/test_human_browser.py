import editdistance
import pytest
from pathlib import Path
from playwright.async_api import async_playwright
from human_browser import HumanBrowser


@pytest.mark.parametrize(
    "typing_p_skip,typing_p_duplication,typing_p_fixed_typo,check_fn",
    [
        (0.0, 0.0, 0.0, lambda got, query, d: d == 0),
        (0.2, 0.0, 0.0, lambda got, query, d: len(got) < len(query)),
        (0.0, 0.2, 0.0, lambda got, query, d: len(got) > len(query)),
        (0.0, 0.0, 0.2, lambda got, query, d: d == 0),
        # (0.01, 0.01, 0.05, lambda got, query, d: True),
    ],
)
@pytest.mark.asyncio
async def test_fill_and_press(
    typing_p_skip, typing_p_duplication, typing_p_fixed_typo, check_fn
):
    selector = "#APjFqb"
    text = "nicotine patches for weight loss"
    human_browser = HumanBrowser(
        typing_speed=50,
        typing_p_skip=typing_p_skip,
        typing_p_duplication=typing_p_duplication,
        typing_p_fixed_typo=typing_p_fixed_typo,
    )
    async with async_playwright() as p:
        # GIVEN
        headless = True
        args = ["--disable-gpu", "--no-sandbox"]
        browser = await p.chromium.launch(headless=headless, args=args)
        context = await browser.new_context()
        page = await context.new_page()
        # WHEN
        for path in (
            "tests/data/google_search_main.html",
            "tests/data/google_search_top.html",
        ):
            for before in ("two", "great concert tickets"):
                url = f"file://{Path(path).absolute()}"
                await page.goto(url)
                await human_browser.type(page, selector, before)
                await human_browser.type(page, selector, text)
                # THEN
                current_value = await page.evaluate(
                    f'document.querySelector("{selector}").value || ""'
                )
                d = editdistance.eval(current_value, text)
                assert check_fn(current_value, text, d)
