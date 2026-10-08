from sqlalchemy.orm import Session

from app.models.active_ingredient_model import ActiveIngredient

from app.repositories.active_ingredient_repository import ActiveIngredientRepository
from app.schemas.active_ingredient_schema import ActiveIngredientCreate, ActiveIngredientPatch, ActiveIngredientUpdate

active_ingredient_repository = ActiveIngredientRepository()

def create_active_ingredient(
    db: Session,
    active_ingredient_data: ActiveIngredientCreate
) -> ActiveIngredient:

    active_ingredient = ActiveIngredient(
        **active_ingredient_data.model_dump()
    )

    active_ingredient = active_ingredient_repository.create(
        db=db,
        active_ingredient=active_ingredient
    )

    return active_ingredient


def get_active_ingredients(
    db: Session
) -> list[ActiveIngredient]:

    active_ingredients = active_ingredient_repository.get_active_ingredients(
        db=db
    )

    return active_ingredients


def get_active_ingredient(
    db: Session,
    active_ingredient_id: int
) -> ActiveIngredient | None:

    active_ingredient = active_ingredient_repository.get_by_id(
        db=db,
        active_ingredient_id=active_ingredient_id
    )

    return active_ingredient


def update_active_ingredient(
    db: Session,
    active_ingredient_id: int,
    active_ingredient_data: ActiveIngredientUpdate | ActiveIngredientPatch
) -> ActiveIngredient | None:

    active_ingredient = active_ingredient_repository.get_by_id(
        db=db,
        active_ingredient_id=active_ingredient_id
    )

    if active_ingredient is None:
        return None

    for field, value in active_ingredient_data.model_dump(exclude_unset=True).items():
        setattr(active_ingredient, field, value)

    active_ingredient = active_ingredient_repository.update(
        db=db,
        active_ingredient=active_ingredient
    )

    return active_ingredient


def delete_active_ingredient(
    db: Session,
    active_ingredient_id: int
) -> bool:

    active_ingredient = active_ingredient_repository.get_by_id(
        db=db,
        active_ingredient_id=active_ingredient_id
    )

    if active_ingredient is None:
        return False

    return active_ingredient_repository.delete(
        db=db,
        active_ingredient=active_ingredient
    )