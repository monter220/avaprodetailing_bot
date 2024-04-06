from fastapi import APIRouter

from app.api.endpoints import user_router, car_router, point_router


main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(car_router)
main_router.include_router(
    point_router,
    prefix='/point',
    tags=['points']
)
