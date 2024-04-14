from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.core.db import Base


class Bonus(Base):
    """Модель бонусов."""
    amount = Column(Integer, nullable=False)
    used = Column(Integer, nullable=False, default=0)
    date_begin = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    date_end = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(
            days=settings.bonus_expiration_period),
    )
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_active = Column(Boolean, nullable=False, default=0)

    user = relationship('User', foreign_keys=[user_id])
    admin = relationship('User', foreign_keys=[admin_id])
    order = relationship('Order', uselist=False, back_populates='bonus')
