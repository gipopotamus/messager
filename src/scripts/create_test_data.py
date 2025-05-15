import asyncio
from uuid import uuid4
from src.core.db import AsyncSessionFactory, Base, engine
from src.models import User, Chat, ChatUser, Message, ChatType
from datetime import datetime


async def create_test_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionFactory() as session:
        # --- Пользователи
        user1 = User(id=1, username="alice", email="alice@example.com", password_hash="alice123")
        user2 = User(id=2, username="bob", email="bob@example.com", password_hash="bob123")
        user3 = User(id=3, username="carol", email="carol@example.com", password_hash="carol123")

        session.add_all([user1, user2, user3])

        # --- Приватный чат Alice + Bob
        private_chat = Chat(name=None, type=ChatType.private)
        session.add(private_chat)
        await session.flush()

        session.add_all([
            ChatUser(chat_id=private_chat.id, user_id=1),
            ChatUser(chat_id=private_chat.id, user_id=2),
        ])

        session.add(Message(
            chat_id=private_chat.id,
            sender_id=1,
            text="Привет, Боб!",
            message_id=uuid4(),
            timestamp=datetime.now(),
            is_read=False
        ))

        # --- Групповой чат: Alice, Bob, Carol
        group_chat = Chat(name="project team", type=ChatType.group)
        session.add(group_chat)
        await session.flush()

        session.add_all([
            ChatUser(chat_id=group_chat.id, user_id=1),
            ChatUser(chat_id=group_chat.id, user_id=2),
            ChatUser(chat_id=group_chat.id, user_id=3),
        ])

        session.add(Message(
            chat_id=group_chat.id,
            sender_id=2,
            text="Добро пожаловать в группу!",
            message_id=uuid4(),
            timestamp=datetime.now(),
            is_read=False
        ))

        await session.commit()
        print("✅ Test data created.")


if __name__ == "__main__":
    asyncio.run(create_test_data())
