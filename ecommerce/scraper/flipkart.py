import re
from typing import ClassVar, Union
from bs4 import BeautifulSoup, Tag
import pandas as pd
import requests

from .util import Product
# from util import Product


class FlipkartScraper:
    def __init__(self, search):
        self.search = search
        self.base_url = "https://www.flipkart.com/search?q="

    def get_results(self):
        product_list = []
        url = self.base_url + self.search.replace(" ", "%20")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")

        items = soup.findAll("div", attrs={"data-id": True})
        for item in items:
            url = None
            urlValue = item.find('a', class_='rPDeLR')
            if urlValue != None:
                url = urlValue.get('href')
            title = item.find("div", class_="syl9yP")
            small_title = item.find("a", class_="WKTcLC")
            price = item.find("div", class_="Nx9bqj")
            image = item.find("img", class_="_53J4C-")

            product = Product(
                url=f'https://www.flipkart.com{url}',
                title=title.get_text() if title else None,
                small_title=small_title.get_text() if small_title else None,
                price=price.get_text() if price else None,
                image=image["src"] if image else None,
                rating=None,
            )
            product_list.append(product.__dict__)

        return product_list


if __name__ == "__main__":
    res = FlipkartScraper("red dress").get_results()
    print(res)
