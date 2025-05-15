from fastapi import WebSocket, WebSocketDisconnect
from uuid import uuid4
import json

from src.ws.manager import ChatManager
from src.services import MessageService
from src.schemas.ws import WSSendMessage, WSReadMessage


async def handle_websocket(
    chat_id: int,
    user_id: int,
    websocket: WebSocket,
    service: MessageService,
    manager: ChatManager,
):
    await manager.connect(chat_id, user_id, websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            match data.get("type"):
                case "send":
                    try:
                        msg = WSSendMessage(**data)
                        msg.message_id = msg.message_id or uuid4()

                        saved = await service.send_message(
                            chat_id=msg.chat_id,
                            user_id=user_id,
                            text=msg.text,
                            message_id=msg.message_id,
                        )

                        await manager.broadcast(
                            chat_id,
                            {
                                "type": "message",
                                "message_id": str(saved.message_id),
                                "text": saved.text,
                                "sender_id": user_id,
                                "timestamp": saved.timestamp.isoformat(),
                            },
                            exclude_user_id=user_id,
                        )
                    except Exception as e:
                        await websocket.send_json({"type": "error", "detail": str(e)})

                case "read":
                    try:
                        msg = WSReadMessage(**data)
                        await service.mark_as_read(
                            user_id=user_id,
                            chat_id=msg.chat_id,
                            message_id=msg.message_id,
                        )
                    except Exception as e:
                        await websocket.send_json({
                            "type": "error",
                            "detail": f"Failed to mark as read: {str(e)}"
                        })

                case _:
                    await websocket.send_json({"error": "Unknown type"})

    except WebSocketDisconnect:
        manager.disconnect(chat_id, user_id)
