import re
from typing import Union
from bs4 import BeautifulSoup
import pandas as pd
import requests
from util import Product, df


class AmazonScraper:
    def __init__(self, search):
        self.search = search
        self.base_url = "https://www.amazon.in/s?k="

    def get_results(self):
        product_list = []
        url = self.base_url + self.search.replace(" ", "+")
        headers = {
            "Host": "www.amazon.in",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Priority": "u=0, i",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("div", {"data-asin": True})

        rating_pattern = re.compile(r"[0-9.]+")
        for item in items:
            url = None
            urlValue = item.find('a', class_='a-link-normal s-no-outline')
            if urlValue != None:
                url = urlValue.get('href')
            title = item.find("h2")
            small_title = item.find("span", class_="a-text-normal")
            price = item.find("span", class_="a-price-whole")
            rating = item.find("span", class_="a-icon-alt")
            image_tag = item.find("img")
            image = (
                image_tag["src"] if image_tag and image_tag.has_attr("src") else None
            )
            rating_value = rating_pattern.search(rating.get_text()) if rating else None

            product = Product(
                url=f'https://www.amazon.in{url}',
                title=title.get_text(strip=True) if title else None,
                small_title=small_title.get_text(strip=True) if small_title else None,
                price=price.get_text(strip=True) if price else None,
                image=image,
                rating=rating_value.group() if rating_value else None,
            )
            product_list.append(product.__dict__)

        return product_list


if __name__ == "__main__":
    res = AmazonScraper("red dress").get_results()
    print(res)
