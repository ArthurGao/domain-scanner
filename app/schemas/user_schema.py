from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    role: str = "member"

class UserCreate(UserBase):
    password: str
    organization_id: UUID

class UserResponse(UserBase):
    id: UUID
    organization_id: UUID

    model_config = {
        "from_attributes": True
    }