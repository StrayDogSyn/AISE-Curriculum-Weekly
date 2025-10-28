import sys
import os
import uuid
from src.application.order_service import OrderService
from src.infrastructure.inmemory_repo import InMemoryOrderRepository
from src.domain.order import OrderItem

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def test_create_order_and_total():
    repo = InMemoryOrderRepository()
    service = OrderService(repo)
    order_id = str(uuid.uuid4())
    order = service.create_order(
        [OrderItem(name="book", quantity=2, price=12.5),
         OrderItem(name="pen", quantity=3, price=1.2)],
        order_id=order_id
    )
    assert order.id == order_id, f"Expected order ID {order_id}, but got {order.id}"
    assert round(order.total(), 2) == round(2 * 12.5 + 3 * 1.2, 2)
    assert repo.get_by_id(order_id) is not None

def test_cancel_order():
    repo = InMemoryOrderRepository()
    service = OrderService(repo)
    order_id = str(uuid.uuid4())
    service.create_order([OrderItem(name="book", quantity=1, price=10.0)], order_id=order_id)
    ok = service.cancel_order(order_id)
    assert ok, "Order cancellation should return True"
    assert repo.get_by_id(order_id).status == "CANCELED"

def test_cancel_missing_order():
    repo = InMemoryOrderRepository()
    service = OrderService(repo)
    order_id = str(uuid.uuid4())
    ok = service.cancel_order(order_id)
    assert not ok, "Cancelling a non-existent order should return False"