from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.point import point_crud
from app.api.validators import check_exist, check_fields_duplicate
from app.models import Point
from app.schemas.point import PointDB, PointCreate, PointUpdate, PointBaseDB


router = APIRouter(
    prefix='/point',
    tags=['Автомойки']
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


# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.api.validators import check_fields_duplicate, check_exist
# from app.core.db import get_async_session
# from app.crud import point_crud
# from app.models import Point
# from app.schemas.point import PointDB, PointCreate, PointUpdate, PointFullDB
#
# router = APIRouter()
#
#
# @router.post(
#     '/',
#     response_model=PointDB,
#     response_model_exclude_none=True,
#     # dependencies=[Depends(current_superuser)],
# )
# async def create_new_point(
#     new_point_json: PointCreate,
#     session: AsyncSession = Depends(get_async_session),
# ) -> Point:
#     """
#     Создание автомойки.
#     Только для суперюзеров.
#     """
#     # Словарь с данными, которые нужно проверить на уникальность.
#     fields_for_check = {
#         'name': new_point_json.name,
#         'address': new_point_json.address
#     }
#     # Проверка на уникальность всех данных
#     await check_fields_duplicate(point_crud, fields_for_check, session)
#     # Создание автомойки
#     new_point_db = await point_crud.create(new_point_json, session)
#     return new_point_db
#
#
# @router.get(
#     '/',
#     response_model=list[PointDB],
#     response_model_exclude_none=True,
# )
# async def get_all_points(
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Возвращает список всех автомоек."""
#     return await point_crud.get_multi(session)
#
#
# @router.patch(
#     '/{point_id}',
#     response_model=PointDB,
#     # dependencies=[Depends(current_superuser)],
# )
# async def update_point(
#     point_id: int,
#     point_json: PointUpdate,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """
#     Только для суперюзеров.
#
#     Редактирование автомойки.
#     """
#
#     # Проверка на существование автомойки в базе
#     project_db = await check_exist(point_crud, point_id, session)
#
#     # Проверка на уникальность переданных данных
#     if point_json.name is not None:
#         fields_for_check = {'name': point_json.name, }
#         await check_fields_duplicate(point_crud, fields_for_check, session)
#     if point_json.address is not None:
#         fields_for_check = {'address': point_json.address, }
#         await check_fields_duplicate(point_crud, fields_for_check, session)
#
#     # Изменяем поля автомойки
#     return await point_crud.update(project_db, point_json, session)
#
#
# @router.delete(
#     '/{point_id}',
#     response_model=PointDB,
#     # dependencies=[Depends(current_superuser)],
# )
# async def delete_point(
#     point_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """
#     Только для суперюзеров.
#
#     Удаляет автомойку.
#     """
#     # Проверка на существование автомойки в базе
#     point_db = await check_exist(point_crud, point_id, session)
#
#     # Удаляем поля автомойки
#     point = await point_crud.remove(point_db, session)
#     return point
#
#
# @router.get(
#     '/{point_id}',
#     response_model=list[PointFullDB],
#     response_model_exclude_none=True,
# )
# async def get_all_data_by_point(
#     point_id,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Возвращает все данные по автомойке."""
#
#     # Проверка на существование автомойки в базе
#     await check_exist(point_crud, point_id, session)
#
#     return await point_crud.get_all_by_id(point_id, session)
# @router.get(
#     '/{point_id}',
#     response_model=PointDB,
#     response_model_exclude_none=True,
# )
# async def get_point_by_id(
#     point_id,
#     request: Request,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Возвращает все данные по автомойке."""
#
#     # Проверка на существование автомойки в базе
#     await check_exist(point_crud, point_id, session)
#
#     # Формируем json со всеми вложенными полями по автомойке
#     point = await point_crud.point_by_id(point_id, session)
#
#     # Выбрать один из вариантов возврата данных!
#
#     return point
