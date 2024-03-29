from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Role(Base):
    name = Column(String)
    reservations = relationship('User', cascade='delete')
