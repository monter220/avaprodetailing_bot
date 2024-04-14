from app.crud.base import CRUDBase
from app.models import Order, OrderedService


class CRUDOrder(CRUDBase):
    """CRUD для модели заказов."""
    pass


class CRUDOrderedService(CRUDBase):
    """CRUD для модели заказанных услуг."""
    pass


order_crud = CRUDOrder(Order)
ordered_service_crud = CRUDOrderedService(OrderedService)
