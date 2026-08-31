from sqlalchemy.orm import Session

from app.repositories.patient_clinics_repository import PatientClinicRepository
from app.repositories.patient_repository import PatientRepository

from app.repositories.clinic_repository import ClinicRepository

from app.models.patient_clinics_model import PatientClinic

from app.core.exceptions import PatientAlreadyAssociatedError
from app.core.exceptions import PatientNotFoundError
from app.core.exceptions import ClinicNotFoundError

patient_clinics_repository = PatientClinicRepository()
patient_repository = PatientRepository()
clinic_repository = ClinicRepository()

def create(db: Session, patient_id: int, clinic_id: int) -> PatientClinic:

    patient = patient_repository.get_by_id(
        db=db,
        patient_id=patient_id
    )

    if patient is None:
        raise PatientNotFoundError

    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id
    )

    if clinic is None:
        raise ClinicNotFoundError

    existing = patient_clinics_repository.get_by_patient_and_clinic(
        db=db,
        patient_id=patient_id,
        clinic_id=clinic_id
    )

    if existing is not None:
        raise PatientAlreadyAssociatedError


    patient_clinic = PatientClinic(
        patient_id=patient_id,
        clinic_id=clinic_id
    )

    patient_clinic = patient_clinics_repository.create(
        db=db,
        patient_clinic=patient_clinic
    )

    return patient_clinic