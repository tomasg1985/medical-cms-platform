from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medication_active_ingredient_schema import MadicationActiveIngredientCreate, MedicationActiveIngredientUpdate, MedicationActiveIngredientResponse
from app.services.medication_active_ingredient_service import create_medication_active_ingredient, get_medication_active_ingredient, get_medication_active_ingredients, update_medication_active_ingredient, delete_medication_active_ingredient
from app.core.exceptions import ActiveIngredientNotFoundException, MedicationActiveIngredientAlreadyExistsException, MedicationActiveIngredientNotFoundException, MedicationNotFoundException

router = APIRouter(
    prefix="/medication_active_ingredients",
    tags=["Medication Active Ingredients"]
)


@router.post("/", response_model=MedicationActiveIngredientResponse)
def create_medication_active_ingredient_endpoint(
    medication_active_ingredient_data: MadicationActiveIngredientCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_medication_active_ingredient(
            db=db,
            medication_active_ingredient_data=medication_active_ingredient_data
        )
    except MedicationNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró la medicación indicada."
        )
    except ActiveIngredientNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró el ingrediente activo indicado."
        )
    except MedicationActiveIngredientAlreadyExistsException:
        raise HTTPException(
            status_code=409, 
            detail="Este ingrediente activo ya está asociado a la medicación indicada."
        )


@router.get("/", response_model=list[MedicationActiveIngredientResponse])
def get_medication_active_ingredient_endpoint(
    db: Session = Depends(get_db)
):
    return get_medication_active_ingredients(db=db)


@router.get(
    "/{medication_id}/{active_ingredients_id}",
    response_model=MedicationActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def get_medication_active_ingredient_endpoint(
    medication_id: int,
    active_ingredients_id: int,
    db: Session = Depends(get_db)
):
    try:
        medication_active_ingredient = get_medication_active_ingredient(
            db=db,
            medication_id=medication_id,
            active_ingredients_id=active_ingredients_id,
        )
        
        return medication_active_ingredient
    except MedicationActiveIngredientNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró la asociación entre la medicación y el ingrediente activo solicitados."
        )


@router.put(
    "/{medication_id}/{active_ingredients_id}",
    response_model=MedicationActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def update_medication_active_ingredient_endpoint(
    medication_id: int,
    active_ingredients_id: int,
    medication_active_ingredient_data: MedicationActiveIngredientUpdate,
    db: Session = Depends(get_db)
):
    try:
        medication_active_ingredient = update_medication_active_ingredient(
            db=db,
            medication_id=medication_id,
            active_ingredients_id=active_ingredients_id,
            medication_active_ingredient_data=medication_active_ingredient_data
        )
        
        return medication_active_ingredient
    except MedicationActiveIngredientNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró la asociación que desea actualizar."
        )
    except MedicationNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró la nueva medicación indicada."
        )
    except ActiveIngredientNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró el nuevo ingrediente activo indicado."
        )
    except MedicationActiveIngredientAlreadyExistsException:
        raise HTTPException(
            status_code=409, 
            detail="La asociación solicitada ya existe para esa medicación y ese ingrediente activo."
        )


@router.patch(
    "/{medication_id}/{active_ingredients_id}",
    response_model=MedicationActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def patch_medication_active_ingredient_endpoint(
    medication_id: int,
    active_ingredients_id: int,
    medication_active_ingredient_data: MedicationActiveIngredientUpdate,
    db: Session = Depends(get_db)
):
    medication_active_ingredient = update_medication_active_ingredient_endpoint(
        medication_id=medication_id,
        active_ingredients_id=active_ingredients_id,
        medication_active_ingredient_data=medication_active_ingredient_data,
        db=db,
    )
    
    return medication_active_ingredient


@router.delete(
    "/{medication_id}/{active_ingredients_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo para la medicación buscada"
        }
    },
)
def delete_medication_active_ingredient_endpoint(
    medication_id: int,
    active_ingredients_id: int,
    db: Session = Depends(get_db)
):
    try:
        delete_medication_active_ingredient(
            db=db,
            medication_id=medication_id,
            active_ingredients_id=active_ingredients_id,
        )
    except MedicationActiveIngredientNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró la asociación que desea eliminar."
        )