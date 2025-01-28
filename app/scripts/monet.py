import time
import requests
import os
import json
from playwright.async_api import async_playwright
import asyncio


class MonetScraper:
    def __init__(self,
                 url="https://digitalprojects.wpi.art/monet/artworks?page=1",
                 base_url="https://digitalprojects.wpi.art"):
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
            self.page.set_default_timeout(5000)
            await self.get_data()
            self.save_data()
            await self.browser.close()

    async def skip_cookies(self):
        await self.wait_for_el('.button-disabled')
        await self.page.eval_on_selector(
            '.button-disabled', 'el => el.removeAttribute("disabled")')
        await self.page.click('.button-disabled')

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
            except Exception:
                print(f'error go to {url}')

    async def get_hrefs(self):
        for i in range(self.pages):
            if i > 0:
                pagination = await self.find_el(
                    'cpd-controls-pagination > button:last-child')
                await pagination.click()
                time.sleep(1)
            el = await self.find_els(
                '.artwork-search-results > article:not(.not-included) > a')
            for e in el:
                self.hrefs.append(await e.get_attribute('href'))

    async def get_image(self, href):
        image = "null"
        i = 0
        self.page.set_default_timeout(10000)
        while image == "null" and i < 30:
            try:
                image = await self.find_el(
                    ".not-full-screen-image-container > img")
            except Exception as e:
                print(f"Error: {e}\n\nOn page: {href}")
                return None
            image = await image.get_attribute('srcset')
            image = image.split(",")
            if len(image) > 0:
                image = image[len(image) - 1].strip().split(" ")[0]
            time.sleep(0.5)
            i += 1

        self.page.set_default_timeout(5000)
        return image

    def curl_image(self, image, title, id):
        try:
            os.mkdir("monet")
        except FileExistsError:
            pass

        if image != "null":
            image_response = requests.get(image)
            if image_response.status_code == 200:
                with open(f'monet/{id}.jpg', 'wb')\
                        as img_file:
                    img_file.write(image_response.content)

    async def get_title(self):
        title = await self.find_el(".details h1")
        title = await title.inner_text()
        return title

    async def get_info(self):
        info = await self.find_els("article[_ngcontent-ng-c746531210] p > p")
        return {
            "date": await info[0].inner_text(),
            "technique": await info[1].inner_text(),
            "dimensions": await info[2].inner_text(),
            "signature": await info[3].inner_text(),
        }

    def save_data(self):
        try:
            os.mkdir("monet")
        except FileExistsError:
            pass
        open("monet/monet.json", "w", encoding="utf8").write(
            json.dumps([d for d in self.data], indent=4, ensure_ascii=False))

    async def get_provenance(self):
        provenances = None
        try:
            provenances = await self.find_els("#provenance p p")
        except Exception:
            return None
        return [await p.inner_text() for p in provenances]

    async def get_exhibitions(self):
        exhibitions = None
        try:
            exhibitions = await self.find_els("#exhibition article")
        except Exception:
            return None
        arr = []
        for paragraph in exhibitions:
            await paragraph.wait_for_selector("p")
            ps = await paragraph.query_selector_all("p")
            arr.append(", ".join([await p.inner_text() for p in ps]))
        return arr

    async def get_bibliography(self):
        bibliography = None
        try:
            bibliography = await self.find_els("#publication article")
        except Exception:
            return None
        arr = []
        for paragraph in bibliography:
            await paragraph.wait_for_selector("p")
            ps = await paragraph.query_selector_all("p")
            arr.append(", ".join([await p.inner_text() for p in ps]))
        return arr

    async def get_data(self):
        for index, href in enumerate(self.hrefs):
            await self.go_to(f"{self.base_url}{href}")
            print(f"{index + 1}/{len(self.hrefs)}")
            image = await self.get_image(href)
            if not image:
                continue
            self.page.set_default_timeout(200)
            title = await self.get_title()
            get_info = await self.get_info()
            provenance = await self.get_provenance()
            exhibitions = await self.get_exhibitions()
            bibliography = await self.get_bibliography()
            self.page.set_default_timeout(5000)

            self.curl_image(image, title, id=index)
            self.data.append({
                "id": index,
                "title": title,
                "date": get_info["date"],
                "name_of_artist": "Claude Monet",
                "technique": get_info["technique"],
                "dimensions": get_info["dimensions"],
                "signature": get_info["signature"],
                "location": None,
                "image_url": image,
                "provenance": provenance if provenance else [],
                "exhibitions": exhibitions if exhibitions else [],
                "bibliography": bibliography if bibliography else [],
            })


if __name__ == "__main__":
    scraper = MonetScraper()
    try:
        asyncio.run(scraper.scrape())
    except KeyboardInterrupt:
        print('\nSaving data to json..\n')
        scraper.save_data()
        asyncio.run(scraper.browser.close())
