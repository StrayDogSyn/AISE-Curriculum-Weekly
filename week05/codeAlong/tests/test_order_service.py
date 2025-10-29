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

def test_remove_order():
    """Test that remove_order completely deletes the order from repository."""
    repo = InMemoryOrderRepository()
    service = OrderService(repo)
    order_id = str(uuid.uuid4())
    
    # Create an order
    service.create_order([OrderItem(name="book", quantity=1, price=10.0)], order_id=order_id)
    assert repo.get_by_id(order_id) is not None, "Order should exist after creation"
    
    # Remove the order
    ok = service.remove_order(order_id)
    assert ok, "Order removal should return True"
    assert repo.get_by_id(order_id) is None, "Order should be deleted from repository"

def test_remove_missing_order():
    """Test that attempting to remove a non-existent order returns False."""
    repo = InMemoryOrderRepository()
    service = OrderService(repo)
    order_id = str(uuid.uuid4())
    
    ok = service.remove_order(order_id)
    assert not ok, "Removing a non-existent order should return False"

def test_cancel_vs_remove():
    """Test the difference between cancel (flag) and remove (delete)."""
    repo = InMemoryOrderRepository()
    service = OrderService(repo)
    
    # Test cancel - order still exists but is flagged
    cancel_id = str(uuid.uuid4())
    service.create_order([OrderItem(name="book", quantity=1, price=10.0)], order_id=cancel_id)
    service.cancel_order(cancel_id)
    canceled_order = repo.get_by_id(cancel_id)
    assert canceled_order is not None, "Canceled order should still exist in repository"
    assert canceled_order.status == "CANCELED", "Order status should be CANCELED"
    
    # Test remove - order is completely deleted
    remove_id = str(uuid.uuid4())
    service.create_order([OrderItem(name="pen", quantity=2, price=1.5)], order_id=remove_id)
    service.remove_order(remove_id)
    removed_order = repo.get_by_id(remove_id)
    assert removed_order is None, "Removed order should not exist in repository"