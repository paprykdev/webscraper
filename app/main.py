from scraper import scrap
import os
import json

urls = ["https://digitalprojects.wpi.art/monet/artworks"]
hrefs = []


def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(directory, "dist", "data.json")
    scrap(urls[0])

    data = []

    try:
        os.mkdir(os.path.join(directory, "dist"))
    except FileExistsError:
        pass
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)
    print("Data has been scraped!")


if __name__ == "__main__":
    main()
