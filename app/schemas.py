from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.models import OrderStatus


# -------------------------
# PRODUCT
# -------------------------

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


# -------------------------
# CART
# -------------------------

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True


# -------------------------
# ORDERS
# -------------------------

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price_at_purchase: float
    product: ProductResponse

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus

# -------------------------
# AUTH
# -------------------------


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str    