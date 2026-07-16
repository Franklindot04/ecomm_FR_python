from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Order, Payment, PaymentStatus, OrderStatus


def create_mock_payment(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == OrderStatus.PAID:
        raise HTTPException(status_code=400, detail="Order is already paid")

    existing_pending_payment = db.query(Payment).filter(
        Payment.order_id == order.id,
        Payment.user_id == user_id,
        Payment.status == PaymentStatus.PENDING
    ).first()

    if existing_pending_payment:
        raise HTTPException(status_code=400, detail="Pending payment already exists for this order")

    payment = Payment(
        order_id=order.id,
        user_id=user_id,
        amount=order.total_price,
        status=PaymentStatus.PENDING,
        provider="mock",
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def process_mock_webhook(db: Session, payment_id: int, new_status: PaymentStatus):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.status == PaymentStatus.PAID:
        raise HTTPException(status_code=400, detail="Payment is already finalized as PAID")

    if payment.status == PaymentStatus.FAILED:
        raise HTTPException(status_code=400, detail="Payment is already finalized as FAILED")

    if new_status == PaymentStatus.PENDING:
        raise HTTPException(status_code=400, detail="Webhook cannot set payment back to PENDING")

    payment.status = new_status

    order = db.query(Order).filter(Order.id == payment.order_id).first()

    if new_status == PaymentStatus.PAID and order.status != OrderStatus.PAID:
        order.status = OrderStatus.PAID

    db.commit()
    db.refresh(payment)
    return payment