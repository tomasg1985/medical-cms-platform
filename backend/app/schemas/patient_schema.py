from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    name: str
    last_name: str
    age: int
    dni: str
    email: str
    phone: str
    address: str
    insurance: str
    
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    dni: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    insurance: Optional[str] = None

class PatientResponse(BaseModel):
    id: int
    name: str
    last_name: str
    age: int
    dni: str
    email: str
    phone: str
    address: str
    insurance: str

    model_config = {
        "from_attributes": True
    }