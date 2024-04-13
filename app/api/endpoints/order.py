from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_exist
from app.core.db import get_async_session
from app.crud import order_crud, service_crud
from app.models import Order
from app.schemas.order import OrderDB, OrderCreate, OrderUpdate, ReturnOrder
from app.api.validators import check_exist

router = APIRouter(
    prefix='/order',
    tags=['Заказы']
)

@router.post(
    '/',
    response_model=ReturnOrder,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def create_new_order(
    order_json: OrderCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Order:
    for service_id in order_json.services:
        await check_exist(service_crud, service_id, session)
    order = await order_crud.create_order_with_bonus(order_json, session)
    return order


@router.get('/order/{order_id}', response_model=OrderDB)
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    order = await order_crud.get(order_id, session)
    if not order:
        raise HTTPException(status_code=404)
    return order


@router.patch(
    '/{order_id}',
    response_model=OrderDB,
    # dependencies=[Depends(current_superuser)],
)
async def update_order(
    order_id: int,
    order_json: OrderUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    order = await check_exist(order_crud, order_id, session)
    return await order_crud.update(order, order_json, session)
