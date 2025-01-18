from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime
from datetime import datetime, timezone

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer, ForeignKey('Users.id'), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)