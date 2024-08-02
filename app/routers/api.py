from fastapi import APIRouter
from app.routers.v1 import categories, products


router = APIRouter(
    prefix='/api/v1'
)


router.include_router(categories.router)
router.include_router(products.router)
