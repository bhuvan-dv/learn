from fastapi import FastAPI
from models import Product
from database import session, engine
from database_model import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "hey there"


products = [
    Product(id=1, name="phone", description="budget phone", price=99, quantity=10),
    Product(
        id=2, name="Flip phone", description="decent phone", price=199, quantity=100
    ),
    Product(
        id=3,
        name="Expensive phone",
        description="flagship phone",
        price=1999,
        quantity=10000,
    ),
]


@app.get("/products")
def get_all_products():
    # db connection
    # fire query
    return products


@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "product not found"


@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product


@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product has been updated"
    return "Product data not found to update"


@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product Has been deleted"
    return "Product not found to be deleted"
