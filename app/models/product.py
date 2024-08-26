import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(String, index=True)
    description = Column(String)
    category_id = Column(
        UUID,
        ForeignKey('categories.id'),
        nullable=True,
    )
    # links = Column(ARRAY(String), nullable=True)

    category = relationship(
        'Category',
        back_populates='products'
    )
    sources = relationship(
        'InfoResource',
        back_populates='product',
        cascade='all, delete-orphan'
    )
