from dataclasses import dataclass
from decimal import Decimal

@dataclass
class AMZNProduct:
    iid: str = ""
    title: str = ""
    url: str = ""
    img_url: str = ""
    price: str = "" # json serialisation
    new_price: str = ""
    pct_change: str = ""
