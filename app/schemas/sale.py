from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class SaleItemCreateSchema(BaseModel):
    """Schema for individual line items inside a customer's shopping cart."""
    product_id: int = Field(..., description="Database ID of the scanned product")
    quantity: int = Field(..., ge=1, description="Number of items purchased")

class SaleCreateSchema(BaseModel):
    """Schema sent by the register counter to process a checkout transaction."""
    session_id: int = Field(..., description="The active cashier shift session ID")
    customer_id: Optional[int] = Field(None, description="Optional CRM loyalty customer ID")
    items: List[SaleItemCreateSchema] = Field(..., min_items=1, description="List of items in the cart")

class SaleResponseSchema(BaseModel):
    """Schema returned after a successful checkout, ready for receipt printing."""
    sale_id: int
    invoice_number: str
    total_amount: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    final_amount: Decimal

    class Config:
        from_attributes = True
