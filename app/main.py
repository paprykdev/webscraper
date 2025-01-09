import asyncio
from scripts.monet import MonetScraper

if __name__ == "__main__":
    scraper = MonetScraper()
    try:
        asyncio.run(scraper.scrape())
    except KeyboardInterrupt:
        print('\nDUPA\n')
        scraper.save_data()
        asyncio.run(scraper.browser.close())
