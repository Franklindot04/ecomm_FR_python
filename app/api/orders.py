from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import get_db
from app.models import (
    CartItem,
    Order,
    OrderItem
)
from app.schemas import OrderResponse

router = APIRouter()


@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(db: Session = Depends(get_db)):

    cart_items = db.query(CartItem).options(
        selectinload(CartItem.product)
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0

    # validate stock
    for item in cart_items:
        product = item.product

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if item.quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        total_price += product.price * item.quantity

    # create order
    order = Order(total_price=total_price)
    db.add(order)
    db.flush()

    # create order items + update stock
    for item in cart_items:
        product = item.product

        product.stock -= item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )

        db.add(order_item)

    # clear cart
    for item in cart_items:
        db.delete(item)

    db.commit()

    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        Order.id == order.id
    ).first()


@router.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).all()


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order