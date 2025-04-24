from typing import Optional
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
from .util import Product


class MyntraScraper:
    def __init__(self, search: str):
        self.search = search
        self.base_url = "https://www.myntra.com/"

    def get_results(self):
        product_list = []
        query = self.search.replace(" ", "-")
        url = f"{self.base_url}{query}"

        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        items = soup.find_all("li", class_="product-base")

        for item in items:
            title = item.find("h3", class_="product-brand")
            small_title = item.find("h4", class_="product-product")
            price = item.find("div", class_="product-price")
            image_tag = item.find("img")
            image = (
                image_tag["src"] if image_tag and image_tag.has_attr("src") else None
            )

            product = Product(
                title=title.get_text(strip=True) if title else None,
                small_title=small_title.get_text(strip=True) if small_title else None,
                price=price.get_text(strip=True) if price else None,
                image=image,
                rating=None,
            )
            product_list.append(product.__dict__)

        return product_list


if __name__ == "__main__":
    results = MyntraScraper("red dress").get_results()
    print(pd.DataFrame(results).head())
