from models.database.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

class Transactions(Base):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True, unique=True)
    gift_card_id = Column(Integer, ForeignKey('GiftCards.id'), nullable=False)
    amount = Column(Integer, nullable=False)