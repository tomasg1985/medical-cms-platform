from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.professional_specialty_schema import ProfessionalSpecialtyCreate, ProfessionalSpecialtyResponse
from app.services.professional_specialty_service import create_professional_specialty

from app.core.exceptions import ProfessionalNotFoundError
from app.core.exceptions import SpecialtyNotFoundError
from app.core.exceptions import ProfessionalSpecialtyAlreadyAssociatedError

router = APIRouter(
    prefix="/professional-specialties",
    tags=["Professional Specialty"]
)

@router.post(
    "/",
    response_model=ProfessionalSpecialtyResponse
)
def create_professional_specialty_endpoint(
    professional_specialty_data: ProfessionalSpecialtyCreate,
    db : Session = Depends(get_db),
):

    try:
        professional_specialty = create_professional_specialty(
            db=db,
            professional_id=professional_specialty_data.professional_id,
            specialty_id=professional_specialty_data.specialty_id
        )
        
        return professional_specialty
    except ProfessionalNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="El profesional que busca no se encuentra registrado."
            )
    
    except SpecialtyNotFoundError:
            raise HTTPException(
                status_code=404,
                detail="La especialidad profesional que busca no se encuentra registrada."
                )
    
    except ProfessionalSpecialtyAlreadyAssociatedError:
            raise HTTPException(
                status_code=409,
                detail="La especialidad que busca ya se encuentra asociada a un profesional."
                )