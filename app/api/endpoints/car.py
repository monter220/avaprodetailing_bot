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




import os
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from aiofiles import open

from app.core.db import get_async_session
from app.core.config import settings
from app.crud import car_crud, user_crud
from app.api.validators import check_user_exist, check_file_format
from app.schemas.car import CarCreate, CarDB


router = APIRouter()


async def get_tg_id_cookie(request: Request):
    """Функция для получения куки tg_id.  """
    return request.cookies.get('tg_id')


@router.post(
    '/car/',
    response_model=CarDB,
    response_model_exclude_none=True,
)
async def create_car(
        file: UploadFile = File(None),
        car: CarCreate = Body(...),
        user_telegram_id: str = Depends(get_tg_id_cookie),
        session: AsyncSession = Depends(get_async_session)
):
    car_dict = car.dict()
    await check_user_exist(car_dict['user_id'], session)
    if file is None:
        car_db = await car_crud.create_car(
            obj_in_data=car_dict,
            session=session,
            model='Car',
            user=await user_crud.catch_user_id(user_telegram_id, session),
        )
    else:
        _, ext = os.path.splitext(file.filename)
        imgdir: str = os.path.join(
            settings.basedir, f'{settings.folder}/{car_dict["user_id"]}')
        if not os.path.exists(imgdir):
            os.makedirs(imgdir)
        content = await file.read()
        check_file_format(file.content_type)
        file_name = f'{uuid.uuid4().hex}{ext}'
        async with open(os.path.join(imgdir, file_name), mode='wb') as f:
            await f.write(content)
        path_to_img = os.path.abspath(os.path.join(imgdir, file_name))
        car_db = await car_crud.create_car(
            path=path_to_img,
            obj_in_data=car_dict,
            session=session,
            model='Car',
            user=await user_crud.get_user_by_telegram_id(user_telegram_id, session),
        )
    if car_db:
        return car_db
