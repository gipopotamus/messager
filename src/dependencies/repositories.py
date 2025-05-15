from src.repositories import MessageRepository, ChatRepository, UserRepository
from src.dependencies.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


async def get_message_repository(db: AsyncSession = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)

def get_chat_repository(db: AsyncSession = Depends(get_db)) -> ChatRepository:
    return ChatRepository(db)

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)