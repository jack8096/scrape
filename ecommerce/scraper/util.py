from typing import Optional, Union
from typing import Union
import pandas as pd


class Product:
    def __init__(
        self,
        url: str,
        title: Optional[str],
        small_title: Optional[str],
        image: Optional[str],
        rating: Optional[str],
        price: Optional[str],
    ) -> None:
        self.url:str = url
        self.title: Optional[str] = title
        self.small_title: Optional[str] = small_title
        self.image: Optional[str] = image
        self.rating: Optional[str] = rating
        self.price: Optional[str] = price


data: dict[str, list[Union[str, None]]] = {
    "title": [],
    "small_title": [],
    "image": [],
    "rating": [],
    "price": [],
}
df = pd.DataFrame(data=data)
