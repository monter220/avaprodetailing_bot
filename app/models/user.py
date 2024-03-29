from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(Base):
    tg_id = Column(Integer)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    date_birth = Column(DateTime)
    phone = Column(String)
    reg_date = Column(DateTime, default=datetime.now)
    role = Column(Integer, ForeignKey('role.id'), default=1)
    reservations = relationship('Car', cascade='delete')