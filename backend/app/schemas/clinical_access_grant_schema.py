from datetime import datetime

from pydantic import BaseModel

class ClinicalAccessGrantCreate(BaseModel):
    status: str

class ClinicalAccessGrantUpdate(BaseModel):
    status: str

class ClinicalAccessGrantResponse(BaseModel):
    id: int
    status: str
    requested_at: datetime
    granted_at: datetime
    expires_at: datetime
    revoked_at: datetime
    created_at: datetime
    
    patient_id: int
    professional_id: int
    clinic_id: int
    appointment_id: int
    
    model_config = {
        "from_attributes": True
    }