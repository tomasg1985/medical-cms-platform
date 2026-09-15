from pydantic import BaseModel

class UserClinicCreate(BaseModel):
    user_id: int
    clinic_id: int


class UserClinicResponse(BaseModel):
    user_id: int
    clinic_id: int
    
    model_config = {
            "from_attributes": True
        }