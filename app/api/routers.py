from fastapi import APIRouter

from app.api.endpoints import (
    user_router,
    car_router,
    point_router,
    category_router,
    service_router
)


main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(car_router)
main_router.include_router(
    point_router,
    prefix='/point',
    tags=['Автомойки']
)
main_router.include_router(
    category_router,
    prefix='/category',
    tags=['Категории услуг']
)
main_router.include_router(
    service_router,
    prefix='/services',
    tags=['Услуги']
)
