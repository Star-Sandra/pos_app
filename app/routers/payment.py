import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sale import Sale
from app.models.payment import Payment, Receipt
from app.schemas.payment import PaymentCreateSchema, PaymentResponseSchema
from typing import List


router = APIRouter(prefix="/payments", tags=["Payment & Receipts"])

@router.post("/pay", response_model=PaymentResponseSchema, status_code=status.HTTP_201_CREATED)
def settle_invoice(payment_data: PaymentCreateSchema, db: Session = Depends(get_db)):
    """Settle an unpaid final checkout sale invoice and instantly generate a matching receipt."""
    # 1. Look up target sales transaction record string
    sale = db.query(Sale).filter(Sale.sale_id == payment_data.sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale invoice record not found.")

    # 2. Instantiate payment registry log model configuration values
    new_payment = Payment(
        sale_id=payment_data.sale_id,
        payment_method=payment_data.payment_method,
        amount_paid=payment_data.amount_paid,
        transaction_reference=payment_data.transaction_reference,
        payment_status="SUCCESS",  # Mocking instant network processing gateway clearance
        paid_at=datetime.datetime.utcnow(),
        user_id=payment_data.user_id
    )
    db.add(new_payment)

    # 3. Handle strict One-to-One rule mapping constraints by issuing exactly one single unique receipt line sequence
    receipt_no = f"REC-{uuid.uuid4().hex[:8].upper()}"
    new_receipt = Receipt(
        sale_id=sale.sale_id,
        receipt_number=receipt_no
    )
    db.add(new_receipt)

    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/history", response_model=List[PaymentResponseSchema])
def get_payment_audit_history(db: Session = Depends(get_db)):
    """
    FINANCIAL AUDIT: Retrieves a master collection of all cleared payments 
    and drawer cash drops to reconcile registers with card merchant terminals.
    """
    return db.query(Payment).all()


@router.get("/receipts/{sale_id}")
def fetch_receipt_by_sale(sale_id: int, db: Session = Depends(get_db)):
    """
    RECEIPT REPRINTING: Looks up the strict 1-to-1 receipt document sequence 
    assigned to a sale, allowing a customer or cashier to reprint a lost receipt.
    """
    receipt = db.query(Receipt).filter(Receipt.sale_id == sale_id).first()
    if not receipt:
        raise HTTPException(
            status_code=404, 
            detail="No printing receipt has been generated for this sale sequence yet."
        )
    return {
        "receipt_id": receipt.receipt_id,
        "sale_id": receipt.sale_id,
        "receipt_number": receipt.receipt_number
    }
