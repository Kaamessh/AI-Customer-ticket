from unittest import result
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.entities.tickets import Ticket, Status, Priority
from uuid import UUID

from . import models

async def get_tickets_by_user_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(Ticket).where(Ticket.user_id == user_id))
    return result.scalars().all()

async def create_ticket(db: AsyncSession, ticket: models.TicketCreate, user_id: UUID):
    new_ticket = Ticket(
        description=ticket.description,
        user_id=user_id
    )
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    return new_ticket

async def updateStatus(db: AsyncSession, id: UUID,status: Status):
    stmt = select(Ticket).where(Ticket.id == id)
    result = await db.execute(stmt)
    ticket = result.scalar_one_or_none()
    if ticket:
        ticket.status = status
        await db.commit()
        await db.refresh(ticket)
    return ticket

async def get_ticket(db: AsyncSession, ticket_id: UUID):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalar_one_or_none()

async def update_ticket(db: AsyncSession, ticket_id: UUID, ticket_update: models.TicketUpdate):
    stmt = select(Ticket).where(Ticket.id == ticket_id)
    result = await db.execute(stmt)
    ticket = result.scalar_one_or_none()
    if ticket:
        if ticket_update.description is not None:
            ticket.description = ticket_update.description
        if ticket_update.status is not None:
            ticket.status = ticket_update.status
        if ticket_update.priority is not None:
            ticket.priority = ticket_update.priority
        await db.commit()
        await db.refresh(ticket)
    return ticket

async def delete_ticket(db: AsyncSession, ticket_id: UUID):
    stmt = select(Ticket).where(Ticket.id == ticket_id)
    result = await db.execute(stmt)
    ticket = result.scalar_one_or_none()
    if ticket:
        await db.delete(ticket)
        await db.commit()
    return ticket
