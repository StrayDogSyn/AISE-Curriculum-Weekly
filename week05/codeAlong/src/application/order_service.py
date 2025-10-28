from typing import List
from src.domain.order import Order, OrderItem
from src.application.ports import OrderRepository

class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository
    def create_order(self, items: List[OrderItem], order_id: str) -> Order:
        order = Order(id=order_id, items=items)
        self.repository.save(order)
        return order
    def cancel_order(self, order_id: str) -> bool:
        order = self.repository.get_by_id(order_id)
        if not order:
            return False
        order.cancel()
        self.repository.save(order)
        return True
