from src.ws.manager import ChatManager

chat_manager = ChatManager()

def get_chat_manager() -> ChatManager:
    return chat_manager
