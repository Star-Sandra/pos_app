from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Category, Supplier
from typing import List
from app.schemas.product import ProductCreateSchema, ProductResponseSchema
from app.services.product import ProductService

router = APIRouter(prefix="/catalog", tags=["Catalog Lookups"])

@router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_product_category(name: str, description: str, db: Session = Depends(get_db)):
    """Creates a new inventory organizational cluster profile (e.g. Groceries, Bakery)."""
    new_cat = Category(category_name=name, description=description)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return {"message": "Category created successfully!", "category_id": new_cat.category_id}


@router.post("/suppliers", status_code=status.HTTP_201_CREATED)
def create_supplier(company_name: str, db: Session = Depends(get_db)):
    """Registers a product supplier company profile in the retail network database."""
    new_sup = Supplier(company_name=company_name)
    db.add(new_sup)
    db.commit()
    db.refresh(new_sup)
    return {"message": "Supplier created successfully!", "supplier_id": new_sup.supplier_id}
@router.get("/", response_model=List[ProductResponseSchema])
def list_all_supermarket_stock(db: Session = Depends(get_db)):
    """Retrieves the complete catalog list with live stock numbers."""
    service = ProductService(db)
    return service.product_repo.get_all_products()

# --- 3. THE GET METHOD (Barcode Scanner lane lookup) ---
@router.get("/scan/{barcode}", response_model=ProductResponseSchema)
def scan_item_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """Acts as the scanner endpoint for the physical checkout register laser."""
    service = ProductService(db)
    product = service.product_repo.get_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode scan failed. Item not found.")
    return product

# --- 4. THE PUT METHOD (Restock delivery updates) ---
@router.put("/{product_id}/restock", response_model=ProductResponseSchema)
def restock_product(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """Increases stock counts when a truck delivery arrives at Star Supermarket."""
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Restock quantity must be greater than 0.")
    try:
        service = ProductService(db)
        return service.replenish_shelf_stock(product_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))