from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.product_schema import (
    ProductOut,
    ProductIn,
)
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.config.database import get_db


router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=ProductOut)
def create_product(
    product: ProductIn,
    db: Session = Depends(get_db)
):
    category_record = CategoryRepository(db).get_by_id(product.category_id)
    if category_record is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )
    return ProductRepository(db).create(product)


@router.get('/{product_id}', response_model=ProductOut)
def read_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    product_record = ProductRepository(db).get_by_id(product_id)
    if product_record is None:
        raise HTTPException(
            status_code=404,
            detail='Product not found'
        )
    return product_record


@router.get('/', response_model=List[ProductOut])
def read_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    products = ProductRepository(db).get_all(skip, limit)
    return products
