from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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


@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# -------------------------
# CART
# -------------------------

@app.get("/cart", response_model=List[CartItemResponse])
def get_cart(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


@app.post("/cart", response_model=CartItemResponse, status_code=201)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == item.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item.quantity > product.stock:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing = db.query(CartItem).filter(
        CartItem.product_id == item.product_id
    ).first()

    if existing:
        if existing.quantity + item.quantity > product.stock:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        existing.quantity += item.quantity

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
def remove_from_cart(cart_id: int, db: Session = Depends(get_db)):

    item = db.query(CartItem).filter(CartItem.id == cart_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item removed"}


@app.delete("/cart")
def clear_cart(db: Session = Depends(get_db)):

    db.query(CartItem).delete()
    db.commit()

    return {"message": "Cart cleared"}


# -------------------------
# ORDERS
# -------------------------

@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(db: Session = Depends(get_db)):

    cart_items = db.query(CartItem).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # preload products (optimization)
    products = db.query(Product).all()
    product_map = {p.id: p for p in products}

    total_price = 0

    # validate stock
    for item in cart_items:
        product = product_map.get(item.product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if item.quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        total_price += product.price * item.quantity

    # create order
    order = Order(total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)

    # create order items + update stock
    for item in cart_items:
        product = product_map[item.product_id]

        product.stock -= item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )

        db.add(order_item)

    # clear cart
    db.query(CartItem).delete()

    db.commit()
    db.refresh(order)

    return order


@app.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order