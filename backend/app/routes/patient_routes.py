from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.patient_schema import PatientCreate, PatientResponse, PatientUpdate
from app.services.patient_service import create_patient, get_patient, get_patients, update_patient, delete_patient


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.post("/", response_model=PatientResponse)
def create_patient_endpoint(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
):
    patient = create_patient(
        db=db,
        patient_data=patient_data,
    )

    return patient


@router.get("/", response_model=list[PatientResponse])
def get_patients_endpoint(
    db: Session = Depends(get_db),
):
    patients = get_patients(db)

    return patients


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    responses={
        404: {
            "description": "No se encontró ningún paciente",
        }
    },
)
def get_patient_endpoint(
    patient_id: int,
    db: Session = Depends(get_db),
):
    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún paciente",
        )

    return patient


@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    responses={
        404: {
            "description": "No se encontró ningún paciente",
        }
    },
)
def update_patient_endpoint(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
):
    patient = update_patient(
        db=db,
        patient_id=patient_id,
        patient_data=patient_data,
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún paciente",
        )

    return patient


@router.delete(
    "/{patient_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún paciente",
        }
    },
)
def delete_patient_endpoint(
    patient_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_patient(
        db=db,
        patient_id=patient_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún paciente",
        )