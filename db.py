from typing import Union
import types
import pandas as pd

data: dict[str, list[Union[str, None]]] = {
    "title": [],
    "small_title": [],
    "image": [],
    "rating": [],
    "price": [],
}
df = pd.DataFrame(
    data=data,
)


def get_pd() -> types.ModuleType:
    return pd
