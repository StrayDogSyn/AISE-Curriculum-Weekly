"""
Repository interface and abstract base class.
"""
from abc import ABC, abstractmethod
from typing import Optional
from ..domain.order import Order


class OrderRepository(ABC):
    """Abstract base class for order repositories."""
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Save an order to the repository."""
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Retrieve an order by its ID."""
        pass
    
    @abstractmethod
    def delete(self, order_id: str) -> bool:
        """Delete an order from the repository."""
        pass
