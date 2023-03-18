from dataclasses import dataclass


@dataclass
class Img:
    image: str
    alt: str


@dataclass
class Product:
    search_term: str
    name: str
    price: float
    url: str
    image: dict(Img)
