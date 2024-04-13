from pydantic import BaseModel, validator


class BonusCreate(BaseModel):
    amount: int
    used: int
    user_id: int

    @validator('amount')
    def check_amount(cls, value, values):
        if value > 0 and values.get('used', 0) > 0:
            raise ValueError('Поле "used" должно быть 0 при значении поля "amount" больше 0')
        if value == 0 and values.get('used', 0) == 0:
            raise ValueError('Поле "used" должно быть больше 0 при значении поля "amount" равном 0')
        return value
    
    @validator('amount', 'used')
    def check_non_negative(cls, value):
        if value < 0:
            raise ValueError('Значение должно быть больше или равно 0')
        return value


class BonusDB(BonusCreate):
    id: int
    author_id: int

    class Config:
        orm_mode = True
