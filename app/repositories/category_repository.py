from uuid import UUID
from typing import Optional, Type, List
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category_schema import (
    CategoryOut,
    CategoryIn,
)


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, _id: UUID) -> Optional[Type[Category]]:
        return self.db.query(Category).filter_by(id=_id).first()

    def get_all(self, skip: int, limit: int) -> List[Type[Category]]:
        return self.db.query(Category).offset(skip).limit(limit).all()

    def create(self, data: CategoryIn) -> Category:
        category_record = Category(
            **data.model_dump(exclude_none=True)
        )
        self.db.add(category_record)
        self.db.commit()
        self.db.refresh(category_record)
        return category_record
