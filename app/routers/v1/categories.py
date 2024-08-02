from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.schemas.category_schema import (
    Category,
    CategoryCreate,
)
from app.config.database import get_db


router = APIRouter(
    prefix='/categories',
    tags=['categories'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=Category)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    return crud.create_category(db=db, category=category)


@router.get('/{category_id}', response_model=Category)
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


@router.get('/', response_model=List[Category])
def read_categories(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    categories = crud.get_categories(db, skip, limit)
    return categories
