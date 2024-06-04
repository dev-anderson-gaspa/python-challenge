"""Main component from controller"""

import logging
from typing import List

from bs4 import BeautifulSoup, NavigableString

from schemas import FilterClass, Product

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductController:
    """Product controller class"""

    _instance = None
    _products: List[Product]
    criteria = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProductController, cls).__new__(cls, *args, **kwargs)
            cls._products = cls._fill_products(ProductController)
            logger.info(f"Products loaded.")
        return cls._instance

    def list_products(self, **kwargs) -> List[Product]:
        """Retrieves a list of products that match the specified filter criteria.

        Args:
            **kwargs: Arbitrary keyword arguments specifying the filter criteria.
                    Possible attributes include 'name', 'price', 'best_seller', and 'rating'.

        Returns:
            List[Product]: A list of products that match all the specified criteria.
                        The list will be empty if no products match the criteria.
        """

        self.criteria = FilterClass(**kwargs)

        products = [product for product in self._products if self._matches(product)]
        # Log the parsed products
        logger.info(f"Parsed products: {products}")

        return products

    def get_product(self, **kwargs) -> Product:
        """Retrieves a product that matches the specified filter criteria.
        Args:
            **kwargs: Arbitrary keyword arguments specifying the filter criteria.
                    Possible attributes include 'name', 'price', 'best_seller', and 'rating'.

        Returns:
            Product: The first product that matches all the specified criteria.
                    Returns None if no product matches the criteria.
        """
        self.criteria = FilterClass(**kwargs)
        for product in self._products:
            if self._matches(product):
                # Log the parsed product
                logger.info(f"Parsed products: {product}")
                return product

        return None

    def _matches(self, product: Product) -> bool:
        """
        Checks if a product matches the specified filter criteria.

        Args:
            product (Product): The product to be checked.

        Returns:
            bool: Returns True if the product matches all the criteria, otherwise False.

        Raises:
            AttributeError: If the product does not have one of the attributes specified in the criteria.
        """
        for attr, value in self.criteria.criteria.items():
            if not hasattr(product, attr):
                raise AttributeError(f"Product has no attribute '{attr}'")
            product_value = getattr(product, attr)
            if not self.criteria.compare(attr, product_value, value):
                return False
        return True

    @staticmethod
    def _fill_products(cls) -> List[Product]:
        """Read and parse the HTML to find the products"""
        try:
            with open("pages/content.html", "r", encoding="utf-8") as e_commerce_html:
                soup = BeautifulSoup(e_commerce_html.read(), "html.parser")
                products_data = soup.findAll(
                    "div",
                    {
                        "class": "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"
                    },
                )
                logger.info(f"Raw products found.")
                products = []

                for product_data in products_data:
                    data = {
                        "best_seller": cls._is_best_seller(product_data),
                        "name": cls._get_name(product_data),
                        "rating": cls._get_rating(product_data),
                        "price": cls._get_price(product_data),
                    }
                    product = Product(**data)
                    products.append(product)

                return products
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


controller = ProductController()
