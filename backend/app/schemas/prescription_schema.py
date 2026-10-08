from datetime import datetime
from pydantic import BaseModel

class PrescriptionCreate(BaseModel):
    prescription_date: datetime 
    instructions: str
    status: str

class PrescriptionUpdate(BaseModel):
    prescription_date: datetime | None = None
    instructions: str | None = None
    status: str | None = None

class PrescriptionResponse(BaseModel):
    id: int
    prescription_date: datetime 
    instructions: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    patient_id: int
    professional_id: int
    medical_record_id: int
    appointment_id: int
    
    model_config = {
        "from_attributes": True
    }