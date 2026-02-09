from fastapi import APIRouter, FastAPI
from src.user.controller import user_router

def initialize_endpoints(app: FastAPI):
    app.include_router(user_router)
