from datetime import date

from pydantic import BaseModel
from typing import Optional

class PatientSummary(BaseModel):
    id: int
    name: str
    last_name: str
    dni: str

    model_config = {
        "from_attributes": True
    }

class ClinicResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class PatientClinicResponse(BaseModel):
    patient_id: int
    clinic_id: int

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

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    dni: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    insurance: Optional[str] = None

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
    clinics: list["ClinicResponse"]

    model_config = {
        "from_attributes": True
    }