from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import Base, engine, get_db
from app.models import Product, CartItem
from app.seed import seed_products

from app.schemas import (
    ProductCreate,
    ProductResponse,
    CartItemCreate,
    CartItemResponse
)

# create tables
Base.metadata.create_all(bind=engine)

# seed initial data
seed_products()

app = FastAPI(
    title="Ecommerce Microservice",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Ecommerce API running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# PRODUCTS
# -------------------------

@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@app.get(
    "/cart",
    response_model=List[CartItemResponse]
)
def get_cart(
    db: Session = Depends(get_db)
):
    return db.query(CartItem).all()    


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.post(
    "/cart",
    response_model=CartItemResponse,
    status_code=201
)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    if item.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )


    existing = db.query(CartItem).filter(
        CartItem.product_id == item.product_id
    ).first()


    if existing:

        existing.quantity += item.quantity


        if existing.quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        db.commit()
        db.refresh(existing)

        return existing



    cart_item = CartItem(
        product_id=item.product_id,
        quantity=item.quantity
    )


    db.add(cart_item)

    db.commit()

    db.refresh(cart_item)

    return cart_item

@app.delete("/cart/{cart_id}")
def remove_from_cart(
        cart_id: int,
        db: Session = Depends(get_db)
):

    item = db.query(CartItem).filter(
        CartItem.id == cart_id
    ).first()


    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )


    db.delete(item)

    db.commit()


    return {
        "message":"Item removed"
    }

@app.delete("/cart")
def clear_cart(
        db: Session = Depends(get_db)
):

    db.query(CartItem).delete()

    db.commit()


    return {
        "message":"Cart cleared"
    }            