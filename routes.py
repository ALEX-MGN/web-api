from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (  create_buy, get_buies, update_buy, delete_buy,
                    create_sale, get_sales, update_sale, delete_sale)

router_websocket = APIRouter()
router_buies = APIRouter(prefix='/buies', tags=['buy'])
router_sales = APIRouter(prefix='/sales', tags=['sale'])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)

@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Клиент #{client_id} присоединилась в чат")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Вы написали: {data}", websocket)
            await manager.broadcast(f"Клиент #{client_id} пишет: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Клиент #{client_id} вышел из чата")

@router_buies.post("/", response_model=schemas.Buy)
async def create_buy_route(buy_data: schemas.BuyCreate, db: Session = Depends(get_db)):
    buy = create_buy(db, buy_data)
    await notify_clients(f"Покупка добавлена: {buy.name}")
    return buy

@router_buies.get("/", response_model=List[schemas.Buy])
async def read_buies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    buies = get_buies(db, skip=skip, limit=limit)
    return buies

@router_buies.patch("/{buy_id}", response_model=schemas.Buy)
async def update_buy_route(buy_id: int, buy_data: schemas.BuyUpdate, db: Session = Depends(get_db)):
    updated_buy = update_buy(db, buy_id, buy_data)
    if updated_buy:
        await notify_clients(f"Покупка обновлена: {updated_buy.name}")
        return updated_buy
    return {"message": "Покупка не найдена"}

@router_buies.delete("/{buy_id}")
async def delete_buy_route(buy_id: int, db: Session = Depends(get_db)):
    deleted = delete_buy(db, buy_id)
    if deleted:
        await notify_clients(f"Покупка удалена: ID {buy_id}")
        return {"message": "Покупка удалена"}
    return {"message": "Покупка не найдена"}

@router_sales.post("/", response_model=schemas.Sale)
async def create_sale_route(schema: schemas.SaleCreate, db: Session = Depends(get_db)):
    sale = create_sale(db, schema)
    await notify_clients(f"Продажа добавлена: {sale.name}")
    return sale

@router_sales.get("/", response_model=List[schemas.Sale])
async def read_sales(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sales = get_sales(db, skip=skip, limit=limit)
    return sales

@router_sales.patch("/{sale_id}")
async def update_sale_route(sale_id: int, schema: schemas.SaleUpdate, db: Session = Depends(get_db)):
    updated_sale = update_sale(db, sale_id, schema)
    if updated_sale:
        await notify_clients(f"Продажа обновлена: {updated_sale.name}")
        return updated_sale
    return {"message": "Продажа не найдена"}

@router_sales.delete("/{sale_id}")
async def delete_sale_route(sale_id: int, db: Session = Depends(get_db)):
    deleted = delete_sale(db, sale_id)
    if deleted:
        await notify_clients(f"Продажа удалена: ID {sale_id}")
        return {"message": "Продажа удалена"}
    return {"message": "Продажа не найдена"}