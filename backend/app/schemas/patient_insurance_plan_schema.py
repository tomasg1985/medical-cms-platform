from datetime import date

from pydantic import BaseModel

from typing import Optional


class PatientInsurancePlanCreate(BaseModel):
    policy_number: str
    is_primary: bool
    expiration_date: date
    status: str

class PatientInsurancePlanUpdate(BaseModel):
    policy_number: Optional[str]
    is_primary: Optional[bool]
    expiration_date: Optional[date]
    status: Optional[str]

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