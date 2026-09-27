from pydantic import BaseModel

class PlanCreate(BaseModel):
    name: str
    description: str

class PlanUpdate(BaseModel):
    name: str
    description: str

class PlanResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    
    model_config = {
            "from_attributes": True
        }