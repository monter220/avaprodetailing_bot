from sqlalchemy import Column, String, Integer, ForeignKey

from app.core.db import Base


class Car(Base):
    brand = Column(String)
    model = Column(String)
    license_plate_number = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
