from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
