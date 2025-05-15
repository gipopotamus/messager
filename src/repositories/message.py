from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.models import Message
from typing import List

class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_chat(self, chat_id: int, limit: int, offset: int) -> List[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.timestamp.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_message(self, chat_id: int, sender_id: int, text: str, message_id: UUID) -> Message:
        msg = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            text=text,
            message_id=message_id,
        )
        self.session.add(msg)
        await self.session.flush()
        await self.session.commit()
        return msg

    async def mark_message_read(self, chat_id: int, user_id: int, message_id: UUID):
        stmt = (
            update(Message)
            .where(
                Message.chat_id == chat_id,
                Message.message_id == message_id,
                Message.sender_id != user_id,
            )
            .values(is_read=True)
        )
        await self.session.execute(stmt)