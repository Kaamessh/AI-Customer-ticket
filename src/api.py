from fastapi import APIRouter, FastAPI
from src.user.controller import user_router
from src.ticket.controller import ticket_router

def initialize_endpoints(app: FastAPI):
    app.include_router(user_router)
    app.include_router(ticket_router)
