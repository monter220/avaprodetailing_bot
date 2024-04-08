from pydantic import BaseModel, PositiveInt


class RoleCreate(BaseModel):
    id: PositiveInt
    name: str


class EventTypesCreate(BaseModel):
    id: PositiveInt
    name: str


class PayTypeCreate(BaseModel):
    id: PositiveInt
    name: str
