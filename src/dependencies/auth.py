from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer
from src.core.auth import decode_access_token
from src.dependencies.db import get_db
from src.repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    user_id = decode_access_token(token)
    if not user_id or not user_id.isdigit():
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return int(user_id)

async def get_current_user_id_ws(websocket: WebSocket) -> int:
    token = websocket.query_params.get("token")
    user_id = decode_access_token(token)
    if not user_id or not user_id.isdigit():
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(user_id)