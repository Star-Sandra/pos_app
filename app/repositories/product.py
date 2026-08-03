from typing import List
from sqlalchemy.orm import Session
from app.models.product import Product, Category, Supplier

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: int) -> Product:
        """Finds a single catalog item by its primary key."""
        return self.db.query(Product).filter(Product.product_id == product_id).first()

    def get_by_barcode(self, barcode: str) -> Product:
        """Crucial lookup for scanning checkout lanes using product barcode indexes."""
        return self.db.query(Product).filter(Product.product_barcode == barcode).first()

    def get_all_products(self) -> List[Product]:
        """Returns the complete supermarket catalog inventory list."""
        return self.db.query(Product).all()

    def save_product(self, product: Product) -> Product:
        """Inserts a new product row into the system inventory database."""
        self.db.add(product)
        self.db.commit()
        return product

    def save_category(self, category: Category) -> Category:
        """Creates a new inventory classification bucket."""
        self.db.add(category)
        self.db.commit()
        return category

    def save_supplier(self, supplier: Supplier) -> Supplier:
        """Logs a product wholesale supplier partner company profile."""
        self.db.add(supplier)
        self.db.commit()
        return supplier
