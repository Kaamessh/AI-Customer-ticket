from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, FLOAT, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from uuid import UUID
import uuid
from enum import Enum

from sqlalchemy import Enum as SQLEnum

from src.database.core import Base

class Status(str, Enum):
    Received = "Issue Received"
    Processing = "Working on it"
    InformationNeed = "Need More Information"
    SolutionProvided = "Solution Provided"
    IssueResolved = "Issue Resolved"

class Priority(str, Enum):
    Default = "Default"
    Low = "Low"
    Medium = "Medium"
    High = "High"


class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(VARCHAR, nullable=False)
    status = Column(SQLEnum, SQLEnum(Status, name="ticket_status", native_enum=True), nullable=False, default=Status.Received)
    priority = Column(SQLEnum, SQLEnum(Priority, name="ticket_priority", native_enum=True), nullable=False, default=Priority.Default)
    user_id = Column(UUID, ForeignKey('user.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)

    user = relationship("User", back_populates="ticket")
