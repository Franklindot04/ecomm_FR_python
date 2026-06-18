from fastapi import FastAPI
from app.database import Base, engine

# create tables (empty for now)
Base.metadata.create_all(bind=engine)

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