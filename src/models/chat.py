from sqlalchemy import ForeignKey, String, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.db import Base
import enum


class ChatType(enum.Enum):
    private = "private"
    group = "group"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType), nullable=False, default=ChatType.private)

    users = relationship("ChatUser", back_populates="chat", cascade="all, delete-orphan")


class ChatUser(Base):
    __tablename__ = "chat_users"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    chat = relationship("Chat", back_populates="users")

    __table_args__ = (
        Index("ix_chatuser_user", "user_id"),
    )
