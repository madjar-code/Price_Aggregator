import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(
        String,
        nullable=False,
        index=True
    )

    products = relationship('Product', back_populates='category')
