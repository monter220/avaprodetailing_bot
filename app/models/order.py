from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship

from app.core.db import Base

service_order = Table('service_order', Base.metadata,
    Column('service_id', Integer, ForeignKey('service.id')),
    Column('order_id', Integer, ForeignKey('order.id'))
)

class Order(Base):
    """
    Модель заказа
    """
    __tablename__ = 'order'
    user_id = Column(Integer, ForeignKey('user.id'))
    author_id = Column(Integer, ForeignKey('user.id'))
    car_id = Column(Integer, ForeignKey('car.id'))
    date = Column(DateTime, default=datetime.now())
    cost = Column(Integer)
    pay_type = Column(Integer, ForeignKey('paytype.id'))
    bonus_event_id = Column(Integer, ForeignKey('bonus_event.id'))
    services = relationship('Service', secondary=service_order, back_populates='order', lazy='selectin')
    bonus_event = relationship('Bonus_event', back_populates='order', lazy="selectin")
