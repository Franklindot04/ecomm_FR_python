from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.auth_utils import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import CartItemCreate, CartItemResponse
from app.services.cart_service import (
    add_item_to_cart,
    clear_user_cart,
    get_cart_items,
    remove_cart_item,
)

router = APIRouter()


@router.get("/cart", response_model=List[CartItemResponse])
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_cart_items(db, current_user.id)


@router.post("/cart", response_model=CartItemResponse, status_code=201)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_item_to_cart(db, current_user.id, item.product_id, item.quantity)


@router.delete("/cart/{cart_id}")
def remove_from_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return remove_cart_item(db, current_user.id, cart_id)


@router.delete("/cart")
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return clear_user_cart(db, current_user.id)