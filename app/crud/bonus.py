from app.crud.base import CRUDBase
from app.models import Bonus_event


class CRUDBonus(CRUDBase):
    pass

bonus_crud = CRUDBonus(Bonus_event)