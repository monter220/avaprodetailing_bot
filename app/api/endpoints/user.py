from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserDB
from app.api.validators import check_duplicate


router = APIRouter()


@router.post(
    '/user',
    response_model=UserDB,
    response_model_exclude_none=True,
)
async def create_new_user(
        new_user: UserCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_duplicate(new_user.phone, session)
    new = await user_crud.create(
        obj_in=new_user, session=session, model='User')
    return new
