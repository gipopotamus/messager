from uuid import UUID

from src.models import Chat, Message
from src.repositories import MessageRepository, ChatRepository
from src.schemas import MessageRead
from typing import List

from src.services.exceptions import NotFoundError


class MessageService:
    def __init__(
        self,
        message_repo: MessageRepository,
        chat_repo: ChatRepository,
    ):
        self.message_repo = message_repo
        self.chat_repo = chat_repo

    async def get_chat_history(
        self, chat_id: int, user_id: int, limit: int, offset: int
    ) -> List[MessageRead]:
        has_access = await self.chat_repo.user_has_access(chat_id, user_id)
        if not has_access:
            raise NotFoundError[Chat](chat_id)

        messages = await self.message_repo.get_by_chat(chat_id, limit, offset)
        return [MessageRead.model_validate(m) for m in messages]

    async def send_message(
        self,
        chat_id: int,
        user_id: int,
        text: str,
        message_id: UUID,
    ) -> Message:
        has_access = await self.chat_repo.user_has_access(chat_id, user_id)
        if not has_access:
            raise NotFoundError[Chat](chat_id)
        return await self.message_repo.create_message(
            chat_id=chat_id,
            sender_id=user_id,
            text=text,
            message_id=message_id,
        )

    async def mark_as_read(
        self,
        user_id: int,
        chat_id: int,
        message_id: UUID,
    ) -> None:
        has_access = await self.chat_repo.user_has_access(chat_id, user_id)
        if not has_access:
            raise NotFoundError[Chat](chat_id)

        await self.message_repo.mark_message_read(
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
        )