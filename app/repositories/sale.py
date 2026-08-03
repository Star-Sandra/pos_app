from sqlalchemy.orm import Session
from app.models.sale import Sale, Customer

class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_sale_by_id(self, sale_id: int) -> Sale:
        """Pulls a single completed sales transaction transaction row."""
        return self.db.query(Sale).filter(Sale.sale_id == sale_id).first()

    def save_sale(self, sale: Sale) -> Sale:
        """Saves a finished point-of-sale customer order entry."""
        self.db.add(sale)
        self.db.commit()
        return sale

    def get_customer_by_id(self, customer_id: int) -> Customer:
        """Looks up a CRM loyalty profile cardholder record."""
        return self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
