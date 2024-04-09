from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import NameDescr


class Service(NameDescr):
    """
    Модель услуги
    """
    cost = Column(Integer, comment='Минимальная сумма услуги')
    default_bonus = Column(
        Integer,
        comment='Минимальный бонус по услуге'
    )
    category_id = Column(
        Integer,
        ForeignKey('category.id'),
        comment='Категория услуги'
    )

