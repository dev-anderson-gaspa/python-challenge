"""Main component from API module"""

import logging
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from controllers import controller

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

@app.get("/list_products")
def list_products(best_seller: bool = False):
    """Returns a list with all products in the page"""
    products = controller.list_products(best_seller=best_seller)
    logger.info(f"list_products: {products}")
    return json.dumps(products)

@app.get("/list_best_seller")
def list_best_seller_products():
    """Return a list with all products in the page marked as 'Mais Vendido'"""
    products = controller.list_products(best_seller=True)
    logger.info(f"list_best_seller_products: {products}")
    return json.dumps(products)

@app.get("/list_best_rated_products")
def list_best_rated_products(rating: float):
    """Return a list with all products that have rating bigger than the rating passed"""
    response = sorted(
        controller.list_products(rating=rating), key=lambda x: x["rating"], reverse=True
    )
    logger.info(f"list_best_rated_products: {response}")

    if len(response) == 0:
        logger.error(f"Product with rating higher than {rating} not found")
        raise HTTPException(status_code=404, detail=f"Product with rating higher than {rating} not found")
    return json.dumps(response)

@app.get("/get_product_by_name")
def get_product_by_name(name: str):
    """Get product by name or not found"""
    response = controller.list_products(name=name)
    logger.info(f"get_product_by_name: {response}")
    if len(response) == 0:
        logger.error(f"Product with name: {name} not found")
        raise HTTPException(status_code=404, detail=f"Product with name: {name} not found")
    return json.dumps(response)