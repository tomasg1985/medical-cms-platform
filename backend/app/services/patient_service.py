from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient_model import Patient
from app.schemas.patient_schema import PatientCreate, PatientUpdate

def create_patient(
    db: Session, 
    patient_data: PatientCreate
) -> Patient:
    
    patient = Patient(
        name=patient_data.name,
        last_name=patient_data.last_name,
        age=patient_data.age,
        dni=patient_data.dni,
        email=patient_data.email,
        phone=patient_data.phone,
        address=patient_data.address,
        insurance=patient_data.insurance
    )

    try:
        db.add(patient)
        db.commit()
        db.refresh(patient)

        return patient

    except Exception:
        db.rollback()
        raise


def get_patients(db: Session) -> list[Patient]:
    statement = select(Patient)
    result = db.execute(statement)
    patients = result.scalars().all()

    return patients


def get_patient(db: Session, patient_id: int) -> Patient | None:
    statement = select(Patient).where(Patient.id == patient_id)
    result = db.execute(statement)
    patient = result.scalar_one_or_none()

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

    try:
        db.commit()
        db.refresh(patient)

        return patient

    except Exception:
        db.rollback()
        raise

def delete_patient(db: Session, patient_id: int) -> bool:

    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        return False

    try:
        db.delete(patient)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise