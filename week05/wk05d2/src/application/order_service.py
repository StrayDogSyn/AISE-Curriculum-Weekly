"""
Application service for managing orders.
"""
from typing import List, Optional
from ..domain.order import Order, OrderItem
from ..domain.repository import OrderRepository


class OrderService:
    """Service class for order operations."""
    
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    
    def create_order(self, items: List[OrderItem], order_id: str = None) -> Order:
        """
        Create a new order with the given items.
        
        Args:
            items: List of OrderItem objects
            order_id: Optional order ID, will be generated if not provided
            
        Returns:
            The created Order object
        """
        order = Order(items, order_id)
        self.repository.save(order)
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Retrieve an order by its ID.
        
        Args:
            order_id: The ID of the order to retrieve
            
        Returns:
            The Order object if found, None otherwise
        """
        return self.repository.get_by_id(order_id)
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order.
        
        Args:
            order_id: The ID of the order to cancel
            
        Returns:
            True if the order was successfully canceled, False otherwise
        """
        order = self.repository.get_by_id(order_id)
        if order is None:
            return False
        order.cancel()
        self.repository.save(order)
        return True
