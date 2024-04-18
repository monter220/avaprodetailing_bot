from typing import List

from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.api.endpoints.user.user import router as user_router
from app.api.endpoints.utils import get_tg_id_cookie
from app.api.validators import check_user_exist
from app.core.config import settings
from app.core.db import get_async_session
from app.crud import car_crud, user_crud, service_crud, bonus_crud
from app.crud.order import order_crud, ordered_service_crud
from app.services.telegram import send_invoice


router = APIRouter(
    prefix="/users/{user_id}/payments"
)

templates = Jinja2Templates(
    directory='app/templates'
)


@router.get('/')
async def get_payments_template(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie),
):
    """Форма оплаты клиента."""
    title = 'Оплата'
    await check_user_exist(user_id, session)
    user = await user_crud.get(user_id, session)
    is_registered = True if user.tg_id else False

    admin = await user_crud.get_user_by_telegram_id(user_telegram_id, session)
    if not admin.point_id:
        return RedirectResponse(
            user_router.url_path_for('get_profile_template')
        )

    cars = await car_crud.get_user_cars(user_id, session)
    if not cars:
        return RedirectResponse(
            url=f'/users/{user_id}/cars/add'
        )

    services = await service_crud.get_services_by_point_id(
        session=session,
        point_id=admin.point_id,
    )

    return templates.TemplateResponse(
        'payments/payment.html',
        {
            'request': request,
            'title': title,
            'cars': cars,
            'services': services,
            'bonus_balance': user.bonus,
            'user_id': user_id,
            'is_registered': is_registered,
        },
    )


@router.post('/')
async def process_payment(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie),
    service_cost: List[str] = Form(None),
    service_id: List[str] = Form(None),
    car_id: int = Form(...),
    payment_type: str = Form(...),
    service_result_cost: int = Form(...),
    service_result_bonus: int = Form(...),
):
    """Обработка платежа."""
    user = await user_crud.get(user_id, session)
    # TODO Сообщение, что не добавлены услуги
    if not service_id:
        return RedirectResponse(
            router.url_path_for('get_payments_template', user_id=user_id),
            status_code=status.HTTP_302_FOUND,
        )
    if service_result_bonus < 0:
        # TODO Сообщение, что бонусов на балансе недостаточно
        if user.bonus + service_result_bonus < 0:
            return RedirectResponse(
                router.url_path_for('get_payments_template', user_id=user_id),
                status_code=status.HTTP_302_FOUND,
            )
        # TODO Сообщение о превышении максимума бонусов от чека
        result_sum = service_result_cost - service_result_bonus
        max_bonuses = int(result_sum * settings.max_bonus_value / 100)
        if max_bonuses + service_result_bonus < 0:
            return RedirectResponse(
                router.url_path_for('get_payments_template', user_id=user_id),
                status_code=status.HTTP_302_FOUND,
            )

    is_active = True if payment_type == 'cash' else False

    admin = await user_crud.get_user_by_telegram_id(user_telegram_id, session)
    bonus = {
        'amount': service_result_bonus,
        'user_id': user_id,
        'admin_id': admin.id,
        'is_active': is_active,
    }
    bonus = await bonus_crud.create_from_dict(bonus, session)

    payment_type = (
        settings.pay_type_cash
        if payment_type == 'cash'
        else settings.pay_type_online
    )
    order = {
        'user_id': user_id,
        'admin_id': admin.id,
        'car_id': car_id,
        'cost': service_result_cost,
        'pay_type_id': payment_type,
        'is_active': is_active,
        'bonus_id': bonus.id,
    }
    order = await order_crud.create_from_dict(order, session)

    services = []
    for s_id, s_cost in zip(service_id, service_cost):
        service = {
            'order_id': order.id,
            'service_id': s_id,
            'cost': s_cost,
        }
        services.append(service)
    await ordered_service_crud.create_multi_from_dict(services, session)

    if payment_type == settings.pay_type_cash:
        # TODO Сообщение, что заказ успешно создан
        await user_crud.update_bonus_amount(
            user_id, service_result_bonus, session)
        if bonus.amount < 0:
            await bonus_crud.burn_user_bonuses(
                user_id, abs(bonus.amount), session)
    else:
        await send_invoice(
            chat_id=user.tg_id,
            order_id=order.id,
            price=service_result_cost,
        )
        # TODO Сообщение, что сообщение об оплате отправлено

    return RedirectResponse(
        url='/users/me'
    )
