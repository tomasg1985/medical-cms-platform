from pydantic import BaseModel

class ClinicalAccessGrantScopeResponse(BaseModel):
    clinical_access_grant_id: int
    scope_id: int
    
    model_config = {
        "from_attributes": True
    }