from datetime import datetime
from pydantic import BaseModel

class MedicationCreate(BaseModel):
    name: str
    description: str
    laboratory: str
    status: str

class MedicationUpdate(BaseModel):
    name: str
    description: str
    laboratory: str
    status: str

class MedicationResponse(BaseModel):
    id: int
    name: str
    description: str
    laboratory: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }