from sqlalchemy.orm import Session
from app.models.payment import Payment, Receipt

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_payment(self, payment: Payment) -> Payment:
        """Logs a customer cash drawer settlement action."""
        self.db.add(payment)
        self.db.commit()
        return payment

    def save_receipt(self, receipt: Receipt) -> Receipt:
        """Fulfills the strict 1-to-1 relationship mapping by printing an audit receipt log."""
        self.db.add(receipt)
        self.db.commit()
        return receipt
