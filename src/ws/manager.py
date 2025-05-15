from typing import Dict, Set
from fastapi import WebSocket


class ChatManager:
    def __init__(self):
        # {chat_id: {user_id: websocket}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, chat_id: int, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(chat_id, {})[user_id] = websocket

    def disconnect(self, chat_id: int, user_id: int):
        chat_conns = self.active_connections.get(chat_id)
        if chat_conns and user_id in chat_conns:
            del chat_conns[user_id]
            if not chat_conns:
                del self.active_connections[chat_id]

    async def send_to_user(self, chat_id: int, user_id: int, data: dict):
        conn = self.active_connections.get(chat_id, {}).get(user_id)
        if conn:
            await conn.send_json(data)

    async def broadcast(self, chat_id: int, data: dict, exclude_user_id: int | None = None):
        chat_conns = self.active_connections.get(chat_id, {})
        for uid, ws in chat_conns.items():
            if uid != exclude_user_id:
                await ws.send_json(data)

    def get_online_users(self, chat_id: int) -> Set[int]:
        return set(self.active_connections.get(chat_id, {}).keys())
