from fastapi import APIRouter, Depends, status
from src.schemas import ChatCreate, ChatRead
from src.services import ChatService
from src.dependencies.services import get_chat_service
from src.dependencies.auth import get_current_user_id

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    user_id: int = Depends(get_current_user_id),
    service: ChatService = Depends(get_chat_service),
):
    return await service.create_chat(creator_id=user_id, data=chat_data)
