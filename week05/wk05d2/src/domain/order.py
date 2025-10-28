"""
Domain models for the Order system.
"""
from dataclasses import dataclass
from typing import List
import uuid


@dataclass
class OrderItem:
    """Represents an item in an order."""
    name: str
    quantity: int
    price: float

    def subtotal(self) -> float:
        """Calculate the subtotal for this item."""
        return self.quantity * self.price


class Order:
    """Represents an order with items and status."""
    
    def __init__(self, items: List[OrderItem], order_id: str = None):
        self.id = order_id or str(uuid.uuid4())
        self.items = items
        self.status = "PENDING"
    
    def total(self) -> float:
        """Calculate the total cost of all items in the order."""
        return sum(item.subtotal() for item in self.items)
    
    def cancel(self) -> None:
        """Cancel the order."""
        self.status = "CANCELED"
