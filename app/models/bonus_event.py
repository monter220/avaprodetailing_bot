from datetime import datetime, timedelta
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.core.config import settings

class Bonus_event(Base):
    """
    Модель для учета бонусов
    """
    __tablename__ = 'bonus_event'
    date_begin = Column(DateTime, default=datetime.now())
    date_end = Column(DateTime, default=datetime.now() + timedelta(settings.bonus_retention_period))
    amount = Column(Integer)
    used = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    order = relationship(
        'Order',
        foreign_keys='Order.bonus_event_id',
        back_populates='bonus_event',
        lazy="selectin"
    )
