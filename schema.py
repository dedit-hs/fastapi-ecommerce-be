from enum import Enum
from typing import List
from pydantic import BaseModel


class StatusEnum(str, Enum):
    unpaid = "Belum dibayar"
    paid = "Dibayar"
    done = "Selesai"


class AuthDetails(BaseModel):
    email: str
    password: str


class ShortUrl(BaseModel):
    url: str


class CustomerBase(BaseModel):
    name: str
    email: str
    address: str

    class Config:
        orm_mode = True


class CustomerCreate(CustomerBase):
    password: str


class CategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class SizeBase(BaseModel):
    size: str
    stock: int

    class Config:
        orm_mode = True


class SizeCreate(SizeBase):
    pass


class Size(SizeBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    url: str

    class Config:
        orm_mode = True


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: str
    color: str
    price: int
    image_url: str

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    category_id: int


class Product(ProductBase):
    id: str
    sizes: List[SizeBase] = []
    gallery: List[ImageBase] = []

    class Config:
        orm_mode = True


class Category(CategoryBase):
    id: int
    products: List[ProductBase] = []

    class Config:
        orm_mode = True


class CartBase(BaseModel):
    size: str
    quantity: int
    price: int

    class Config:
        orm_mode = True


class CartCreate(CartBase):
    customer_id: int
    product_id: int


class Cart(CartBase):
    id: int
    customer: List[CustomerBase] = []
    product: List[ProductBase] = []

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    total: int

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    customer_id: int


class OrderDetailBase(BaseModel):
    quantity: int
    price: int

    class Config:
        orm_mode = True


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    product_id: int


class OrderDetail(OrderDetailBase):
    id: int
    product: List[ProductBase] = []

    class Config:
        orm_mode = True


class Order(OrderBase):
    id: int
    status: StatusEnum = StatusEnum.unpaid
    details: List[OrderDetail] = []

    class Config:
        orm_mode = True


class Customer(CustomerBase):
    id: int
    orders: List[OrderBase] = []
    cart: List[CartBase] = []

    class Config:
        orm_mode = True
