import os
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, Body
from sqlalchemy.ext.asyncio import AsyncSession
from aiofiles import open

from app.core.db import get_async_session
from app.core.config import settings
from app.crud import car_crud
from app.api.validators import check_user_exist, check_file_format
from app.schemas.car import CarCreate, CarDB


router = APIRouter()


@router.post(
    '/car/',
    response_model=CarDB,
    response_model_exclude_none=True,
)
async def create_product(
        file: UploadFile = File(None),
        car: CarCreate = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    car_dict = car.dict()
    await check_user_exist(car_dict['user_id'], session)
    if file is None:
        car_db = await car_crud.create_car(car_dict, session)
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
        car_db = await car_crud.create_car(car_dict, session, path_to_img)
    if car_db:
        return car_db
