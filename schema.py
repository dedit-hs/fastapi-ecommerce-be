from pydantic import BaseModel


class AuthDetails(BaseModel):
    email: str
    password: str


class Customer(BaseModel):
    name: str
    email: str
    address: str
    password: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Size(BaseModel):
    size: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    description: str
    category_id: int
    color: str
    price: int
    stock: int
    image_url: str

    class Config:
        orm_mode = True


class ProductSize(BaseModel):
    size_id: int

    class Config:
        orm_mode = True


class Cart(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    price: int

    class Config:
        orm_mode = True
