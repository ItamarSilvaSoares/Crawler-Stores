from time import sleep
from typing import Optional, Iterable, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


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
        self.cards = []

    def get_url_to_search(self, product_name: str = "") -> str:
        return self.URL_BASE + self.URL_SEARCH + product_name.replace(" ", "+").lower()

    def get_classes_name(self, class_: str):
        return classes_name[class_].replace(" ", ".")

    def _get_products_cards(self) -> None:
        self.cards.extend(
            self.get_elements_by_something(
                By.CLASS_NAME, self.get_classes_name(self.CARD)
            )
        )

    def _get_product_name(self, card: WebElement, search_term: str) -> Optional[str]:
        try:
            name = card.find_element(
                By.CLASS_NAME, self.get_classes_name(self.TITLE)
            ).text
            return name if search_term in name.lower() else None
        except NoSuchElementException:
            return None

    def _get_product_price(self, card: WebElement) -> Optional[float]:
        try:
            price = (
                card.find_element(By.CLASS_NAME, self.get_classes_name(self.PRICE)).text
            ).replace(",", "")

            cents = card.find_element(
                By.CLASS_NAME, self.get_classes_name(self.CENTS)
            ).text
            price_final = price + "." + cents

            return float(price_final)
        except NoSuchElementException:
            return None

    def _get_product_url(self, card: WebElement) -> Optional[str]:
        try:
            element_a = card.find_element(
                By.CLASS_NAME, self.get_classes_name(self.LINK)
            )
            href = element_a.get_attribute("href")
            return href
        except NoSuchElementException:
            return None

    def _get_product_img(self, card: WebElement) -> Dict:
        img = card.find_element(By.CLASS_NAME, self.get_classes_name(self.IMG))
        src = img.get_attribute("src")
        alt = img.get_attribute("alt")
        return {"src": src, "alt": alt}

    def _get_next_page(self):
        next_button = self.get_element_by_something(
            By.CLASS_NAME, self.get_classes_name(self.NEXT_PAGE)
        )
        return next_button.get_attribute("href") if next_button else next_button

    def get_products(self, product_name: str, sampling: int = 60):
        url = self.get_url_to_search(product_name)
        while len(self.cards) < sampling and url:
            self.go_to(url)
            self._get_products_cards()
            url = self._get_next_page()

        return self.cards


if __name__ == "__main__":
    a = Amazon()
    a.get_products("mouse rgb")
    sleep(30)
