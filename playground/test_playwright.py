import asyncio
from playwright.async_api import async_playwright

async def main():
    # proxy = "http://123.123.123.123:8080"  # Replace with your proxy

    async with async_playwright() as p:
        # browser = await p.chromium.launch(proxy={"server": proxy}, headless=False)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # await page.goto("https://www.google.com")
        await page.goto("http://mevzuat.gov.tr")

        await page.screenshot(path="screenshot.png", full_page=True)
        print("Screenshot saved as screenshot.png")

        await browser.close()

asyncio.run(main())
