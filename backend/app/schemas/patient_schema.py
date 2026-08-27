from datetime import date

from pydantic import BaseModel
from typing import Optional

class ClinicResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class PatientCreate(BaseModel):
    name: str
    last_name: str
    birth_date: Optional[date] = None
    dni: str
    email: str
    phone: str
    address: str
    insurance: str
    clinic_id: int
    
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    dni: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    insurance: Optional[str] = None
    clinic_id: Optional[int] = None

class PatientResponse(BaseModel):
    id: int
    name: str
    last_name: str
    birth_date: Optional[date] = None
    dni: str
    email: str
    phone: str
    address: str
    insurance: str
    clinic_id: int
    clinic: ClinicResponse

    model_config = {
        "from_attributes": True
    }