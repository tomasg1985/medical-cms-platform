from sqlalchemy.orm import Session

from app.models.medication_model import Medication

from app.repositories.medication_repository import MedicationRepository
from app.schemas.medication_schema import MedicationUpdate

medication_repository = MedicationRepository()

def create_medication(
    db: Session,
    name: str,
    description: str,
    laboratory: str,
    status: str
) -> Medication | None:
    
    medication = Medication(
        name=name,
        description=description,
        laboratory=laboratory,
        status=status
    )
    
    medication = medication_repository.create(
        db=db,
        medication=medication
    )
    
    return medication


def get_medications(
    db: Session
) -> list[Medication]:
    
    medications = medication_repository.get_medications(
        db=db
    )
    
    return medications


def get_medication(
    db: Session,
    medication_id: int
) -> Medication | None:
    
    medication = medication_repository.get_by_id(
        db=db,
        medication_id=medication_id
    )
    
    return medication


def update_medication(
    db: Session,
    medication_id: int,
    medication_data: MedicationUpdate
) -> Medication | None:
    
    medication = get_medication(
        db=db,
        medication_id=medication_id
    )
    
    if medication is None:
        return None
    
    medication.name = medication_data.name
    medication.description = medication_data.description
    medication.laboratory = medication_data.laboratory
    medication.status = medication_data.status

    medication = medication_repository.update(
        db=db,
        medication=medication
    )
    
    return medication


def delete_medication(
    db: Session,
    medication_id: int
) -> bool:
    
    medication = medication_repository.get_by_id(
        db=db,
        medication_id=medication_id
    )
    
    if medication is None:
        return False
    
    return medication_repository.delete(
        db=db,
        medication=medication
    )