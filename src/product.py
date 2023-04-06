from dataclasses import dataclass


@dataclass
class Product:
    search_term: str
    name: str
    price: float
    url: str
    image: dict

    def __str__(self):
        return (
            f"Termo de Pesquisa: {self.search_term}\n"
            f"Nome do Produto: {self.name}\n"
            f"Preço do Produto: {self.price}\n"
            f"Link do Produto: {self.url}"
        )
