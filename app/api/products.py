import json
import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.cache_utils import invalidate_product_caches
from app.database import get_db
from app.models import Product
from app.redis_client import redis_client
from app.schemas import ProductCreate, ProductResponse

load_dotenv()

PRODUCT_CACHE_TTL = int(os.getenv("PRODUCT_CACHE_TTL", "60"))

router = APIRouter()


def serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
    }


@router.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    cache_key = "products:all"
    cached_products = await redis_client.get(cache_key)

    if cached_products:
        return json.loads(cached_products)

    products = db.query(Product).all()
    serialized = [serialize_product(product) for product in products]

    await redis_client.setex(
        cache_key,
        PRODUCT_CACHE_TTL,
        json.dumps(serialized),
    )

    return serialized


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    cache_key = f"products:{product_id}"
    cached_product = await redis_client.get(cache_key)

    if cached_product:
        return json.loads(cached_product)

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    serialized = serialize_product(product)

    await redis_client.setex(
        cache_key,
        PRODUCT_CACHE_TTL,
        json.dumps(serialized),
    )

    return serialized


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    await invalidate_product_caches()

    return new_product