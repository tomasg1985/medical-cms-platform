from datetime import datetime

from pydantic import BaseModel

class MedicalRecordCreate(BaseModel):
    patient_id: int
    clinic_id: int
    

class MedicalRecordUpdate(BaseModel):
    patient_id: int
    clinic_id: int

class MedicalRecordResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    
    patient_id: int
    clinic_id: int
    
    model_config = {
        "from_attributes": True
    }