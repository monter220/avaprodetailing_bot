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

    __table_args__ = (
        # Проверка на то, чтобы стоимость была положительной
        CheckConstraint('cost > 0', name='cost_positive'),
        # Проверка на то, чтобы бонус по умолчанию был положительный
        CheckConstraint('default_bonus_p > 0', name='bonus_positive'),
    )
