"""Main component from API module"""

import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from controllers import controller
from schemas import Product

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

app.mount("/pages", StaticFiles(directory="pages"), name="pages")


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the HTML interface."""
    with open("pages/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/products", response_model=List[Product])
def list_products(best_seller: bool = None, rating: float = None):
    """Returns a list with all products in the page"""
    return controller.list_products(best_seller=best_seller, rating=rating)


@app.get("/products/{name}", response_model=dict or None)
def get_product_by_name(name: str):
    """Get product by name or not found"""
    product = controller.get_product(name=name)
    if not product:
        logger.error(f"Product with name: {name} not found")
        raise HTTPException(
            status_code=404, detail=f"Product with name: {name} not found"
        )
    return product
