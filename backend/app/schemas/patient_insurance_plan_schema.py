from datetime import date

from pydantic import BaseModel

from typing import Optional


class PatientInsurancePlanCreate(BaseModel):
    policy_number: str
    is_primary: bool
    expiration_date: date
    status: str

class PatientInsurancePlanUpdate(BaseModel):
    policy_number: Optional[str] = None
    is_primary: Optional[bool] = None
    expiration_date: Optional[date] = None
    status: Optional[str] = None

class PatientInsurancePlanResponse(BaseModel):
    id: int
    policy_number: str
    is_primary: bool
    expiration_date: date
    status: str
    
    patient_id: int
    insurance_plan_id: int

    model_config = {
            "from_attributes": True
        }