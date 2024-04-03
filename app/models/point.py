from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import NameDescr


class Point(NameDescr):
    """
    Модель автомойки
    """
    address = Column(String(250), comment='Адрес автомойки')
    # Все адимистраторы автомойки
    admins = relationship('User', cascade='save-update',)
    # Все услуги, оказываемые на автомойке
    services = relationship('Service', cascade='delete',)

