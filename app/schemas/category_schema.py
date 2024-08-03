from uuid import UUID
from typing import List
from pydantic import BaseModel, Field
from .product_schema import ProductOut


class CategoryIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryOut(BaseModel):
    id: UUID
    name: str = Field(..., max_length=50)
    products: List['ProductOut'] = []
