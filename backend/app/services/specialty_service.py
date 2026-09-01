from sqlalchemy.orm import Session

from app.models.specialty_model import Specialty
from app.schemas.specialty_schema import SpecialtyCreate, SpecialtyUpdate
from app.repositories.specialty_repository import SpecialtyRepository

specialty_repository = SpecialtyRepository()

def create_specialty(
    db: Session,
    specialty_data: SpecialtyCreate
) -> Specialty:
    
    specialty = Specialty(
        official_name=specialty_data.official_name,
        alternative_name=specialty_data.alternative_name,
        short_description=specialty_data.short_description,
        snomed_code=specialty_data.snomed_code,
        medical_exercise=specialty_data.medical_exercise
    )
    
    specialty = specialty_repository.create(
        db=db,
        specialty=specialty
    )
    
    return specialty


def get_specialties(db: Session) -> list[Specialty]:
    
    specialties = specialty_repository.get_specialties(
        db=db
    )
    
    return specialties


def get_specialty(db: Session, specialty_id: int) -> Specialty | None:
    
    specialty = specialty_repository.get_by_id(
        db=db,
        specialty_id=specialty_id,
    )

    return specialty


def update_specialty(
    db: Session, 
    specialty_id: int, 
    specialty_data: SpecialtyUpdate
) -> Specialty | None:
    
    specialty = get_specialty(
        db=db,
        specialty_id=specialty_id
    )
    
    if specialty is None:
        return None
    
    data = specialty_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(specialty, field, value)
    
    specialty = specialty_repository.update(
        db=db,
        specialty=specialty
    )
    
    return specialty


def delete_specialty(db: Session, specialty_id: int) -> bool:
    specialty = get_specialty(
        db=db,
        specialty_id=specialty_id,
    )
    
    if specialty is None:
        return False
    
    return specialty_repository.delete(
        db=db,
        specialty=specialty
    )