from datetime import datetime

from pydantic import BaseModel

class ClinicalEvolutionModelCreate(BaseModel):
    content: str
    

class ClinicalEvolutionUpdate(BaseModel):
    content: str

class ClinicalEvolutionModelResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    
    medical_record_id: int
    professional_id: int
    appointment_id: int

    
    model_config = {
            "from_attributes": True
        }