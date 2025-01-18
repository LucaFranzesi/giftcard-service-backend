from datetime import datetime
from pydantic import BaseModel

class CreateGiftCardRequest(BaseModel):
    amount: int
    expiration: datetime = None