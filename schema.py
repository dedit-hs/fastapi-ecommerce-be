from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    email: str
    address: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    description: str
    category_id: int
    color: str
    price: int
    stock: int

    class Config:
        orm_mode = True


class Cart(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    price: int

    class Config:
        orm_mode = True
