import os
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware, db
import uvicorn

from fastapi import FastAPI
from models import Category, Product
from schema import Category as SchemaCategory
from schema import Product as SchemaProduct

app = FastAPI()
load_dotenv(".env")

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DB_URL"])


@app.get("/")
def root():
    return {"message": "hello World"}


@app.post("/category/add", response_model=SchemaCategory)
def add_category(category: SchemaCategory):
    db_category = Category(name=category.name)
    db.session.add(db_category)
    db.session.commit()
    return db_category


@app.get("/category")
def get_category():
    categories = db.session.query(Category).all()
    return categories


@app.post("/product/add", response_model=SchemaProduct)
def add_product(product: SchemaProduct):
    db_product = Product(
        name=product.name,
        description=product.description,
        category_id=product.category_id,
        color=product.color,
        price=product.price,
        stock=product.stock,
    )
    db.session.add(db_product)
    db.session.commit()
    return db_product


@app.get("/products")
def get_products():
    products = db.session.query(Product).all()
    return products
