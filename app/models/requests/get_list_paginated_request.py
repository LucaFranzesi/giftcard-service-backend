from pydantic import BaseModel

class GetListPaginatedRequest(BaseModel):
    items: int = None
    page: int = None
    search: str = None
    sort_field: str = None
    sort_order: str = None
    filters: dict = None