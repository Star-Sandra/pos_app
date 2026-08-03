import uuid
import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.models.payment import Payment, Receipt

class PaymentService:
    @staticmethod
    def process_invoice_settlement(db: Session, sale_id: int, method: str, amount: Decimal, reference: str, user_id: int) -> Payment:
        """Validates checkout totals, registers incoming payments, and logs a one-to-one printer receipt entry."""
        # 1. Verify outstanding invoice balance properties
        sale = db.query(Sale).filter(Sale.sale_id == sale_id).first()
        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target sales record reference not found.")

        if amount < sale.final_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient payment. Required: {sale.final_amount}, Received: {amount}")

        # 2. Register successful cash registry or merchant transaction pipeline log
        payment_record = Payment(
            sale_id=sale_id,
            payment_method=method,
            amount_paid=amount,
            transaction_reference=reference,
            payment_status="SUCCESS",
            paid_at=datetime.datetime.utcnow(),
            user_id=user_id
        )
        db.add(payment_record)

        # 3. Fulfill strict database relational constraints by assigning exactly one unique receipt mapping row
        receipt_no = f"REC-{uuid.uuid4().hex[:8].upper()}"
        receipt_record = Receipt(
            sale_id=sale_id,
            receipt_number=receipt_no
        )
        db.add(receipt_record)

        db.commit()
        db.refresh(payment_record)
        return payment_record
