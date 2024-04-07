from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
)

from app.core.db import Base


class Events(Base):
    author = Column(Integer, ForeignKey('user.id'), nullable=False)
    date = Column(DateTime, default=datetime.now)
    model = Column(String, nullable=False)
    data = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('eventtyps.id'), nullable=False)
