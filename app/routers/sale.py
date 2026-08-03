import uuid
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.product import Product
from app.models.sale import Sale, SaleItem
from app.schemas.sale import SaleCreateSchema, SaleResponseSchema
from app.models.sale import Sale
from typing import List

router = APIRouter(prefix="/sales", tags=["Sales & Checkout"])

@router.post("/checkout", response_model=SaleResponseSchema, status_code=status.HTTP_201_CREATED)
def process_checkout(cart: SaleCreateSchema, db: Session = Depends(get_db)):
    """
    Safely processes an active checkout transaction cart payload.
    Uses pessimistic row locking to prevent stock overselling across registers.
    """
    total_amount = Decimal("0.00")
    total_tax = Decimal("0.00")
    total_discount = Decimal("0.00")
    sale_items_to_create = []

    try:
        for item in cart.items:
            # 1. Fetch item profile and execute lock block against parallel checkouts
            product = db.query(Product).filter(Product.product_id == item.product_id).with_for_update().first()

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {item.product_id} not found."
                )

            # 2. Check store inventory stock constraints
            if product.product_stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {product.product_name}. Available: {product.product_stock_quantity}"
                )

            # 3. Deduct active physical supermarket inventory balance
            product.product_stock_quantity -= item.quantity

            # 4. Process math parameters based on point-in-time snapshot records
            item_subtotal = product.product_price_per_unit * item.quantity
            item_discount = product.product_discount * item.quantity
            
            # Calculate VAT on the net discounted subtotal amount
            net_amount = item_subtotal - item_discount
            item_tax = net_amount * (product.product_vat / Decimal("100.00"))

            total_amount += item_subtotal
            total_discount += item_discount
            total_tax += item_tax

            # 5. Build transactional sale line sub-model
            line_item = SaleItem(
                product_id=product.product_id,
                quantity=item.quantity,
                unit_price=product.product_price_per_unit,
                subtotal=net_amount
            )
            sale_items_to_create.append(line_item)

        # 6. Generate distinct structured business invoice reference sequence string
        invoice_no = f"INV-{uuid.uuid4().hex[:8].upper()}"
        
        # 7. Complete master sale model instantiation
        new_sale = Sale(
            invoice_number=invoice_no,
            session_id=cart.session_id,
            customer_id=cart.customer_id,
            total_amount=total_amount,
            tax_amount=total_tax,
            discount_amount=total_discount,
            final_amount=(total_amount - total_discount + total_tax),
            items=sale_items_to_create
        )

        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        return new_sale

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Checkout routine processing failed: {str(e)}"
        )

@router.get("/history", response_model=List[SaleResponseSchema])
def get_transaction_history(db: Session = Depends(get_db)):
    """Retrieves structural audit logs of all historical supermarket sales."""
    return db.query(Sale).all()
