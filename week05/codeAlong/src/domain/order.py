from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class OrderItem:
    name: str
    quantity: int
    price: float
    def line_total(self) -> float:
        return self.quantity * self.price

@dataclass
class Order:
    id: str
    items: List[OrderItem] = field(default_factory=list)
    status: str = "OPEN"  # OPEN/CANCELED/COMPLETED
    def total(self) -> float:
        return sum(item.line_total() for item in self.items)
    def cancel(self) -> None:
        if self.status != "CANCELED":
            self.status = "CANCELED"
