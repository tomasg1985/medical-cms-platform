from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.professional_schema import ProfessionalCreate, ProfessionalResponse, ProfessionalUpdate
from app.services.professional_service import create_professional, get_professional, get_professionals, update_professional, delete_professional, add_clinic_to_professional

from app.core.exceptions import ProfessionalNotFoundError, ClinicNotFoundError, ProfessionalAlreadyAssociatedError

router = APIRouter(
    prefix="/professionals",
    tags=["Professionals"],
)

@router.post("/", response_model=ProfessionalResponse)
def create_professional_endpoint(
    professional_data: ProfessionalCreate,
    db: Session = Depends(get_db),
):

    professional = create_professional(
        db=db,
        professional_data=professional_data,
    )

    return professional


@router.post("/{professional_id}/clinics/{clinic_id}")
def add_clinic_to_professional_endpoint(
    professional_id: int,
    clinic_id: int,
    db: Session = Depends(get_db)
):
    try:
        professional = add_clinic_to_professional(
            db=db,
            professional_id=professional_id,
            clinic_id = clinic_id
        )

        return professional

    except ProfessionalNotFoundError:
        raise HTTPException(
        status_code=404,
        detail="No se encontró el profesional médico solicitado",
    )

    except ClinicNotFoundError:
        raise HTTPException(
        status_code=404,
        detail="No se encontró la clínica solicitada",
    )

    except ProfessionalAlreadyAssociatedError:
        raise HTTPException(
        status_code=409,
        detail="El profesional ya está asociado a la clínica solicitada",
    )


@router.get("/", response_model=list[ProfessionalResponse])
def get_professionals_endpoint(
    db: Session = Depends(get_db),
):
    professionals = get_professionals(db)
    
    return professionals


@router.get(
    "/{professional_id}",
    response_model=ProfessionalResponse,
    responses={
        404: {
            "description": "No se encontró ningún profesional",
        }
    },
)
def get_professional_endpoint(
    professional_id: int,
    db: Session = Depends(get_db),
):
    professional = get_professional(
        db=db,
        professional_id=professional_id,
    )

    if professional is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún profesional",
        )

    return professional


@router.put(
    "/{professional_id}",
    response_model=ProfessionalResponse,
    responses={
        404: {
            "description": "No se encontró ningún profesional",
        }
    },
)
def update_professional_endpoint(
    professional_id: int,
    professional_data: ProfessionalUpdate,
    db: Session = Depends(get_db),
):
    professional = update_professional(
        db=db,
        professional_id=professional_id,
        professional_data=professional_data,
    )

    if professional is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún profesional",
        )

    return professional


@router.delete(
    "/{professional_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún profesional",
        }
    },
)
def delete_professional_endpoint(
    professional_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_professional(
        db=db,
        professional_id=professional_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún profesional",
        )