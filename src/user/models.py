from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID | None = None
    name: str
    email: EmailStr
    password: str
    phone: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    email: EmailStr
    phone: str

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: EmailStr
    password: str
    phone: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
