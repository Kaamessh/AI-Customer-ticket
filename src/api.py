from fastapi import APIRouter, FastAPI

async def iniitialize_endpoints(app: FastAPI):
    app.include_router
