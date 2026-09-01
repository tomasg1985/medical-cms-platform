from pydantic import BaseModel
from typing import Optional


class SpecialtyCreate(BaseModel):
    official_name: str
    alternative_name: str
    short_description: str
    snomed_code: str
    medical_exercise: str


class SpecialtyUpdate(BaseModel):
    official_name: Optional[str] = None
    alternative_name: Optional[str] = None
    short_description: Optional[str] = None
    snomed_code: Optional[str] = None
    medical_exercise: Optional[str] = None


class SpecialtyResponse(BaseModel):
    id: int
    official_name: str
    alternative_name: str
    short_description: str
    snomed_code: str
    medical_exercise: str

    model_config = {
            "from_attributes": True
        }