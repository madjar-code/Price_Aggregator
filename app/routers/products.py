from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal, engine, get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(db=db, product=product)


@router.get('/{product_id}', response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return db_product


@router.get('/', response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    products = crud.get_products(db, skip, limit)
    return products
