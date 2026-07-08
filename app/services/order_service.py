from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.models import CartItem, Order, OrderItem, OrderStatus as ORMOrderStatus
from app.schemas import OrderStatus


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


def get_user_order_or_404(db: Session, order_id: int, user_id: int) -> Order:
    order = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        Order.user_id == user_id
    ).all()


def validate_transition(current_status: OrderStatus, new_status: OrderStatus):
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


def create_order_from_cart(db: Session, user_id: int):
    cart_items = db.query(CartItem).options(
        selectinload(CartItem.product)
    ).filter(
        CartItem.user_id == user_id
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
        user_id=user_id,
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

    return get_user_order_or_404(db, order.id, user_id)


def update_user_order_status(db: Session, order_id: int, user_id: int, new_status: OrderStatus):
    order = get_user_order_or_404(db, order_id, user_id)

    current_status = OrderStatus(order.status.value)
    validate_transition(current_status, new_status)

    order.status = ORMOrderStatus(new_status.value)
    db.commit()
    db.refresh(order)

    return get_user_order_or_404(db, order.id, user_id)


def cancel_user_order(db: Session, order_id: int, user_id: int):
    order = get_user_order_or_404(db, order_id, user_id)

    current_status = OrderStatus(order.status.value)
    validate_transition(current_status, OrderStatus.CANCELLED)

    order.status = ORMOrderStatus.CANCELLED
    db.commit()
    db.refresh(order)

    return get_user_order_or_404(db, order.id, user_id)