from uuid import UUID
from typing import Optional, Type, List
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import (
    ProductOut,
    ProductIn,
)


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, _id: UUID) -> Optional[Type[ProductOut]]:
        return self.db.query(ProductOut).filter_by(id=_id).first()

    def get_all(self, skip: int, limit: int) -> List[ProductOut]:
        return self.db.query(ProductOut).offset(skip).limit(limit).all()

    def create(self, data: ProductIn) -> Product:
        product_record = Product(
            **data.model_dump(exclude_none=True)
        )
        self.db.add(product_record)
        self.db.commit()
        self.db.refresh(product_record)
        return product_record
