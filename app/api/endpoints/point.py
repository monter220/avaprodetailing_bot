from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.point import point_crud

router = APIRouter(
    prefix='/point',
    tags=['Points']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/{point_id}')
async def get_point(
        point_id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    point = await point_crud.get(session, point_id)

    # TODO: В контексте так же нужно передавть "point_phone_number"
    # это должен быть номер администратора, привязанного к точке на данный момент
    # если у точки есть какой-то статичный номер телефона - нужно отразить это в модели.

    # TODO: Так же в контексте должен передаваться словарь с услугами и их категориями.
    # Это необходимо для корректного отображения услуг и их категорий в шаблоне.
    # Пример: {'category_1': [service_1, service_2], 'category_2': [service_3]}.

    return templates.TemplateResponse(
        'point.html',
        {
            'request': request,
            'point': point
        }
    )
