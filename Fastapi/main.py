from fastapi import FastAPI
from models import Product
from database import session, engine
import database_model

app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)


def init_db():
    db = session()

    count = db.query(database_model.Product).count
    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
    # in the above line we can't use Pydantic model for inserting data into DB
    # so we convert our pydantic model into of database_model
    # such that convert pydantic object using model_dump() which gives you a dictionary
    # and then we unpack it using ** finally getting key value pair and create Product object for you
    db.commit()


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

init_db()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


get_db()


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
