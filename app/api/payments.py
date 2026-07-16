from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth_utils import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import PaymentCreate, PaymentResponse, PaymentWebhookPayload
from app.services.payment_service import create_mock_payment, process_mock_webhook

router = APIRouter()


@router.post(
    "/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Order is already paid or a pending payment already exists"},
        404: {"description": "Order not found"},
    },
)
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_mock_payment(db, payload.order_id, current_user.id)


@router.post(
    "/webhooks",
    response_model=PaymentResponse,
    responses={
        400: {"description": "Invalid or finalized payment status change"},
        404: {"description": "Payment not found"},
    },
)
def handle_payment_webhook(
    payload: PaymentWebhookPayload,
    db: Session = Depends(get_db),
):
    return process_mock_webhook(db, payload.payment_id, payload.status)