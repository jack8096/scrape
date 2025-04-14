import re
from typing import Union
from bs4 import BeautifulSoup
import pandas as pd
import requests
from util import Product, df


productList: list[dict[str, Union[str, None]]] = []

baseURL: str = "https://www.amazon.in/s?k="
search: str = "red dress"
URL: str = (baseURL + search).replace(" ", "+")
print(URL)

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
response: requests.Response = requests.get(URL, headers=headers)
if response.status_code != 200:
    exit()
# with open('content.txt', 'w') as file:
#     file.write(response.content.__str__())
soup = BeautifulSoup(response.content)
items_container = soup.findAll(
    "div",
    class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20",
)
print(items_container.__len__())
rating_pattern = re.compile(r"[0-9.]*")
for item_container in items_container:
    title = item_container.find("h2", class_="a-size-mini s-line-clamp-1")
    small_title = item_container.find(
        "h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal"
    )
    price = item_container.find("span", class_="a-price-whole")
    rating = item_container.find("span", class_="a-icon-alt")
    image = item_container.find("img")["src"]

    ratingValue = None if rating == None else rating_pattern.search(rating.get_text())
    productDict: dict[str, Union[str, None]] = Product(
        title=title.get_text(),
        small_title=small_title.get_text(),
        price=price.get_text(),
        image=image,
        rating=None if ratingValue == None else ratingValue.group(),
    ).__dict__
    productList.append(productDict)


amazon_df = pd.DataFrame(data=productList)

final_pd: pd.DataFrame = pd.concat([df, amazon_df])
print(final_pd)
