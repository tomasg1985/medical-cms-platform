from datetime import datetime
from pydantic import BaseModel

class MedicationPresentationCreate(BaseModel):
    presentation: str
    concentration: str
    quantity: str
    unit: str
    status: str

class MedicationPresentationUpdate(BaseModel):
    presentation: str
    concentration: str
    quantity: str
    unit: str
    status: str

class MedicationPresentationResponse(BaseModel):
    id: int
    presentation: str
    concentration: str
    quantity: str
    unit: str
    status: str
    created_at: datetime

    medication_id: int

    model_config = {
        "from_attributes": True
    }