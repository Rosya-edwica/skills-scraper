import requests
import re
from bs4 import BeautifulSoup

from rabota_ru_cities.config import Region
import mysql_file


res = requests.get("https://rabota.ru/regions")
soup = BeautifulSoup(res.text, 'lxml')


def get_regions() -> list[Region]:
    regions: list[Region] = []

    blocks = soup.find_all("section", class_="indent-large")
    for block in blocks:
        urls = block.find("ul", class_="list-inline list-inline_md list-unstyled list-indents-sm clearfix").find_all("li")
        for url in urls:
            id = re.findall(r"\/\/.*?\.", url.a["href"])[0] # Забираем из строки "//shablykino.rabota.ru" следующее: "//shablykino."
            id = re.sub(r"\/|\.", "", id)
            regions.append(Region(Id=id, Name=url.text.replace("\n", ""))) # Вырезаем лишние символы

    return regions      


if __name__ == "__main__":
    regions = get_regions()
    mysql_file.update_mysql_city_table(regions)