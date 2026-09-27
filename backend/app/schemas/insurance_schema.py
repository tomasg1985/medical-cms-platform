from pydantic import BaseModel

class InsuranceCreate(BaseModel):
    name: str
    registration: str

class InsuranceUpdate(BaseModel):
    name: str
    registration: str

class InsuranceResponse(BaseModel):
    id: int
    name: str
    registration: str
    is_active: bool
    
    model_config = {
            "from_attributes": True
        }