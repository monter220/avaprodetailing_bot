from fastapi import APIRouter

from app.api.endpoints import (
    guest_router,
    payment_router,
    point_router,
    reports_router,
    sending_ads_router,
    user_router
)


main_router = APIRouter()

main_router.include_router(guest_router)
main_router.include_router(payment_router)
main_router.include_router(point_router)
main_router.include_router(reports_router)
main_router.include_router(sending_ads_router)
main_router.include_router(user_router)

# main_router.include_router(
#     point_router,
#     prefix='/point',
#     tags=['Автомойки']
# )
# # main_router.include_router(
# #     category_router,
# #     prefix='/category',
# #     tags=['Категории услуг']
# # )
# # main_router.include_router(
# #     service_router,
# #     prefix='/services',
# #     tags=['Услуги']
# # )
