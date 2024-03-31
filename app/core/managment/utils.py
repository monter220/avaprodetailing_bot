import jwt

from typing import Optional
from datetime import datetime, timedelta
from typing import Union, Any

from app.core.config import settings


def create_access_token(
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        settings.hash_algorithm,
    )
    return encoded_jwt


def create_refresh_token(
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.refresh_token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_refresh_secret_key,
        settings.hash_algorithm,
    )
    return encoded_jwt
