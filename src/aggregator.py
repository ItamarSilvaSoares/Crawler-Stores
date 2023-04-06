from .websites import Amazon
from .product import Product


def test(sampling_cards, search_term, website):
    return (
        Product(search_term, name, price, url, image)
        for card in sampling_cards
        if (name := website._get_product_name(card, search_term)) is not None
        and (price := website._get_product_price(card)) is not None
        and (url := website._get_product_url(card)) is not None
        and (image := website._get_product_img(card)) is not None
    )


def get_products(search_term: str, amount):
    website = Amazon()
    url = website.get_url_to_search(search_term)
    sampling_cards = website.get_products(search_term)
    generator = test(sampling_cards, search_term, website)
    products = []
    a = True

    def tests(url):
        print(a)

    for i in range(5):
        try:
            products.append(next(generator))
        except StopIteration:
            break

    print(products)
    website.close_driver()


def tests(website, products):
    if url is None:
        website = Amazon()
        url = website.get_url_to_search(search_term)


if __name__ == "__main__":
    get_products("overlord")
