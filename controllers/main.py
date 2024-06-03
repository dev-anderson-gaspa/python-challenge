"""Main component from controleer"""

from typing import List
from bs4 import BeautifulSoup, NavigableString, ResultSet

from models.product import Product


class Controller:
    """App controller class"""

    _instance = None
    _raw_products: ResultSet

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls, *args, **kwargs)
            cls._raw_products = cls._fill_products()
        return cls._instance

    def list_products(self, **kwargs):
        """Method responsable to read and parser the content page and return the list of products.
        If best sellers argument is given the list will contains only the best sellers
        If rating argument is given, the list will contains only products with rating higher than the value passed
        If name or part of the name was given, the list will return the list with products with the given name 
        Args:
            best_seller(bool): flags if the list will be a fulfilled with best seller products or all products
        """
        products = []
        for raw_product in self._raw_products:
            is_best_seller = self._is_best_seller(raw_product)
            name = self._get_name(raw_product)
            rating = self._get_rating(raw_product)
            price = self._get_price(raw_product)
            product = Product(name, price, is_best_seller, rating)

            if kwargs.get("best_seller"):
                if product.best_seller:
                    products.append(product.to_json())
            elif kwargs.get("rating"):
                if product.rating > kwargs.get("rating"):
                    products.append(product.to_json())
            elif kwargs.get("name"):
                if kwargs.get("name").lower() in product.name.lower():
                    products.append(product.to_json())
            else:
                products.append(product.to_json())

        # This should return the list of products
        return products
    
    def _fill_products():
        """Read and parse the html to find the products"""
        # Read html
        with open("pages/content.html", "r", encoding="utf-8") as e_commerce_html:

            # Parse html
            soup = BeautifulSoup(e_commerce_html.read(), "html.parser")

            raw_products = soup.findAll(
                "div",
                {
                    "class": "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"
                },
            )
            return raw_products

    def _is_best_seller(self, product: NavigableString) -> bool:
        """Analize the product if it is a best seller

        Args:
            product (NavigableString): the product that will be analized

        Returns:
            bool: indicate if the product is a best seller
        """
        return product.find("span", {"class": "a-badge-text"}) is not None

    def _get_name(self, product: NavigableString) -> str:
        """Extract and return the name from the product

        Args:
            product (NavigableString): the product that will be analized

        Returns:
            str: the formated name of the product
        """
        return " ".join(
            product.find(
                "span", {"class": "a-size-base-plus a-color-base a-text-normal"}
            ).text.split()
        )

    def _get_price(self, product: NavigableString) -> float:
        """Extract the price from the product

        Args:
            product (NavigableString): the product that will be analized

        Returns:
            float: the price of the product
        """

        integer_price = float(
            product.find("span", {"class": "a-price-whole"})
            .text.replace(",", "")
            .replace(".", "")
        )
        fraction_price = (
            float(product.find("span", {"class": "a-price-fraction"}).text) / 100
        )

        return integer_price + fraction_price

    def _get_rating(self, product: NavigableString) -> float:
        """Extract the rating from the product

        Args:
            product (NavigableString):  the product that will be analized

        Returns:
            float: the rating  of the product
        """
        raw_rating = product.find("a", {"class": "a-popover-trigger a-declarative"})
        rating = float(raw_rating.text.split(" de 5")[0].replace(",", "."))
        return rating


controller = Controller()
