from pydantic import BaseModel, ConfigDict
from uuid import UUID

class User(BaseModel):
    conig = ConfigDict(from_attributes=True)
    id: UUID | None = None
    name: str
    email: str
    password: str
    phone: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str

class UserLogin(BaseModel):
    email: str
    password: str
