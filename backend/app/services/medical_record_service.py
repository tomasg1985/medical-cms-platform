from sqlalchemy.orm import Session

from app.models.medical_record_model import MedicalRecord
from app.repositories.medical_record_repository import MedicalRecordRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.clinic_repository import ClinicRepository
from app.schemas.medical_record_schema import MedicalRecordCreate, MedicalRecordUpdate
from app.core.exceptions import ClinicNotFoundError, MedicalRecordAlreadyExistsException, MedicalRecordNotFoundException, PatientNotFoundError

medical_record_repository = MedicalRecordRepository()
patient_repository = PatientRepository()
clinic_repository = ClinicRepository()


def create_medical_record(
    db: Session,
    medical_record_data: MedicalRecordCreate,
) -> MedicalRecord:
    patient_id = medical_record_data.patient_id
    clinic_id = medical_record_data.clinic_id

    patient = patient_repository.get_by_id(
        db=db,
        patient_id=patient_id,
    )
    if patient is None:
        raise PatientNotFoundError()

    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id,
    )
    if clinic is None:
        raise ClinicNotFoundError()

    existing = medical_record_repository.get_patient_clinic(
        db=db,
        patient_id=patient_id,
        clinic_id=clinic_id,
    )
    if existing is not None:
        raise MedicalRecordAlreadyExistsException()

    medical_record = MedicalRecord(
        patient_id=patient_id,
        clinic_id=clinic_id,
    )

    return medical_record_repository.create(
        db=db,
        medical_record=medical_record,
    )


def get_medical_records(db: Session) -> list[MedicalRecord]:
    return medical_record_repository.get_medical_records(db=db)


def get_medical_record(db: Session, medical_record_id: int) -> MedicalRecord:
    medical_record = medical_record_repository.get_by_id(
        db=db,
        medical_record_id=medical_record_id,
    )
    if medical_record is None:
        raise MedicalRecordNotFoundException()

    return medical_record


def update_medical_record(
    db: Session,
    medical_record_id: int,
    medical_record_data: MedicalRecordUpdate,
) -> MedicalRecord:
    medical_record = get_medical_record(
        db=db,
        medical_record_id=medical_record_id,
    )

    patient = patient_repository.get_by_id(
        db=db,
        patient_id=medical_record_data.patient_id,
    )
    if patient is None:
        raise PatientNotFoundError()

    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=medical_record_data.clinic_id,
    )
    if clinic is None:
        raise ClinicNotFoundError()

    existing = medical_record_repository.get_patient_clinic(
        db=db,
        patient_id=medical_record_data.patient_id,
        clinic_id=medical_record_data.clinic_id,
    )
    if existing is not None and existing.id != medical_record.id:
        raise MedicalRecordAlreadyExistsException()

    medical_record.patient_id = medical_record_data.patient_id
    medical_record.clinic_id = medical_record_data.clinic_id

    return medical_record_repository.update(
        db=db,
        medical_record=medical_record,
    )
