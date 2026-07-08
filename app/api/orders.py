from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.auth_utils import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import OrderResponse, OrderStatusUpdate
from app.services.order_service import (
    cancel_user_order,
    create_order_from_cart,
    get_user_order_or_404,
    get_user_orders,
    update_user_order_status,
)

router = APIRouter()


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    responses={
        400: {"description": "Cart is empty or stock is insufficient"},
        404: {"description": "Product not found"}
    }
)
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_order_from_cart(db, current_user.id)


@router.get("/orders", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_orders(db, current_user.id)


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
    return get_user_order_or_404(db, order_id, current_user.id)


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
    return update_user_order_status(db, order_id, current_user.id, payload.status)


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
    return cancel_user_order(db, order_id, current_user.id)