import os
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware, db
import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from auth import AuthHandler
from models import Category, Customer, Product, ProductSize, Size
from schema import Category as SchemaCategory
from schema import Product as SchemaProduct
from schema import AuthDetails as SchemaAuth
from schema import Customer as SchemaCustomer
from schema import ProductSize as SchemaProductSize
from schema import Size as SchemaSize

app = FastAPI()
load_dotenv(".env")

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DB_URL"])

auth_handler = AuthHandler()


@app.post("/register", response_model=SchemaCustomer)
def register(customer: SchemaCustomer):
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


@app.post("/login")
def login(auth_details: SchemaAuth):
    user = db.session.query(Customer).filter_by(email=auth_details.email).first()

    if (user is None) or (
        not auth_handler.verify_password(auth_details.password, user.password)
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    token = auth_handler.encode_token(user.email)
    return {"accessToken": token}


# customer=Depends(auth_handler.auth_wrapper)


@app.post(
    "/category/add",
    response_model=SchemaCategory,
)
def add_category(category: SchemaCategory):
    db_category = Category(name=category.name)
    db.session.add(db_category)
    db.session.commit()
    return db_category


@app.get("/categories")
def get_category():
    categories = db.session.query(Category).all()
    return categories


@app.get("/category/{id}")
def get_category_by_id(id):
    category = db.session.query(Category).get(id)
    return category


@app.post(
    "/product/add",
    response_model=SchemaProduct,
)
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


@app.get("/products/{id}")
def get_product_by_id(id):
    product = (
        db.session.query(Product)
        .join(ProductSize, Product.id == ProductSize.product_id)
        .join(Size, ProductSize.size_id == Size.id)
        .where(Product.id == id)
        .all()
    )
    return product


@app.get("/products/category/{id}")
def get_products_by_category(id):
    products = db.session.query(Product).filter_by(category_id=id).all()
    return products


@app.post("/size/add", response_model=SchemaSize)
def add_size(size: SchemaSize):
    new_size = Size(size=size.size)
    db.session.add(new_size)
    db.session.commit()
    return new_size


@app.post("/product/{id}/addsize")
def add_product_size(id, size: SchemaProductSize):
    new_product_size = ProductSize(product_id=id, size_id=size.size_id)
    db.session.add(new_product_size)
    db.session.commit()

    return {"message": "Size was successfully added."}


@app.get("/product/{id}/sizes")
def get_product_sizes(id):
    sizes = (
        db.session.query(Size)
        .join(ProductSize, Size.id == ProductSize.size_id)
        .where(ProductSize.product_id == id)
        .all()
    )
    return sizes


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
