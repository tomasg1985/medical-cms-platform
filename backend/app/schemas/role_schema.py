from datetime import datetime

from typing import Optional

from pydantic import BaseModel


class RoleSummary(BaseModel):
    id: int
    name: str
    description: str

    model_config = {
                "from_attributes": True
            }


class RoleCreate(BaseModel):
    name: str
    description: str


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
            "from_attributes": True
        }