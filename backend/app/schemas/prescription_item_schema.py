from pydantic import BaseModel

class PrescriptionItemCreate(BaseModel):
    dosage: str
    frequency: str
    duration: str
    instructions: str

class PrescriptionItemUpdate(BaseModel):
    dosage: str
    frequency: str
    duration: str
    instructions: str

class PrescriptionItemResponse(BaseModel):
    id: int
    dosage: str
    frequency: str
    duration: str
    instructions: str

    prescription_id: int
    medication_id: int

    model_config = {
        "from_attributes": True
    }