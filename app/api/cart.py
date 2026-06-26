from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Product, CartItem
from app.schemas import (
    CartItemCreate,
    CartItemResponse
)

router = APIRouter()


@router.get("/cart", response_model=List[CartItemResponse])
def get_cart(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


@router.post("/cart", response_model=CartItemResponse, status_code=201)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == item.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item.quantity > product.stock:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing = db.query(CartItem).filter(
        CartItem.product_id == item.product_id
    ).first()

    if existing:
        if existing.quantity + item.quantity > product.stock:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        existing.quantity += item.quantity

        db.commit()
        db.refresh(existing)
        return existing

    cart_item = CartItem(
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.delete("/cart/{cart_id}")
def remove_from_cart(cart_id: int, db: Session = Depends(get_db)):

    item = db.query(CartItem).filter(CartItem.id == cart_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item removed"}


@router.delete("/cart")
def clear_cart(db: Session = Depends(get_db)):

    db.query(CartItem).delete()
    db.commit()

    return {"message": "Cart cleared"}