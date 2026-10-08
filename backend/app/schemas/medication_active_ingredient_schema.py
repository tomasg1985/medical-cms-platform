from pydantic import BaseModel

class MadicationActiveIngredientCreate(BaseModel):
    medication_id: int
    active_ingredients_id: int


class MedicationActiveIngredientUpdate(BaseModel):
    medication_id: int
    active_ingredients_id: int


class MedicationActiveIngredientResponse(BaseModel):
    medication_id: int
    active_ingredients_id: int
    
    model_config = {
        "from_attributes": True
    }