from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogCreate(BaseModel):
    action: str
    resource_type: str
    outcome: str
    
    ip_address: str | None = None
    user_agent: str | None = None
    
    tenant_id: int | None = None
    clinic_id: int | None = None
    actor_user_id: int | None = None
    

class AuditLogResponse(BaseModel):
    id: int
    action: str
    resource_type: str
    resource_id: str | None
    outcome: str
    occurred_at: datetime
    ip_address: str | None
    user_agent: str | None
    request_id: str | None
    metadata_: dict
    
    tenant_id: int | None
    clinic_id: int | None
    actor_user_id: int | None
    
    model_config = ConfigDict(from_attributes = True)