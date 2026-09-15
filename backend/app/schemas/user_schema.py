from pydantic import BaseModel
from datetime import datetime


class UserSummary(BaseModel):
    id: int
    email: str
    
    model_config = {
            "from_attributes": True
        }


class UserCreate(BaseModel):
    email: str

class UserUpdate(BaseModel):
    email: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
            "from_attributes": True
        }