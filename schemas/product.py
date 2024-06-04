from pydantic import BaseModel


class Product(BaseModel):
    """Product schema"""

    name: str
    price: float
    best_seller: bool
    rating: float
