from pydantic import BaseModel, ConfigDict
from typing import List, Literal


class ChatBase(BaseModel):
    name: str | None = None
    type: Literal["private", "group"]


class ChatCreate(ChatBase):
    users: List[int]  # список user_id, кроме текущего


class ChatRead(ChatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

