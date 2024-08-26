from uuid import UUID
from typing import Optional, List, Type
from sqlalchemy.orm import Session
from app.models.info_resource import InfoResource
from app.schemas.resource_schema import (
    ResourceIn,
    ResourceOut,
)


class ResourceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_product_id(self, _product_id: UUID) ->\
            Optional[List[Type[InfoResource]]]:
        return self.db.query(InfoResource).filter_by(product_id=_product_id).all()

    def get_by_id(self, _id: UUID) -> List[Type[InfoResource]]:
        return self.db.query(InfoResource).filter_by(id=_id).first()

    def get_all(self, skip: int, limit: int) -> List[Type[InfoResource]]:
        return self.db.query(InfoResource).offset(skip).limit(limit).all()

    def create(self, data: ResourceIn) -> Type[InfoResource]:
        resource_record = InfoResource(
            name=data.name,
            url=str(data.url),
            state=data.state,
            product_id=data.product_id
        )
        self.db.add(resource_record)
        self.db.commit()
        self.db.refresh(resource_record)
        return resource_record

    def delete(self, resource: Type[InfoResource]) -> bool:
        self.db.delete(resource)
        self.db.commit()
        return True

    def update(self, resource: Type[InfoResource], data: ResourceIn) -> ResourceOut:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(resource, key, value)
        self.db.commit()
        self.db.refresh()
        return ResourceOut(**resource.__dict__)
