from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import get_db
from .models import Product
from .schemas import ProductCreate, ProductUpdate, ProductResponse
from .utils import normalize_sku

router = APIRouter(prefix="/products", tags=["products"])

# CREATE
@router.post("/", response_model=ProductResponse)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    sku_norm = normalize_sku(payload.sku)

    # Check duplicate SKU (case-insensitive)
    existing = db.query(Product).filter(Product.sku_norm == sku_norm).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")

    new_product = Product(
        sku=payload.sku,
        sku_norm=sku_norm,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        active=payload.active
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# LIST
@router.get("/", response_model=list[ProductResponse])
def list_products(
    sku: str = None,
    name: str = None,
    description: str = None,
    active: bool = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if sku:
        query = query.filter(Product.sku_norm == normalize_sku(sku))

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))

    if active is not None:
        query = query.filter(Product.active == active)

    query = query.offset(offset).limit(limit)

    return query.all()

# GET SINGLE
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

# DELETE
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Deleted successfully"}
