from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Boolean, Column, Integer, DateTime
from datetime import datetime, timezone

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.now(timezone.utc), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)