from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func
from src.models import ChatUser, Chat, ChatType


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_has_access(self, chat_id: int, user_id: int) -> bool:
        stmt = (
            select(1)
            .select_from(ChatUser)
            .where(ChatUser.chat_id == chat_id, ChatUser.user_id == user_id)
            .limit(1)
        )
        result = await self.session.scalar(stmt)
        return result is not None

    async def find_private_chat_between(self, user1: int, user2: int) -> Chat | None:
        stmt = (
            select(Chat)
            .join(ChatUser)
            .where(Chat.type == ChatType.private)
            .where(ChatUser.user_id.in_([user1, user2]))
            .group_by(Chat.id)
            .having(
                func.count(ChatUser.user_id.distinct()) == 2
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_chat(
        self,
        name: str | None,
        type: str,
        user_ids: list[int],
    ) -> Chat:
        chat = Chat(name=name, type=ChatType(type))
        self.session.add(chat)
        await self.session.flush()

        stmt = insert(ChatUser).values([
            {"chat_id": chat.id, "user_id": uid}
            for uid in user_ids
        ])
        await self.session.execute(stmt)

        return chat