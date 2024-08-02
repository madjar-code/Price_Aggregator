from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.schemas.product_schema import (
    Product,
    ProductCreate,
)
from app.config.database import get_db


router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    category = crud.get_category(db, category_id=product.category_id)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )
    return crud.create_product(db=db, product=product)


@router.get('/{product_id}', response_model=Product)
def read_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail='Product not found'
        )
    return db_product


@router.get('/', response_model=List[Product])
def read_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    products = crud.get_products(db, skip, limit)
    return products
