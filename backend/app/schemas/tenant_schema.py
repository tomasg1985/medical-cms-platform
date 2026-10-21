from datetime import datetime

from pydantic import BaseModel


class TenantCreate(BaseModel):
    name: str
    status: str

class TenantUpdate(BaseModel):
    name: str
    status: str

class TenantResponse(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }