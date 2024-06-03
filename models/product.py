class Product:
    """A class representing a product in a retail shop.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        best_seller (bool): Indicates whether the product is a best seller.
        rating (float): The rating of the product.
    """

    def __init__(self, name: str, price: float, best_seller: bool, rating: float):
        """Initialize a Product instance."""
        self.name: str = name
        self.price: float = price
        self.best_seller: bool = best_seller
        self.rating: float = rating

    def to_json(self):
        """Transform the Product object into a JSON-compatible dictionary.
        Returns:
            dict: A dictionary containing the product information.
        """

        return {
            "name": self.name,
            "price": self.price,
            "best_seller": self.best_seller,
            "rating": self.rating,
        }
