from typing import Generic, List, TypeVar
from pydantic import BaseModel

# Definizione di un tipo generico T
T = TypeVar("T")

class TableResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]