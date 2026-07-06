from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import get_db
from app.models import (
    CartItem,
    Order,
    OrderItem,
    OrderStatus as ORMOrderStatus,
    User,
)
from app.schemas import OrderResponse, OrderStatusUpdate, OrderStatus
from app.auth_utils import get_current_user

router = APIRouter()

ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {
        OrderStatus.PAID,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PAID: {
        OrderStatus.PROCESSING,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PROCESSING: {
        OrderStatus.SHIPPED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.SHIPPED: {
        OrderStatus.DELIVERED,
    },
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}


def _get_order_or_404(db: Session, order_id: int, user_id: int) -> Order:
    order = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


def _validate_transition(current_status: OrderStatus, new_status: OrderStatus):
    if current_status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=400,
            detail="Cannot move a cancelled order to another status"
        )

    if current_status == OrderStatus.DELIVERED and new_status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel a delivered order"
        )

    if new_status == OrderStatus.CANCELLED and current_status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=400,
            detail="Order is already cancelled"
        )

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status transition"
        )


@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_items = db.query(CartItem).options(
        selectinload(CartItem.product)
    ).filter(
        CartItem.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0

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

    order = Order(
        user_id=current_user.id,
        total_price=total_price,
        status=ORMOrderStatus.PENDING
    )
    db.add(order)
    db.flush()

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

    for item in cart_items:
        db.delete(item)

    db.commit()

    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        Order.id == order.id,
        Order.user_id == current_user.id
    ).first()


@router.get("/orders", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        Order.user_id == current_user.id
    ).all()


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    responses={
        404: {"description": "Order not found"}
    }
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return _get_order_or_404(db, order_id, current_user.id)


@router.patch(
    "/orders/{order_id}/status",
    response_model=OrderResponse,
    responses={
        400: {"description": "Invalid or disallowed order status change"},
        404: {"description": "Order not found"}
    }
)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = _get_order_or_404(db, order_id, current_user.id)

    current_status = OrderStatus(order.status.value)
    new_status = payload.status

    _validate_transition(current_status, new_status)

    order.status = ORMOrderStatus(new_status.value)
    db.commit()
    db.refresh(order)

    return _get_order_or_404(db, order.id, current_user.id)


@router.post(
    "/orders/{order_id}/cancel",
    response_model=OrderResponse,
    responses={
        400: {"description": "Order cannot be cancelled"},
        404: {"description": "Order not found"}
    }
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = _get_order_or_404(db, order_id, current_user.id)

    current_status = OrderStatus(order.status.value)
    _validate_transition(current_status, OrderStatus.CANCELLED)

    order.status = ORMOrderStatus.CANCELLED
    db.commit()
    db.refresh(order)

    return _get_order_or_404(db, order.id, current_user.id)