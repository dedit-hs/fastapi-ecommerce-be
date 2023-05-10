from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = Column(String)
    password = Column(String)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())



class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))
    color = Column(String)
    price = Column(String)
    stock = Column(Integer)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())
    category = relationship("Category")


class ProductImage(Base):
    __tablename__ = "product_image"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    image_id = Column(Integer, ForeignKey("image.id"))
    default = Column(Boolean, default=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())
    product = relationship("Product")
    image = relationship("Image")


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    total = Column(Integer)
    status = Column(String)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())
    customer = relationship("Customer")


class OrderDetail(Base):
    __tablename__ = "order_detail"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    price = Column(Integer)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())
    order = relationship("Order")
    product = relationship("Product")


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    price = Column(Integer)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())
    customer = relationship("Customer")
    product = relationship("Product")


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())
