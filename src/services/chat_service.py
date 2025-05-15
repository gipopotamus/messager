from src.schemas import ChatCreate, ChatRead
from src.repositories import ChatRepository
from src.services.exceptions import ServiceError


class ChatService:
    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo

    async def create_chat(self, creator_id: int, data: ChatCreate) -> ChatRead:
        participants = set(data.users)
        participants.add(creator_id)

        if data.type == "private":
            if len(participants) != 2:
                raise ServiceError("Private chat must have exactly 2 participants")

            existing = await self.chat_repo.find_private_chat_between(*participants)
            if existing:
                return ChatRead.model_validate(existing)

        # Создаём чат
        new_chat = await self.chat_repo.create_chat(
            name=data.name,
            type=data.type,
            user_ids=list(participants),
        )

        return ChatRead.model_validate(new_chat)
