from pydantic import BaseModel

class ProfessionalResponse(BaseModel):
    id: int
    name: str
    last_name: str
    specialty: str

    model_config = {
            "from_attributes": True
        }

class ClinicCreate(BaseModel):
    name: str


class ClinicUpdate(BaseModel):
    name: str


class ClinicResponse(BaseModel):
    id: int
    name: str
    professionals: list["ProfessionalResponse"]

    model_config = {
        "from_attributes": True
    }
