import re
from typing import ClassVar, Union
from bs4 import BeautifulSoup, Tag
import pandas as pd
import requests

from util import Product


productList: list[dict[str, Union[str, None]]] = []

baseURL: str = "https://www.flipkart.com/search?q="
search: str = "red dress"
URL: str = (baseURL + search).replace(" ", "%20")
print(URL)
headers = {
    "Host": "www.flipkart.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Connection": "keep-alive",
    "Priority": "u=0, i",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}
response: requests.Response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print("flipkart response is not 200")
    print(response)
    exit()
soup = BeautifulSoup(response.content)
item_containers: list[Tag] = soup.findAll("div", attrs={"data-id": True})
if item_containers.__len__() == 0:
    exit()
print(type(item_containers))
print(item_containers.__len__())
for item in item_containers:
    title: Union[str, None] = getattr(
        item.find("div", class_="syl9yP"), "get_text", lambda: None
    )()
    small_title: Union[str, None] = getattr(
        item.find("a", class_="WKTcLC"), "get_text", lambda: None
    )()

    price: Union[str, None] = getattr(
        item.find("div", class_="Nx9bqj"), "get_text", lambda: None
    )()
    image: Union[None, str] = getattr(
        item.find("img", class_="_53J4C-"), "get_text", lambda: None
    )()

    productList.append(
        Product(
            title=title, small_title=small_title, price=price, image=image, rating=None
        ).__dict__
    )

flipkart_df = pd.DataFrame(data=productList)
print(flipkart_df)
