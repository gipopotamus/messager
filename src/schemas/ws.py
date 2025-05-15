from pydantic import BaseModel, UUID4
from typing import Literal
from datetime import datetime


class WSBase(BaseModel):
    type: Literal["send", "read"]


class WSSendMessage(WSBase):
    type: Literal["send"]
    chat_id: int
    message_id: UUID4 | None = None
    text: str


class WSReadMessage(WSBase):
    type: Literal["read"]
    chat_id: int
    message_id: UUID4
    read_at: datetime
