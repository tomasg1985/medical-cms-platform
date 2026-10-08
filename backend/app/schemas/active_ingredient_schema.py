from datetime import datetime

from pydantic import BaseModel

class ActiveIngredientCreate(BaseModel):
    name: str
    description: str
    code: str
    status: str


class ActiveIngredientUpdate(BaseModel):
    name: str
    description: str
    code: str
    status: str


class ActiveIngredientPatch(BaseModel):
    name: str | None = None
    description: str | None = None
    code: str | None = None
    status: str | None = None


class ActiveIngredientResponse(BaseModel):
    id: int
    name: str
    description: str
    code: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }