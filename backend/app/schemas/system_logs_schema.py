from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SystemLogCreate(BaseModel):
    level: str
    event_type: str
    message: str
    source: str
    exception_type: str | None = None
    stack_trace: str | None = None
    

class SystemLogResponse(BaseModel):
    id: int
    level: str
    event_type: str
    message: str
    source: str
    occurred_at: datetime
    request_id: str | None
    correlation_id: str | None
    exception_type: str | None
    stack_trace: str | None
    metadata_: dict

    tenant_id: int | None
    clinic_id: int | None
    actor_user_id: int | None
    
    model_config = ConfigDict(from_attributes = True)