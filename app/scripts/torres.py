import time
import requests
import os
import json
from playwright.async_api import async_playwright
import asyncio


class TorresScraper:
    def __init__(self,
                 url="https://www.torresgarcia.com"):
        self.hrefs = []
        self.url = url
        self.data = []
        self.pages = 41
        self.email = "jinaj73631@nalwan.com"

    async def scrape(self):
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            await self.go_to(self.url)
            await self.login()
            await self.get_hrefs()
            self.page.set_default_timeout(5000)
            await self.get_data()
            self.save_data()
            await self.browser.close()

    async def login(self):
        enter_button = await self.find_el('#enterSiteLink')
        await enter_button.click()
        input = await self.find_el('#email')
        await input.fill(self.email)
        submit_button = await self.find_el('#loginReturn')
        await submit_button.click()

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
                    '#next')
                await pagination.click()
                time.sleep(1)
            el = await self.find_els(
                '#catWorks > .item > .recordContainer')
            for e in el:
                self.hrefs.append(await e.get_attribute('href'))

    async def get_image(self, href):
        image = "null"
        i = 0
        self.page.set_default_timeout(10000)
        while image == "null" and i < 30:
            try:
                image = await self.find_el(
                    "#mainImage")
            except Exception as e:
                print(f"Error: {e}\n\nOn page: {href}")
                return None
            image = await image.get_attribute('src')
            time.sleep(0.5)
            i += 1
        self.page.set_default_timeout(5000)
        return image

    def curl_image(self, image, id):
        try:
            os.mkdir("torres")
        except FileExistsError:
            pass

        if image != "null":
            image_response = requests.get(image)
            if image_response.status_code == 200:
                with open(f'torres/{id}.jpg', 'wb')\
                        as img_file:
                    img_file.write(image_response.content)

    async def get_title(self):
        try:
            title = await self.find_el(".div_Title em")
            title = await title.inner_text()
            return title
        except Exception:
            return None

    async def get_date(self):
        try:
            date = await self.find_el(".div_fullDate")
            date = await date.inner_text()
            return date
        except Exception:
            return None

    async def get_technique(self):
        try:
            technique = await self.find_el(".div_fullMedium")
            technique = await technique.inner_text()
            return technique
        except Exception:
            return None

    async def get_dimensions(self):
        try:
            dimensions = await self.find_el(".div_fullDimension")
            dimensions = await dimensions.inner_text()
            return dimensions
        except Exception:
            return None

    async def get_signature(self):
        try:
            signature = await self.find_el(".div_fullInscription")
            signature = await signature.inner_text()
            return signature
        except Exception:
            return

    async def get_location(self):
        try:
            location = await self.find_el(".div_CreditLine")
            location = await location.inner_text()
            return location
        except Exception:
            return None

    async def get_provenance(self):
        try:
            provenance = await self.find_els("#sectionProvenance > .sectionContent > .item")
            arr = []
            for paragraph in provenance:
                arr.append(await paragraph.inner_text())
            return arr
        except Exception:
            return []

    async def get_exhibitions(self):
        try:
            exhibitions = await self.find_els("#sectionExhibitions > .sectionContent > .item")
            arr = []
            for paragraph in exhibitions:
                arr.append(await paragraph.inner_text())
            return arr
        except Exception:
            return []

    async def get_bibliography(self):
        try:
            bibl = await self.find_els("#sectionLiterature > .sectionContent > .item")
            arr = []
            for paragraph in bibl:
                arr.append(await paragraph.inner_text())
            return arr
        except Exception:
            return []

    def save_data(self):
        try:
            os.mkdir("torres")
        except FileExistsError:
            pass
        open("torres/torres.json", "w", encoding="utf8").write(
            json.dumps([d for d in self.data], indent=4, ensure_ascii=False))

    async def get_data(self):
        for index, href in enumerate(self.hrefs):
            await self.go_to(f"{self.url}{href}")
            print(f"{index + 1}/{len(self.hrefs)}")
            image = await self.get_image(href)
            if not image:
                continue
            self.page.set_default_timeout(200)
            title = await self.get_title()
            date = await self.get_date()
            technique = await self.get_technique()
            dimensions = await self.get_dimensions()
            signature = await self.get_signature()
            location = await self.get_location()
            provenance = await self.get_provenance()
            exhibitions = await self.get_exhibitions()
            bibliography = await self.get_bibliography()
            self.page.set_default_timeout(5000)
            self.curl_image(image, index)

            self.data.append({
                "id": index,
                "title": title,
                "date": date,
                "name_of_artist": "Joan Torres Garcia",
                "technique": technique,
                "dimensions": dimensions,
                "signature": signature,
                "location": location,
                "image_url": image,
                "provenance": provenance,
                "exhibitions": exhibitions,
                "bibliography": bibliography
            })


if __name__ == "__main__":
    scraper = TorresScraper()
    try:
        asyncio.run(scraper.scrape())
    except KeyboardInterrupt:
        print('\nSaving data to json..\n')
        scraper.save_data()
        asyncio.run(scraper.browser.close())
