import asyncio
from uuid import uuid4
from aioconsole import ainput
import websockets
import json
import aiohttp
import getpass


API_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"


async def get_token(username: str, password: str) -> str:
    async with aiohttp.ClientSession() as session:
        data = {
            "username": username,
            "password": password,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with session.post(f"{API_URL}/auth/token", data=data, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"❌ Auth failed: {resp.status} - {text}")
            result = await resp.json()
            return result["access_token"]


async def chat_client():
    print("🔐 Вход в систему")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    chat_id = input("Chat ID: ").strip()

    try:
        token = await get_token(username, password)
    except Exception as e:
        print(str(e))
        return

    url = f"{WS_URL}/{chat_id}?token={token}"
    print(f"\n📡 Connecting to {url} ...\n")

    async with websockets.connect(url) as ws:
        print("✅ Connected. Type 'exit' to quit.\n")

        async def receive():
            print("👂 RECEIVE STARTED")
            try:
                async for msg in ws:
                    print("📥 raw:", msg)
                    try:
                        data = json.loads(msg)
                        print("📥 parsed:", data)
                    except Exception as e:
                        print(f"❌ JSON parse error: {e}")
            except Exception as e:
                print(f"❌ receive() error: {e}")


        async def send():
            while True:
                text = await ainput("You: ")
                if text == "exit":
                    await ws.close()
                    break

                data = {
                    "type": "send",
                    "chat_id": int(chat_id),
                    "message_id": str(uuid4()),
                    "text": text
                }
                await ws.send(json.dumps(data))
                print("📤 sent:", data)

        await asyncio.gather(receive(), send())


if __name__ == "__main__":
    try:
        asyncio.run(chat_client())
    except KeyboardInterrupt:
        print("\n🔌 Disconnected.")
