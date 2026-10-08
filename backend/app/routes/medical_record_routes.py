from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medical_record_schema import MedicalRecordCreate, MedicalRecordResponse, MedicalRecordUpdate
from app.services.medical_record_service import create_medical_record, get_medical_record, get_medical_records, update_medical_record


router = APIRouter(
    prefix="/medical_records",
    tags=["Medical Records"]
)

@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record_endpoint(
    medical_record_data: MedicalRecordCreate,
    db: Session = Depends(get_db)
):
    return create_medical_record(
        db=db,
        medical_record_data=medical_record_data
    )


@router.get("/", response_model=list[MedicalRecordResponse])
def get_medical_records_endpoint(
    db: Session = Depends(get_db)
):
    return get_medical_records(db=db)


@router.get(
    "/{medical_record_id}",
    response_model=MedicalRecordResponse,
    responses={
        404: {
            "description": "No se encontró ningún registro médico"
        }
    },
)
def get_medical_record_endpoint(
    medical_record_id: int,
    db: Session = Depends(get_db)
):
    medical_record = get_medical_record(
        db=db,
        medical_record_id=medical_record_id
    )
    
    if medical_record is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún registro médico"
        )
    
    return medical_record


@router.put(
    "/{medical_record_id}",
    response_model=MedicalRecordResponse,
    responses={
        404: {
            "description": "No se encontró ningún registro médico"
        } 
    },
)
def update_medical_record_endpoint(
    medical_record_id: int,
    medical_record_data: MedicalRecordUpdate,
    db: Session = Depends(get_db)
):
    medical_record = update_medical_record(
        db=db,
        medical_record_id=medical_record_id,
        medical_record_data=medical_record_data
    )
    
    if medical_record is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún registro médico"
        )
        
    return medical_record


@router.patch(
    "/{medical_record_id}",
    response_model=MedicalRecordResponse,
    responses={
        404: {
            "description": "No se encontró ningún registro médico"
        } 
    },
)
def patch_medical_record_endpoint(
    medical_record_id: int,
    medical_record_data: MedicalRecordUpdate,
    db: Session = Depends(get_db)
):
    medical_record = update_medical_record(
        db=db,
        medical_record_id=medical_record_id,
        medical_record_data=medical_record_data
    )
    
    if medical_record is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún registro médico"
        )
        
    return medical_record