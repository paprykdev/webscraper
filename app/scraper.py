import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


class Scraper:
    def __init__(self, url):
        self.url = url
        self.hrefs = []
        self.driver = self.load_driver()

    def load_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        return webdriver.Chrome(
            options=options,
            service=(
                Service(ChromeDriverManager().install())
                if os.path.exists("/.dockerenv")
                else None
            ),
        )

    def skip_cookies(self) -> None:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[_ngcontent-ng-c745257238]")
            )
        )

        button = self.driver.find_element(By.CSS_SELECTOR, "[_ngcontent-ng-c745257238]")
        self.driver.execute_script(
            """
                arguments[0].removeAttribute('disabled');
                arguments[0].className = 'border-button';
            """,
            button,
        )
        button.click()
        time.sleep(2)

    def load_page(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def locate_valid_artworks(self) -> list[str]:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".artwork-search-results"))
        )
        artworks = self.driver.find_elements(
            By.CSS_SELECTOR, ".artwork-search-results article"
        )
        for artwork in artworks:
            href = artwork.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            self.hrefs.append(href)
        return self.hrefs


def scrap(url: str):
    instance = Scraper(url)
    driver = instance.driver
    driver.get(url)

    instance.skip_cookies()
    instance.load_page()
    hrefs = instance.locate_valid_artworks()

    print(hrefs)
    html = driver.page_source
    driver.quit()
    return html
