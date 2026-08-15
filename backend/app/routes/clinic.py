from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.clinic import ClinicCreate, ClinicResponse
from app.services.clinic_service import create_clinic


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
