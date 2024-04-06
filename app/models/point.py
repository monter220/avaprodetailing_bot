from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.models.base import NameDescr


class Point(NameDescr):
    """
    Модель автомойки
    """
    address = Column(
        String(settings.max_address_len),
        comment='Адрес автомойки',
        unique=True
    )
    # Все адимистраторы автомойки
    admins = relationship('User', )
    # Все услуги, оказываемые на автомойке
    services = relationship('Service', cascade='delete', )
