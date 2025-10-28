"""
In-memory implementation of the OrderRepository.
"""
from typing import Dict, Optional
from ..domain.order import Order
from ..domain.repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory storage implementation of OrderRepository."""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def save(self, order: Order) -> None:
        """Save an order to memory."""
        self._orders[order.id] = order
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Retrieve an order by its ID from memory."""
        return self._orders.get(order_id)
    
    def delete(self, order_id: str) -> bool:
        """Delete an order from memory."""
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False
