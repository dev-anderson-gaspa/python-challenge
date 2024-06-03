"""Main component from controller"""

import logging
from typing import List
from bs4 import BeautifulSoup, NavigableString, ResultSet
from models.product import Product

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Controller:
    """App controller class"""

    _instance = None
    _raw_products: ResultSet

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls, *args, **kwargs)
            cls._raw_products = cls._fill_products()
            logger.info(f"Products loaded.")
        return cls._instance

    def list_products(self, **kwargs):
        """Method responsible to read and parse the content page and return the list of products.
        If best sellers argument is given, the list will contain only the best sellers.
        If rating argument is given, the list will contain only products with a rating higher than the value passed.
        If name or part of the name is given, the list will return the list with products with the given name.
        Args:
            best_seller (bool): Flag if the list will be fulfilled with best seller products or all products.
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

        # Log the parsed products for debugging
        logger.info(f"Parsed products: {products}")
        return products

    @staticmethod
    def _fill_products():
        """Read and parse the HTML to find the products"""
        try:
            with open("pages/content.html", "r", encoding="utf-8") as e_commerce_html:
                soup = BeautifulSoup(e_commerce_html.read(), "html.parser")
                raw_products = soup.findAll(
                    "div",
                    {
                        "class": "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"
                    },
                )
                logger.info(f"Raw products found.")
                return raw_products
        except FileNotFoundError:
            logger.error("Error: content.html file not found.")
            return []

    @staticmethod
    def _is_best_seller(product: NavigableString) -> bool:
        """Analyze the product to see if it is a best seller
        Args:
            product (NavigableString): The product to be analyzed
        Returns:
            bool: Indicates if the product is a best seller
        """
        return product.find("span", {"class": "a-badge-text"}) is not None

    @staticmethod
    def _get_name(product: NavigableString) -> str:
        """Extract and return the name of the product
        Args:
            product (NavigableString): The product to be analyzed
        Returns:
            str: The formatted name of the product
        """
        return " ".join(
            product.find(
                "span", {"class": "a-size-base-plus a-color-base a-text-normal"}
            ).text.split()
        )

    @staticmethod
    def _get_price(product: NavigableString) -> float:
        """Extract the price of the product
        Args:
            product (NavigableString): The product to be analyzed
        Returns:
            float: The price of the product
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

    @staticmethod
    def _get_rating(product: NavigableString) -> float:
        """Extract the rating of the product
        Args:
            product (NavigableString): The product to be analyzed
        Returns:
            float: The rating of the product
        """
        raw_rating = product.find("a", {"class": "a-popover-trigger a-declarative"})
        rating = float(raw_rating.text.split(" de 5")[0].replace(",", "."))
        return rating

controller = Controller()
