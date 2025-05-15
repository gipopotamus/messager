from pydantic import BaseModel, UUID4, ConfigDict
from datetime import datetime
from src.schemas.user import UserRead


class MessageBase(BaseModel):
    chat_id: int
    text: str
    timestamp: datetime


class MessageCreate(MessageBase):
    message_id: UUID4 | None = None


class MessageRead(BaseModel):
    id: int
    message_id: UUID4
    chat_id: int
    sender: UserRead
    text: str
    timestamp: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)


class MessageInDB(MessageRead):
    sender_id: int
