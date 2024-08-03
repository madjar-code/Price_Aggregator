from uuid import UUID
from typing import List, Optional, Union
from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(..., min_length=5, max_length=150)
    category_id: Union[UUID, None]


class ProductOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    category_id: Union[UUID, None]
