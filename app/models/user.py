from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(Base):
    tg_id = Column(Integer, nullable=True)
    surname = Column(String(100), comment='Фамилия', nullable=False)
    name = Column(String(100), comment='Имя', nullable=False)
    patronymic = Column(String(100), comment='Отчество', nullable=True)
    date_birth = Column(DateTime, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    reg_date = Column(DateTime, default=datetime.now)
    role = Column(Integer, ForeignKey('role.id'), default=1)
    reservations = relationship('Car', cascade='delete')
