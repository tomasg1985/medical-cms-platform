from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.active_ingredient_schema import ActiveIngredientCreate, ActiveIngredientPatch, ActiveIngredientResponse, ActiveIngredientUpdate
from app.services.active_ingredient_service import create_active_ingredient, get_active_ingredients, get_active_ingredient, update_active_ingredient, delete_active_ingredient


router = APIRouter(
    prefix="/active_ingredients",
    tags=["Active Ingredients"]
)

@router.post("/", response_model=ActiveIngredientResponse)
def create_active_ingredient_endpoint(
    active_ingredient_data: ActiveIngredientCreate,
    db: Session = Depends(get_db)
):
    return create_active_ingredient(
        db=db,
        active_ingredient_data=active_ingredient_data
    )


@router.get("/", response_model=list[ActiveIngredientResponse])
def get_active_ingredients_endpoint(
    db: Session = Depends(get_db)
):
    return get_active_ingredients(db)



@router.get(
    "/{active_ingredient_id}",
    response_model=ActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo"
        }
    },
)
def get_active_ingredient_endpoint(
    active_ingredient_id: int,
    db: Session = Depends(get_db),
):
    active_ingredient = get_active_ingredient(
        db=db,
        active_ingredient_id=active_ingredient_id
    )
    
    if active_ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo"
        )
    
    return active_ingredient


@router.put(
    "/{active_ingredient_id}",
    response_model=ActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo"
        }
    },
)
def update_active_ingredient_endpoint(
    active_ingredient_id: int,
    active_ingredient_data: ActiveIngredientUpdate,
    db: Session = Depends(get_db)
):
    active_ingredient = update_active_ingredient(
        db=db,
        active_ingredient_id=active_ingredient_id,
        active_ingredient_data=active_ingredient_data
    )

    if active_ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo"
        )

    return active_ingredient


@router.patch(
    "/{active_ingredient_id}",
    response_model=ActiveIngredientResponse,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo"
        }
    },
)
def patch_active_ingredient_endpoint(
    active_ingredient_id: int,
    active_ingredient_data: ActiveIngredientPatch,
    db: Session = Depends(get_db)
):
    active_ingredient = update_active_ingredient(
        db=db,
        active_ingredient_id=active_ingredient_id,
        active_ingredient_data=active_ingredient_data
    )

    if active_ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo"
        )

    return active_ingredient

@router.delete(
    "/{active_ingredient_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún ingrediente activo"
        }
    },
)
def delete_active_ingredient_endpoint(
    active_ingredient_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_active_ingredient(
        db=db,
        active_ingredient_id=active_ingredient_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún ingrediente activo"
        )