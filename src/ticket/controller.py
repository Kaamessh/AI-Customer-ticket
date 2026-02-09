from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.entities.tickets import Ticket, Status
import uuid

from src.security import oauth2_scheme
from src.database.core import get_db
from . import models, service
from src.user.service import get_user_by_email, verify_token

ticket_router = APIRouter(prefix="/tickets", tags=["tickets"])
    
@ticket_router.get("/", response_model=list[models.Ticket])
async def get_tickets(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_email = await verify_token(token)
    user = await get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    tickets = await service.get_tickets_by_user_id(db, user_id=user.id)
    return tickets

@ticket_router.post("/", response_model=models.Ticket)
async def create_ticket(ticket: models.TicketCreate, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_email = await verify_token(token)
    user = await get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    created_ticket = await service.create_ticket(db, ticket, user.id)
    return created_ticket

@ticket_router.get("/{ticket_id}", response_model=models.Ticket)
async def get_ticket(ticket_id: uuid.UUID, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_email = await verify_token(token)
    user = await get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    ticket = await service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    if ticket.user_id != user.id:
         raise HTTPException(status_code=403, detail="Not authorized to access this ticket")
         
    return ticket

@ticket_router.put("/{ticket_id}", response_model=models.Ticket)
async def update_ticket(ticket_id: uuid.UUID, ticket_update: models.TicketUpdate, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_email = await verify_token(token)
    user = await get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ticket = await service.get_ticket(db, ticket_id)
    if not ticket:
         raise HTTPException(status_code=404, detail="Ticket not found")
         
    if ticket.user_id != user.id:
         raise HTTPException(status_code=403, detail="Not authorized to update this ticket")

    updated_ticket = await service.update_ticket(db, ticket_id, ticket_update)
    return updated_ticket

@ticket_router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: uuid.UUID, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_email = await verify_token(token)
    user = await get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ticket = await service.get_ticket(db, ticket_id)
    if not ticket:
         raise HTTPException(status_code=404, detail="Ticket not found")
         
    if ticket.user_id != user.id:
         raise HTTPException(status_code=403, detail="Not authorized to delete this ticket")

    await service.delete_ticket(db, ticket_id)
    return {"ok": True}
