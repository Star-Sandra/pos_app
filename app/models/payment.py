import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import base

class Payment(base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False)
    payment_method = Column(String(250), nullable=False)
    amount_paid = Column(Numeric(10, 2), nullable=False)
    transaction_reference = Column(String(250), nullable=True)
    payment_status = Column(String(250), nullable=False)
    paid_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    
    sale = relationship("Sale", back_populates="payments")


class Receipt(base):
    __tablename__ = "receipts"

    receipt_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), unique=True, nullable=False)
    receipt_number = Column(String(250), unique=True, nullable=False)

    
    sale = relationship("Sale", back_populates="receipt")
