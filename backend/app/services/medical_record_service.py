from sqlalchemy.orm import Session

from app.models.medical_record_model import MedicalRecord

from app.repositories.medical_record_repository import MedicalRecordRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.clinic_repository import ClinicRepository
from app.schemas.medical_record_schema import MedicalRecordCreate

medical_record_repository = MedicalRecordRepository()
patient_repository = PatientRepository()
clinic_repository = ClinicRepository()

def create_medical_record(
    db: Session,
    medical_record_data: MedicalRecordCreate
) -> MedicalRecord | None:

    patient_id = medical_record_data.patient_id
    clinic_id = medical_record_data.clinic_id
    
    patient = patient_repository.get_by_id(
        db=db,
        patient_id=patient_id
    )
    
    if patient is None:
        return None
    
    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id
    )
    
    if clinic is None:
        return None
    
    existing = medical_record_repository.get_patient_clinic(
        db=db,
        patient_id=patient_id,
        clinic_id=clinic_id
    )
    
    if existing is not None:
        return None
    
    medical_record = MedicalRecord(
        patient_id=patient_id,
        clinic_id=clinic_id
    )
    
    medical_record = medical_record_repository.create(
        db=db,
        medical_record=medical_record
    )
    
    return medical_record


def get_medical_records(
    db: Session
) -> list[MedicalRecord]:
    
    medical_records = medical_record_repository.get_medical_records(
        db=db
    )
    
    return medical_records


def get_medical_record(
    db: Session,
    medical_record_id: int
) -> MedicalRecord | None:
    
    medical_record = medical_record_repository.get_by_id(
        db=db,
        medical_record_id=medical_record_id
    )
    
    return medical_record


def update_medical_record(
    db: Session,
    medical_record_id: int
) -> MedicalRecord | None:
    
    medical_record = medical_record_repository.get_by_id(
        db=db,
        medical_record_id=medical_record_id
    )
    
    return medical_record