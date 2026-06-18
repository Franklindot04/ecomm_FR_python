from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import Base, engine, get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse
from app.seed import seed_products

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


@app.post("/products", response_model=ProductResponse, status_code=201)
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