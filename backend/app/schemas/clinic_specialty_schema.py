from pydantic import BaseModel


class ClinicSpecialtyCreate(BaseModel):
    clinic_id: int
    specialty_id: int

class ClinicSpecialtyResponse(BaseModel):
    clinic_id: int
    specialty_id: int

    model_config = {
        "from_attributes": True
    }