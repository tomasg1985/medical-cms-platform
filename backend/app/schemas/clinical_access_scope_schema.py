from pydantic import BaseModel

class ClinicalAccessScopeCreate(BaseModel):
    code: str
    name: str
    description: str

class ClinicalAccessScopeUpdate(BaseModel):
    code: str
    name: str
    description: str

class ClinicalAccessScopeResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str
    
    model_config = {
        "from_attributes": True
    }