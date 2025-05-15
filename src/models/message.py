# src/models/message.py
from __future__ import annotations

from sqlalchemy import ForeignKey, String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import UUID, uuid4
from datetime import datetime
from src.core.db import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[UUID] = mapped_column(unique=True, index=True, default=uuid4)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(String(1000))
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    is_read: Mapped[bool] = mapped_column(default=False)

    sender = relationship("User", lazy="joined")
    chat = relationship("Chat", lazy="joined")

    __table_args__ = (
        Index("ix_chat_timestamp", "chat_id", "timestamp"),
    )

    def __repr__(self) -> str:
        return f"<Message id={self.id} chat={self.chat_id} sender={self.sender_id}>"
