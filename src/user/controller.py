from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, service
from src.database.core import get_db

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/register")
async def register_user(user: models.UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_user(db, user)
