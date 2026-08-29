from datetime import date

from typing import Optional

from pydantic import BaseModel

class ClinicResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class ProfessionalCreate(BaseModel):
    name: str
    last_name: str
    gender: str
    birth_date: date
    phone: str
    email: str
    credential: str
    credential_expiration: date
    dni: str
    specialty: str
    address: str
    medical_facility: str
    working_insurance: str


class ProfessionalUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    credential: Optional[str] = None
    credential_expiration: Optional[date] = None
    specialty: Optional[str] = None
    address: Optional[str] = None
    medical_facility: Optional[str] = None
    working_insurance: Optional[str] = None


class ProfessionalResponse(BaseModel):
    id: int
    name: str
    last_name: str
    gender: str
    birth_date: date
    phone: str
    email: str
    credential: str
    credential_expiration: date
    dni: str
    specialty: str
    address: str
    medical_facility: str
    working_insurance: str
    
    clinics: list["ClinicResponse"]

    model_config = {
            "from_attributes": True
        }