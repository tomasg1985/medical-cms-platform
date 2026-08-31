from sqlalchemy.orm import Session

from app.models.patient_model import Patient
from app.schemas.patient_schema import PatientCreate, PatientUpdate
from app.repositories.patient_repository import PatientRepository

patient_repository = PatientRepository()

def create_patient(
    db: Session, 
    patient_data: PatientCreate
) -> Patient:

    patient = Patient(
        name=patient_data.name,
        last_name=patient_data.last_name,
        birth_date=patient_data.birth_date,
        dni=patient_data.dni,
        email=patient_data.email,
        phone=patient_data.phone,
        address=patient_data.address,
        insurance=patient_data.insurance,
    )

    patient = patient_repository.create(
        db=db,
        patient=patient
    )

    return patient


def get_patients(db: Session, clinic_id: int | None = None) -> list[Patient]:

    patients = patient_repository.get_patients(
        db=db, 
        clinic_id=clinic_id
    )

    return patients



def get_patient(db: Session, patient_id: int) -> Patient | None:

    patient = patient_repository.get_by_id(
        db=db,
        patient_id=patient_id
    )

    return patient



def update_patient(db: Session, patient_id: int, patient_data: PatientUpdate) -> Patient | None:

    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        return None

    data= patient_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(patient, field, value)

    patient = patient_repository.update(
        db=db,
        patient=patient
    )

    return patient



def delete_patient(db: Session, patient_id: int) -> bool:

    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        return False

    return patient_repository.delete(
    db=db,
    patient=patient
)