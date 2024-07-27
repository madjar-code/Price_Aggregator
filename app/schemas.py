from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProductCreate(ProductBase):
    category_id: UUID


class Product(ProductCreate):
    id: UUID
    category_id: UUID

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: UUID
    products: List[Product] = []

    class Config:
        orm_mode = True
