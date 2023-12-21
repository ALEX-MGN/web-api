from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Buy(Base):
    __tablename__ = 'buy'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sale = relationship('Sale', back_populates='buy')
    buy_price = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, ForeignKey('buy.name'))
    buy = relationship('Buy', back_populates='sale')
    sale_price = Column(Integer)
    profit = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())

    def calculate_profit(self):
        if self.buy and self.buy.buy_price is not None and self.sale_price is not None:
            self.profit = self.sale_price - self.buy.buy_price
        else:
            self.profit = 0
    