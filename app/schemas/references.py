from pydantic import BaseModel, PositiveInt


class ReferenceCreate(BaseModel):
    id: PositiveInt
    name: str
