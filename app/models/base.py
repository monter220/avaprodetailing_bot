from sqlalchemy import Column, String

from app.core.db import Base


class NameDescr(Base):
    name = Column(String(50), comment='Название')
    description = Column(String, nullable=True, comment='Описание')

    __abstract__ = True