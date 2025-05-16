# 💬 Real-time Chat API

FastAPI-приложение с поддержкой:

- JWT-аутентификации (`OAuth2PasswordBearer`)
- отправки и получения сообщений в real-time (`WebSocket`)
- сохранения сообщений в PostgreSQL
- поддержки групповых чатов
- Docker-сборки и Alembic-миграций

---

## 🚀 Быстрый старт

```bash
# Клонируй проект и собери контейнер
docker compose build

# Запусти контейнеры
docker compose up -d

# Сгенерировать тестовые данные
docker compose exec api python -m src.scripts.create_test_data

```
## Пример запроса
POST /auth/token
Content-Type: application/x-www-form-urlencoded
username=alice&password=alice123
---
GET /messages/1?limit=50&offset=0
Authorization: Bearer <access_token>
---
Создать чат

POST /chats
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "type": "group",
  "name": "project team"
}

---
WebSocket-клиент (консоль)

pip install websockets aiohttp aioconsole

python src/scripts/ws_chat_client.py

---
## Тестовые данные
Пользователи:
- alice / alice123
- bob / bob123
- carol / carol123

Чаты:
- Приватный чат(id - 1): alice + bob
- Групповой чат(id - 2): alice + bob + carol
