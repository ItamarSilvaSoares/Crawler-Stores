from time import sleep
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.websites.abstract_classes.driver import Driver
from src.websites.amazon.utils.classes_names_amazon import classes_name


class Amazon(Driver):
    URL_BASE = "https://www.amazon.com.br"
    URL_SEARCH = "/s?k="

    CARD = "CLASS_CARD_PRODUCTS"
    TITLE = "SPAN_CLASS_TITLE"
    PRICE = "PRICE_WHOLE"
    CENTS = "PRICE_FRACTION"
    LINK = "URL_LINK_PRODUCT"
    NEXT_PAGE = "NEXT_PAGE"
    IMG = "IMG"

    def __init__(self) -> None:
        self.init_driver()

    def get_url_to_search(self, product_name: str = ""):
        url = self.URL_BASE + self.URL_SEARCH + product_name.replace(" ", "+").lower()
        self.go_to(url)

    def get_classes_name(self, class_: str):
        return classes_name[class_].replace(" ", ".")

    def _get_products_card(self) -> None:
        self.cards = self.get_elements_by_something(
            By.CLASS_NAME, self.get_classes_name(self.CARD)
        )

    def _get_product_name(self, card: WebElement) -> Optional[str]:
        return card.find_element(By.CLASS_NAME, self.get_classes_name(self.TITLE)).text

    def _get_product_price(self, card: WebElement) -> Optional[float]:
        price = card.find_element(
            By.CLASS_NAME, self.get_classes_name(self.PRICE).text
        ).replace(",", "")

        cents = card.find_element(By.CLASS_NAME, self.get_classes_name(self.CENTS)).text
        price_final = price + "." + cents

        return float(price_final)

    def _get_product_url(self, card: WebElement) -> Optional[str]:
        element_a = card.find_element(By.CLASS_NAME, self.get_classes_name(self.LINK))
        href = element_a.get_attribute("href")
        return self.URL_BASE + href

    def _get_product_img(self, card: WebElement) -> Optional[tuple[str]]:
        src = card.get_attribute("src")
        alt = card.get_attribute("alt")
        return src, alt

    def _get_next_page(self):
        next_button = self.get_element_by_something(
            By.CLASS_NAME, self.get_classes_name(self.NEXT_PAGE)
        )
        href = next_button.get_attribute("href")
        return self.URL_BASE + href


if __name__ == "__main__":
    a = Amazon()
    a._get_products_card("mouse rgb")

    sleep(30)
