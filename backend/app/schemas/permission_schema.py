from datetime import datetime

from typing import Optional

from pydantic import BaseModel

class PermissionSummary(BaseModel):
    id: int
    name: str
    description: str
    resource: str
    action: str

    model_config = {
            "from_attributes": True
        }


class PermissionCreate(BaseModel):
    name: str
    description: str
    resource: str
    action: str


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    is_active: Optional[bool] = None


class PermissionResponse(BaseModel):
    id: int
    name: str
    description: str
    resource: str
    action: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
            "from_attributes": True
        }