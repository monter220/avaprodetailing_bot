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
    admins = relationship('User', backref='point')
    # Все категории услуг на автомойке
    categories = relationship('Category', cascade='delete', backref='point')