from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import base

class Category(base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)

    
    products = relationship("Product", back_populates="category")


class Supplier(base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(250), nullable=False)

    
    products = relationship("Product", back_populates="supplier")


class Product(base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=True)
    product_exp_date = Column(Date, nullable=True)
    product_barcode = Column(String(250), unique=True, nullable=False, index=True)
    product_stock_quantity = Column(Integer, default=0, nullable=False)
    product_vat = Column(Numeric(5, 2), nullable=False)
    product_price_per_unit = Column(Numeric(10, 2), nullable=False)
    product_discount = Column(Numeric(10, 2), default=0.00, nullable=False)

    
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")
