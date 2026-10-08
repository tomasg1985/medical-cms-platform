from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medication_schema import MedicationCreate, MedicationResponse, MedicationUpdate
from app.services.medication_service import create_medication, get_medication, get_medications, update_medication, delete_medication

router = APIRouter(
    prefix="/medications",
    tags=["Medications"]
)

@router.post(
    "/",
    response_model=MedicationResponse
)
def create_medication_endpoint(
    medication_data: MedicationCreate,
    db: Session = Depends(get_db)
):
    return create_medication(
        db=db,
        medication_data=medication_data
    )


@router.get("/", response_model=list[MedicationResponse])
def get_medications_endpoint(
    db: Session = Depends(get_db)
):
    return get_medications(db=db)


@router.get(
    "/{medication_id}",
    response_model=MedicationResponse,
    responses={
        404: {
            "description": "No se encontró ninguna medicación asociada a su busqueda."
        }
    },
)
def get_medication_endpoint(
    medication_id: int,
    db: Session = Depends(get_db)
):
    medication = get_medication(
        db=db,
        medication_id=medication_id
    )
    
    if medication is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna medicación asociada a su busqueda."
        )
        
    return medication


@router.put(
    "/{medication_id}",
    response_model= MedicationResponse,
    responses={
        404: {
            "description": "No se encontró ninguna medicación asociada a su busqueda."
        }
    },
)
def update_medication_endpoint(
    medication_id: int,
    medication_data: MedicationUpdate,
    db: Session = Depends(get_db)
):
    medication = update_medication(
        db=db,
        medication_id=medication_id,
        medication_data=medication_data
    )
    
    if medication is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna medicación asociada a su busqueda."
        )
    
    return medication


@router.delete(
    "/{medication_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ninguna medicación asociada a su busqueda."
        }
    },
)
def delete_medication_endpoint(
    medication_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_medication(
        db=db,
        medication_id=medication_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna presentacion médica asociada a su busqueda."
        )

