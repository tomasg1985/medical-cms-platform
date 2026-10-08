from sqlalchemy.orm import Session

from app.models.patient_contacts_model import PatientContact
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient_contact_schema import PatientContactCreate, PatientContactUpdate

from app.repositories.patient_contact_repository import PatientContactRepository

patient_contact_repository = PatientContactRepository()
patient_repository = PatientRepository()

def create_patient_contact(
    db: Session,
    patient_contact_data: PatientContactCreate
) -> PatientContact | None:

    patient = patient_repository.get_by_id(
        db=db,
        patient_id=patient_contact_data.patient_id
    )
    if patient is None:
        return None
    
    patient_contact = PatientContact(
        **patient_contact_data.model_dump()
    )
    
    patient_contact = patient_contact_repository.create(
        db=db,
        patient_contact=patient_contact
    )
    
    return patient_contact


def get_patient_contacts(
    db: Session
) -> list[PatientContact]:
    
    patient_contacts = patient_contact_repository.get_patient_contacts(
        db=db
    )
    
    return patient_contacts


def get_patient_contact(
    db: Session,
    patient_contact_id: int
) -> PatientContact | None:
    
    patient_contact = patient_contact_repository.get_by_id(
        db=db,
        patient_contacts_id=patient_contact_id
    )
    
    return patient_contact


def update_patient_contact(
    db: Session,
    patient_contact_id: int,
    patient_contact_data: PatientContactUpdate
) -> PatientContact | None:
    
    patient_contact = get_patient_contact(
        db=db,
        patient_contact_id=patient_contact_id
    )
    
    if patient_contact is None:
        return None
    
    for field, value in patient_contact_data.model_dump(exclude_unset=True).items():
        setattr(patient_contact, field, value)
    
    
    patient_contact = patient_contact_repository.update(
        db=db,
        patient_contact=patient_contact
    )
    
    return patient_contact


def delete_patient_contacts(
    db: Session,
    patient_contact_id: int
) -> bool:
    
    patient_contact = get_patient_contact(
        db=db,
        patient_contact_id=patient_contact_id
    )
    
    if patient_contact is None:
        return False
    
    return patient_contact_repository.delete(
        db=db,
        patient_contact=patient_contact
    )