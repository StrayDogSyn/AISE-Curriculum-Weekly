from typing import Optional, Dict
from src.domain.order import Order

class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._db: Dict[str, Order] = {}
    def save(self, order: Order) -> None:
        self._db[order.id] = order
    def get_by_id(self, id: str) -> Optional[Order]:
        return self._db.get(id)
    def delete(self, id: str) -> None:
        if id in self._db:
            del self._db[id]
