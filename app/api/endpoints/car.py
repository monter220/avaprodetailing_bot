from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from aiofiles import open

from app.core.db import get_async_session
from app.crud.car import car_crud


router = APIRouter(
    prefix='/car',
    tags=['car']
)

templates = Jinja2Templates(
    directory='app/templates'
)


@router.get('/add')
async def get_add_car_template(request: Request):
    """Форма добавления машины"""
    return templates.TemplateResponse('car/add-car.html', {'request': request})


@router.post('/add')
async def add_car(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """Обработка формы создания машины. """
    # TODO: Здесь должна происходить валидация данных формы
    # и сохранение машины в базу данных.

    pass


@router.get('/{car_id}')
async def get_edit_car_template(
    car_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения формы редактирования машины. """
    car = await car_crud.get(
        obj_id=car_id,
        session=session
    )
    return templates.TemplateResponse(
        'car/edit-car.html',
        {'request': request, 'car': car}
    )


@router.post('/{car_id}')
async def edit_car(
    request: Request,
    car_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Обработка формы для редактирования машины."""
    # TODO: Здесь должна происходить валидация данных формы
    # и сохранение машины в базу данных.
    pass
