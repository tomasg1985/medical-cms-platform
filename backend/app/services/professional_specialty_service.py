from sqlalchemy.orm import Session

from app.models.medical_specialty_model import ProfessionalSpecialty

from app.repositories.professional_specialty_repository import ProfessionalSpecialtyRepository
from app.repositories.professional_repository import ProfessionalRepository
from app.repositories.specialty_repository import SpecialtyRepository

from app.core.exceptions import ProfessionalNotFoundError
from app.core.exceptions import SpecialtyNotFoundError
from app.core.exceptions import ProfessionalSpecialtyAlreadyAssociatedError


professional_specialty_repository = ProfessionalSpecialtyRepository()
professional_repository = ProfessionalRepository()
specialty_repository = SpecialtyRepository()

def create_professional_specialty( db: Session, professional_id: int, specialty_id: int) -> ProfessionalSpecialty:
    
    professional = professional_repository.get_by_id(
        db=db,
        professional_id=professional_id
    )
    
    if professional is None:
        raise ProfessionalNotFoundError
    
    specialty = specialty_repository.get_by_id(
        db=db,
        specialty_id=specialty_id
    )
    
    if specialty is None:
        raise SpecialtyNotFoundError
    
    
    existing = professional_specialty_repository.get_by_professional_and_specialty(
        db=db,
        professional_id=professional_id,
        specialty_id=specialty_id
    )
    
    if existing is not None:
        raise ProfessionalSpecialtyAlreadyAssociatedError
    
    professional_specialty = ProfessionalSpecialty(
        professional_id=professional_id,
        specialty_id=specialty_id
    )
    
    professional_specialty = professional_specialty_repository.create_professional_specialty(
        db=db,
        professional_specialty=professional_specialty
    )
    
    return professional_specialty