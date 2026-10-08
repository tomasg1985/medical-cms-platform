from sqlalchemy.orm import Session

from app.models.medication_active_ingredient_model import MedicationActiveIngredient

from app.repositories.medication_active_ingredient_repository import MedicationActiveIngredientRepository
from app.repositories.medication_repository import MedicationRepository
from app.repositories.active_ingredient_repository import ActiveIngredientRepository
from app.schemas.medication_active_ingredient_schema import MadicationActiveIngredientCreate, MedicationActiveIngredientUpdate
from app.core.exceptions import (
    ActiveIngredientNotFoundException,
    MedicationActiveIngredientAlreadyExistsException,
    MedicationActiveIngredientNotFoundException,
    MedicationNotFoundException,
)

medication_active_ingredient_repository = MedicationActiveIngredientRepository()
medication_repository = MedicationRepository()
active_ingredient_repository = ActiveIngredientRepository()

def create_medication_active_ingredient(
    db: Session,
    medication_active_ingredient_data: MadicationActiveIngredientCreate,
) -> MedicationActiveIngredient:
    medication_id = medication_active_ingredient_data.medication_id
    active_ingredients_id = medication_active_ingredient_data.active_ingredients_id

    medication = medication_repository.get_by_id(
        db=db,
        medication_id=medication_id
    )

    if medication is None:
        raise MedicationNotFoundException()

    active_ingredient = active_ingredient_repository.get_by_id(
        db=db,
        active_ingredient_id=active_ingredients_id
    )

    if active_ingredient is None:
        raise ActiveIngredientNotFoundException()


    existing = medication_active_ingredient_repository.get_by_medication_active_ingredient(
        db=db,
        medication_id=medication_id,
        active_ingredients_id=active_ingredients_id
    )

    if existing is not None:
        raise MedicationActiveIngredientAlreadyExistsException()


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
    medication_id: int,
    active_ingredients_id: int,
) -> MedicationActiveIngredient:

    medication_active_ingredient = medication_active_ingredient_repository.get_by_medication_active_ingredient(
        db=db,
        medication_id=medication_id,
        active_ingredients_id=active_ingredients_id,
    )

    if medication_active_ingredient is None:
        raise MedicationActiveIngredientNotFoundException()

    return medication_active_ingredient


def update_medication_active_ingredient(
    db: Session,
    medication_id: int,
    active_ingredients_id: int,
    medication_active_ingredient_data: MedicationActiveIngredientUpdate,
) -> MedicationActiveIngredient:

    medication_active_ingredient = medication_active_ingredient_repository.get_by_medication_active_ingredient(
        db=db,
        medication_id=medication_id,
        active_ingredients_id=active_ingredients_id,
    )

    if medication_active_ingredient is None:
        raise MedicationActiveIngredientNotFoundException()

    medication = medication_repository.get_by_id(
        db=db,
        medication_id=medication_active_ingredient_data.medication_id,
    )
    if medication is None:
        raise MedicationNotFoundException()

    active_ingredient = active_ingredient_repository.get_by_id(
        db=db,
        active_ingredient_id=medication_active_ingredient_data.active_ingredients_id,
    )
    if active_ingredient is None:
        raise ActiveIngredientNotFoundException()

    existing = medication_active_ingredient_repository.get_by_medication_active_ingredient(
        db=db,
        medication_id=medication_active_ingredient_data.medication_id,
        active_ingredients_id=medication_active_ingredient_data.active_ingredients_id,
    )
    if existing is not None and existing != medication_active_ingredient:
        raise MedicationActiveIngredientAlreadyExistsException()

    medication_active_ingredient.medication_id = medication_active_ingredient_data.medication_id
    medication_active_ingredient.active_ingredients_id = medication_active_ingredient_data.active_ingredients_id

    return medication_active_ingredient_repository.update(
        db=db,
        medication_active_ingredient=medication_active_ingredient,
    )


def delete_medication_active_ingredient(
    db: Session,
    medication_id: int,
    active_ingredients_id: int,
) -> bool:

    medication_active_ingredient = get_medication_active_ingredient(
        db=db,
        medication_id=medication_id,
        active_ingredients_id=active_ingredients_id,
    )

    return medication_active_ingredient_repository.delete(
        db=db,
        medication_active_ingredient=medication_active_ingredient
    )