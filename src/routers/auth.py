from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.services import UserService
from src.dependencies.services import get_user_service
from src.schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.authenticate(form_data.username, form_data.password)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid credentials")
