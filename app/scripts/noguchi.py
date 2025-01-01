import time
from playwright.async_api import async_playwright
import asyncio

# TODO: Scrape through all the pages
"""
NOTE:
    Some pages doesn'y have info about paintings, so we need to skip them
"""


class NoguchiScraper:
    def __init__(self, url="https://archive.noguchi.org/Browse/CR", base_url="https://archive.noguchi.org"):
        self.hrefs = []
        self.base_url = base_url
        self.url = url
        self.data = []
        self.pages = 3

    async def scrape(self):
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            await self.go_to(self.url)
            await self.skip_cookies()
            await self.get_hrefs()
            self.page.set_default_timeout(10000)
            # await self.get_data()
            # self.save_data()
            await self.browser.close()

    async def skip_cookies(self):
        element = await self.find_el('a.acceptCookie')
        await element.click()

    async def find_el(self, selector: str):
        await self.wait_for_el(selector)
        return await self.page.query_selector(selector)

    async def find_els(self, selector: str):
        await self.wait_for_el(selector)
        return await self.page.query_selector_all(selector)

    async def wait_for_el(self, selector: str):
        await self.page.wait_for_selector(selector)

    async def go_to(self, url, tabs=False):
        hack = True
        while hack:
            try:
                await self.page.goto(url, timeout=60000)
                hack = False
            except Exception as e:
                print(e)
                print(f'error go to {url}')

    async def load_more(self):
        button = await self.find_el('.load-more-wrapper > a')
        await button.click()
        time.sleep(5)

    async def get_hrefs(self):
        await self.load_more()
        await self.load_more()
        links = await self.find_els('div.grid-flex.grid-cr-browse div.item-grid a')
        arr = []
        for link in links:
            href = await link.get_attribute('href')
            arr.append(href)
        print(arr)


if __name__ == "__main__":
    scraper = NoguchiScraper()
    asyncio.run(scraper.scrape())
