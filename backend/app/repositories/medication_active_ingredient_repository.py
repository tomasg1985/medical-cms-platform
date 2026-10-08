from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medication_active_ingredient_model import MedicationActiveIngredient


class MedicationActiveIngredientRepository:
    
    def get_by_id(self, db: Session, medication_active_ingredient_id: int) -> MedicationActiveIngredient | None:
        statement = (
            select(MedicationActiveIngredient)
            .where(MedicationActiveIngredient.id == medication_active_ingredient_id)
        )
        result = db.execute(statement)
        medication_active_ingredient = result.scalar_one_or_none()
        
        return medication_active_ingredient


    def create(self, db: Session, medication_active_ingredient: MedicationActiveIngredient) -> MedicationActiveIngredient:
        try:
            db.add(medication_active_ingredient)
            db.commit()
            db.refresh(medication_active_ingredient)

            return medication_active_ingredient

        except Exception:
            db.rollback()
            raise


    def get_by_medication_active_ingredient(
        self, 
        db: Session, 
        medication_id: int, 
        active_ingredients_id: int
    ) -> MedicationActiveIngredient | None:
        statement = (
            select(MedicationActiveIngredient)
            .where(
                MedicationActiveIngredient.medication_id == medication_id, 
                MedicationActiveIngredient.active_ingredients_id == active_ingredients_id
            )
        )
        result = db.execute(statement)
        medication_active_ingredient = result.scalar_one_or_none()

        return medication_active_ingredient
    
    
    def get_medication_active_ingredients(
        self,
        db: Session,
    ) -> list[MedicationActiveIngredient]:
        
        statement = select(MedicationActiveIngredient)
        result = db.execute(statement)
        medication_active_ingredients = result.scalars().all()
        
        
        return medication_active_ingredients


    def update(self, db: Session, medication_active_ingredient: MedicationActiveIngredient) -> MedicationActiveIngredient:
        try:
            db.commit()
            db.refresh(medication_active_ingredient)

            return medication_active_ingredient
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, medication_active_ingredient: MedicationActiveIngredient) -> bool:
        try:
            db.delete(medication_active_ingredient)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise

