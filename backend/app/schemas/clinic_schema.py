from pydantic import BaseModel

from app.schemas.patient_schema import PatientSummary
from app.schemas.professional_schema import ProfessionalSummary

class ClinicCreate(BaseModel):
    name: str


class ClinicUpdate(BaseModel):
    name: str


class ClinicResponse(BaseModel):
    id: int
    name: str
    professionals: list["ProfessionalSummary"]
    patients: list["PatientSummary"]

    model_config = {
        "from_attributes": True
    }
