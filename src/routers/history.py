from fastapi import APIRouter, Depends, Query, Path
from typing import List

from src.dependencies.auth import get_current_user_id
from src.dependencies.services import get_message_service
from src.schemas import MessageRead
from src.services import MessageService

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{chat_id}", response_model=List[MessageRead])
async def get_history(
    chat_id: int = Path(...),
    limit: int = Query(50),
    offset: int = Query(0),
    user_id: int = Depends(get_current_user_id),
    service: MessageService = Depends(get_message_service),
):
    return await service.get_chat_history(
        chat_id=chat_id,
        user_id=user_id,
        limit=limit,
        offset=offset,
    )
