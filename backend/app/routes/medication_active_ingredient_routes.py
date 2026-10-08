from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medication_active_ingredient_schema import MadicationActiveIngredientCreate, MedicationActiveIngredientUpdate, MedicationActiveIngredientResponse
from app.services.medication_active_ingredient_service import create_medication_active_ingredient, get_medication_active_ingredient, get_medication_active_ingredients, update_medication_active_ingredient, delete_medication_active_ingredient

router = APIRouter(
    prefix="/medication_active_ingredients",
    tags=["Medication Active Ingredients"]
)

@router.post("/", response_model=MedicationActiveIngredientResponse)
def create_medication_active_ingredient_endpoint(
    medication_active_ingredient_data: MadicationActiveIngredientCreate,
    db: Session = Depends(get_db)
):
    return create_medication_active_ingredient(
        db=db,
        medication_active_ingredient_data=medication_active_ingredient_data
    )


@router.get("/", response_model=list[MedicationActiveIngredientResponse])
def get_medication_active_ingredient_endpoint(
    db: Session = Depends(get_db)
):
    return get_medication_active_ingredients(db=db)


@router.get(
    "/{medication_active_ingredient_id}",
    response_model=MedicationActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def get_medication_active_ingredient_endpoint(
    medication_active_ingredient_id: int,
    db: Session = Depends(get_db)
):
    medication_active_ingredient = get_medication_active_ingredient(
        db=db,
        medication_active_ingredient_id=medication_active_ingredient_id
    )
    
    if medication_active_ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo para la medicación buscada"
        )
    
    return medication_active_ingredient


@router.put(
    "/{medication_active_ingredient_id}",
    response_model=MedicationActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def update_medication_active_ingredient_endpoint(
    medication_active_ingredient_id: int,
    medication_active_ingredient_data: MedicationActiveIngredientUpdate,
    db: Session = Depends(get_db)
):
    medication_active_ingredient = update_medication_active_ingredient(
        db=db,
        medication_active_ingredient_id=medication_active_ingredient_id,
        medication_active_ingredient_data=medication_active_ingredient_data
    )

    if medication_active_ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo para la medicación buscada"
        )

    return medication_active_ingredient


@router.patch(
    "/{medication_active_ingredient_id}",
    response_model=MedicationActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def patch_medication_active_ingredient_endpoint(
    medication_active_ingredient_id: int,
    medication_active_ingredient_data: MedicationActiveIngredientUpdate,
    db: Session = Depends(get_db)
):
    medication_active_ingredient = update_medication_active_ingredient(
        db=db,
        medication_active_ingredient_id=medication_active_ingredient_id,
        medication_active_ingredient_data=medication_active_ingredient_data
    )

    if medication_active_ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo para la medicación buscada"
        )

    return medication_active_ingredient


@router.delete(
    "/{medication_active_ingredient_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def delete_medication_active_ingredient_endpoint(
    medication_active_ingredient_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_medication_active_ingredient(
        db=db,
        medication_active_ingredient_id=medication_active_ingredient_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo para la medicación buscada"
        )