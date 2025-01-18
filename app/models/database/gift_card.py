from models.database.base import Base
from sqlalchemy import Column, DateTime, Integer, String

class GiftCard(Base):
    __tablename__ = 'GiftCards'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    residual_amount = Column(Integer, nullable=False)
    expiration = Column(DateTime, nullable=True)
