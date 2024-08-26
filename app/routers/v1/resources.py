from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.resource_schema import (
    ResourceOut,
    ResourceIn,
)
from app.repositories.resource_repository import ResourceRepository
from app.repositories.product_repository import ProductRepository
from app.config.database import get_db

router = APIRouter(
    prefix='/resources',
    tags=['resources'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=ResourceOut)
def create_resource(
    resource: ResourceIn,
    db: Session = Depends(get_db)
):
    product_record = ProductRepository(db).get_by_id(resource.product_id)
    if product_record is None:
        raise HTTPException(
            status_code=404,
            detail='Product not found'
        )
    return ResourceRepository(db).create(resource)


@router.get('/{resource_id}', response_model=ResourceOut)
def read_resource(
    resource_id: UUID,
    db: Session = Depends(get_db),
):
    resource_record = ResourceRepository(db).get_by_id(resource_id)
    if resource_record is None:
        raise HTTPException(
            status_code=404,
            detail='Resource not found'
        )
    return resource_record


@router.get('/', response_model=List[ResourceOut])
def read_resources(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    resources = ResourceRepository(db).get_all(skip, limit)
    return resources


@router.delete('/{resource_id}', status_code=204)
def delete_resource(
    resource_id: UUID,
    db: Session = Depends(get_db)
):
    resource_repository = ResourceRepository(db)
    resource_record = resource_repository.get_by_id(resource_id)
    if resource_record is None:
        raise HTTPException(
            status_code=404,
            detail='Resource not found'
        )
    return resource_repository.delete(resource_record)
