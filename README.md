# Web scraper 🔍

## Description

This project is a web scraper designed to extract data from websites.

## How to use

1. Clone the repository
1. `cd webscraper`
1. `cd app`
1. `pip3 install -r requirements.txt`
1. `python3 scripts/monet.py` for the monet scraper
1. `python3 scripts/torres.py` for the torres scraper

## How to use with Docker

1. Clone the repository
1. `cd webscraper/app`
1. `docker compose up -d`
1. `docker exec -it docker exec -it scraper xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 1920x1080x24' python3 scripts/monet.py` for the monet scraper
1. `docker exec -it docker exec -it scraper xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 1920x1080x24' python3 scripts/torres.py` for the torres scraper
1. `docker compose down`

