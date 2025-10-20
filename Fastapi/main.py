from fastapi import Depends, FastAPI
from models import Product
from database import session, engine
import database_model
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"]
)
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
def get_all_products(db: Session = Depends(get_db)):
    # import Session and using dependecy injection insert the object here
    # notice here you are getting the object through dependecy injection
    db_products = db.query(database_model.Product).all()
    # db connection
    # fire query
    return db_products


@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_model.Product).filter(database_model.Product.id == id).first()
    )
    if db_product:
        return db_product
    return "product not found"


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    # products.append(product)
    db.commit()
    # whenever you make changes to
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_model.Product).filter(database_model.Product.id == id).first()
    )
    if db_product:
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db_product.name = product.name
        db.commit()
        return "Product updated sucessfully!"
    else:
        return "Product data not found to update"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_model.Product).filter(database_model.Product.id == id).first()
    )
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "Product not found to be deleted"
