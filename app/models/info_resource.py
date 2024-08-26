import uuid
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
from enum import Enum as PyEnum


class ResourceState(PyEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class InfoResource(Base):
    __tablename__ = 'sources'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    url = Column(String, nullable=False)
    state = Column(
        Enum(ResourceState),
        nullable=False,
        default=ResourceState.INACTIVE,
    )
    name = Column(String, nullable=True)
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey('products.id'),
        nullable=False,
    )
    product = relationship(
        'Product',
        back_populates='sources'
    )
