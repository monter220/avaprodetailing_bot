from sqlalchemy import Column, String

from app.core.config import settings
from app.core.db import Base


class NameDescr(Base):
    name = Column(String(settings.max_name_len), comment='Название')
    description = Column(String, nullable=True, comment='Описание')

    __abstract__ = True