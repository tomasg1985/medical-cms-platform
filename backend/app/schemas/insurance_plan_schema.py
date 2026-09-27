from pydantic import BaseModel

class InsurancePlanCreate(BaseModel):
    insurance_id: int
    plan_id: int
    

class InsurancePlanUpdate(BaseModel):
    insurance_id: int
    plan_id: int
    

class InsurancePlanResponse(BaseModel):
    id: int
    
    insurance_id: int
    plan_id: int

    model_config = {
            "from_attributes": True
        }