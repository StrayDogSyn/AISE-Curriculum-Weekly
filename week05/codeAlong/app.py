from fastapi import FastAPI, HTTPException
from src.application.order_service import OrderService
from src.infrastructure.inmemory_repo import InMemoryOrderRepository
from src.domain.order import OrderItem
from pydantic import BaseModel, Field
from typing import List
import uuid

class ItemPayload(BaseModel):
    name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0.0)

class CreateOrderPayload(BaseModel):
    items: List[ItemPayload]

repo = InMemoryOrderRepository()
service = OrderService(repo)

app = FastAPI(title="W5D2 DDD + Hexagonal Demo")

@app.post("/orders")
def create_order(payload: CreateOrderPayload):
    items = [OrderItem(name=i.name, quantity=i.quantity, price=i.price) for i in payload.items]
    order_id = str(uuid.uuid4())
    order = service.create_order(items, order_id=order_id)
    return {"order_id": order.id, "total": order.total()}

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Not found")
    return {"order_id": order.id, "items": [i.__dict__ for i in order.items], "total": order.total(), "status": order.status}

@app.delete("/orders/{order_id}")
def cancel_order(order_id: str):
    canceled = service.cancel_order(order_id)
    if not canceled:
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}
