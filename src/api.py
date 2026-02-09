from fastapi import APIRouter, FastAPI
from src.user.controller import user_router

def iniitialize_endpoints(app: FastAPI):
    app.include_router(user_router)
