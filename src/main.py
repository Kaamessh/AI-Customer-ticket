from fastapi import FastAPI
from src.api import iniitialize_endpoints
from src.database.core import Base, SessionLocal

app = FastAPI(title="AI Customer Ticket")

iniitialize_endpoints(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Customer Ticket API!"}
