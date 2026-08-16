from pydantic import BaseModel


class ClinicCreate(BaseModel):
    name: str


class ClinicResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
