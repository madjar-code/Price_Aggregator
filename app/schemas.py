from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)


class Category(BaseModel):
    id: UUID
    name: str = Field(..., max_length=50)
    products: List['Product'] = []


class ProductCreate(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(..., min_length=5, max_length=150)
    category_id: UUID


class Product(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    category_id: UUID
