from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.clinic import ClinicCreate, ClinicResponse
from app.services.clinic_service import create_clinic, get_clinic, get_clinics


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
