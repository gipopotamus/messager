from fastapi import APIRouter, WebSocket, Depends
from src.dependencies.auth import get_current_user_id_ws
from src.dependencies.services import get_message_service
from src.dependencies.ws import get_chat_manager
from src.services import MessageService
from src.ws.manager import ChatManager
from src.ws.handlers import handle_websocket

router = APIRouter()


@router.websocket("/ws/{chat_id}")
async def websocket_chat(
    websocket: WebSocket,
    chat_id: int,
    user_id: int = Depends(get_current_user_id_ws),
    service: MessageService = Depends(get_message_service),
    manager: ChatManager = Depends(get_chat_manager),
):
    await handle_websocket(chat_id, user_id, websocket, service, manager)
