from pydantic import PositiveFloat
from sqlalchemy import Column, Float, CheckConstraint, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import NameDescr


class Category(NameDescr):
    """
    Модель категории услуг
    """
    # Все услуги по категории
    services = relationship('Service', cascade='delete', )


class Service(NameDescr):
    """
    Модель услуги
    """
    cost = Column(Float, comment='Минимальная сумма услуги')
    default_bonus_p = Column(
        Float,
        comment='Минимальный бонус по услуге'
    )
    category_id = Column(
        Integer,
        ForeignKey('category.id'),
        comment='Категория услуги'
    )
    point_id = Column(
        Integer,
        ForeignKey('point.id'),
        comment='Автомойка, на которой оказывается услуга'
    )