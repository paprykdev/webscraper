import asyncio
from scripts.monet import MonetScraper

if __name__ == "__main__":
    scraper = MonetScraper()
    asyncio.run(scraper.scrape())
