from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category_schema import (
    CategoryIn,
    CategoryOut,
)
from app.config.database import get_db
from app.repositories.category_repository import \
    CategoryRepository

router = APIRouter(
    prefix='/categories',
    tags=['categories'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=CategoryOut)
def create_category(
    category: CategoryIn,
    db: Session = Depends(get_db)
):
    return CategoryRepository(db).create(category)


@router.get('/{category_id}', response_model=CategoryOut)
def read_category(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    category_record = CategoryRepository(db).get_by_id(category_id)
    if category_record is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )
    return category_record


@router.get('/', response_model=List[CategoryOut])
def read_categories(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return CategoryRepository(db).get_all(skip, limit)
