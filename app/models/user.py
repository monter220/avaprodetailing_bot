from datetime import datetime, timedelta
from sqlalchemy import Column, Boolean, Integer, DateTime, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(Base):
    tg_id = Column(Integer)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    date_birth = Column(DateTime)
    phone = Column(String)
    discount_points = Column(Integer, default=100)
    reg_date = Column(DateTime, default=datetime.now)
    end_points_date = Column(DateTime, default=datetime.now().date() + timedelta(days=365))
    is_client = Column(Boolean, default=1)
    is_super = Column(Boolean, default=0)
    reservations = relationship('Car', cascade='delete')