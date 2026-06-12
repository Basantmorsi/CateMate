from datetime import datetime
from pydantic import BaseModel


class MessageCreate(BaseModel):
    recipient_id: int
    content: str
    cat_id: int | None = None


class MessageRead(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    cat_id: int | None = None
    content: str
    created_at: datetime
