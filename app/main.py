from app.api.products import router as products_router
from app.api.cart import router as cart_router
from app.api.orders import router as orders_router
from app.api.auth import router as auth_router

from fastapi import FastAPI

from app.database import Base, engine
from app.seed import seed_products

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed initial data
seed_products()

app = FastAPI(
    title="Ecommerce Microservice",
    version="1.0.0"
)

# Register API routers
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(auth_router)

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
