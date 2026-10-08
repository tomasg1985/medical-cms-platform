from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medication_presentation_schema import MedicationPresentationCreate, MedicationPresentationResponse, MedicationPresentationUpdate
from app.services.medication_presentation_service import create_medication_presentation, get_medication_presentation, get_medication_presentations, update_medication_presentation, delete_medication_presentation


router = APIRouter(
    prefix="/medication_presentations",
    tags=["Medication Presentations"]
)

@router.post("/", response_model=MedicationPresentationResponse)
def create_medical_presentation_endpoint(
    medication_presentation_data: MedicationPresentationCreate,
    db: Session = Depends(get_db)
):
    return create_medication_presentation(
        db=db,
        medication_presentation_data=medication_presentation_data
    )


@router.get("/", response_model=list[MedicationPresentationResponse])
def get_medication_presentations_endpoint(
    db: Session = Depends(get_db)
):
    return get_medication_presentations(db=db)


@router.get(
    "/{medication_presentation_id}",
    response_model=MedicationPresentationResponse,
    responses={
        404: {
            "description": "No se encontró ninguna presentacion médica asociada a su busqueda."
        }
    },
)
def get_medication_presentation_endpoint(
    medication_presentation_id: int,
    db: Session = Depends(get_db)
):
    medication_presentation = get_medication_presentation(
        db=db,
        medication_presentation_id=medication_presentation_id
    )
    
    if medication_presentation is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna presentacion médica asociada a su busqueda."
        )
        
    return medication_presentation


@router.put(
    "/{medication_presentation_id}",
    response_model=MedicationPresentationResponse,
    responses={
        404: {
            "description": "No se encontró ninguna presentacion médica asociada a su busqueda."
        }
    },
)
def update_medication_presentation_endpoint(
    medication_presentation_id: int,
    medication_presentation_data: MedicationPresentationUpdate,
    db: Session = Depends(get_db)
):
    medication_presentation = update_medication_presentation(
        db=db,
        medication_presentation_id=medication_presentation_id,
        medication_presentation_data=medication_presentation_data
    )
    
    if medication_presentation is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna presentacion médica asociada a su busqueda."
        )
    
    return medication_presentation


@router.patch(
    "/{medication_presentation_id}",
    response_model=MedicationPresentationResponse,
    responses={
        404: {
            "description": "No se encontró ninguna presentacion médica asociada a su busqueda."
        }
    },
)
def patch_medication_presentation_endpoint(
    medication_presentation_id: int,
    medication_presentation_data: MedicationPresentationUpdate,
    db: Session = Depends(get_db)
):
    medication_presentation = update_medication_presentation(
        db=db,
        medication_presentation_id=medication_presentation_id,
        medication_presentation_data=medication_presentation_data
    )
    
    if medication_presentation is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna presentacion médica asociada a su busqueda."
        )
    
    return medication_presentation


@router.delete(
    "/{medication_presentation_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ninguna presentacion médica asociada a su busqueda."
        }
    },
)
def delete_medication_presentation_endpoint(
    medication_presentation_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_medication_presentation(
        db=db,
        medication_presentation_id=medication_presentation_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna presentacion médica asociada a su busqueda."
        )