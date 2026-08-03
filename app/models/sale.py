import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import base

class Customer(base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(250), nullable=False)
    phone_number = Column(String(50), nullable=True)
    customer_loyal_points = Column(Integer, default=0, nullable=False)

    
    sales = relationship("Sale", back_populates="customer")


class Sale(base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(250), unique=True, nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("cashier_sessions.session_id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    final_amount = Column(Numeric(10, 2), nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    
    session = relationship("CashierSession", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale")
    payments = relationship("Payment", back_populates="sale")
    receipt = relationship("Receipt", uselist=False, back_populates="sale")


class SaleItem(base):
    __tablename__ = "sale_items"

    sale_item_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")
