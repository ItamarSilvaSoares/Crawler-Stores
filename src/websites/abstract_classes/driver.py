from abc import ABC, abstractmethod
from typing import Iterable, Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from src.product import Product


class Driver(ABC):
    USER_AGENT = {
        "userAgent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/110.0.0.0"
            " Safari/537.36 Edg/111.0.1661.44"
        )
    }
    TIMEOUT = 5

    def init_driver(self) -> None:
        service = Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        )

        options = Options()
        options.add_argument("--user-data-dir=chrome-data")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-browser-side-navigation")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.__driver = webdriver.Chrome(service=service, options=options)

        self.__driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.__driver.execute_cdp_cmd("Network.setUserAgentOverride", self.USER_AGENT)

        print(
            f'userAgent used: {self.__driver.execute_script("return navigator.userAgent;")}'
        )

    def go_to(self, url: str) -> None:
        """Go to page specific"""
        self.__driver.get(url)

    def close_driver(self) -> None:
        """Close the webDriver"""
        self.__driver.quit()

    def get_element_by_something(self, by, value: str) -> WebElement:
        """Get one element in page"""
        try:
            return WebDriverWait(self.__driver, timeout=self.TIMEOUT).until(
                lambda d: d.find_element(by, value)
            )
        except TimeoutException:
            return None

    def get_elements_by_something(self, by, value: str) -> Iterable[WebElement]:
        """Get several element in page"""
        try:
            return WebDriverWait(self.__driver, timeout=self.TIMEOUT).until(
                lambda d: d.find_elements(by, value)
            )
        except TimeoutException:
            return None

    def factory_products(
        self, cards: Iterable[WebElement], search_term
    ) -> Iterable[Product]:
        return (
            Product(search_term, name, price, url, image)
            for card in cards
            if (name := self._get_product_name(card, search_term)) is not None
            and (price := self._get_product_price(card)) is not None
            and (url := self._get_product_url(card)) is not None
            and (image := self._get_product_img(card)) is not None
        )

    @abstractmethod
    def _get_product_img(self, card: WebElement) -> Optional[str]:
        """Get the url and alt image from the product's page in the website"""
        raise NotImplementedError

    @abstractmethod
    def _get_product_name(self, card: WebElement) -> Optional[str]:
        """Get the product's full name as displayed in the search results"""
        raise NotImplementedError

    @abstractmethod
    def _get_product_price(self, card: WebElement) -> Optional[float]:
        """Get the product's price"""
        raise NotImplementedError

    @abstractmethod
    def _get_product_url(self, card: WebElement) -> Optional[str]:
        """Get the url to the product's page in the website"""
        raise NotImplementedError

    @abstractmethod
    def get_classes_name(self, class_: str) -> str:
        """Get and format the class name the objects in page"""
        raise NotImplementedError

    @abstractmethod
    def _get_next_page(self) -> str:
        """Get the url to next page"""
        raise NotImplementedError
