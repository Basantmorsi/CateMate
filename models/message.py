from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="owner.id")
    recipient_id: int = Field(foreign_key="owner.id")
    # Optional cat this message is about, so owners know which cat prompted the contact.
    cat_id: int | None = Field(default=None, foreign_key="cat.id")
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
