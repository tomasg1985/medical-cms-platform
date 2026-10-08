from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.prescription_schema import PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate
from app.services.prescription_service import create_prescription, get_prescription, update_prescription, delete_prescription

from app.core.exceptions import PatientNotFoundError, ProfessionalNotFoundError, MedicalRecordNotFoundException, AppointmentNotFoundError

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)

@router.post("/", response_model=PrescriptionResponse)
def create_prescription_endpoint(
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db)
):
    try:
        prescription = create_prescription(
            db=db,
            prescription_data=prescription_data
        )
        
        return prescription
    except PatientNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el paciente asociado a la receta.",
        )
    except ProfessionalNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el profesional asociado a la receta.",
        )
    except MedicalRecordNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la historia clínica asociada a la receta.",
        )
    except AppointmentNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el turno asociado a la receta.",
        )


@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
    responses={
        404: {
            "description": "No se encontró la receta solicitada."
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
            detail="No se encontró la receta solicitada."
        )
    
    return prescription


@router.put(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
    responses={
        404: {
            "description": "No se encontró la receta solicitada."
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
            detail="No se encontró la receta solicitada."
        )
    
    return prescription


@router.delete(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
    responses={
        404: {
            "description": "No se encontró la receta solicitada."
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
            detail="No se encontró la receta solicitada."
        )