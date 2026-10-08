from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ClinicNotFoundError,
    MedicalRecordAlreadyExistsException,
    MedicalRecordNotFoundException,
    PatientNotFoundError,
)
from app.database import get_db
from app.schemas.medical_record_schema import MedicalRecordCreate, MedicalRecordResponse, MedicalRecordUpdate
from app.services.medical_record_service import create_medical_record, get_medical_record, get_medical_records, update_medical_record

router = APIRouter(
    prefix="/medical_records",
    tags=["Medical Records"],
)


@router.post(
    "/",
    response_model=MedicalRecordResponse,
    responses={
        404: {"description": "No se encontró el paciente o la clínica indicados."},
        409: {"description": "El paciente ya tiene un registro médico en esta clínica."},
    },
)
def create_medical_record_endpoint(
    medical_record_data: MedicalRecordCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_medical_record(
            db=db,
            medical_record_data=medical_record_data,
        )
    except PatientNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el paciente indicado para crear el registro médico.",
        )
    except ClinicNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la clínica indicada para crear el registro médico.",
        )
    except MedicalRecordAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="El paciente ya tiene un registro médico asociado a esta clínica.",
        )
        
        

@router.get("/", response_model=list[MedicalRecordResponse])
def get_medical_records_endpoint(db: Session = Depends(get_db)):
    return get_medical_records(db=db)



@router.get(
    "/{medical_record_id}",
    response_model=MedicalRecordResponse,
    responses={404: {"description": "No se encontró el registro médico solicitado."}},
)
def get_medical_record_endpoint(
    medical_record_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_medical_record(
            db=db,
            medical_record_id=medical_record_id,
        )
    except MedicalRecordNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el registro médico solicitado.",
        )



@router.put(
    "/{medical_record_id}",
    response_model=MedicalRecordResponse,
    responses={
        404: {"description": "No se encontró el registro, paciente o clínica indicados."},
        409: {"description": "Ya existe un registro para el paciente y la clínica indicados."},
    },
)
def update_medical_record_endpoint(
    medical_record_id: int,
    medical_record_data: MedicalRecordUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_medical_record(
            db=db,
            medical_record_id=medical_record_id,
            medical_record_data=medical_record_data,
        )
    except MedicalRecordNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el registro médico que desea actualizar.",
        )
    except PatientNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el nuevo paciente indicado.",
        )
    except ClinicNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la nueva clínica indicada.",
        )
    except MedicalRecordAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="El paciente ya tiene otro registro médico asociado a esta clínica.",
        )



@router.patch(
    "/{medical_record_id}",
    response_model=MedicalRecordResponse,
    responses={
        404: {"description": "No se encontró el registro, paciente o clínica indicados."},
        409: {"description": "Ya existe un registro para el paciente y la clínica indicados."},
    },
)
def patch_medical_record_endpoint(
    medical_record_id: int,
    medical_record_data: MedicalRecordUpdate,
    db: Session = Depends(get_db),
):
    return update_medical_record_endpoint(
        medical_record_id=medical_record_id,
        medical_record_data=medical_record_data,
        db=db,
    )
