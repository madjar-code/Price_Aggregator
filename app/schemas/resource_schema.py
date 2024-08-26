from uuid import UUID
from pydantic import BaseModel, HttpUrl
from app.models.info_resource import ResourceState


class ResourceIn(BaseModel):
    name: str
    url: HttpUrl
    state: ResourceState
    product_id: UUID


class ResourceOut(BaseModel):
    id: UUID
    name: str
    url: HttpUrl
    state: ResourceState
    product_id: UUID
