from abc import ABC, abstractmethod
from typing import List, Optional

from bs4 import BeautifulSoup

HTML = str


class Website(ABC):
    USER_AGENT = {
        "userAgent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/110.0.0.0"
            " Safari/537.36 Edg/111.0.1661.44"
        )
    }

    @abstractmethod
    def _get_search_page_with_search_results(self, product_name: str) -> BeautifulSoup:
        """Request the search page and return it's BeautifulSoup object"""

    @abstractmethod
    def _get_next_page(self) -> str:
        """Get the url to next page"""
        raise NotImplementedError

    @abstractmethod
    def _get_products_html(self, name: str) -> List[HTML]:
        """Get the HTML content of all products in the search page"""
        raise NotImplementedError

    @abstractmethod
    def _get_product_name(self, product_html: str) -> Optional[str]:
        """Get the product's full name as displayed in the search results"""
        raise NotImplementedError

    @abstractmethod
    def _get_product_price(self, product_html: str) -> Optional[float]:
        """Get the product's price"""
        raise NotImplementedError

    @abstractmethod
    def _get_product_url(self, product_html: str) -> Optional[str]:
        """Get the url to the product's page in the website"""
        raise NotImplementedError
