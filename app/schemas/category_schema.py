from uuid import UUID
from typing import List
from pydantic import BaseModel, Field
from .product_schema import Product


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)


class Category(BaseModel):
    id: UUID
    name: str = Field(..., max_length=50)
    products: List['Product'] = []
