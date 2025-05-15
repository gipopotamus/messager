from fastapi import Depends
from src.services import MessageService, ChatService
from src.repositories import MessageRepository, ChatRepository, UserRepository
from src.dependencies.repositories import get_message_repository, get_chat_repository, get_user_repository
from src.services.user_service import UserService


def get_message_service(
    message_repo: MessageRepository = Depends(get_message_repository),
    chat_repo: ChatRepository = Depends(get_chat_repository),
) -> MessageService:
    return MessageService(message_repo, chat_repo)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

def get_chat_service(repo: ChatRepository = Depends(get_chat_repository)) -> ChatService:
    return ChatService(repo)