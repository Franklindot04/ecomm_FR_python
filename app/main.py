from app.api.products import router as products_router
from app.api.cart import router as cart_router
from app.api.orders import router as orders_router

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import Base, engine, get_db
from app.models import Product, CartItem, Order, OrderItem
from app.seed import seed_products

from app.schemas import (
    ProductCreate,
    ProductResponse,
    CartItemCreate,
    CartItemResponse,
    OrderResponse
)

# create tables
Base.metadata.create_all(bind=engine)

# seed initial data
seed_products()

app = FastAPI(
    title="Ecommerce Microservice",
    version="1.0.0"
)

app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)

# -------------------------
# HEALTH
# -------------------------

@app.get("/")
def root():
    return {
        "message": "Ecommerce API running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
