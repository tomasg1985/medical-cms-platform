from sqlalchemy.orm import Session

from app.models.medication_active_ingredient_model import MedicationActiveIngredient

from app.repositories.medication_active_ingredient_repository import MedicationActiveIngredientRepository
from app.repositories.medication_repository import MedicationRepository
from app.repositories.active_ingredient_repository import ActiveIngredientRepository

medication_active_ingredient_repository = MedicationActiveIngredientRepository()
medication_repository = MedicationRepository()
active_ingredient_repository = ActiveIngredientRepository()

def create_medication_active_ingredient(
    db: Session,
    medication_id: int,
    active_ingredients_id: int
) -> MedicationActiveIngredient | None:

    medication = medication_repository.get_by_id(
        db=db,
        medication_id=medication_id
    )

    if medication is None:
        return None

    active_ingredient = active_ingredient_repository.get_by_id(
        db=db,
        active_ingredient_id=active_ingredients_id
    )

    if active_ingredient is None:
        return None


    existing = medication_active_ingredient_repository.get_by_medication_active_ingredient(
        db=db,
        medication_id=medication_id,
        active_ingredients_id=active_ingredients_id
    )

    if existing is not None:
        return None


    medication_active_ingredient = MedicationActiveIngredient(
        medication_id=medication_id,
        active_ingredients_id=active_ingredients_id
    )

    medication_active_ingredient = medication_active_ingredient_repository.create(
        db=db,
        medication_active_ingredient=medication_active_ingredient
    )

    return medication_active_ingredient


def get_medication_active_ingredients(
    db: Session
) -> list[MedicationActiveIngredient]:
    
    medication_active_ingredients = medication_active_ingredient_repository.get_medication_active_ingredients(
        db=db
    )
    
    return medication_active_ingredients


def get_medication_active_ingredient(
    db: Session,
    medication_active_ingredient_id: int
) -> MedicationActiveIngredient | None:

    medication_active_ingredient = medication_active_ingredient_repository.get_by_id(
        db=db,
        medication_active_ingredient_id=medication_active_ingredient_id
    )

    return medication_active_ingredient


def update_medication_active_ingredient(
    db: Session,
    medication_active_ingredient_id: int
) -> MedicationActiveIngredient | None:

    medication_active_ingredient = medication_active_ingredient_repository.get_by_id(
        db=db,
        medication_active_ingredient_id=medication_active_ingredient_id
    )

    return medication_active_ingredient


def delete_medication_active_ingredient(db: Session, medication_active_ingredient_id: int) -> bool:

    medication_active_ingredient = get_medication_active_ingredient(
        db=db,
        medication_active_ingredient_id=medication_active_ingredient_id
    )

    if medication_active_ingredient is None:
        return False

    return medication_active_ingredient_repository.delete(
        db=db,
        medication_active_ingredient=medication_active_ingredient
    )