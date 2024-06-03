"""Main component from API module"""

from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse

from controllers import controller


app = FastAPI(debug=True)


@app.get("/list_products")
def list_products(best_seller: bool = False):
    """Returns a list with all products in the page"""
    return controller.list_products(best_seller=best_seller)


@app.get("/list_best_seller")
def list_best_seller_products():
    """Return a list with all products in the page marked as 'Mais Vendido'"""
    return controller.list_products(best_seller=True)


@app.get("/list_best_rated_products")
def list_best_rated_products(rating: float):
    """Return a list with all products that have rating bigger than the rating passed"""
    response = sorted(
        controller.list_products(rating=rating), key=lambda x: x["rating"], reverse=True
    )

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f"Product with rating higher than {rating} not found")
    return response


@app.get("/get_product_by_name")
def get_product_by_name(name: str):
    """Get product by name or not found"""
    response = controller.list_products(name=name)
    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f"Product with name: {name} not found")
    return response

