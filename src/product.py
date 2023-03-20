from dataclasses import dataclass


@dataclass
class Product:
    search_term: str
    name: str
    price: float
    url: str
    image: dict
