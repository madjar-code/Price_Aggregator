from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal, engine, get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix='/categories',
    tags=['categories'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    return crud.create_category(db=db, category=category)


@router.get('/{category_id}', response_model=schemas.Category)
def read_category(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )
    return db_category


@router.get('/', response_model=List[schemas.Category])
def read_categories(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    categories = crud.get_categories(db, skip, limit)
    return categories
