import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class ProductCreateSchema(BaseModel):
    """Schema for adding new stock items to the supermarket catalog."""
    product_name: str = Field(..., max_length=250, description="Name on receipt")
    category_id: int = Field(..., description="ID from categories lookup table")
    supplier_id: Optional[int] = Field(None, description="Optional primary supplier identifier")
    product_exp_date: Optional[datetime.date] = Field(None, description="Expiration date if perishable")
    product_barcode: str = Field(..., max_length=250, description="Unique scan index barcode")
    product_stock_quantity: int = Field(0, ge=0, description="Initial shelf inventory count")
    product_vat: Decimal = Field(..., description="Tax percentage rate (e.g. 16.00)")
    product_price_per_unit: Decimal = Field(..., description="Price before store discount rules")
    product_discount: Decimal = Field(Decimal("0.00"), description="Flat product markdown amount")

class ProductResponseSchema(ProductCreateSchema):
    """Schema returning product details including its system-assigned database ID."""
    product_id: int

    class Config:
        from_attributes = True
