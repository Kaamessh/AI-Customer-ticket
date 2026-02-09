from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from . import models, service
from src.database.core import get_db
from src.security import oauth2_scheme

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/register", response_model=models.UserOut)
async def register_user(user: models.UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_user(db, user)

@user_router.post("/token", response_model=models.Token)
async def login_user_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user = await service.authenticate_user(db, form_data)
    token = await service.create_access_token(user.id, user.email)
    return models.Token(access_token=token, token_type="Bearer")

@user_router.get("/me", response_model=models.UserOut)
async def me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    email = await service.verify_token(token)
    user = await service.get_user_by_email(db, email)

    return user
