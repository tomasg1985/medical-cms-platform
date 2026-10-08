from pydantic import BaseModel

from typing import Optional

class PatientContactCreate(BaseModel):
    patient_id: int
    first_name: str
    last_name: str
    relationship_type: str
    phone: str
    email: str
    is_emergency: bool

class PatientContactUpdate(BaseModel):
    first_name: Optional[str] =None
    last_name: Optional[str] =None
    relationship_type: Optional[str] =None
    phone: Optional[str] =None
    email: Optional[str] =None
    is_emergency: Optional[bool] = None

class PatientContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    relationship_type: str
    phone: str
    email: str
    is_emergency: bool
    
    patient_id: int

    model_config = {
            "from_attributes": True
        }