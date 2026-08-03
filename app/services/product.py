import datetime
from sqlalchemy.orm import Session
from app.models.product import Product, Category, Supplier

class ProductService:
    @staticmethod
    def create_category(db: Session, name: str, description: str) -> Category:
        """Creates an organizational lookup grouping for products."""
        category = Category(category_name=name, description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def create_supplier(db: Session, company_name: str) -> Supplier:
        """Registers a merchant wholesale supplier within the store framework."""
        supplier = Supplier(company_name=company_name)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def add_catalog_product(db: Session, product_data: dict) -> Product:
        """Injects a unique scanner barcode item reference directly into inventory repositories."""
        new_product = Product(**product_data)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @staticmethod
    def add_stock_replenishment(db: Session, product_id: int, added_quantity: int) -> Product:
        """Safely updates physical inventory quantities upon delivery dock receipt processing."""
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise ValueError("Target inventory entry not found.")
            
        product.product_stock_quantity += added_quantity
        db.commit()
        db.refresh(product)
        return product
