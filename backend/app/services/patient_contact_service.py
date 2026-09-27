from sqlalchemy.orm import Session

from app.models.patient_contacts_model import PatientContact

from app.repositories.patient_contact_repository import PatientContactRepository

patient_contact_repository = PatientContactRepository()

def create_patient_contact(
    db: Session,
    first_name: str,
    last_name: str,
    relationship_type: str,
    phone: str,
    email: str
) -> PatientContact:
    
    patient_contact = PatientContact(
        first_name=first_name,
        last_name=last_name,
        relationship_type=relationship_type,
        phone=phone,
        email=email
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
    first_name: str,
    last_name: str,
    relationship_type: str,
    phone: str,
    email: str
) -> PatientContact | None:
    
    patient_contact = get_patient_contact(
        db=db,
        patient_contact_id=patient_contact_id
    )
    
    if patient_contact is None:
        return None
    
    patient_contact.first_name=first_name
    patient_contact.last_name=last_name
    patient_contact.relationship_type=relationship_type
    patient_contact.phone=phone
    patient_contact.email=email
    
    
    patient_contact = patient_contact_repository.update(
        db=db,
        patient_contact=patient_contact
    )
    
    return patient_contact


def delete_patient_contacts(
    db: Session,
    patient_contacts_id: int
) -> bool:
    
    patient_contact = get_patient_contact(
        db=db,
        patient_contacts_id=patient_contacts_id
    )
    
    if patient_contact is None:
        return False
    
    return patient_contact_repository.delete(
        db=db,
        patient_contact=patient_contact
    )