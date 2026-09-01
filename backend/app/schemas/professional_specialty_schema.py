from pydantic import BaseModel


class ProfessionalSpecialtyCreate(BaseModel):
    professional_id: int
    specialty_id: int

class ProfessionalSpecialtyResponse(BaseModel):
    professional_id: int
    specialty_id: int

    model_config = {
        "from_attributes": True
    }