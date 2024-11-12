import os
import json


def scraper():
    directory = "dist"
    file_path = os.path.join(directory, "data.json")

    data = []

    try:
        os.mkdir("dist")
    except FileExistsError:
        pass
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)
    print("Data has been scraped!")
