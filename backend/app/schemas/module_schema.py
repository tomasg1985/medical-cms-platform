
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ModuleCreate(BaseModel):
    name: str
    description: str
    is_active: bool


class ModuleUpdate(BaseModel):
    name: str
    description: str
    is_active: bool


class ModuleResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
