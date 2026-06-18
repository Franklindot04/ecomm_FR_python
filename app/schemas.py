from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True