from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    products:Mapped[List["Products"]] = relationship(back_populates="user")
    payments:Mapped[List["Payments"]] = relationship(back_populates="user")

class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="products")
    sales: Mapped[List["Sales"]] = relationship(back_populates="product")

class Sales(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)    
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    product: Mapped["Products"] = relationship(back_populates="sales")
    payments: Mapped[List["Payments"]] = relationship(back_populates="sale")

class Payments(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sales_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    mrid: Mapped[str] = mapped_column(String(100))
    crid: Mapped[str] = mapped_column(String(100))
    trans_code: Mapped[int] = mapped_column(Integer, nullable=True)
    trans_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    phone_paid: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    sale: Mapped["Sales"] = relationship(back_populates="payments")
    # user: Mapped["User"] = relationship(back_populates="payments")