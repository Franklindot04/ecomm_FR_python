from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from typing import List

from app.auth_utils import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import OrderResponse, OrderStatusUpdate
from app.services.invoice_service import generate_invoice_file
from app.services.notification_service import write_order_notification
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
async def create_order(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = await create_order_from_cart(db, current_user.id)

    background_tasks.add_task(
        generate_invoice_file,
        order.id,
        current_user.id,
        current_user.email,
        order.total_price,
        order.status.value,
        [
            {
                "product_id": item.product_id,
                "product_name": item.product.name if item.product else "Unknown product",
                "quantity": item.quantity,
                "price_at_purchase": item.price_at_purchase,
            }
            for item in order.items
        ],
    )

    background_tasks.add_task(
        write_order_notification,
        order.id,
        current_user.id,
        current_user.email,
        "ORDER_CREATED",
        f"Order #{order.id} was created successfully with status {order.status.value}."
    )

    return order


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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = update_user_order_status(db, order_id, current_user.id, payload.status)

    background_tasks.add_task(
        write_order_notification,
        order.id,
        current_user.id,
        current_user.email,
        "ORDER_STATUS_UPDATED",
        f"Order #{order.id} status changed to {order.status.value}."
    )

    return order


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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = cancel_user_order(db, order_id, current_user.id)

    background_tasks.add_task(
        write_order_notification,
        order.id,
        current_user.id,
        current_user.email,
        "ORDER_CANCELLED",
        f"Order #{order.id} was cancelled."
    )

    return order