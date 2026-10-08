from datetime import datetime
from pydantic import BaseModel

class StudyCreate(BaseModel):
    study_type: str
    file_path: str
    status: str
    requested_at: datetime
    completed_at: datetime

class StudyUpdate(BaseModel):
    study_type: str | None = None
    file_path: str | None = None
    status: str | None = None
    requested_at: datetime | None = None
    completed_at: datetime | None = None

class StudyResponse(BaseModel):
    id: int
    study_type: str
    file_path: str
    status: str
    requested_at: datetime
    completed_at: datetime
    created_at: datetime
    updated_at: datetime
    
    patient_id: int
    professional_id: int
    medical_record_id: int
    appointment_id: int
    
    model_config = {
        "from_attributes": True
    }