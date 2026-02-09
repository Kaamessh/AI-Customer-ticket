from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import initialize_endpoints
from src.database.core import Base, engine

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield

app = FastAPI(title="AI Customer Ticket")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_endpoints(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Customer Ticket API!"}
