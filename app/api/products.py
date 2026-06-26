from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Product
from app.schemas import (
    ProductCreate,
    ProductResponse
)

router = APIRouter()


@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product