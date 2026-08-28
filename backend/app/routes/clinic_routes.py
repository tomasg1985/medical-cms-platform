from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.clinic_schema import ClinicCreate, ClinicResponse, ClinicUpdate
from app.services.clinic_service import create_clinic, get_clinic, get_clinics, update_clinic, delete_clinic
from app.services.patient_service import get_patients


router = APIRouter(
    prefix="/clinics",
    tags=["Clinics"],
)


@router.post("/", response_model=ClinicResponse)
def create_clinic_endpoint(
    clinic_data: ClinicCreate,
    db: Session = Depends(get_db),
):
    clinic = create_clinic(
        db=db,
        name=clinic_data.name,
    )

    return clinic


@router.get("/", response_model=list[ClinicResponse])
def get_clinics_endpoint(
    db: Session = Depends(get_db),
):
    clinics = get_clinics(db)

    return clinics


@router.get(
    "/{clinic_id}",
    response_model=ClinicResponse,
    responses={
        404: {
            "description": "No se encontró la clínica solicitada",
        }
    },
)
def get_clinic_endpoint(
    clinic_id: int,
    db: Session = Depends(get_db),
):
    clinic = get_clinic(
        db=db,
        clinic_id=clinic_id,
    )

    if clinic is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la clínica solicitada",
        )

    return clinic


@router.get(
    "/{clinic_id}/patients",
)
def get_clinic_patients_endpoint(
    clinic_id: int,
    db: Session = Depends(get_db),
):
    patients = get_patients(
        db=db,
        clinic_id=clinic_id,
    )

    return patients


@router.put(
    "/{clinic_id}",
    response_model=ClinicResponse,
    responses={
        404: {
            "description": "No se encontró la clínica solicitada",
        }
    },
)
def update_clinic_endpoint(
    clinic_id: int,
    clinic_data: ClinicUpdate,
    db: Session = Depends(get_db),
):
    clinic = update_clinic(
        db=db,
        clinic_id=clinic_id,
        name=clinic_data.name,
    )

    if clinic is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la clínica solicitada",
        )

    return clinic


@router.delete(
    "/{clinic_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró la clínica solicitada",
        }
    },
)
def delete_clinic_endpoint(
    clinic_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_clinic(
        db=db,
        clinic_id=clinic_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la clínica solicitada",
        )