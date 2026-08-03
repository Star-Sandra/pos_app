from decimal import Decimal
from pydantic import BaseModel, Field

class PaymentCreateSchema(BaseModel):
    """Schema used to log a payment transaction against a specific invoice."""
    sale_id: int = Field(..., description="The ID of the sale being settled")
    payment_method: str = Field(..., description="e.g., 'Cash', 'Card', 'Mobile Money'")
    amount_paid: Decimal = Field(..., ge=0.01, description="Exact money amount received")
    transaction_reference: str = Field(..., description="Merchant approval code or receipt ref")
    user_id: int = Field(..., description="The ID of the staff member processing the cash drawer")

class PaymentResponseSchema(BaseModel):
    """Schema confirming the payment status back to the lane screen."""
    payment_id: int
    payment_status: str
    amount_paid: Decimal

    class Config:
        from_attributes = True
