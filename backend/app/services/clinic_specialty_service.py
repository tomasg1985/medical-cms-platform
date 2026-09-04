from sqlalchemy.orm import Session

from app.models.clinic_specialty_model import ClinicSpecialty

from app.repositories.clinic_specialty_repository import ClinicSpecialtyRepository
from app.repositories.clinic_repository import ClinicRepository
from app.repositories.specialty_repository import SpecialtyRepository

from app.core.exceptions import ClinicNotFoundError
from app.core.exceptions import SpecialtyNotFoundError
from app.core.exceptions import ClinicSpecialtyAlreadyAssociatedError

clinic_specialty_repository = ClinicSpecialtyRepository()
clinic_repository = ClinicRepository()
specialty_repository = SpecialtyRepository()

def create_clinic_specialty(db: Session, clinic_id: int, specialty_id: int) -> ClinicSpecialty:
    
    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id
    )
    
    if clinic is None:
        raise ClinicNotFoundError
    
    specialty = specialty_repository.get_by_id(
        db=db,
        specialty_id=specialty_id
    )
    
    if specialty is None:
        raise SpecialtyNotFoundError
    
    existing = clinic_specialty_repository.get_by_clinic_and_specialty(
        db=db,
        clinic_id=clinic_id,
        specialty_id=specialty_id
    )
    
    if existing is not None:
        raise ClinicSpecialtyAlreadyAssociatedError
    
    clinic_specialty = ClinicSpecialty(
        clinic_id=clinic_id,
        specialty_id=specialty_id
    )
    
    clinic_specialty = clinic_specialty_repository.create_clinic_specialty(
        db=db,
        clinic_specialty=clinic_specialty
    )
    
    return clinic_specialty