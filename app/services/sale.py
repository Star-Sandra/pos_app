import uuid
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.sale import Sale, SaleItem, Customer

class SaleService:
    @staticmethod
    def process_customer_checkout(db: Session, session_id: int, items_list: list[dict], customer_id: int = None) -> Sale:
        """
        Locks product inventory rows and processes complete POS checkout calculations.
        Ensures strict math validation across parallel terminal lanes.
        """
        total_amount = Decimal("0.00")
        total_tax = Decimal("0.00")
        total_discount = Decimal("0.00")
        line_items_to_save = []

        # 1. Engage database transactional lock context
        for item in items_list:
            prod_id = item["product_id"]
            qty = item["quantity"]

            # Select item and immediately apply row-level execution locks
            product = db.query(Product).filter(Product.product_id == prod_id).with_for_update().first()

            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {prod_id} not found.")

            if product.product_stock_quantity < qty:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient inventory shelf stock for {product.product_name}.")

            # 2. Deduct active physical supermarket inventory balance
            product.product_stock_quantity -= qty

            # 3. Process math parameters based on point-in-time catalog values
            subtotal = product.product_price_per_unit * qty
            discount = product.product_discount * qty
            net_amount = subtotal - discount
            tax = net_amount * (product.product_vat / Decimal("100.00"))

            total_amount += subtotal
            total_discount += discount
            total_tax += tax

            line_items_to_save.append(SaleItem(
                product_id=product.product_id,
                quantity=qty,
                unit_price=product.product_price_per_unit,
                subtotal=net_amount
            ))

        # 4. Generate unique alphanumeric invoice sequence string
        invoice_no = f"INV-{uuid.uuid4().hex[:8].upper()}"
        final_computed_amount = total_amount - total_discount + total_tax

        # 5. Handle customer CRM loyalty updates if present (1 point per 100 base cash units spent)
        if customer_id:
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            if customer:
                customer.customer_loyal_points += int(final_computed_amount // Decimal("100.00"))

        # 6. Instantiate master sales model record mapping values
        new_sale = Sale(
            invoice_number=invoice_no,
            session_id=session_id,
            customer_id=customer_id,
            total_amount=total_amount,
            tax_amount=total_tax,
            discount_amount=total_discount,
            final_amount=final_computed_amount,
            items=line_items_to_save
        )

        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        return new_sale
