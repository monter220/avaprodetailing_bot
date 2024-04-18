from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import NameDescr


class Category(NameDescr):
    """
    Модель категории услуг
    """
    # Точка, на которой присутствуют категории услуг
    point_id = Column(
        Integer,
        ForeignKey('point.id'),
        comment='Автомойка, на которой присутствует категория'
    )
    # Все услуги каждой категории
    services = relationship('Service', cascade='delete', backref='category')
