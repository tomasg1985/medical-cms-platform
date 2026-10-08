from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.prescription_schema import PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate
from app.services.prescription_service import create_prescription, get_prescription, update_prescription, delete_prescription

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)

@router.post("/", response_model=PrescriptionResponse)
def create_prescription_endpoint(
    prescription_data: PrescriptionResponse,
    db: Session = Depends(get_db)
):
    return create_prescription(
        db=db,
        prescription_data=prescription_data
    )
    

@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
    responses={
        404: {
            "description": "No se encontró ninguna receta médica asociada a su busqueda."
        }
    },
)
def get_prescription_endpoint(
    prescription_id: int,
    db: Session = Depends(get_db)
):
    prescription = get_prescription(
        db=db,
        prescription_id=prescription_id
    )
    
    if prescription is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna receta médica asociada a su busqueda."
        )
    
    return prescription


@router.put(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
    responses={
        404: {
            "description": "No se encontró ninguna receta médica asociada a su busqueda."
        }
    },
)
def update_prescription_endpoint(
    prescription_id: int,
    prescription_data: PrescriptionUpdate,
    db: Session = Depends(get_db)
):
    prescription = update_prescription(
        db=db,
        prescription_id=prescription_id,
        prescription_data=prescription_data
    )
    
    if prescription is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna receta médica asociada a su busqueda."
        )
    
    return prescription


@router.delete(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
    responses={
        404: {
            "description": "No se encontró ninguna receta médica asociada a su busqueda."
        }
    },
)
def delete_prescription_endpoint(
    prescription_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_prescription(
        db=db,
        prescription_id=prescription_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna receta médica asociada a su busqueda."
        )