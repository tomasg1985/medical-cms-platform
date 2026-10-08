from datetime import datetime

from pydantic import BaseModel


class MedicalDocumentCreate(BaseModel):
    name: str
    file_path: str
    document_type: str
    patient_id: int
    medical_record_id: int
    professional_id: int
    clinic_id: int

class MedicalDocumentUpdate(BaseModel):
    name: str
    file_path: str
    document_type: str

class MedicalDocumentResponse(BaseModel):
    id: int
    name: str
    file_path: str
    document_type: str
    created_at: datetime
    updated_at: datetime
    
    patient_id: int
    medical_record_id: int
    professional_id: int
    clinic_id: int
    
    model_config = {
        "from_attributes": True
    }