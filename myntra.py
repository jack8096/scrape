from typing import Optional
from playwright.sync_api import sync_playwright
from pandas.core import base
import requests
from bs4 import BeautifulSoup, Tag


baseUrl: str = "https://www.myntra.com/"
search: str = "red dress"
URL: str = baseUrl + search.replace(" ", "-")
print(URL)
html: Optional[str] = None


class MyntraScraper:
    def get_html(self, URL: str) -> Optional[str]:
        try:
            with sync_playwright() as pw:
                broswer = pw.firefox.launch(headless=False)
                page = broswer.new_page()
                page.goto(URL)
                html = page.content()
                return html
        except Exception as e:
            print(e)
            return None


html = MyntraScraper().get_html(URL)

if html == None:
    exit()
soup = BeautifulSoup(html, features="lxml")
item_containers: list[Tag] = soup.findAll("li", class_="product-base")
if item_containers.__len__() == 0:
    exit()
print(type(item_containers))
print(item_containers.__len__())
for item in item_containers:
    pass
