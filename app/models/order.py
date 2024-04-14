from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False)
    date = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    cost = Column(Integer, nullable=False)
    pay_type_id = Column(Integer, ForeignKey('paytype.id'), nullable=False)
    bonus_id = Column(
        Integer, ForeignKey('bonus.id'), nullable=True, unique=True)
    is_active = Column(Boolean, default=False, nullable=False)

    user = relationship('User', foreign_keys=[user_id])
    admin = relationship('User', foreign_keys=[admin_id])
    car = relationship('Car')
    pay_type = relationship('PayType')
    bonus = relationship('Bonus', uselist=False, back_populates='order')
    ordered_services = relationship('OrderedService', back_populates='order')


class OrderedService(Base):
    """Модель заказанных услуг в конкретном Заказе."""
    __tablename__ = 'ordered_services'

    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    cost = Column(Integer, nullable=False)

    order = relationship('Order', back_populates='ordered_services')
