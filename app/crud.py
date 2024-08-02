from uuid import UUID
from sqlalchemy.orm import Session
from .schemas.product_schema import ProductCreate
from .schemas.category_schema import (
    CategoryCreate,
    Category,
)
from .models.category import Category
from .models.product import Product


def get_product(db: Session, product_id: UUID):
    return db.query(Product).\
        filter(Product.id == product_id).\
        first()


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_category(db: Session, category_id: UUID):
    return db.query(Category).\
        filter(Category.id == category_id).\
        first()


def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
