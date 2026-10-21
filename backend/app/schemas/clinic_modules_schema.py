from datetime import datetime

from pydantic import BaseModel




class ClinicModuleCreate(BaseModel):
    status: str
    clinic_id: int
    module_id: int

class ClinicModuleUpdate(BaseModel):
    status: str
    clinic_id: int
    module_id: int

class ClinicModuleResponse(BaseModel):
    status: str
    activated_at: datetime
    deactivated_at: datetime

    clinic_id: int
    module_id: int
    
    model_config = {
        "from_attributes": True
    }