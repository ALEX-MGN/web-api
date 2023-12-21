from sqlalchemy.orm import Session

import schemas
from models import Buy, Sale

def create_buy(db: Session, schema: schemas.BuyCreate):
    db_buy = Buy(**schema.model_dump())
    db.add(db_buy)
    db.commit()
    db.refresh(db_buy)
    return db_buy

def get_buies(db: Session, skip: int = 0, limit: int = 25):
    return db.query(Buy).offset(skip).limit(limit).all()

def update_buy(db: Session, buy_id: int, buy_data: schemas.BuyUpdate | dict):
    db_buy = db.query(Buy).filter_by(id=buy_id).first()

    buy_data = buy_data if isinstance(buy_data, dict) else buy_data.model_dump()

    if db_buy:
        for key, value in buy_data.items():
            if hasattr(db_buy, key):
                setattr(db_buy, key, value)

        db.commit()
        db.refresh(db_buy)

    return db_buy

def delete_buy(db: Session, buy_id: int):
    db_buy = db.query(Buy).filter_by(id=buy_id).first()
    if db_buy:
        db.delete(db_buy)
        db.commit()
        return True
    return False

def create_sale(db: Session, schema: schemas.SaleCreate):
    db_sale = Sale(**schema.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Sale).offset(skip).limit(limit).all()

def update_sale(db: Session, sale_id: int, sale_data: schemas.SaleUpdate | dict):
    db_sale = db.query(Sale).filter_by(id=sale_id).first()

    sale_data = sale_data if isinstance(sale_data, dict) else sale_data.model_dump()

    if db_sale:
        for key, value in sale_data.items():
            if hasattr(db_sale, key):
                setattr(db_sale, key, value)

        db.commit()
        db.refresh(db_sale)
        return db_sale
    return None

def delete_sale(db: Session, sale_id: int):
    db_sale = db.query(Sale).filter_by(id=sale_id).first()
    if db_sale:
        db.delete(db_sale)
        db.commit()
        return True
    return False
