import os
from typing import List
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware, db
import pyshorteners
import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from auth import AuthHandler
from models import Cart, Category, Customer, Image, Product, Size
from schema import Category as SchemaCategory
from schema import CategoryCreate as SchemaCategoryCreate
from schema import Product as SchemaProduct
from schema import AuthDetails as SchemaAuth
from schema import CustomerBase as SchemaCustomerBase
from schema import CustomerCreate as SchemaCustomerCreate
from schema import ProductCreate as SchemaProductCreate
from schema import ImageCreate as SchemaImageCreate
from schema import SizeBase as SchemaSizeBase
from schema import SizeCreate as SchemaSizeCreate
from schema import ShortUrl as SchemaShortUrl
from schema import CartCreate as SchemaCartCreate

app = FastAPI()
load_dotenv(".env")

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DB_URL"])

auth_handler = AuthHandler()


@app.post("/shortener", tags=["URL Shortener"])
def short_url(url: SchemaShortUrl):
    shortener = pyshorteners.Shortener()
    shorted_url = shortener.tinyurl.short(url.url)

    return {"shortUrl": shorted_url}


@app.post("/register", tags=["Customer"], response_model=SchemaCustomerBase)
def register(customer: SchemaCustomerCreate):
    is_customer = db.session.query(Customer).filter_by(email=customer.email).all()

    if is_customer:
        raise HTTPException(status_code=400, detail="Email already registered.")
    hashed_password = auth_handler.get_password_hash(customer.password)
    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        address=customer.address,
        password=hashed_password,
    )
    db.session.add(new_customer)
    db.session.commit()
    return new_customer


@app.post("/login", tags=["Customer"])
def login(auth_details: SchemaAuth):
    user = db.session.query(Customer).filter_by(email=auth_details.email).first()

    if (user is None) or (
        not auth_handler.verify_password(auth_details.password, user.password)
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    token = auth_handler.encode_token(user.email)
    return {"accessToken": token}


@app.post("/category/add", tags=["Category"], response_model=SchemaCategory)
def add_category(
    category: SchemaCategoryCreate, customer=Depends(auth_handler.auth_wrapper)
):
    db_category = Category(name=category.name)
    db.session.add(db_category)
    db.session.commit()
    return db_category


@app.get("/categories", tags=["Category"], response_model=List[SchemaCategory])
def get_category():
    categories = db.session.query(Category).all()
    return categories


@app.get("/category/{id}", tags=["Category"], response_model=SchemaCategory)
def get_category_by_id(id):
    category = db.session.query(Category).filter(Category.id == id).first()
    return category


@app.post(
    "/product/add",
    tags=["Product"],
    response_model=SchemaProduct,
)
def add_product(
    product: SchemaProductCreate, customer=Depends(auth_handler.auth_wrapper)
):
    shortener = pyshorteners.Shortener()
    url = shortener.tinyurl.short(product.image_url)

    db_product = Product(
        name=product.name,
        description=product.description,
        category_id=product.category_id,
        color=product.color,
        price=product.price,
        image_url=url,
    )
    db.session.add(db_product)
    db.session.commit()
    return db_product


@app.get("/products", tags=["Product"], response_model=List[SchemaProduct])
async def get_products():
    products = db.session.query(Product).all()
    return products


@app.get("/products/{id}", tags=["Product"], response_model=SchemaProduct)
def get_product_by_id(id):
    product = db.session.query(Product).filter(Product.id == id).first()
    return product


@app.get("/allsizes", tags=["Size"])
def get_all_sizes():
    sizes = db.session.query(Size).all()
    return sizes


@app.get(
    "/products/category/{id}", tags=["Product"], response_model=List[SchemaProduct]
)
def get_products_by_category(id):
    products = db.session.query(Product).filter_by(category_id=id).all()
    return products


@app.post("/product/{id}/addsize", tags=["Size"])
def add_product_size(
    id, size: SchemaSizeCreate, customer=Depends(auth_handler.auth_wrapper)
):
    new_product_size = Size(product_id=id, size=size.size, stock=size.stock)
    db.session.add(new_product_size)
    db.session.commit()

    return {"message": "Size was successfully added."}


@app.get("/product/{id}/sizes", tags=["Size"])
def get_product_sizes(id):
    sizes = db.session.query(Size).filter(Size.product_id == id).all()
    return sizes


@app.post("/product/{id}/addimage", tags=["Image"])
def add_product_image(
    id, image: SchemaImageCreate, customer=Depends(auth_handler.auth_wrapper)
):
    new_product_image = Image(product_id=id, image_url=image.url)
    db.session.add(new_product_image)
    db.session.commit()

    return {"message": "Image was successfully added."}


@app.get(
    "/product/{id}/images",
    tags=["Image"],
)
def get_product_images(id):
    images = db.session.query(Image).filter(Image.product_id == id).all()
    return images


@app.post("/cart", tags=["Cart"])
def add_to_cart(product: SchemaCartCreate, customer=Depends(auth_handler.auth_wrapper)):
    new_cart_product = Cart(
        customer_id=product.customer_id,
        product_id=product.product_id,
        size=product.size,
        quantity=product.quantity,
        price=product.price,
    )
    db.session.add(new_cart_product)
    db.session.commit()

    return {"message": "Product successfully added."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
