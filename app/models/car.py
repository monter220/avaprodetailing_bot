from sqlalchemy import Column, String, Integer, ForeignKey


from app.core.db import Base


class Car(Base):
    image = Column(String, nullable=True)
    brand = Column(String, comment='Марка', nullable=False)
    model = Column(String, comment='Модель', nullable=False)
    license_plate_number = Column(
        String, unique=True, comment='Гос номер', nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
