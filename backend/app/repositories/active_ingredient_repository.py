from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.active_ingredient_model import ActiveIngredient


class ActiveIngredientRepository:
    def get_by_id(self, db: Session, active_ingredient_id: int) -> ActiveIngredient | None:
        statement = (
            select(ActiveIngredient)
            .where(ActiveIngredient.id == active_ingredient_id)
        )
        result = db.execute(statement)
        active_ingredient = result.scalar_one_or_none()

        return active_ingredient


    def get_active_ingredients(self, db: Session) -> list[ActiveIngredient]:
        statement = select(ActiveIngredient)
        result = db.execute(statement)
        active_ingredients = result.scalars().all()

        return active_ingredients


    def create(self, db: Session, active_ingredient: ActiveIngredient) -> ActiveIngredient:
        try:
            db.add(active_ingredient)
            db.commit()
            db.refresh(active_ingredient)

            return active_ingredient
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, active_ingredient: ActiveIngredient) -> ActiveIngredient:
        try:
            db.commit()
            db.refresh(active_ingredient)

            return active_ingredient
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, active_ingredient: ActiveIngredient) -> bool:
        try:
            db.delete(active_ingredient)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise