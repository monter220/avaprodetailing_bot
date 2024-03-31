from pydantic import (BaseModel)


class RoleCreate(BaseModel):
    id: int
    name: str
