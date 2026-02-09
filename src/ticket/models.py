from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from src.entities.tickets import Status

class Ticket(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID | None = None
    description: str
    status: Status | None = None
    priority: str | None = None
    user_id: uuid.UUID
    created_at: datetime | None = None

class TicketCreate(BaseModel):
    description: str

class TicketUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    description: str | None = None
    status: Status | None = None
    priority: str | None = None

class TicketStatusUpdate(BaseModel):
    id: uuid.UUID
    status: Status
